# Thesis project: Gaussian splatting world of Tartu

Karl-Ustav's BSc thesis (UT Institute of Computer Science, course LTAT.01.004). Mostly writing, data and experiments; some code. Folder
layout and what is tracked is in `README.md`. Timetable and deadlines:
`plan/ajakava.md` (Estonian). Check it when planning work.

## Rules

- **Never commit large data.** Raw captures go in `data/`, trained splats and
  checkpoints in `outputs/`; both are gitignored. If something big shows up in
  `git status`, extend `.gitignore` rather than committing it.
- **New capture → `data/MANIFEST.md` entry.** When data is added to `data/`,
  make sure it has a manifest row.
- **New training run → `experiments/<YYYY-MM-DD>_<scene>_<variant>/`** with the
  config used, metrics, and a one-line verdict (convention in
  `experiments/README.md`).
- **Log the work.** After a meaningful chunk of work in a session (a decision,
  an experiment result, a written section, a problem solved), add a short dated
  entry to `LOG.md` in English: what was done, what was decided and *why*,
  open problems. Write it so it can later feed the thesis methods section. The
  SessionEnd hook adds a mechanical entry (commits, changed files) on its own;
  the entry you write is the human-readable one, so don't duplicate the file list.
- Thesis source is LaTeX in `thesis/`; build with `cd thesis && latexmk`.
- Commit messages: short imperative subject saying what changed
  (`Add capture plan for Raekoja plats`).
