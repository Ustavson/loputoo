# Research log

Dated entries, newest at the bottom. Two kinds:

- **Written entries** (`## YYYY-MM-DD: title`): what was done, decisions and why,
  open problems. Written by hand or by Claude after a chunk of work.
- **Auto entries** (`### YYYY-MM-DD HH:MM · session end (auto)`): appended by the
  Claude Code SessionEnd hook (`.claude/hooks/log-session.sh`) with the commits
  and uncommitted changes since the previous auto entry.

---

## 2026-11-01: Project set up

- Created the project folder with git, folder layout, LaTeX skeleton and this log.
- Decision: raw captures and trained splats stay out of git (`data/`, `outputs/`);
  `data/MANIFEST.md` describes them instead. Reason: they will be tens to hundreds
  of GB, far beyond what git or GitLab LFS quotas handle.
- Next: full-thesis timetable (`plan/`).

## 2026-11-01: Timetable

- Wrote `plan/ajakava.md` (in Estonian, for LTAT.01.004): fixed deadlines, phases, SMART short-term goals up to 08.12.
- Checked the institute's 2026/27 deadlines page: topic registration **02.11.2026**, submission **12.05.2027**, defence **04.–11.06.2027**. The dates in the course handout (14 May, 5–12 June 2026) were last year's.
- Open questions: own filming vs. existing data, filming date, GPU for gsplat (needs CUDA). The plan does all data-independent work first. Target for the data decision is the 13.01 meeting. If we film ourselves, the best window is late March to April (no snow, no leaves), by 15.04 at the latest.
- Official LaTeX template: https://gitlab.cs.ut.ee/unitartucs-thesis-templates/bsc-msc-latex-template (not yet adopted in `thesis/`).

## 2026-11-01: Timetable updates

- GPU is no longer an open question: training will run on the UT HPC cluster. Removed it from the open questions in `plan/ajakava.md`.
- Topic registration form submitted, under a different title from the working title in the timetable. The final title will be agreed with the supervisors.

### 2026-11-01 22:15 · session end (auto)

Commits:
- `5ef86ac` Add thesis timetable with deadlines and SMART goals
- `60acd4c` Update timetable: HPC settled, topic registered under another title
- `6a2a472` Add supervisors, PDF export of timetable, md2pdf script

## 2026-11-01: First video → splat pipeline

- GPU options checked: upstream gsplat is CUDA-only, so it can't train on the Mac (M4). Colab (free T4) is for quick tests and the 04.11 demo; UT HPC (A100/H200) is for real runs. OpenSplat or Brush can train on the Mac for previews, but they aren't gsplat.
- Wrote `code/video2splat.py` (video → ffmpeg frames → COLMAP → gsplat `simple_trainer.py` → `splat.ply` + `summary.json`) and `code/video2splat_colab.ipynb`.
- Choices and why:
  - Frames are spread evenly over the video (default 200, longest side 1600 px), with no sharpness filtering yet.
  - COLMAP uses `sequential_matcher` because video frames are ordered, which is much cheaper than exhaustive matching.
  - One shared camera with the OPENCV model; gsplat undistorts it when loading.
  - `--Mapper.multiple_models 0`, because gsplat reads only `sparse/0`.
  - gsplat pinned to v1.5.3, using its default config with `--steps_scaler 0.25` (7.5k steps) for quick tests.
  - PSNR/SSIM/LPIPS come from gsplat's held-out split (every 8th frame).
- Output is a standard 3DGS `.ply` (position, scale, rotation, opacity, SH colour per Gaussian), viewable in SuperSplat.
- Only frame extraction was tested locally. COLMAP and training haven't been run yet (no COLMAP on the Mac, no GPU).
- Open: blur filtering for frames; the COLMAP option names changed in 3.12, and the script detects which form is in use.

### 2026-11-02 09:14 · session end (auto)

Uncommitted (2):
- `??` code/video2splat.py
- `??` code/video2splat_colab.ipynb

## 2026-11-03: Batch runs and training variants

- `video2splat.py`: one WORKDIR now holds one set of frames + COLMAP result, shared by several training variants (`--variant NAME` → `runs/NAME/`). Added `--trainer-config default|mcmc` to pick gsplat's densification strategy. Why: comparing configurations on the same video shouldn't redo COLMAP, and the comparison is fairer when every variant uses identical camera poses.
- The settings used are saved (`prep.json` for frames/SfM, `runs/NAME/run.json` for training). A rerun with different settings stops with an error. Before this, the script skipped any step whose output existed, so changing e.g. `--frames` would silently reuse the old frames.
- Fixed: the final metrics and render were picked by text sort, so with `steps_scaler 1.0` `summary.json` would have reported step 6999 instead of 29999. Now sorted by step number. `summary.json` also records all settings and the evaluated step.
- Colab notebook is now a batch runner: a list of runs (video + settings), and frames + COLMAP cached on Drive under `prep/` so a dropped session resumes without redoing COLMAP. Finished runs are skipped, and a table compares the metrics at the end.
- Tested on the Mac with stand-in COLMAP and trainer scripts (plumbing, reuse, settings checks, resume). Real COLMAP and gsplat still untested.

