"""The list of video -> splat runs.

Read by prep_local.py (frames + COLMAP on the Mac) and by the Colab notebook
(training). Edit it here, then copy it to MyDrive/loputoo/ next to video2splat.py.

One run = one video + one configuration; settings left out use DEFAULTS.

    frames    frames taken, spread evenly over the video          (redoes COLMAP)
    fps       instead of frames: frames per second of video;      (redoes COLMAP)
              1 is about one frame per metre at walking pace
    max_size  longest side of the frames in px                    (redoes COLMAP)
    overlap   how many following frames each frame is matched to  (redoes COLMAP)
    config    "default" (original 3DGS densification) or "mcmc" (capped number of Gaussians)
    steps     training length: 0.25 = 7.5k steps (quick look), 1.0 = 30k (full quality)
    extra     extra simple_trainer.py flags, e.g. "--antialiased", or "--packed" if
              the GPU runs out of memory

Runs of the same video with the same frames/fps, max_size and overlap share one
set of frames + COLMAP result (the same prep_key). Name runs like the
experiments/ folders (YYYY-MM-DD_scene_variant).
"""

from pathlib import Path

DEFAULTS = dict(frames=200, fps=None, max_size=1600, overlap=10,
                config="default", steps=0.25, extra="")

RUNS = [  # video = file name in data/videos/ (Mac) and MyDrive/loputoo/videos/ (Colab)
    # short videos (38 s, 64 s): 200 frames = 3-5 frames per second, plenty
    dict(name="2026-11-03_short_1_way_quick", video="short_1_way.MOV"),
    dict(name="2026-11-03_short_2_way_quick", video="short_2_way.MOV"),   # 200 frames = 3.1 fps
    # frame-rate sweep on short_2_way (64 s): each fps gets its own frames + COLMAP, training is identical
    dict(name="2026-11-03_short_2_way_fps1_quick",  video="short_2_way.MOV", fps=1),    # ~64 frames
    dict(name="2026-11-03_short_2_way_fps2_quick",  video="short_2_way.MOV", fps=2),    # ~129
    dict(name="2026-11-03_short_2_way_fps5_quick",  video="short_2_way.MOV", fps=5),    # ~321
    dict(name="2026-11-03_short_2_way_fps10_quick", video="short_2_way.MOV", fps=10),   # ~643
    # long videos (7-8 min): 200 frames would be one every ~2.4 s, too sparse; 1 per second = 410-470 frames
    dict(name="2026-11-03_hole1_fps1_quick", video="hole1.MOV", fps=1),
    dict(name="2026-11-03_hole2_fps1_quick", video="hole2.MOV", fps=1),
    dict(name="2026-11-03_long_2_way_fps1_quick", video="long_2_way.MOV", fps=1),
    # a variant: same frames + COLMAP as the first run, other training strategy
    dict(name="2026-11-03_short_1_way_mcmc", video="short_1_way.MOV", config="mcmc"),
]


def runs() -> list[dict]:
    """RUNS with DEFAULTS filled in."""
    out = [{**DEFAULTS, **r} for r in RUNS]
    names = [r["name"] for r in out]
    dupes = {n for n in names if names.count(n) > 1}
    assert not dupes, f"run names used twice: {dupes}"
    return out


def prep_key(r: dict) -> str:
    """Folder name for the run's frames + COLMAP, e.g. short_2_way_fps5_s1600_o10."""
    spacing = f"fps{r['fps']:g}" if r["fps"] else f"f{r['frames']}"
    return f"{Path(r['video']).stem}_{spacing}_s{r['max_size']}_o{r['overlap']}"


def prep_args(r: dict) -> list[str]:
    """video2splat.py options for the run's frames + COLMAP."""
    spacing = ["--fps", str(r["fps"])] if r["fps"] else ["--frames", str(r["frames"])]
    return [*spacing, "--max-size", str(r["max_size"]), "--overlap", str(r["overlap"])]


def train_args(r: dict) -> list[str]:
    """video2splat.py options for the run's training."""
    extra = ["--", *r["extra"].split()] if r["extra"] else []
    return ["--variant", r["name"], "--trainer-config", r["config"],
            "--steps-scaler", str(r["steps"]), *extra]
