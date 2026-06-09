# AGENTS.md

## Purpose
This folder is for data science work, including notebooks, scripts, datasets, models, and analysis outputs.
Acts like local instructions for work in that folder and its subfolders.

- AGENTS.md tells me how to behave in this workspace area.
- It does not replace the current user request.
- It does not override safety rules or higher-priority instructions.

## Working Rules
- Inspect the existing files and data structure before making changes.
- Prefer small, reproducible changes over broad refactors.
- Preserve user work, analysis outputs, and any validated results.
- Keep code readable and consistent with the surrounding project style.
- Avoid renaming, moving, or deleting files unless it clearly helps the task.
- Keep the same coding style and variable naming as for now.

## Data Handling
- Treat source data as read-only unless the task explicitly requires transformation.
- Make assumptions explicit when cleaning, filtering, or imputing data.
- Record any dropped rows, changed columns, or derived features.
- Prefer deterministic steps and document random seeds when relevant.
- Be careful with privacy-sensitive or personally identifiable data.

## Analysis And Modeling
- Validate inputs before training, scoring, or aggregating.
- Check for leakage, class imbalance, missing values, and outliers when relevant.
- Use appropriate baselines before more complex methods.
- Compare results with clear metrics and note limitations.
- Prefer reproducible pipelines over one-off notebook-only logic.

## Notebooks
- Keep notebook cells ordered logically and easy to rerun from top to bottom.
- Minimize hidden state and stale outputs.
- Move reusable logic into scripts or modules when it grows beyond the notebook.
- Add short markdown notes where the reasoning is not obvious.

## Verification
- Run the relevant checks, tests, or small sanity checks when available.
- Confirm shapes, schema, summary statistics, and sample rows after transformations.
- Verify that charts, tables, and exported files match expectations.

## Communication
- Summarize what changed, what was verified, and any remaining risks.
- Call out assumptions, tradeoffs, and anything that needs follow-up.
