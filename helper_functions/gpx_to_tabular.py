import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import gpxpy

# -------------------------------------------------
# Slope categories - Common classification
# -------------------------------------------------

SLOPE_CATEGORIES = {
    "Flat": (0,1),
    "Very easy": (1,3),
    "Easy": (3,7),
    "Moderate": (7, 12),
    "Steep": (12, 20),
    "Very steep": (20, 30),
    "Extreme": (30, np.inf) 
}

# -------------------------------------------------
# Classify slope based on categories
# -------------------------------------------------

def classify_slope(
        slope_percent: float, 
        slope_categories: dict = SLOPE_CATEGORIES
    ) -> str:
    if slope_percent > list(slope_categories.values())[0][1]:
        direction = "Uphill"
    elif abs(slope_percent) > list(slope_categories.values())[0][1]:
        direction = "Downhill"
    else:
        direction = "Flat"

    for cat_name, (min_val, max_val) in slope_categories.items():
        if min_val <= abs(slope_percent) < max_val:
            if direction == "Flat":
                return cat_name
            else:
                return direction + " | " + cat_name

# -------------------------------------------------
# Convert .gpx file to DataFrame
# -------------------------------------------------

def gpx_to_tabular(
        gpx_file: gpxpy.gpx.GPX,
        slope_categories: dict = SLOPE_CATEGORIES
    ) -> pd.DataFrame: 

    # GPX file is a container that can hold multiple tracks, routes, ...
    # A track represents a complete path / activity
    track = gpx_file.tracks[0]
    points = []
    i = 0

    # Inside track there are track segments - a continuous portion of a track
    # Used for when there are gaps in GPS record or for logical separations

    total_distance_2d = 0
    total_distance_3d = 0
    total_elevation_gain = 0
    total_elevation_loss = 0

    for segment in track.segments:

        point_distance_2d = 0
        point_distance_3d = 0
        point_elevation_gain = 0
        point_elevation_loss = 0
        slope_percent = 0
        slope_class = list(slope_categories.keys())[0]

        prev_point = None
        prev_elevation = None
        
        # Each segment contains track points
        # Each point stores a specific location along the track
        # Points are ordered in the sequence they were recorded
        for point in segment.points:
            if prev_point is not None:

                # 2D distance - horizontal distance along the map plane
                point_distance_2d = point.distance_2d(prev_point)
                total_distance_2d += point_distance_2d

                # 3D distance - account for the vertical change (3D >= 2D)
                point_distance_3d = point.distance_3d(prev_point)
                total_distance_3d += point_distance_3d

                point_elevation = point.elevation - prev_elevation
                if point_elevation >= 0:
                    point_elevation_loss = 0
                    point_elevation_gain = point_elevation
                    total_elevation_gain += point_elevation
                else:
                    point_elevation_gain = 0
                    point_elevation_loss = abs(point_elevation)
                    total_elevation_loss += abs(point_elevation)

                if point_distance_2d != 0:
                    slope_percent = (point.elevation - prev_elevation) / point_distance_2d * 100
                else: 
                    slope_percent = 0
            
            points.append({
                "point_index": i,
                "latitude": point.latitude,
                "longitude": point.longitude,
                "elevation_m": point.elevation,

                "point_distance_2d_m": point_distance_2d,
                "point_distance_3d_m": point_distance_3d,
                "point_elevation_gain_m": point_elevation_gain,
                "point_elevation_loss_m": point_elevation_loss,
                "slope_perc": slope_percent,
                "slope_class": classify_slope(slope_percent, slope_categories),

                "total_distance_2d_m": total_distance_2d,
                "total_distance_3d_m": total_distance_3d,
                "total_elevation_gain_m": total_elevation_gain,
                "total_elevation_loss_m": total_elevation_loss,

            })

            prev_point = point
            prev_elevation = point.elevation
            i += 1

    # Return in Tabular format
    return pd.DataFrame(points)

# ------------------------------------------------
# Plot Course Profile
# -------------------------------------------------

def plot_course_profile(
        gpx_tabular_df: pd.DataFrame,
        course_name: str,
        slope_categories: dict = SLOPE_CATEGORIES,
    ) -> None:

    fig, ax = plt.subplots(1,1, figsize = (25, 6))

    slope_colors = {
        "Flat": "white",
        "Uphill | Very easy": "#E0F0FF",
        "Uphill | Easy": "#A8D8FF",
        "Uphill | Moderate": "#70BFFF",
        "Uphill | Steep": "#3898FF",
        "Uphill | Very steep": "#0066CC",
        "Uphill | Extreme": "#003366",
        
        "Downhill | Very easy": "#FFE0E0",
        "Downhill | Easy": "#FFB0B0",
        "Downhill | Moderate": "#FF6060",
        "Downhill | Steep": "#FF4040",
        "Downhill | Very steep": "#CC0000",
        "Downhill | Extreme": "#660000",
    }

    plot_data = gpx_tabular_df.copy()
    distance_2d_100m_edges = np.arange(0, gpx_tabular_df["total_distance_2d_m"].max() + 110, 100)
    plot_data["total_distance_2d_m_bin"] = pd.cut(plot_data["total_distance_2d_m"], bins=distance_2d_100m_edges, right=False)
    plot_data = plot_data.groupby("total_distance_2d_m_bin", observed=True).aggregate({
        "total_distance_2d_m": "min",
        "elevation_m": "max",
        "slope_perc": "mean"
        })
    plot_data["slope_class"] = plot_data["slope_perc"].apply(lambda s: classify_slope(s, slope_categories))

    ax.set_title(f"{course_name}", fontsize=16)

    slope_classes = plot_data["slope_class"].values
    change_idx = [0] + (np.where(slope_classes[1:] != slope_classes[:-1])[0] + 1).tolist() + [len(plot_data["total_distance_2d_m"])]
    for start, end in zip(change_idx[:-1], change_idx[1:]):
        sc = slope_classes[start]
        color = slope_colors.get(sc, "grey")
        ax.fill_between(plot_data["total_distance_2d_m"][start:end],  plot_data["elevation_m"][start:end], color=color, alpha=0.6)

    ax.plot(plot_data["total_distance_2d_m"], plot_data["elevation_m"], color="black")

    ax.set_xticks(np.arange(0, plot_data["total_distance_2d_m"].max() + 1, 10_000))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x/1000:,.0f}"))

    ax.set_yticks(np.arange(0, plot_data["elevation_m"].max() + 1, 200))
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
    ax.set_ylim( plot_data["elevation_m"].min() - 0.5*plot_data["elevation_m"].std(),  plot_data["elevation_m"].max() + 0.5*plot_data["elevation_m"].std())

    ax.set_xlabel("Distance [km]", fontsize=12)
    ax.set_ylabel("Elevation [m]", fontsize=12)

    plt.grid(alpha=.5)
    plt.tight_layout()
    plt.show()