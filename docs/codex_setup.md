# Codex Setup

This project uses project-local instructions plus reusable Codex skills.

## Required Reusable Skills

- `utmb-research`
- `data-science-project-workflow`

These skills are not stored directly in this project. Their source copies should live in the separate `Codex-Instructions` repository and be installed into the local Codex skills folder.

## Why This Exists

Project-local files such as `AGENTS.md` should describe this UTMB project.

Reusable workflows should live as Codex skills so they can be shared across projects without copying a large `SKILL.md` file into every repository.

## Setup On A New Machine

1. Clone this project.
2. Clone the `Codex-Instructions` repository.
3. Install the reusable skills from `Codex-Instructions` into the local Codex skills folder.

Example:

```powershell
python "C:\Users\Urh\Desktop\Urh\Github Repositories\Codex-Instructions\scripts\Install-CodexSkill.py" --all
```

This installs skills into:

```text
C:\Users\Urh\.codex\skills\
```

## Source vs Installed Copy

Source copy:

```text
C:\Users\Urh\Desktop\Urh\Github Repositories\Codex-Instructions\skills\
```

Installed copy:

```text
C:\Users\Urh\.codex\skills\
```

When a reusable skill changes in `Codex-Instructions`, run the install script again so Codex uses the updated version.
