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
