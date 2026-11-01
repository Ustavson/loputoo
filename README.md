# Lõputöö: a Gaussian splatting world of Tartu

Thesis project: capturing parts of Tartu and reconstructing them as a navigable
3D Gaussian splatting scene.

## Layout

| Folder         | What goes there                                                   | In git? |
|----------------|-------------------------------------------------------------------|---------|
| `thesis/`      | LaTeX source of the thesis (`main.tex`, `chapters/`, `references.bib`) | yes |
| `plan/`        | Timetable, milestones, deadlines                                  | yes     |
| `notes/`       | Literature notes, supervisor meeting notes, ideas                 | yes     |
| `code/`        | Scripts: frame extraction, SfM/COLMAP, training, viewer           | yes     |
| `experiments/` | One folder per run: config, metrics, short verdict (see its README) | yes (no big files) |
| `figures/`     | Working figures / renders worth keeping                           | yes     |
| `data/`        | Raw captures (photos, video), SfM output. Described in `data/MANIFEST.md` | **no** |
| `outputs/`     | Trained splats, checkpoints, full-res renders                     | **no**  |

`LOG.md` is the research log: dated entries, newest at the bottom. A Claude Code
hook also appends an automatic entry at the end of each session listing commits
and changed files.

## Data and backups

Raw data is **not** in git. Every capture gets an entry in `data/MANIFEST.md`
(date, location, device, settings, where the backup lives). Keep at least one
copy of `data/` off this laptop.

## Building the thesis

```sh
cd thesis && latexmk
```
PDF ends up in `thesis/build/main.pdf`. Requires a TeX distribution (MacTeX).

## Regenerating the timetable PDF

```sh
python3 -m venv .venv && .venv/bin/pip install -r code/requirements.txt   # once
.venv/bin/python code/md2pdf.py plan/ajakava.md                          # → plan/ajakava.pdf
```
Uses headless Google Chrome for printing.
