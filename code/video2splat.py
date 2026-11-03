#!/usr/bin/env python3
"""Video -> Gaussian splat, in one command.

    video  --ffmpeg-->  frames  --COLMAP-->  camera poses + sparse points
           --gsplat-->  trained Gaussians  -->  splat.ply

Usage:
    python video2splat.py VIDEO WORKDIR --gsplat-dir PATH/TO/gsplat [options]

Each step writes into WORKDIR and is skipped if its output already exists, so
you can rerun after a crash, or run frames + SfM on the Mac (`--stop-after sfm`,
needs `brew install colmap`) and only the training on a GPU machine.

One WORKDIR holds one set of frames + SfM, which several training variants can
share: rerun with another `--variant NAME` (and other training options) and only
the training runs again. The settings each part was made with are saved
(prep.json, runs/NAME/run.json); rerunning with different ones stops with an
error instead of silently reusing the old results.

WORKDIR layout (images/ + sparse/0/ is what gsplat's COLMAP loader expects):
    prep.json       video, frame count or fps, frame size, matcher overlap,
                    the video's colour transfer (HDR video is converted to SDR)
    images/         extracted frames
    database.db     COLMAP features and matches
    sparse/0/       COLMAP reconstruction (cameras, poses, sparse points)
    sfm.json        which COLMAP mapper ran, how many frames got a pose
    runs/NAME/      one training variant = gsplat result_dir:
        run.json        trainer config, steps, extra trainer arguments
        ckpts/ ply/ stats/ renders/ cfg.yml   (written by gsplat)
        splat.ply       final splat, copied from ply/
        summary.json    numbers for experiments/<run>/metrics.json

Needs ffmpeg + ffprobe and the colmap CLI on PATH. Training needs an NVIDIA GPU
and a clone of github.com/nerfstudio-project/gsplat (for examples/simple_trainer.py)
with gsplat and examples/requirements.txt installed. Extra arguments after `--`
go straight to simple_trainer.py, e.g. `-- --packed --antialiased`.
"""

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], check=True, **kw)


def step_number(path: str) -> int:
    """gsplat names outputs by step without zero padding (val_step6999.json,
    val_step29999.json), so sort them by number, not as text."""
    return int(re.search(r"\d+", Path(path).name).group())


def same_settings(path: Path, want: dict, what: str):
    """Record the settings `what` was made with, or stop if they differ from last time."""
    if path.exists():
        have = json.loads(path.read_text())
        if have != want:
            diff = {k: (have.get(k), want.get(k)) for k in want if have.get(k) != want.get(k)}
            sys.exit(f"{what} in {path.parent} was made with other settings "
                     f"(setting: (before, now)): {diff}\n"
                     f"Use another {'WORKDIR' if path.name == 'prep.json' else '--variant'}, "
                     f"or delete {path.parent} to start over.")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(want, indent=2))


