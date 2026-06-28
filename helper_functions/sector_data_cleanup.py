import numpy as np
import pandas as pd

# Sector rows are arrival-based: each row describes the segment from the previous checkpoint to the current checkpoint.
# - sector_race_time_at_checkpoint - formatted cumulative race time at sector (checkpoint) arrival
# - sector_time_seconds - cumulative race time at sector (checkpoint) arrival
# - sector_time - previous sector time (time for the segment that ended at this checkpoint) - excluding rest at the previous checkpoint.
# - sector_rest_time / sector_rest_time_seconds - checkpoint stop time, but some rows may be special rest-only checkpoint rows.
# - Row (j) means sector from previous checkpoint to current checkpoint and not sector starting at current checkpoint

# For row (j):
# - `sector_time_moving_min` = previous checkpoint departure → current checkpoint arrival
# - `sector_time_elapsed_min` = previous checkpoint arrival → current checkpoint arrival
# - `sector_rest_time_min` = current checkpoint arrival → current checkpoint departure
# - `sector_previous_rest_time_min` = previous checkpoint arrival → previous checkpoint departure


# - Rest can be assigned to the sector in multiple ways:
# - sector_time_full_no_rest_min = movement only
# - sector_time_full_start_rest_min = previous checkpoint rest + movement to current checkpoint
# - sector_time_full_end_rest_min = movement to current checkpoint + current checkpoint rest

# -------------------------------------------------
# Clean sector data columns
# -------------------------------------------------

# - sector_arrival_time_dt
# - sector_departure_time_dt
# - sector_race_time_at_checkpoint_min
# - sector_time_moving_min
# - sector_time_elapsed_min
# - sector_rest_time_min
# - sector_previous_rest_time_min
# - sector_time_full_start_rest_min
# - sector_time_full_end_rest_min
# - sector_time_full_no_rest_min
# - sector_rest_time_share_start_rest
# - sector_rest_time_end_share
# - sector_distance_km_runner_estimate
# - sector_distance_km
# - cumulative_sector_distance_km

def clean_runner_race_sector_data(
        sector_df: pd.DataFrame
    ) -> pd.DataFrame:

    sector_df = (
        sector_df
        .sort_values(["runner_id", "sector_checkpoint_id"])
        .assign(

            # Checkpoint timing
            sector_arrival_time_dt = lambda df: pd.to_datetime(
                df["sector_arrival_time"],
                errors="coerce",
            ),
            sector_departure_time_dt = lambda df: pd.to_datetime(
                df["sector_departure_time"],
                errors="coerce",
            ),

            # Cumulative race time at checkpoint arrival
            sector_race_time_at_checkpoint_min = lambda df: (
                df["sector_time_seconds"] / 60
            ),

            # Movement-ish time: previous checkpoint departure -> current checkpoint arrival
            sector_time_moving_min = lambda df: (
                pd.to_timedelta(df["sector_time"]).dt.total_seconds() / 60
            ),

            # Race-clock elapsed time: previous checkpoint arrival -> current checkpoint arrival
            # This includes rest at the previous checkpoint.
            sector_time_elapsed_min = lambda df: (
                (df.groupby("runner_id")["sector_time_seconds"].diff() / 60)
                .fillna(df["sector_time_moving_min"])
            ),

            # Rest/stop time at checkpoint
            sector_rest_time_min = lambda df: (
                pd.to_timedelta(df["sector_rest_time"]).dt.total_seconds() / 60
            ).fillna(0),
        )
        .assign(
            # Rest/stop time at previous checkpoint
            sector_previous_rest_time_min = lambda df: (
                df.groupby("runner_id")["sector_rest_time_min"].shift(1).fillna(0)
            ),

            # Previous checkpoint arrival -> current checkpoint arrival
            # Includes rest at the previous checkpoint.
            sector_time_full_start_rest_min = lambda df: (
                df["sector_previous_rest_time_min"] + df["sector_time_moving_min"]
            ),
            # Previous checkpoint departure -> current checkpoint departure
            # Includes rest at the current checkpoint.
            sector_time_full_end_rest_min = lambda df: (
                df["sector_time_moving_min"] + df["sector_rest_time_min"]
            ),
            # Movement only: previous checkpoint departure -> current checkpoint arrival
            sector_time_full_no_rest_min = lambda df: (
                df["sector_time_moving_min"]
            ),
        )
        .assign(
            # Useful rest share feature
            # Share of start-rest sector time spent resting at the previous checkpoint.
            sector_rest_time_share_start_rest = lambda df: (
                df["sector_previous_rest_time_min"] / df["sector_time_full_start_rest_min"]
            ),
            # Share of end-rest sector time spent resting at the current checkpoint.
            sector_rest_time_end_share = lambda df: (
                df["sector_rest_time_min"] / df["sector_time_full_end_rest_min"]
            ),
        )
        .assign(
            # Runner-level sector distance estimate [km]
            sector_distance_km_runner_estimate = lambda df: (
                df["sector_time_moving_min"] / df["sector_pace_min_per_km"]
            ),
            # Sector distance [km]: median estimate within race/year/sector
            sector_distance_km = lambda df: (
                df.groupby(
                    ["race_id", "year", "sector_checkpoint_id"]
                )["sector_distance_km_runner_estimate"]
                .transform("median")
            ),
            # Cumulative sector distance [km] within runner
            cumulative_sector_distance_km = lambda df: (
                df.groupby("runner_id")["sector_distance_km"].cumsum()
            ),
        )
        # Remove start rows
        .loc[lambda df: df["sector_checkpoint_id"] != 0]
        .reset_index(drop=True)
    )

    return sector_df

