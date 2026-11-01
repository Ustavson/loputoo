# Experiments

One folder per training / reconstruction run:

```
experiments/2026-11-15_raekoja-plats_baseline/
├── config.yaml     # exact config / command used (copy, don't reference)
├── metrics.json    # PSNR, SSIM, LPIPS, #Gaussians, train time, GPU
└── NOTES.md        # input data ID (from data/MANIFEST.md), what changed vs. previous run, verdict
```

Big outputs (`.ply`, checkpoints, render videos) go to `outputs/<same-folder-name>/`,
which is gitignored. Small preview images (a few PNG/JPG) can stay here.

`NOTES.md` should end with a one-line **Verdict:**, e.g.
"Verdict: floaters near the tower gone, but sky worse; keep densification change, revert sky mask."
