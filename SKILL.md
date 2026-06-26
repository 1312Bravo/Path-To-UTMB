# SKILL.md

## Skill Name
Data Science Project Workflow

## Purpose
Use this skill when working on data science tasks in this folder, including notebooks, scripts, datasets, models, and analysis outputs.
It captures the reusable workflow and style conventions to follow when helping with analysis tasks.

## When To Use
- Inspecting datasets and understanding schema
- Cleaning, transforming, or validating data
- Building analysis notebooks or scripts
- Training or evaluating machine learning models
- Creating charts, tables, or summary outputs
- Preparing reproducible data science deliverables

## Core Workflow
1. Inspect the project structure and identify the relevant files, data sources, and outputs.
2. Clarify the goal and constraints before making changes.
3. Validate inputs early, including schema, row counts, missing values, and obvious anomalies.
4. Prefer small, deterministic steps with explicit random seeds when randomness is involved.
5. Record assumptions, dropped rows, derived features, and transformation logic.
6. Prefer simple baselines before more complex methods.
7. Verify results with summary statistics, samples, shapes, and relevant metrics.
8. Save outputs in clear, reproducible formats.

## Notebook Style
- Keep notebook cells ordered so the notebook can run top to bottom.
- Minimize hidden state, stale outputs, and duplicated logic.
- Move reusable code into scripts or modules when a notebook becomes too large.
- Add short markdown notes where the reasoning is not obvious.
- Prefer plots and tables that are easy to review and rerun.
- Write notebooks like a clear analysis story: setup, load data, inspect data, clean data, explore, fit model, diagnose model, summarize.
- Use short markdown section headers to separate phases, such as `# Libraries`, `# Get Data`, `# Research`, `# About`, `# Plots`, and `# Model diagnostic`.
- Keep markdown and printouts plain, direct, and easy to scan.
- Use question-driven notes when introducing a goal, then answer the goal with code below.
- Number subgoals when that improves readability.
- Keep exploratory work and modeling work in separate sections when possible.
- Use `print` statements for summaries, checks, and takeaways when they are clearer than a table.

## Code Style
- Prefer explicit, readable steps over dense one-liners when the code is meant to explain something.
- Keep code blocks visually simple and linear, with one obvious task per block.
- Prefer direct notebook-style code over abstract helper functions unless reuse is clearly beneficial.
- Use short section comments like `# Libraries`, `# Get Data`, `# About`, `# Fit`, `# Predict`, and `# Model diagnostic` to organize the flow.
- Keep setup code at the top of the notebook, then move through data loading, summary, modeling, and interpretation in order.
- Prefer clear, descriptive variable names that show the role of the object in the analysis.
- Keep related variable names consistent across logistic and linear parts of the notebook, for example `target_logit`, `features_logit`, `fit_logit`, and `y_pred_logit`.
- Use plain, readable assignment chains instead of deeply nested expressions when the logic is easier to follow step by step.
- Break complex logic into small steps with comments above each block.
- Add inline comments only when deeper intent needs clarification.
- Use `.copy()` deliberately when creating a working dataframe.
- Use `.reset_index(drop=True)` when normalizing indexes after filtering or slicing.
- Use `.dropna(how="any")` explicitly when removing incomplete rows before modeling.
- Use `.query(...)` when it reads more clearly than a long boolean mask.
- Use `.assign(...)` when adding derived columns that should stay in the dataframe pipeline.
- Use `lambda df:` inside `assign` when the new value depends on the current dataframe.
- Use `np.where(...)` when you need a compact conditional transformation in a dataframe pipeline.
- Keep `assign` calls readable by keeping the new column name and expression aligned on separate lines when needed.
- When using `assign` for new dataframe columns, prefer spaces around `=` in assignments, for example `new_col = lambda df: ...`.
- When defining plotting parameters, prefer spaces around `=` in keyword-style arguments, for example `s = 8`.
- When indexing subplots, prefer `ax[0,0]` instead of `ax[0, 0]`.
- Prefer explicit keyword arguments in plotting calls so the code reads like a sentence.
- Use `line_kws` and other plotting keyword dictionaries when you need a small amount of plot customization without creating extra variables.
- Use `plt.tight_layout()` right before `plt.show()` so the final figure is cleaned up at the end of the block.
- Keep commas and spacing tidy in dataframe lists and function calls.
- When providing longer code blocks, keep comments above each chunk to explain what it does, and add inline comments when deeper intent needs clarification.

