# AGENTS.md

## Purpose
This folder is for data science work, including notebooks, scripts, datasets, models, and analysis outputs.
Use these notes as the local style guide for work in this repository.

- Follow the current user request first.
- Do not override safety rules or higher-priority instructions.

## Working Principles
- Inspect the existing files and data structure before making changes.
- Prefer small, reproducible edits over broad refactors.
- Preserve user work, validated outputs, and intermediate analysis artifacts.
- Keep code readable, explicit, and consistent with the surrounding notebook style.
- Avoid renaming, moving, or deleting files unless it clearly helps the task.
- Keep the same coding style and variable naming patterns already used in the project.
- If these instructions need to be synced elsewhere, do it from the terminal with a script or command.

## Notebook Style
- Structure notebooks like a story: setup, load data, inspect data, clean data, explore, fit model, diagnose model, then summarize insights.
- Use short markdown headings to separate phases, such as `# Libraries`, `# Get Data`, `# Research`, `# About`, `# Plots`, and `# Model diagnostic`.
- Write markdown in plain, direct language and keep it easy to scan.
- Use question-driven notes when introducing a goal, then answer the goal with code below.
- Number subgoals when helpful instead of burying them in a paragraph.
- Keep exploratory work and modeling work in separate sections when possible.
- Use `print` statements for summaries, checks, and takeaways when that is clearer than a table.

## Code Style
- Prefer explicit, readable steps over dense one-liners when the code is meant to explain something.
- Use clear intermediate names, especially for dataframes and model stages, such as `df_full`, `df_finisher`, `data_model_logit`, `fit_logit`, `y_pred_logit`, or `finish_rate_agg`.
- Break complex logic into small steps with comments that explain the purpose of each block.
- Keep longer code blocks annotated with comments above each chunk, and add inline comments only when deeper intent needs clarification.
- Use `.copy()` deliberately when creating a working dataframe.
- Use `.reset_index(drop=True)` when normalizing indexes after filtering or slicing.
- Use `.dropna(how="any")` explicitly when removing incomplete rows before modeling.
- Use `.query(...)` when it reads more clearly than a long boolean mask.
- Use `.assign(...)` when adding derived columns that should stay in the dataframe pipeline.
- When using `assign` for new dataframe columns, prefer spaces around `=` in assignments, for example `new_col = lambda df: ...`.
- When defining plotting parameters, prefer spaces around `=` in keyword-style arguments, for example `s = 8`.
- When indexing subplots, prefer `ax[0,0]` instead of `ax[0, 0]`.

## Dataframe Style
- Comment each type of column group, and keep related columns grouped under those comments.
- Keep column selections compact when they still read well, but allow multiple lines when there are many columns.
- For wide selections, prefer grouped chunks over one value per line when the layout still stays readable.
- When creating derived columns, use descriptive names and keep the derivation easy to follow.
- When creating binned or grouped variables, name the intermediate objects clearly, such as `bin_edges`, `bin_centers`, or `*_agg`.
- Use `pd.cut(...)` for binning when you need discrete groups from a continuous variable.
- Use named aggregations in `groupby(...).agg(...)` so the output reads clearly.
- Prefer `groupby(...).agg(...).reset_index()` when the result will be plotted or printed.
- Keep aggregation results in a separate variable instead of nesting them inside plotting code.
- Keep dataframe transforms in a small chain rather than a deeply nested expression.
- Keep commas and spacing tidy in dataframe lists and function calls.

## Modeling Style
- Keep the modeling story simple and explainable: one main predictor, one target, clean data, fit, predict, diagnose, interpret.
- Separate preparation, fitting, prediction, metrics, and diagnostics into distinct cells or blocks.
- Use logistic regression when the target is binary and linear regression when the target is continuous.
- Use `statsmodels` when interpretability matters and you want summaries, coefficients, p-values, and confidence intervals.
- Use `sklearn.metrics` or `scipy.stats` for supporting metrics and diagnostics.
- Keep model input preparation explicit by defining target, features, source dataframe, modeling dataframe, feature matrix, and target series as separate variables.
- Use consistent naming patterns for related objects, especially when comparing logistic and linear models side by side.
- Keep metric dictionaries separate from the printout logic.
- When a conclusion depends on a threshold, compute it explicitly and print it clearly.
- Use visual diagnostics rather than over-formalizing the analysis when the plot already tells the story well.
- Keep uncertainty calculations explicit when they support the conclusion.

## Plotting Style
- Prefer `fig, ax = plt.subplots(...)` as the default setup pattern.
- Use simple subplot layouts like `1,2`, `2,2`, or `1,3` when comparing related views.
- Keep subplot access in the compact `ax[0,0]` style.
- Give each axis a direct title with `ax[i].set_title(...)`.
- Set axis labels explicitly with `set_xlabel(...)` and `set_ylabel(...)`.
- End plot blocks with `plt.tight_layout()` and `plt.show()`.
- Use light grids such as `ax[i].grid(alpha=.5)` when they improve readability.
- Use `sns.scatterplot`, `sns.lineplot`, `sns.kdeplot`, `sns.histplot`, and `sns.regplot` as the main plotting tools.
- Keep colors simple and consistent, often black for points or lines, grey for reference lines, and blue/red for class comparison.
- Use small marker sizes for dense scatter plots.
- Use `alpha` to reduce visual clutter when needed.
- Use `markeredgecolor`, `linewidth`, and `lw` directly when they improve the appearance of a plot.
- Use `axhline` and `axvline` for thresholds, baselines, or decision boundaries.
- Add legends when a plot compares multiple series or groups.
- For distributions, combine histograms and KDEs when that makes the shape easier to read.
- For relationships, use scatter plus regression line when you want the trend to be obvious.
- For classification, use ROC curves and predicted-probability distributions.
- For residual analysis, use residual-vs-predicted plots and residual distributions.
- For summary trends across a predictor range, use binning or a grid and compare observed and model-based values.
- Keep multi-panel figures focused, with each panel showing one idea.
- Order panels logically, usually from raw data to fitted model to residuals to summary.
- Prefer clean plots with enough white space over crowded annotations.
- Keep annotation text minimal unless it directly supports the conclusion.

## Data Handling
- Treat source data as read-only unless the task explicitly requires transformation.
- Make assumptions explicit when cleaning, filtering, or imputing data.
- Record dropped rows, changed columns, and derived features.
- Prefer deterministic steps and document random seeds when relevant.
- Be careful with privacy-sensitive or personally identifiable data.

## Verification
- Run the relevant checks, tests, or small sanity checks when available.
- Confirm shapes, schema, summary statistics, and sample rows after transformations.
- Verify that charts, tables, and exported files match expectations.

## Communication
- Summarize what changed, what was verified, and any remaining risks.
- Call out assumptions, tradeoffs, and anything that needs follow-up.
