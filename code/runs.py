"""The list of video -> splat runs.

Read by prep_local.py (frames + COLMAP on the Mac) and by the Colab notebook
(training). Edit it here, then commit and push: the notebook pulls it from GitHub.

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

RUNS = [  # video = path under data/videos/ (Mac) and videos/ in the Drive folder (Colab),
          # one subfolder per filming day: videos/<YYYY-MM-DD>/<name>.MOV
    # short videos (38 s, 64 s): 200 frames = 3-5 frames per second, plenty
    dict(name="2026-11-03_short_1_way_quick", video="2026-11-03/short_1_way.MOV"),
    dict(name="2026-11-03_short_2_way_quick", video="2026-11-03/short_2_way.MOV"),   # 200 frames = 3.1 fps
    # frame-rate sweep on short_2_way (64 s): each fps gets its own frames + COLMAP, training is identical
    dict(name="2026-11-03_short_2_way_fps1_quick",  video="2026-11-03/short_2_way.MOV", fps=1),    # ~64 frames
    dict(name="2026-11-03_short_2_way_fps2_quick",  video="2026-11-03/short_2_way.MOV", fps=2),    # ~129
    dict(name="2026-11-03_short_2_way_fps5_quick",  video="2026-11-03/short_2_way.MOV", fps=5),    # ~321
    dict(name="2026-11-03_short_2_way_fps10_quick", video="2026-11-03/short_2_way.MOV", fps=10),   # ~643
    # long videos (7-8 min): 200 frames would be one every ~2.4 s, too sparse; 1 per second = 410-470 frames
    dict(name="2026-11-03_hole1_fps1_quick", video="2026-11-03/hole1.MOV", fps=1),
    dict(name="2026-11-03_hole2_fps1_quick", video="2026-11-03/hole2.MOV", fps=1),
    dict(name="2026-11-03_long_2_way_fps1_quick", video="2026-11-03/long_2_way.MOV", fps=1),
    # a variant: same frames + COLMAP as the first run, other training strategy
    dict(name="2026-11-03_short_1_way_mcmc", video="2026-11-03/short_1_way.MOV", config="mcmc"),

    # 2026-11-14 videos, 4-9 min each. On 03 Nov, 1 fps broke the long videos into many separate
    # pieces, and 10 fps joined short_2_way. 3 fps is a middle ground COLMAP on the Mac can still handle.
    # suur.MOV = suur_part1 + suur_part2 joined back to back (538 s).
    dict(name="2026-11-14_suur_fps3_quick",        video="2026-11-14/suur.MOV", fps=3),         # ~1610 frames
    dict(name="2026-11-14_roosi_jaama_fps3_quick", video="2026-11-14/roosi_jaama.MOV", fps=3),  # ~690
    dict(name="2026-11-14_ujula_fps3_quick",       video="2026-11-14/ujula.MOV", fps=3),        # ~810
    dict(name="2026-11-14_sild_fps3_quick",        video="2026-11-14/sild.MOV", fps=3),         # ~820
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
