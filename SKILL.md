# SKILL.md

## Skill Name
Data Science Project Workflow

## Purpose
Use this skill when working on data science tasks in this folder, including Python notebooks, data cleaning, ETL, analysis, modeling, and visualization.

## When To Use
- Inspecting datasets and understanding schema
- Cleaning, transforming, or validating data
- Building analysis notebooks or scripts
- Training or evaluating machine learning models
- Creating charts, tables, or summary outputs
- Preparing reproducible data science deliverables

## Core Workflow
1. Inspect the project structure and identify the relevant files, data sources, and outputs.
2. Clarify the goal of the task and any constraints before making changes.
3. Validate inputs early, including schema, row counts, missing values, and obvious anomalies.
4. Prefer small, deterministic steps with explicit random seeds when randomness is involved.
5. Record assumptions, dropped rows, derived features, and transformation logic.
6. Prefer simple baselines before more complex methods.
7. Verify results with summary statistics, samples, shapes, and relevant metrics.
8. Save outputs in clear, reproducible formats.

## Python Notebooks
- Keep notebook cells ordered so the notebook can run top to bottom.
- Minimize hidden state, stale outputs, and duplicated logic.
- Move reusable code into scripts or modules when a notebook becomes too large.
- Add short markdown notes where the reasoning is not obvious.
- Prefer plots and tables that are easy to review and rerun.

## Data Cleaning And ETL
- Treat source data as read-only unless transformation is explicitly requested.
- Document filtering, joins, deduplication, missing-value handling, encoding, and scaling choices.
- Check for broken keys, duplicate records, type mismatches, and unexpected nulls.
- Preserve auditability by keeping raw inputs separate from derived outputs when possible.
- Make transformations deterministic and easy to reproduce.

## Machine Learning
- Use appropriate train, validation, and test splits.
- Watch for leakage, class imbalance, target drift, and overfitting.
- Compare against a simple baseline before using more complex models.
- Report metrics clearly and explain what they mean in context.
- Save the feature definitions, preprocessing steps, and model settings needed to reproduce results.

## Best Practices
- Keep source data and user work intact unless the task requires change.
- Keep code readable and consistent with the surrounding project style.
- Avoid unnecessary renames, moves, or deletions.
- Make assumptions explicit and call out limitations.
- Prefer reviewable outputs over opaque or one-off results.

## Verification
- Confirm shapes, schema, summary statistics, and sample rows after transformations.
- Validate charts, tables, and exports against expectations.
- Run relevant tests or sanity checks when available.
- Check that results can be reproduced from the documented steps.

## Deliverables
- Clean and readable code
- Reproducible analysis or pipeline steps
- Clear notes on assumptions and limitations
- Verified outputs with sanity checks
- Concise summary of what changed and why

## Guardrails
- Do not overwrite user work without explicit instruction.
- Do not delete or rename files unless necessary and clearly justified.
- Do not treat exploratory outputs as final without verification.
- Escalate uncertainties that could affect the interpretation of results.
