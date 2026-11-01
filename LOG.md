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