## Dataframe Style
- Use clear intermediate names, especially for dataframes and model stages, such as `df_full`, `df_finisher`, `data_model_logit`, `fit_logit`, `y_pred_logit`, or `finish_rate_agg`.
- Keep dataframe preparation explicit, with a named source dataframe, a modeling dataframe, and separate feature and target objects.
- Prefer `df_...` for analysis tables and `data_...` for modeling inputs when that distinction helps readability.
- Use `_df` suffixes for tables that are meant to be inspected or plotted.
- Use `_agg` suffixes for aggregated tables that will be plotted or printed.
- Use `_grid`, `_edges`, or `_centers` for helper vectors that define binning or plotting ranges.
- Comment each type of column group, and keep related columns grouped under those comments.
- Keep column selections compact when they still read well, but allow multiple lines when there are many columns.
- For wide selections, prefer grouped chunks over one value per line when the layout still stays readable.
- When creating derived columns, use descriptive names and keep the derivation easy to follow.
- Keep derived columns close to the selection or preparation step that needs them.
- When creating binned or grouped variables, name the intermediate objects clearly, such as `bin_edges`, `bin_centers`, or `*_agg`.
- Use `pd.cut(...)` for binning when you need discrete groups from a continuous variable.
- Use named aggregations in `groupby(...).agg(...)` so the output reads clearly.
- Prefer `groupby(...).agg(...).reset_index()` when the result will be plotted or printed.
- Keep aggregation results in a separate variable instead of nesting them inside plotting code.
- Keep dataframe transforms in a small chain rather than a deeply nested expression.
- Use compact, grouped column lists when selecting many fields, but split into multiple lines when needed for readability.
- Preserve comment blocks above grouped column selections when they explain the categories.
- Keep boolean checks and data quality assertions close to the transformation they validate.
- Use `assert` for simple sanity checks when you want the notebook to fail fast on an unexpected data issue.
- Keep `print`-based data summaries human-readable and formatted for quick inspection.
- Prefer `query(...).iloc[0]` or similar direct access only when you already know the result should be a single row.

## Modeling Style
- Keep the modeling story simple and explainable: one main predictor, one target, clean data, fit, predict, diagnose, interpret.
- Separate preparation, fitting, prediction, metrics, and diagnostics into distinct cells or blocks.
- Use logistic regression when the target is binary and linear regression when the target is continuous.
- Use `statsmodels` when interpretability matters and you want summaries, coefficients, p-values, and confidence intervals.
- Use `sklearn.metrics` or `scipy.stats` for supporting metrics and diagnostics.
- Keep model input preparation explicit by defining target, features, source dataframe, modeling dataframe, feature matrix, and target series as separate variables.
- Build model inputs with a minimal number of columns so the intent stays obvious.
- Keep model fitting code short and direct, with the model object and fitted result stored separately.
- Use `fit(..., disp=False)` for model fitting when you want to keep notebook output clean.
- Store predictions immediately after fitting so the notebook reads in the same order as the modeling steps.
- Keep metric dictionaries separate from the printout logic.
- When a conclusion depends on a threshold, compute it explicitly and print it clearly.
- Prefer visual diagnostics rather than over-formalizing the analysis when the plot already tells the story well.
- Keep uncertainty calculations explicit when they support the conclusion.
- Use consistent naming patterns for related objects, especially when comparing logistic and linear models side by side.
- Keep model summary variables such as prediction intervals, confidence intervals, and residuals separate from the fitted model object.
- Use direct notebook printouts to explain the meaning of a metric right after you calculate it.

## Plotting Style
- Prefer `fig, ax = plt.subplots(...)` as the default plot setup pattern.
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
- Keep scatter plots dark and simple when the purpose is to show trend rather than styling.
- Use KDEs and histograms together when comparing distributions, especially for class splits or residual diagnostics.
- Use regression lines on top of scatter plots when you want the trend to be obvious without extra explanation.
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
- Keep plot titles and axis labels short but informative, and make units explicit when they matter.
- Use reference lines and legends to make threshold-based conclusions easy to read from the figure.

## Data Handling
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

## Communication
- Treat user ideas and suggestions as hypotheses, not facts.
- Do not assume the user is right just because they have a clear opinion.
- Respond like an experienced colleague who evaluates the approach critically and helps refine it.
- Assume the user usually knows the goal or what they want to achieve, while you guide the best way to do it and also suggest strong alternative approaches when they seem better.
- Push back gently when a suggestion is risky, inefficient, or inconsistent with the codebase.
- Explain tradeoffs clearly and recommend the most robust implementation, even when it differs from the user’s first idea.
- Stay collaborative and respectful, but do not become passive or deferential when a better approach is available.

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
