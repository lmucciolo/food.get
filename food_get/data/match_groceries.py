import pandas as pd
from math import asin, sqrt, cos, sin, radians

EARTH_R_MI = 3963


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on a sphere (like Earth) in miles.

    https://en.wikipedia.org/wiki/Haversine_formula

    :param lat1: latitude of first point
    :param lon1: longitude of first point
    :param lat2: latitude of second point
    :param lon2: longitude of second point

    :return: distance in miles
    """

    rlat1, rlon1, rlat2, rlon2 = (
        radians(lat1),
        radians(lon1),
        radians(lat2),
        radians(lon2),
    )

    d = (
        2
        * EARTH_R_MI
        * asin(
            sqrt(
                sin((rlat2 - rlat1) / 2) ** 2
                + cos(rlat1) * cos(rlat2) * sin((rlon2 - rlon1) / 2) ** 2
            )
        )
    )

    return d


def match_grocery_stores(stores1_df, stores2_df, max_dist):
    """
    Matches grocery stores from two data sets with address and lat/long given a
    max_dist. Matches on dist and the numbers of an address. Only uses the first match
    even if there are multiple.
    """

    stores1_df["match_id"] = None
    stores2_df["match_id"] = None
    stores1_df["address_num"] = stores1_df["address"].str.split(" ").str[0]
    stores2_df["address_num"] = stores2_df["address"].str.split(" ").str[0]
    match_id = 1

    for index1, store1 in stores1_df.iterrows():
        for index2, store2 in stores2_df.iterrows():
            if stores1_df.loc[index1, "match_id"] is None:
                dist = haversine_distance(
                    float(store1["latitude"]),
                    float(store1["longitude"]),
                    float(store2["latitude"]),
                    float(store2["longitude"]),
                )
                # dist is how many feet away
                if (
                    dist * 5280 <= max_dist
                    and store1["address_num"] == store2["address_num"]
                ):
                    stores1_df.loc[index1, "match_id"] = match_id
                    stores2_df.loc[index2, "match_id"] = match_id
                    match_id += 1
                    print(match_id)

    matches_1 = stores1_df[~stores1_df["match_id"].isna()]
    matches_2 = stores2_df[~stores2_df["match_id"].isna()]
    # change non matches so they dont get matched
    merged_df = pd.merge(matches_1, matches_2, on="match_id")

    merge_drop_cols = [
        "store_name_y",
        "address_num_x",
        "address_num_y",
        "address_x",
        "latitude_y",
        "longitude_y",
        "address_y",
    ]

    merged_df = merged_df.drop(merge_drop_cols, axis=1)
    merged_df.rename(
        {
            "store_name_x": "store_name",
            "latitude_x": "latitude",
            "longitude_x": "longitude",
        },
        axis=1,
        inplace=True,
    )

    nonmatches_1 = stores1_df[stores1_df["match_id"].isna()]
    nonmatches_2 = stores2_df[stores2_df["match_id"].isna()]

    nonmatches_1.drop(["address", "address_num"], axis=1, inplace=True)
    nonmatches_2.drop(["address", "address_num"], axis=1, inplace=True)

    final_df = pd.concat([merged_df, nonmatches_1, nonmatches_2])
    print(merged_df.columns)
    print(nonmatches_1.columns)
    print(nonmatches_2.columns)

    return final_df


# QA
# print(f"Total in original: {len(g_clean) + len(s_clean)}")
# print(f"Total merged: {len(df[df['match_id'].notna()])}")
# print(f"Total in merge: {len(df)}")
# print(f"Total in OG minus merged: {len(g_clean) + len(s_clean) - len(df[df['match_id'].notna()])} :)")