## 2026-11-03: iPhone HDR video, frame spacing for long videos

- First own test captures: 5 videos from an iPhone 16, 2026-11-03 (38 s to 7.9 min). All are 1080p 30 fps HEVC, filmed in portrait, and **HDR**: HLG curve, BT.2020 colours, 10 bit, Dolby Vision. HDR video is the iPhone's default.
- Problem: JPEG frames extracted from HDR video as-is come out grey and flat. Homebrew's ffmpeg has no `zscale`, the usual tool for HDR conversion. Fix: when the video is HLG, `video2splat.py` adds ffmpeg's built-in `colorspace` filter. It reads the HLG signal as an ordinary BT.2020 signal (HLG is designed to look right that way) and converts the colours to BT.709. Compared on one frame against macOS's own SDR export (`avconvert`): close, slightly lighter, much better than no conversion. Using a built-in filter means the conversion is identical on the Mac, Colab and HPC. For splat training, consistent colour across frames matters more than exact colour.
- For future captures: consider turning HDR video off on the phone (Settings → Camera → Record Video → HDR Video), so frames don't depend on any conversion at all.
- Added `--fps` as an alternative to `--frames`. 200 frames over a 7–8 min walk is one frame every ~2.4 s (~3 m at walking pace), probably too sparse for COLMAP to link the frames. A fixed rate keeps frames roughly a fixed distance apart whatever the video length. First pass: 1 fps for the long videos (~410–470 frames).
- Seen in the frames: motion blur when walking fast or turning. Filtering blurry frames is still open.

## 2026-11-03: Frame-rate sweep planned

- Added runs to the Colab list for `short_2_way` (64 s) at 1, 2, ~3.1 (the default 200 frames), 5 and 10 fps, all with identical quick training (default strategy, 7.5k steps).
- Caveat for comparing them: gsplat holds out every 8th frame of *that run's* frames for evaluation. At higher fps the held-out frames sit closer to training frames, so the views are easier to reproduce, and PSNR/SSIM/LPIPS will rise partly for that reason alone. Across frame rates, compare registered frames, number of Gaussians, training time and visual quality in SuperSplat. Treat the metrics with care until there's a fixed shared test set (e.g. the same held-out video frames registered into each reconstruction).

## 2026-11-03: Drive storage and Colab GPU budget

