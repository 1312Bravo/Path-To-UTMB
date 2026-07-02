import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# ------------------------------------------------------------------
#  Univariate analysis - helper function: target ~ numeric feature
# ------------------------------------------------------------------

def univariate_numeric_linear_analysis(
        feature_col: str,
        target_col: str,
        df: pd.DataFrame,
        feature_col_name: str = None,
        target_col_name: str = None,
        print_summary: bool = True,
        plot: bool = True,
        n_bins: int = 20,
        figsize: tuple = (25, 5),
        scatter_kws: dict = None,
    ) -> pd.DataFrame:

    if scatter_kws is None:
        scatter_kws = {
            "alpha": 0.25,
            "s": 15,
            "color": "black",
        }

    # Keep only valid rows
    data_clean = (
        df[[feature_col, target_col]]
        .dropna()
        .copy()
    )

    # Fit linear regression model
    X = sm.add_constant(data_clean[feature_col])
    y = data_clean[target_col]

    model = sm.OLS(y, X).fit()

    intercept = model.params.get("const", np.nan)
    coef = model.params.get(feature_col, np.nan)
    scaled_coef = coef * data_clean[feature_col].std()
    p_value = model.pvalues.get(feature_col, np.nan)
    r2 = model.rsquared
    n_obs = int(model.nobs)

    # Print summary
    if print_summary:
        print("{} ~ {}:".format(target_col, feature_col))
        print(" - number of observations: {:,}".format(n_obs))
        print(" - intercept: {:.6f}".format(intercept))
        print(" - coefficient: {:.6f}".format(coef))
        print(" - scaled coefficient: {:.6f}".format(scaled_coef))
        print(" - p-value: {:.6f}".format(p_value))
        print(" - R2: {:.6f}".format(r2))

    # Return one row summary
    summary_df = pd.DataFrame([{
        "feature_col": feature_col,
        "target_col": target_col,
        "n_obs": n_obs,
        "intercept": intercept,
        "coef": coef,
        "scaled_coef": scaled_coef,
        "p_value": p_value,
        "r2": r2,
    }])

    if plot:
        # Prepare percentile bins for plot
        plot_df = data_clean.copy()
        try:
            plot_df["feature_bin"] = pd.qcut(
                plot_df[feature_col],
                q = n_bins,
                duplicates = "drop",
            )
        except ValueError:
            plot_df["feature_bin"] = pd.cut(
                plot_df[feature_col],
                bins = min(n_bins, plot_df[feature_col].nunique()),
                include_lowest = True,
            )

        bin_summary = (
            plot_df
            .groupby("feature_bin", observed = True)
            .agg(
                feature_mean = (feature_col, "mean"),
                target_mean = (target_col, "mean"),
                n_rows = (target_col, "size"),
            )
            .reset_index(drop = True)
        )

        # Plot
        fig, ax = plt.subplots(1, 2, figsize = figsize)

        if feature_col_name is None:
            feature_col_name = feature_col
        if target_col_name is None:
            target_col_name = target_col

        # Scatter with linear fit
        ax[0].set_title(
            f"{target_col_name} ~ {feature_col_name} [Scatter & Linear Fit]",
            fontsize = 14,
        )

        sns.regplot(
            data = data_clean,
            x = feature_col,
            y = target_col,
            ax = ax[0],
            scatter_kws = scatter_kws,
            line_kws = {"color": "red", "linewidth": 2},
        )

        ax[0].set_xlabel(feature_col_name)
        ax[0].set_ylabel(target_col_name)

        # Binned percentile plot
        ax[1].set_title(
            f"{target_col_name} ~ {feature_col_name} [Percentile-Binned Mean]",
            fontsize = 14,
        )

        ax[1].stem(
            bin_summary["feature_mean"],
            bin_summary["target_mean"],
            linefmt = "k--",
            markerfmt = "o",
            basefmt = " ",
        )
        ax[1].plot(
            bin_summary["feature_mean"],
            bin_summary["target_mean"],
            color = "grey",
            linewidth = 1.5,
            linestyle = "-",
        )
        ax[1].plot(
            bin_summary["feature_mean"].values,
            model.params["const"] + model.params[feature_col] * bin_summary["feature_mean"].values,
            color = "red",
            linewidth = 1,
            linestyle = "--",
        )
        
        ax[1].set_xlabel(f"{feature_col_name} [quantile bins, n = {n_bins}]")
        ax[1].set_ylabel(f"{target_col_name} [bin mean]")

        for i in [0, 1]:
            ax[i].grid(alpha = 0.5)

        plt.tight_layout()
        plt.show()

    return summary_df