# -------------------------------------------------
# Correct rest only sectors
# -------------------------------------------------

# Creates / updates:
# - sector_is_rest_only
# - sector_time_moving_min
# - sector_distance_km_runner_estimate
# - sector_distance_km
# - cumulative_sector_distance_km

def apply_rest_only_checkpoint_correction(
        sector_df: pd.DataFrame
    ) -> pd.DataFrame:

    # Identify rest only sectors
    rest_only_checkpoint_check_df = (
        sector_df
        .loc[
            lambda df: (
                df["runner_is_finisher"]
                & df["sector_time_moving_min"].notna()
                & (df["sector_checkpoint_id"] != 0)
            )
        ]
        .groupby(["race_id", "year", "sector_checkpoint_id"], as_index=False)
        .agg(
            number_of_observations=("runner_id", "size"),
            missing_pace_share=(
                "sector_pace_min_per_km",
                lambda x: x.isna().mean(),
            ),
            median_sector_time_min=(
                "sector_time_moving_min",
                "median",
            ),
            median_rest_time_min=(
                "sector_rest_time_min",
                "median",
            ),
        )
        .assign(
            checkpoint_is_rest_only = lambda df: (
                (df["missing_pace_share"] >= 0.95)
                & (df["median_rest_time_min"] > 0)
            )
        )
    )

    # Update data
    sector_df = (
        sector_df
        .merge(
            rest_only_checkpoint_check_df[
                [
                    "race_id",
                    "year",
                    "sector_checkpoint_id",
                    "checkpoint_is_rest_only",
                ]
            ],
            on = ["race_id", "year", "sector_checkpoint_id"],
            how = "left",
            validate = "m:1",
        )
        .assign(
            sector_is_rest_only = lambda df: (
                df["checkpoint_is_rest_only"]
                .astype("boolean")
                .fillna(False)
            ),
            sector_time_moving_min = lambda df: np.where(
                df["sector_is_rest_only"],
                0,
                df["sector_time_moving_min"],
            ),
            sector_distance_km_runner_estimate = lambda df: np.where(
                df["sector_is_rest_only"],
                0,
                df["sector_time_moving_min"] / df["sector_pace_min_per_km"],
            ),
            sector_distance_km = lambda df: (
                df
                .groupby(["race_id", "year", "sector_checkpoint_id"])
                ["sector_distance_km_runner_estimate"]
                .transform("median")
            ),
            cumulative_sector_distance_km = lambda df: (
                df.groupby("runner_id")["sector_distance_km"].cumsum()
            ),
        )
        .drop(columns="checkpoint_is_rest_only")
    )

    return sector_df


# -------------------------------------------------
# Total race distance and relative sector distance
# -------------------------------------------------

# - total_distance_km
# - sector_start_distance_km
# - sector_end_distance_km
# - relative_sector_distance
# - relative_cumulative_sector_distance
# - relative_sector_start_distance
# - relative_sector_end_distance