def probe(video: Path) -> tuple[float, str]:
    """Duration in seconds and the transfer curve of the first video stream
    (e.g. bt709 for normal video, arib-std-b67 for HLG HDR)."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "format=duration:stream=color_transfer", "-of", "json", str(video)],
        check=True, capture_output=True, text=True,
    ).stdout
    info = json.loads(out)
    return float(info["format"]["duration"]), info["streams"][0].get("color_transfer", "unknown")


# iPhones film HDR by default: HLG curve, BT.2020 colours, 10 bit. Written to JPEG
# as is, the frames come out grey and flat. ffmpeg's built-in colorspace filter has
# no HLG curve, but HLG is designed to look right when shown as an ordinary BT.2020
# signal, so read it as that and convert the colours to standard BT.709. Checked on
# an iPhone 16 clip against macOS's own SDR export: close, slightly lighter.
HDR_TO_SDR = {
    "arib-std-b67": "colorspace=all=bt709:itrc=bt2020-10:format=yuv420p",
}


def extract_frames(video: Path, work: Path, fps: float, max_size: int, transfer: str):
    images = work / "images"
    if images.is_dir() and any(images.iterdir()):
        print(f"[frames] {images} already has frames, skipping")
        return
    images.mkdir(parents=True, exist_ok=True)
    # Evenly spaced frames; longest side capped at max_size. ffmpeg applies
    # the phone's rotation flag on its own, so portrait video stays portrait.
    m = max_size
    vf = (f"fps={fps:.6f},"
          f"scale=w='if(gte(iw,ih),min({m},iw),-2)':h='if(gte(iw,ih),-2,min({m},ih))'")
    if transfer in HDR_TO_SDR:
        print(f"[frames] HDR video ({transfer}), converting colours to standard (BT.709)")
        vf += "," + HDR_TO_SDR[transfer]
    elif transfer == "smpte2084":
        print("[frames] WARNING: PQ HDR video, colours will look dark and flat. "
              "Convert it to SDR first.")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", video,
         "-vf", vf, "-q:v", "2", images / "frame_%05d.jpg"])
    print(f"[frames] wrote {len(list(images.iterdir()))} frames at {fps:.2f} fps")


def colmap_option(colmap: str, command: str, new: str, old: str) -> str:
    """COLMAP 3.12 renamed e.g. SiftExtraction.use_gpu to FeatureExtraction.use_gpu.
    Pick whichever name this COLMAP build knows."""
    help_text = subprocess.run([colmap, command, "-h"], capture_output=True, text=True)
    return new if new in (help_text.stdout + help_text.stderr) else old


def run_sfm(work: Path, colmap: str, use_gpu: bool, overlap: int, mapper: str) -> int:
    if shutil.which(colmap) is None:
        sys.exit(f"[sfm] '{colmap}' not found. Mac: brew install colmap; "
                 "Ubuntu/Colab: apt-get install colmap")
    sparse0 = work / "sparse" / "0"
    db = work / "database.db"
    images = work / "images"
    env = {**os.environ, "QT_QPA_PLATFORM": "offscreen"}  # headless servers
    gpu = "1" if use_gpu else "0"
    info_file = work / "sfm.json"
    info = json.loads(info_file.read_text()) if info_file.exists() else {}

    if not (sparse0 / "cameras.bin").exists():
        if mapper == "auto":
            has_global = subprocess.run([colmap, "global_mapper", "-h"],
                                        capture_output=True).returncode == 0
            mapper = "global" if has_global else "incremental"
            if not has_global:
                print("[sfm] this COLMAP has no global_mapper (needs 3.13+), using the "
                      "incremental mapper")
        db.unlink(missing_ok=True)
        ext_gpu = colmap_option(colmap, "feature_extractor",
                                "FeatureExtraction.use_gpu", "SiftExtraction.use_gpu")
        match_gpu = colmap_option(colmap, "sequential_matcher",
                                  "FeatureMatching.use_gpu", "SiftMatching.use_gpu")
        # One camera for the whole video; OPENCV model (gsplat undistorts it).
        run([colmap, "feature_extractor", "--database_path", db, "--image_path", images,
             "--ImageReader.single_camera", "1", "--ImageReader.camera_model", "OPENCV",
             f"--{ext_gpu}", gpu], env=env)
        # Video frames are ordered, so match each frame only with its neighbours.
        run([colmap, "sequential_matcher", "--database_path", db,
             "--SequentialMatching.overlap", overlap, f"--{match_gpu}", gpu], env=env)
        (work / "sparse").mkdir(exist_ok=True)
        if mapper == "global":
            # Global SfM (GLOMAP, built into COLMAP 3.13+): estimates all camera
            # rotations, then all positions, at once. On the first iPhone test video
            # (short_1_way, 200 frames) it posed 196/200 frames; the incremental
            # mapper of COLMAP 4.2.1 got stuck at its initial pair (2/200).
            run([colmap, "global_mapper", "--database_path", db, "--image_path", images,
                 "--output_path", work / "sparse"], env=env)
        else:
            # One model only: gsplat reads sparse/0.
            run([colmap, "mapper", "--database_path", db, "--image_path", images,
                 "--output_path", work / "sparse", "--Mapper.multiple_models", "0"], env=env)
        info["mapper"] = mapper
    else:
        print(f"[sfm] {sparse0} exists, skipping")

    out = subprocess.run([colmap, "model_analyzer", "--path", sparse0],
                         capture_output=True, text=True, env=env)
    m = re.search(r"Registered images:\s*(\d+)", out.stdout + out.stderr)
    registered = int(m.group(1)) if m else -1
    total = len(list(images.iterdir()))
    print(f"[sfm] registered {registered} / {total} frames")
    info.update(registered=registered, frames=total)
    info_file.write_text(json.dumps(info))
    if 0 <= registered < 0.5 * total:
        print("[sfm] WARNING: under half the frames got a pose. Expect a poor splat. "
              "Usual causes: motion blur, fast turns, plain walls, moving people.")
    return registered


def train(work: Path, result: Path, gsplat_dir: Path, config: str,
          steps_scaler: float, extra: list):
    if glob.glob(str(result / "ply" / "*.ply")):
        print(f"[train] {result}/ply already has a splat, skipping")
        return None
    trainer = gsplat_dir / "examples" / "simple_trainer.py"
    if not trainer.exists():
        sys.exit(f"[train] {trainer} not found; point --gsplat-dir at a gsplat clone")
    t0 = time.time()
    run([sys.executable, trainer.name, config,
         "--data_dir", work.resolve(),
         "--data_factor", "1",            # frames are already downscaled
         "--result_dir", result.resolve(),
         "--steps_scaler", steps_scaler,  # 1.0 = 30k steps, 0.25 = 7.5k
         "--save_ply",
         "--disable_viewer",
         *extra], cwd=trainer.parent)     # trainer imports datasets/ and utils.py
    return time.time() - t0


def summarize(work: Path, result: Path, args, extra: list, registered: int,
              train_seconds: float):
    plys = sorted(glob.glob(str(result / "ply" / "point_cloud_*.ply")), key=step_number)
    if not plys:
        sys.exit(f"[export] no .ply found in {result}/ply/")
    shutil.copy(plys[-1], result / "splat.ply")

    stats_files = sorted(glob.glob(str(result / "stats" / "val_step*.json")), key=step_number)
    val = json.loads(Path(stats_files[-1]).read_text()) if stats_files else {}
    summary = {
        "video": str(args.video),
        "variant": args.variant,
        "source_color_transfer": json.loads((work / "prep.json").read_text())["color_transfer"],
        "frames": len(list((work / "images").iterdir())),
        "registered_frames": registered,
        "mapper": json.loads((work / "sfm.json").read_text()).get("mapper"),
        "max_size": args.max_size,
        "overlap": args.overlap,
        "trainer_config": args.trainer_config,
        "steps_scaler": args.steps_scaler,
        "trainer_extra_args": extra,
        "train_seconds": round(train_seconds) if train_seconds else None,
        "eval_step": step_number(stats_files[-1]) + 1 if stats_files else None,
        "psnr": val.get("psnr"), "ssim": val.get("ssim"), "lpips": val.get("lpips"),
        "num_gaussians": val.get("num_GS"),
        "ply": str(result / "splat.ply"),
        "ply_mb": round((result / "splat.ply").stat().st_size / 1e6, 1),
    }
    (result / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


def main():
    argv = sys.argv[1:]
    extra = []
    if "--" in argv:
        i = argv.index("--")
        argv, extra = argv[:i], argv[i + 1:]

    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video", type=Path)
    p.add_argument("workdir", type=Path)
    p.add_argument("--gsplat-dir", type=Path, help="gsplat git clone (needed for training)")
    g = p.add_argument_group("frames + SfM (shared by all variants in a WORKDIR)")
    spacing = g.add_mutually_exclusive_group()
    spacing.add_argument("--frames", type=int,
                         help="frames to extract, spread evenly over the video (default 200)")
    spacing.add_argument("--fps", type=float,
                         help="frames per second of video instead, e.g. 2 (better for long videos)")
    g.add_argument("--max-size", type=int, default=1600,
                   help="longest side of the frames in px (default 1600)")
    g.add_argument("--colmap", default="colmap", help="colmap binary")
    g.add_argument("--colmap-gpu", action="store_true",
                   help="use GPU SIFT in COLMAP (only if COLMAP is built with CUDA)")
    g.add_argument("--overlap", type=int, default=10,
                   help="sequential matcher: neighbours per frame (default 10)")
    g.add_argument("--mapper", choices=["auto", "global", "incremental"], default="auto",
                   help="COLMAP reconstruction step (default auto: global if this COLMAP "
                        "has it, else incremental)")
    t = p.add_argument_group("training (one variant)")
    t.add_argument("--variant", help="name of this training run, results go to "
                   "WORKDIR/runs/NAME (default: CONFIG_xSTEPS, e.g. default_x0.25)")
    t.add_argument("--trainer-config", choices=["default", "mcmc"], default="default",
                   help="gsplat densification strategy (default: default)")
    t.add_argument("--steps-scaler", type=float, default=0.25,
                   help="training length, 1.0 = 30k steps (default 0.25 = 7.5k, quick test)")
    p.add_argument("--stop-after", choices=["frames", "sfm", "train"], default="train")
    args = p.parse_args(argv)
    if args.variant is None:
        args.variant = f"{args.trainer_config}_x{args.steps_scaler:g}"

    if not args.video.exists():
        sys.exit(f"{args.video} not found")
    if args.frames is None and args.fps is None:
        args.frames = 200
    duration, transfer = probe(args.video)
    fps = args.fps or args.frames / duration
    work = args.workdir
    work.mkdir(parents=True, exist_ok=True)
    same_settings(work / "prep.json", {"video": args.video.name, "frames": args.frames,
                                       "fps": args.fps, "max_size": args.max_size,
                                       "overlap": args.overlap, "mapper": args.mapper,
                                       "color_transfer": transfer},
                  "Frames + SfM")

    extract_frames(args.video, work, fps, args.max_size, transfer)
    if args.stop_after == "frames":
        return
    registered = run_sfm(work, args.colmap, args.colmap_gpu, args.overlap, args.mapper)
    if args.stop_after == "sfm":
        return
    if args.gsplat_dir is None:
        sys.exit("--gsplat-dir is required for training")
    result = work / "runs" / args.variant
    same_settings(result / "run.json", {"trainer_config": args.trainer_config,
                                        "steps_scaler": args.steps_scaler,
                                        "trainer_extra_args": extra},
                  f"Variant '{args.variant}'")
    train_seconds = train(work, result, args.gsplat_dir, args.trainer_config,
                          args.steps_scaler, extra)
    summarize(work, result, args, extra, registered, train_seconds)


if __name__ == "__main__":
    main()
