# AGENTS.md

## Purpose
This repository stores UTMB race-result extraction, course analysis, pacing analysis, notebooks, and derived data outputs.

Use this file for project-specific guidance only. Reusable workflows should live as installed Codex skills, not as copied root-level `SKILL.md` files.

## Working Principles
- Inspect the existing files before editing.
- Keep changes small, readable, and reversible.
- Preserve user work and validated outputs.
- Avoid renames, moves, or deletes unless they are clearly needed.
- Treat helper code, notebooks, and existing data outputs as the source of truth for current project behavior.

## Project Areas
- `helper_functions/` contains reusable UTMB helper code. Inspect `helper_functions/utmb_api.py` before changing data fetch logic.
- `utmb_under_27h/` contains UTMB under-27-hour data work and outputs.
- `pacing_strategy/` contains pacing and derived analysis work.
- `course_analysis/` contains course analysis notebooks and outputs.
- `data/` contains project data files.

## Reusable Skills
- Use `utmb-research` for UTMB-specific data fetching, race-result outputs, pacing analysis, and project workflow.
- Use `data-science-project-workflow` for notebooks, dataframes, modeling, plotting, and analysis style.
- These reusable skills are installed globally under `C:\Users\Urh\.codex\skills\`.
- Their source copies live in `C:\Users\Urh\Desktop\Urh\Github Repositories\Codex-Instructions\skills\`.
- Do not recreate large copied `SKILL.md` files in this project; update the source skill in `Codex-Instructions` and reinstall it when reusable guidance changes.

## Verification
- Check changed files after edits.
- Run focused commands or notebook checks when available and relevant.
- Summarize what changed, which files were touched, and where any data outputs were written.