def add_sector_distance_features(
        sector_df: pd.DataFrame
    ) -> pd.DataFrame:

    # Total race distance after rest-only sectors are corrected
    total_distance_km_by_year = (
        sector_df
        .query("runner_is_finisher == 1")
        .groupby(["runner_id", "year"])["sector_distance_km"]
        .sum()
        .reset_index()
        .groupby("year")["sector_distance_km"]
        .mean()
    )

    sector_df = (
        sector_df
        .assign(
            # Total race distance
            total_distance_km = lambda df: df["year"].map(total_distance_km_by_year),

            # Sector start and end distance [km]
            sector_start_distance_km = lambda df: (
                df["cumulative_sector_distance_km"] - df["sector_distance_km"]
            ),
            sector_end_distance_km = lambda df: (
                df["cumulative_sector_distance_km"]
            ),

            # Sector distance relative to total race distance
            relative_sector_distance = lambda df: (
                df["sector_distance_km"] / df["total_distance_km"]
            ).clip(lower=0, upper=1),
            relative_cumulative_sector_distance = lambda df: (
                df["cumulative_sector_distance_km"] / df["total_distance_km"]
            ).clip(lower=0, upper=1),
        )
        .assign(
            # Relative sector start and end distance
            relative_sector_start_distance = lambda df: (
                df["relative_cumulative_sector_distance"] - df["relative_sector_distance"]
            ).clip(lower=0, upper=1),
            relative_sector_end_distance = lambda df: (
                df["relative_cumulative_sector_distance"]
            ),
        )
    )

    # Assert
    finisher_max = (
        sector_df
        .query("runner_is_finisher == 1")
        .groupby("runner_id")["relative_cumulative_sector_distance"]
        .max()
    )
    assert np.allclose(
        finisher_max,
        1.0,
        atol=1e-3,
    ), "Relative cumulative sector distance does not end at 1 for every finisher."

    return sector_df


# -------------------------------------------------
# Connect UTMB Course GPX data to sector data
# -------------------------------------------------

# - sector_boundary_index
# - sector_start_distance_m
# - sector_end_distance_m

def build_sector_boundaries(
        sector_df: pd.DataFrame
    ) -> pd.DataFrame:

    group_cols = ["race_id", "year", "sector_checkpoint_id"]
    boundary_group_cols = ["race_id", "year"]
    sort_cols =  ["race_id", "year", "cumulative_sector_distance_km"]

    sector_boundaries_df = (
        sector_df
        .query("runner_is_finisher == 1")
        .groupby(group_cols)
        .agg(
            sector_distance_km=("sector_distance_km", "median"),
            cumulative_sector_distance_km=("cumulative_sector_distance_km", "median"),
        )
        .reset_index()
        .sort_values(sort_cols)
        .reset_index(drop=True)
        .assign(
            sector_start_distance_m = lambda df: (
                (
                    df.groupby(boundary_group_cols)["cumulative_sector_distance_km"].shift(1)
                    if boundary_group_cols
                    else df["cumulative_sector_distance_km"].shift(1)
                )
                .fillna(0)
                * 1_000
            ),
            sector_end_distance_m = lambda df: (
                df["cumulative_sector_distance_km"] * 1_000
            ),
        )
        .assign(
            sector_boundary_index = lambda df: (
                df.groupby(boundary_group_cols).cumcount()
                if boundary_group_cols
                else np.arange(len(df))
            )
        )
    )

    return sector_boundaries_df

# -------------------------------------------------
# Assign GPX course points to year-specific sectors
# -------------------------------------------------

# - sector_checkpoint_id
# - sector_boundary_index
# - sector_start_distance_m
# - sector_end_distance_m

# same GPX point
# -> 2022 sector assignment
# -> 2023 sector assignment
# -> 2024 sector assignment
# -> 2025 sector assignment

