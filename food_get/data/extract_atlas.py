"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: extract_atlas.py
Author: Danielle Rosenthal

Description:
    This file imports historic USDA Food Atlas Research Data for 2010, 2015, and 2019
    and combines them into one dataframe based on what is required for the map
    visualization.
"""
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

import pandas as pd
import numpy as np
import pathlib

def import_atlas_data(export=False, years=["2010", "2015", "2019"]):
    """
    Imports dataframes for historical Food Atlas data and adds labels for each year.
        These files have been pre-filtered to meet file size restrictions, but the
        following function is built to filter to necessary columns.

    Args:
        export (bool): if True, saves a csv with the compiled dataframe
        years (list of strings): years we want to compile for

    Returns:
        atlas_sets (pandas DataFrame): pandas DataFrame of the compiled historical datasets
    """
    atlas_sets = pd.DataFrame()

    for year in years:
        Atlas_Raw = pd.read_csv(
            pathlib.Path(__file__).parent
            / "../data/import_data/Atlas{}.csv".format(year)
        )

        Atlas_Filtered = Atlas_Raw[
            [
                "CensusTract",
                "LowIncomeTracts",
                "LATracts_half",
                "lapophalfshare",
                "lapophalf",
            ]
        ]
        Atlas_Filtered = Atlas_Filtered.add_suffix("_{}".format(year))
        Atlas_Filtered.rename(
            columns={"CensusTract_{}".format(year): "CensusTract"}, inplace=True
        )

        if len(atlas_sets) == 0:
            atlas_sets = Atlas_Filtered
        else:
            atlas_sets = atlas_sets.merge(Atlas_Filtered, on="CensusTract", how="outer")

    if export:
        atlas_sets.to_csv("atlas_historical.csv")

    return atlas_sets


def percentage_string_label(value):
    """
    Creates a clean string label of the proporton of low access households.

    Args:
        value (int): the integer value we want to convert to a clean percent string

    Returns:
        label (string): clean percentage label string
    """
    return f"{value * 100:.1f}%"


def filtered_atlas(export=False, years=["2010", "2015", "2019"]):
    """
    Makes datatype and formatting edits to align historical Atlas datasets.

    Args:
        export (bool): if True, saves a csv with the compiled dataframe
        years (list of strings): years we want to compile for

    Returns:
        filtered_df (pandas DataFrame): pandas DataFrame of the compiled historical datasets
    """
    filtered_df = import_atlas_data()

    # Making some small adjustments to 2019 columns to account for changes to raw data structure
    filtered_df["LowIncomeTracts_2019"] = filtered_df[
        "LowIncomeTracts_2019"
    ].values.astype(np.int64)
    filtered_df["LATracts_half_2019"] = filtered_df["LATracts_half_2019"].values.astype(
        np.int64
    )
    filtered_df["lapophalfshare_2019"] = filtered_df["lapophalfshare_2019"].fillna(0)
    filtered_df["lapophalfshare_2019"] = filtered_df["lapophalfshare_2019"] / 100

    for year in years:
        col_name = f"lapophalfshare_{year}"
        filtered_df[col_name] = 1 - filtered_df[col_name]
        label_column_name = f"{year}_prop_label"
        filtered_df[label_column_name] = filtered_df[col_name].apply(
            lambda x: percentage_string_label(x)
        )

    if export:
        filtered_df.to_csv("filtered_atlas_update.csv")

    return filtered_df
