#!/usr/bin/env python3
"""Frames + COLMAP for the runs in runs.py, on this machine (no GPU needed).

    python3 code/prep_local.py                 # every run
    python3 code/prep_local.py --only short    # runs whose name contains "short"

For each distinct frames + COLMAP setting it writes data/prep/<prep_key>/:
extracted frames, the COLMAP model and prep.json. These are the folders the Colab
notebook looks for in prep/ in its Drive folder (DRIVE in the notebook). Upload
them there and Colab only trains. Finished folders are skipped, so rerunning picks
up where it stopped.

COLMAP's database.db (features + matches, not needed for training) is moved to
data/colmap_db/<prep_key>.db, so data/prep/ holds only what Colab needs.

Needs ffmpeg and colmap on PATH (brew install ffmpeg colmap).
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import runs as runlist

CODE = Path(__file__).resolve().parent
REPO = CODE.parent


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--videos", type=Path, default=REPO / "data" / "videos",
                   help="folder with the videos (default data/videos)")
    p.add_argument("--out", type=Path, default=REPO / "data" / "prep",
                   help="where the prep folders go (default data/prep)")
    p.add_argument("--only", help="only runs whose name contains this text")
    args = p.parse_args()

    todo = {}  # prep_key -> first run that needs it
    for r in runlist.runs():
        if args.only is None or args.only in r["name"]:
            todo.setdefault(runlist.prep_key(r), r)
    if not todo:
        sys.exit("no runs match")
    missing = sorted({r["video"] for r in todo.values() if not (args.videos / r["video"]).exists()})
    if missing:
        sys.exit(f"not found in {args.videos}: {', '.join(missing)}")

    db_dir = args.out.parent / "colmap_db"
    db_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for i, (key, r) in enumerate(todo.items(), 1):
        work = args.out / key
        print(f"\n=== [{i}/{len(todo)}] {key}", flush=True)
        t0 = time.time()
        cmd = [sys.executable, CODE / "video2splat.py", args.videos / r["video"], work,
               *runlist.prep_args(r), "--stop-after", "sfm"]
        ok = subprocess.run([str(c) for c in cmd]).returncode == 0
        if (work / "database.db").exists():
            shutil.move(work / "database.db", db_dir / f"{key}.db")
        sfm = work / "sfm.json"
        if ok and sfm.exists():
            s = json.loads(sfm.read_text())
            results[key] = f"{s['registered']:>4} / {s['frames']:<4} frames got a pose   {time.time() - t0:5.0f} s"
        else:
            results[key] = "FAILED (see output above)"

    print("\n=== summary")
    for key, res in results.items():
        print(f"{key:36s} {res}")
    print(f"\nUpload the folders in {args.out}/ to prep/ in the notebook's Drive folder (MyDrive/Colab Notebooks/loputoo/prep/).")


if __name__ == "__main__":
    main()