- gsplat saves a ~4.3 MB PNG (real | render) per held-out frame at every evaluation step. For the planned 10 runs that would be ~3.3 GB on Drive. The notebook now keeps only the last evaluation, converted to JPEG (~1 MB each, ~0.4 GB in total).
- Estimated Drive use for the full run list: videos 2.4 GB, frames ~1.3 GB, splats ~1–5 GB (248 bytes per Gaussian; the count isn't known yet), renders ~0.4 GB. That's about 5–9 GB against a free account's 15 GB, which Gmail and Photos share.
- Colab doesn't publish its free GPU quota: sessions last at most 12 h, idle sessions are cut, and the limits change. COLMAP runs on the CPU but still uses up GPU-session time while the GPU sits idle. Better: run frames + COLMAP on the Mac (M4) and use Colab only for training.

## 2026-11-03: COLMAP on the Mac, switch to the global mapper

- Installed COLMAP 4.2.1 (Homebrew, CPU only). Added `code/runs.py` (the run list, shared by the Mac and Colab, so their prep folder names always match) and `code/prep_local.py` (frames + COLMAP for every run in the list, into `data/prep/<key>/`; databases moved to `data/colmap_db/`). The notebook now reads `runs.py` from Drive and uses uploaded prep folders, so Colab only trains.
- First real COLMAP run (`short_1_way`, 200 frames): the **incremental mapper posed only 2/200 frames**, even though the features (~13.7k per frame) and matches (~1000 verified matches between neighbouring frames) were fine. It got stuck after its initial pair. Lowering `init_min_tri_angle` to 4° and giving a focal-length prior didn't help.
- The **global mapper** (`colmap global_mapper`, GLOMAP built into COLMAP 4) on the same database posed **196/200** frames, with 95k points and 0.52 px mean reprojection error. The camera path is a smooth line (largest step between frames 1.25× the median, no jumps). It estimated focal ≈ 1368/1380 px for 900×1600 frames, close to my estimate of ~1300 from the iPhone 16's 26 mm-equivalent lens. COLMAP's default guess (1.2 × long side = 1920 px) was far off, which probably explains the many "uncalibrated" pairs.
- Decision: `video2splat.py` uses the global mapper whenever the installed COLMAP has it (`--mapper auto`), and records which mapper ran in `sfm.json` and `summary.json`. Colab's apt COLMAP (3.7) has no global mapper, which is another reason to run COLMAP on the Mac.
- Checked that COLMAP 4.2.1's binary model has exactly the layout gsplat's reader (rmbrualla/pycolmap) expects: a stdlib parser with the same struct formats consumed every file exactly. The new rigs.bin/frames.bin are ignored by gsplat.
- Cost on the M4: 200 frames ≈ 9.6 min, so the whole run list (~3000 frames) is about 2 h. One prep folder is ~0.78 MB per frame (frames + `images.bin`, which stores every keypoint).

## 2026-11-03: Colab gets the code from GitHub

- The notebook is now opened straight from GitHub (colab.research.google.com/github/Ustavson/loputoo/blob/main/code/video2splat_colab.ipynb), and it clones or pulls the repo into `/content/loputoo` before running. Drive holds only data (`videos/`, `prep/`, `outputs/`). Why: copying `video2splat.py`/`runs.py` to Drive by hand after every change was error-prone, and the Drive copy could silently differ from git. Now Colab always runs a pushed commit, and the notebook prints which one, so every result can be traced back to a commit.
- Added `ONLY` (a run-name filter) for testing single runs.

## 2026-11-03: Colab install cached on Drive

- Every Colab session starts on a clean machine. Most of the install time is compiling CUDA code (gsplat, fused-ssim, fused-bilagrid). The install cell now compiles them once into wheels (gsplat built from source so its CUDA code is compiled ahead of time; the PyPI wheel compiles on first use instead), saves them to `MyDrive/loputoo/wheels/<python_torch_cuda_gpu>/`, and later sessions install from there. Ordinary PyPI packages are still installed normally.
- The cache folder name includes Python, torch, CUDA and GPU compute capability, so a Colab torch upgrade or a different GPU triggers one fresh compile instead of breaking. Compiling uses `TORCH_CUDA_ARCH_LIST` for the current GPU only, which is faster. If installing from the cache fails, the cell deletes the cache and asks to be rerun.
- Not yet tested on Colab.

## 2026-11-03: First COLMAP results on all test videos: the chains break

| prep | frames placed (model 0) | how it splits |
|---|---|---|
| short_1_way, 200 f | 196 / 200 | one piece |
| short_2_way, 1 / 2 / 3.1 / 5 fps | 33/64, 65/129, 101/200, 162/321 | always 2 halves, split at the middle |
| short_2_way, 10 fps | 639 / 643 | one piece |
| hole2, 1 fps | 136 / 414 | 9 models kept (136, 106, 16, 15, 10, …) |
| hole1, 1 fps | 53 / 415 | 16 models kept, mostly 3–13 frames |

- The global mapper splits the frames into groups that are connected by matches ("components") and reconstructs each separately; `Global mapping failed` / `Number of tracks = 0` / `no 3D points` are tiny 3-frame groups that couldn't be triangulated. gsplat uses only `sparse/0` (the largest), so the rest of the video is simply missing from the splat.
- **short_2_way** splits exactly at the turnaround (frames 33|35, 102|107, 164|170): turning on the spot puts consecutive frames too many degrees apart to match at ≤5 fps. At 10 fps the turn is sampled densely enough and both halves join. So the frame-rate sweep isn't a like-for-like comparison: at ≤5 fps model 0 covers only the outbound walk, at 10 fps it covers both directions.
- **hole1/hole2** break into many pieces from motion blur and rolling-shutter skew. Looking at the frames: fast pans, the phone swinging over the ground and slopes, trees leaning sideways. Each break is at a blurred frame (e.g. hole2 frame 139, a whip-pan smear between two sharp frames). Overcast November light probably means long exposures, which makes it worse.
- COLMAP also warns that the global mapper wants a focal-length prior. We know it for this phone and mode from short_1_way (≈1370 px for 900×1600), so it could be passed to all iPhone 16 1080p videos.
- Takeaways for the filming guide: walk slowly, turn slowly (especially at turnarounds), no fast pans, keep the phone steady and pointed at the scene rather than the ground, film in good light.
- Pipeline options: (1) pick the sharpest frame in each time window instead of evenly spaced frames; (2) higher fps (10 fps joined short_2_way); (3) the focal prior; (4) loop-closure matching so the outbound and return passes are matched to each other.

## 2026-11-03: First Colab training attempt: two fixes

- The Drive folder is `MyDrive/Colab Notebooks/loputoo`, not `MyDrive/loputoo`. `DRIVE` is now set once, in the cell that mounts Drive, and checked to exist. The path has a space, so the shell commands in the install cell now quote it.
- Training crashed with `ModuleNotFoundError: No module named 'datasets.colmap'`. gsplat's `examples/datasets/` has no `__init__.py`. For such a folder, Python prefers any installed package with the same name, and Colab ships Hugging Face's `datasets`. Reproduced locally; fixed by `video2splat.py` creating an empty `__init__.py` there before starting the trainer (also covers HPC, if `datasets` is installed there).

## 2026-11-03: NumPy 2 vs gsplat's COLMAP reader

- After the `datasets` fix, training crashed when importing `pycolmap`: `INVALID_POINT3D = np.uint64(-1)` raises `OverflowError` on NumPy 2. gsplat v1.5.3 pins an old pycolmap fork (rmbrualla @ cc7ea4b) and `numpy<2` for this reason. I had dropped the numpy pin, wrongly assuming the code was fine on NumPy 2. Going back to NumPy 1 isn't possible: Colab is on Python 3.13, which NumPy 1.x doesn't support.
- Fix: after installing, the notebook's install cell rewrites that line to `np.iinfo(np.uint64).max` (the same value, 2^64−1) and checks that `pycolmap` imports. A search of gsplat v1.5.3 (examples + library) and the pinned reader for other APIs NumPy 2 removed found nothing else.
- Longer term: gsplat's main branch has moved to the official `pycolmap>=3.10` and `numpy>=2`. Upgrading gsplat would remove this patch, but is a bigger change (trainer CLI and outputs may differ). Revisit before the HPC runs.


### 2026-11-05 13:51 · session end (auto)

Commits:
- `9bd151d` Add video-to-splat pipeline: Mac COLMAP prep, Colab training
- `f0d1782` Pull code from GitHub in the Colab notebook
- `aaf5928` Cache compiled gsplat wheels on Drive in the Colab notebook
- `2866c05` Fix Colab Drive path and gsplat datasets import clash
- `b1397ed` Patch gsplat's pycolmap reader for NumPy 2 in the Colab install

Uncommitted (1):
- `??` notes/2026-11-04-meeting/

## 2026-11-15: Second filming day (14 Nov) added; data folders reorganised

- Five new iPhone 16 videos from 14 Nov (1080p30 HLG HDR, like the first ones): suur_part1/part2, roosi_jaama, ujula, sild. `suur_part1` and `suur_part2` are one walk with a ~46 s pause between them, and part2 starts where part1 ended. They were joined into `suur.MOV` (538 s) with ffmpeg's concat demuxer and stream copy (no re-encode). Checked: frame counts add up (4249 + 11893 = 16142), and the HLG transfer tag and portrait rotation survive, so `video2splat.py` still converts HDR to SDR and keeps the frames upright.
- `data/videos/` now has one subfolder per filming day (`2026-11-03/`, `2026-11-14/`), and `runs.py` gives each video's path relative to `videos/`. Old prep folders stay valid: `prep_key` and the `prep.json` check use only the file name. Drive's `videos/` needs the same subfolders.
- Local `outputs/` held loose `.ply` files with inconsistent names. They are now in `outputs/<run name>/splat.ply`, the same layout as on Drive.
- New runs use 3 fps. On 03 Nov, 1 fps broke the long videos into many separate pieces, and 10 fps was the only rate that joined short_2_way. 10 fps on 4-9 min videos would be 7000-16000 frames, too many for COLMAP on the Mac and for a T4. 3 fps (690-1610 frames) is a middle ground. If these still break into pieces, the next step is choosing the sharpest frames or adding loop-closure matching (see 2026-11-03).
- Drive no longer needs the videos for runs whose prep folder is already there. `video2splat.py` used to `ffprobe` the video on every call, even when frames + SfM were finished, and the notebook stopped if any video was missing. Now, when `prep.json`, `images/` and `sparse/0` exist, the colour transfer is read from `prep.json`. Only the video's file name is still checked against it, so a changed frame count or fps still stops with an error. Why: uploading ~2 GB of video per filming day to Drive was pointless, since Colab only trains. Tested locally on a copy of a prep folder with a video path that doesn't exist.