def assign_course_points_to_sectors(
        utmb_course_df: pd.DataFrame,
        sector_boundaries_df: pd.DataFrame
    ) -> pd.DataFrame:

    course_sector_list = []
    sector_boundary_groups = sector_boundaries_df.groupby(["race_id", "year"], dropna=False)

    for group_key, sector_boundaries_group_df in sector_boundary_groups:

        sector_end_distances_m = (
            sector_boundaries_group_df["sector_end_distance_m"].to_numpy()
        )

        course_sector_group_df = (
            utmb_course_df
            .sort_values("total_distance_2d_m")
            .reset_index(drop=True)
            .assign(
                sector_boundary_index = lambda df: np.searchsorted(
                    sector_end_distances_m,
                    df["total_distance_2d_m"],
                    side="left",
                )
            )
            .assign(
                sector_boundary_index = lambda df: df["sector_boundary_index"].clip(
                    upper=len(sector_boundaries_group_df) - 1
                )
            )
            .merge(
                sector_boundaries_group_df,
                on = "sector_boundary_index",
                how = "left",
                validate = "m:1",
            )
        )

        course_sector_list.append(course_sector_group_df)

    course_sector_df = pd.concat(
        course_sector_list,
        ignore_index=True,
    )

    return course_sector_df


# -------------------------------------------------
# Aggregate GPX elevation by sector
# -------------------------------------------------

# - race_id
# - year
# - sector_checkpoint_id
# - sector_elevation_gain_m
# - sector_elevation_loss_m

def build_course_sector_elevation_aggregation(
        utmb_course_df: pd.DataFrame,
        sector_boundaries_df: pd.DataFrame
    ) -> pd.DataFrame:

    course_sector_df = assign_course_points_to_sectors(
        utmb_course_df = utmb_course_df,
        sector_boundaries_df = sector_boundaries_df,
    )

    course_sector_agg_df = (
        course_sector_df
        .groupby(["race_id", "year", "sector_checkpoint_id"])
        .agg(
            sector_elevation_gain_m = ("point_elevation_gain_m", "sum"),
            sector_elevation_loss_m = ("point_elevation_loss_m", "sum"),
        )
        .reset_index()
    )

    return course_sector_agg_df


# -------------------------------------------------
# Add additional sector data to "main" data and calculate some new features
# -------------------------------------------------

# - sector_elevation_gain_m
# - sector_elevation_loss_m
# - cumulative_sector_elevation_gain_m
# - cumulative_sector_elevation_loss_m
# - sector_start_elevation_gain_m
# - sector_end_elevation_gain_m
# - sector_start_elevation_loss_m
# - sector_end_elevation_loss_m
# - total_elevation_gain_m
# - total_elevation_loss_m
# - relative_sector_elevation_gain
# - relative_sector_elevation_loss
# - relative_cumulative_sector_elevation_gain
# - relative_cumulative_sector_elevation_loss
# - relative_sector_start_elevation_gain
# - relative_sector_end_elevation_gain
# - relative_sector_start_elevation_loss
# - relative_sector_end_elevation_loss

def add_sector_elevation_features(
        sector_df: pd.DataFrame,
        course_sector_agg_df: pd.DataFrame,
    ) -> pd.DataFrame:

    if "sector_is_rest_only" not in sector_df.columns:
        sector_df = sector_df.assign(sector_is_rest_only = False)

    sector_df = (
        sector_df
        .merge(
            course_sector_agg_df,
            on = ["race_id", "year", "sector_checkpoint_id"],
            how = "left",
            validate = "m:1",
        )
        .assign(
            # Rest-only checkpoints have no course distance, so elevation change is 0.
            sector_elevation_gain_m = lambda df: np.where(
                df["sector_is_rest_only"].fillna(False),
                df["sector_elevation_gain_m"].fillna(0),
                df["sector_elevation_gain_m"],
            ),
            sector_elevation_loss_m = lambda df: np.where(
                df["sector_is_rest_only"].fillna(False),
                df["sector_elevation_loss_m"].fillna(0),
                df["sector_elevation_loss_m"],
            ),

            # Cumulative sector elevation gain [m] within runner
            cumulative_sector_elevation_gain_m = lambda df: (
                df.groupby("runner_id")["sector_elevation_gain_m"].cumsum()
            ),
            # Cumulative sector elevation loss [m] within runner
            cumulative_sector_elevation_loss_m = lambda df: (
                df.groupby("runner_id")["sector_elevation_loss_m"].cumsum()
            ),

            # Cumulative elevation gain at sector start and end [m]
            sector_start_elevation_gain_m = lambda df: (
                df["cumulative_sector_elevation_gain_m"] - df["sector_elevation_gain_m"]
            ),
            sector_end_elevation_gain_m = lambda df: (
                df["cumulative_sector_elevation_gain_m"]
            ),

            # Cumulative elevation loss at sector start and end [m]
            sector_start_elevation_loss_m = lambda df: (
                df["cumulative_sector_elevation_loss_m"] - df["sector_elevation_loss_m"]
            ),
            sector_end_elevation_loss_m = lambda df: (
                df["cumulative_sector_elevation_loss_m"]
            ),
        )
    )

    # Total race elevation gain and loss (year specific)
    total_gain_loss_m_by_year = (
        sector_df
        .query("runner_is_finisher == 1")
        .groupby(["runner_id", "year"])[["sector_elevation_gain_m", "sector_elevation_loss_m"]]
        .sum()
        .reset_index()
        .groupby("year")[["sector_elevation_gain_m", "sector_elevation_loss_m"]]
        .mean()
    )

    sector_df = (
        sector_df
        .assign(
            # Total race elevation gain & loss
            total_elevation_gain_m = lambda df: df["year"].map(
                total_gain_loss_m_by_year["sector_elevation_gain_m"]
            ),
            total_elevation_loss_m = lambda df: df["year"].map(
                total_gain_loss_m_by_year["sector_elevation_loss_m"]
            ),
            # Relative sector elevation gain & loss [%]
            relative_sector_elevation_gain = lambda df: (
                df["sector_elevation_gain_m"] / df["total_elevation_gain_m"]
            ).clip(lower=0, upper=1),
            relative_sector_elevation_loss = lambda df: (
                df["sector_elevation_loss_m"] / df["total_elevation_loss_m"]
            ).clip(lower=0, upper=1),
        )
    )

    # Adjust so it sums to 1 (only for finishers)
    sector_df = (
        sector_df
        .assign(
            relative_cumulative_sector_elevation_gain = lambda df: np.where(
                df["runner_is_finisher"] == 1,
                df["cumulative_sector_elevation_gain_m"]
                / df.groupby("runner_id")["cumulative_sector_elevation_gain_m"].transform("max"),
                np.nan,
            ),
            relative_cumulative_sector_elevation_loss = lambda df: np.where(
                df["runner_is_finisher"] == 1,
                df["cumulative_sector_elevation_loss_m"]
                / df.groupby("runner_id")["cumulative_sector_elevation_loss_m"].transform("max"),
                np.nan,
            ),
        )
        .assign(
            relative_cumulative_sector_elevation_gain = lambda df: (
                df["relative_cumulative_sector_elevation_gain"].clip(lower=0, upper=1)
            ),
            relative_cumulative_sector_elevation_loss = lambda df: (
                df["relative_cumulative_sector_elevation_loss"].clip(lower=0, upper=1)
            ),

            # Relative cumulative elevation gain at sector start and end
            relative_sector_start_elevation_gain = lambda df: (
                df["relative_cumulative_sector_elevation_gain"] - df["relative_sector_elevation_gain"]
            ).clip(lower=0, upper=1),
            relative_sector_end_elevation_gain = lambda df: (
                df["relative_cumulative_sector_elevation_gain"]
            ),

            # Relative cumulative elevation loss at sector start and end
            relative_sector_start_elevation_loss = lambda df: (
                df["relative_cumulative_sector_elevation_loss"] - df["relative_sector_elevation_loss"]
            ).clip(lower=0, upper=1),
            relative_sector_end_elevation_loss = lambda df: (
                df["relative_cumulative_sector_elevation_loss"]
            ),
        )
    )

    # Assert
    finisher_max = (
        sector_df
        .query("runner_is_finisher == 1")
        .groupby("runner_id")[
            [
                "relative_cumulative_sector_elevation_gain",
                "relative_cumulative_sector_elevation_loss",
            ]
        ]
        .max()
    )

    assert np.allclose(
        finisher_max["relative_cumulative_sector_elevation_gain"],
        1.0,
        atol=1e-2,
    )
    assert np.allclose(
        finisher_max["relative_cumulative_sector_elevation_loss"],
        1.0,
        atol=1e-2,
    )

    return sector_df
