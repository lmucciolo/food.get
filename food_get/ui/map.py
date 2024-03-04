"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: map.py
Authors: Austin Steinhart

Description:
    This file creates teh maps used in the dash script using Folium.
"""

import folium
from folium import plugins
from food_get.analysis.agg_metrics import track_comparison_df


def create_base_map():
    """
    creates base folium map with tiles and zoom restrictions
    """

    m = folium.Map(
        location=[41.83491987636846, -87.62004994799588],
        zoom_start=10.6,
        zoomSnap=0.5,
        tiles=None,
        min_zoom=10,
        max_zoom=12,
        min_lat=41.6,
        max_lat=42.1,
        min_lon=-87.27481026390364,
        max_lon=-87.981026390364,
        max_bounds=True,
    )
    base_map = folium.FeatureGroup(name="Basemap", overlay=True, control=False)
    folium.TileLayer(tiles="cartodb positron").add_to(base_map)
    base_map.add_to(m)
    # m.fit_bounds(m.get_bounds(), padding=(30, 30))

    return m


def create_tracks_inclusion(name=None):
    """
    creates map to show which tracks we are using and dropping as well as waterway
    adjustments
    """
    m = create_base_map()

    map_tract_inclusion_settings(m)

    folium.LayerControl(collapsed=False).add_to(m)

    if name:
        output = name + ".html"
        m.save(output)
    else:
        return m


def create_historic_map(df, name=None):
    """
    Create the map for the 2010 - 2019 Food Atlas metric
    """
    m = create_base_map()

    map_historic_settings(df, m)

    folium.LayerControl(collapsed=False).add_to(m)

    if name:
        output = name + ".html"
        m.save(output)
    else:
        return m


def create_2022_map(metrics_df, grocery_df, name=None):
    """
    Create the map for the constructed 2022 Food Atlas metric with grocery stores
    """
    m = create_base_map()

    map_2022_settings(metrics_df, grocery_df, m)

    folium.LayerControl(collapsed=False).add_to(m)

    if name:
        output = name + ".html"
        m.save(output)
    else:
        return m


def create_total_map(metrics_df, grocery_df, name=None):
    """
    Create the map that includes all labels for the conclusions.
    """
    m = create_base_map()

    map_historic_settings(metrics_df, m)

    map_2022_settings(metrics_df, grocery_df, m)

    folium.LayerControl(collapsed=False).add_to(m)

    if name:
        output = name + ".html"
        m.save(output)
    else:
        return m


def map_tract_inclusion_settings(m):
    """
    Adds styles and layers for create_tracks_inclusion(). Takes a base map object that
    is return from create_base_map() m as input.

    No return
    """
    # prep data
    tracts_keep, tracts_drop, tracts_keep_shore, lake = track_comparison_df()

    styleKeep = {"color": "#005AB5"}
    styleDrop = {"color": "#DC3220"}
    styleLake = {"color": "#9ccaff"}
    styleKeepShore = {"color": "#005AB5"}

    tooltip1 = folium.GeoJsonTooltip(
        fields=["geoid10"],
        aliases=["Tract ID:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
        max_width=800,
    )
    tooltip2 = folium.GeoJsonTooltip(
        fields=["geoid10"],
        aliases=["Tract ID:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
        max_width=800,
    )
    tooltip3 = folium.GeoJsonTooltip(
        fields=["geoid10"],
        aliases=["Tract ID:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
        max_width=800,
    )

    folium.GeoJson(
        tracts_keep,
        name="Keep with Waterways",
        style_function=lambda x: styleKeepShore,
        overlay=False,
        show=True,
        tooltip=tooltip1,
    ).add_to(m)

    folium.GeoJson(
        tracts_keep_shore,
        name="Keep without Waterways",
        style_function=lambda x: styleKeep,
        overlay=False,
        show=False,
        tooltip=tooltip3,
    ).add_to(m)

    folium.GeoJson(
        tracts_drop,
        name="Dropped Tracts",
        style_function=lambda x: styleDrop,
        overlay=True,
        show=True,
        tooltip=tooltip2,
    ).add_to(m)

    folium.GeoJson(
        lake,
        name="Waterways",
        style_function=lambda x: styleLake,
        overlay=True,
        show=False,
    ).add_to(m)


def map_2022_settings(metrics_df, grocery_df, m):
    """
    Adds styles and layers for create_2022_map(). Takes a base map object that
    is return from create_base_map() m as input.

    No return
    """
    # styles
    colors_2022 = ["#8856a7", "#9ebcda", "#e0ecf4"]  # dark  # med  # light

    stripes_lowa = folium.plugins.pattern.StripePattern(
        angle=-45, opacity=1, color=colors_2022[0]
    ).add_to(m)
    stripes_meda = folium.plugins.pattern.StripePattern(
        angle=-45, opacity=1, color=colors_2022[1]
    ).add_to(m)
    stripes_higha = folium.plugins.pattern.StripePattern(
        angle=-45, opacity=1, color=colors_2022[2]
    ).add_to(m)

    circles = folium.plugins.pattern.CirclePattern(
        width=10,
        height=10,
        radius=3,
        fill_opacity=1,
        opacity=0.5,
        fill_color="#808080",
        color="#808080",
    ).add_to(m)

    def style_function_2022(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }
        if feature["properties"]["lapophalfshare_2022"] is not None:
            if feature["properties"]["lapophalfshare_2022"] <= 1 / 3:
                default_style["fillColor"] = colors_2022[0]
                default_style["fillOpacity"] = 0.7
            elif feature["properties"]["lapophalfshare_2022"] <= 2 / 3:
                default_style["fillColor"] = colors_2022[1]
                default_style["fillOpacity"] = 0.7
            else:
                default_style["fillColor"] = colors_2022[2]
                default_style["fillOpacity"] = 0.7
        else:
            default_style["fillPattern"] = circles

        return default_style

    def style_function_2022_lowi(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }
        if feature["properties"]["lapophalfshare_2022"] is not None:
            if feature["properties"]["lapophalfshare_2022"] <= 1 / 3:
                default_style["fillColor"] = colors_2022[0]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2022"] == 1:
                    default_style["fillPattern"] = stripes_lowa
            elif feature["properties"]["lapophalfshare_2022"] <= 2 / 3:
                default_style["fillColor"] = colors_2022[1]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2022"] == 1:
                    default_style["fillPattern"] = stripes_meda
            else:
                default_style["fillColor"] = colors_2022[2]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2022"] == 1:
                    default_style["fillPattern"] = stripes_higha
        else:
            default_style["fillPattern"] = circles

        return default_style

    def style_function_diff(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }
        if feature["properties"]["10_22_diff"] == "Better":
            default_style["fillColor"] = "#99d8c9"
            default_style["fillOpacity"] = 0.7
        elif feature["properties"]["10_22_diff"] == "Worse":
            default_style["fillColor"] = "#ef6548"
            default_style["fillOpacity"] = 0.7
        else:
            default_style["fillColor"] = "#bdbdbd"
            default_style["fillOpacity"] = 0.7

        return default_style

    tooltip_22 = folium.GeoJsonTooltip(
        fields=["GEOID_TRACT_20", "2022_prop_label"],
        aliases=["Tract ID:", "2022 Low-Access Proportion:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
        max_width=800,
    )

    folium.GeoJson(
        metrics_df,
        name="2022 Access Proportion",
        style_function=style_function_2022,
        tooltip=tooltip_22,
        overlay=False,
        show=True,
    ).add_to(m)

    tooltip_22_lowi = folium.GeoJsonTooltip(
        fields=["GEOID_TRACT_20", "2022_prop_label"],
        aliases=["Tract ID:", "2022 Low-Access Proportion:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
    background-color: #F0EFEF;
    border: 2px solid black;
    border-radius: 3px;
    box-shadow: 3px;
    """,
        max_width=800,
    )

    folium.GeoJson(
        metrics_df,
        name="2022 Access Proportion with Low-Income",
        style_function=style_function_2022_lowi,
        tooltip=tooltip_22_lowi,
        overlay=False,
        show=False,
    ).add_to(m)

    tooltip_diff = folium.GeoJsonTooltip(
        fields=[
            "GEOID_TRACT_20",
            "lapophalfshare_2019",
            "lapophalfshare_2022",
            "10_22_diff",
        ],
        aliases=[
            "Tract ID:",
            "2019 Low-Access Proportion:",
            "2022 Low-Access Proportion:",
            "2019-2022 Change in Food Access:",
        ],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    folium.GeoJson(
        metrics_df,
        name="2019-2022 Change in Food Access",
        style_function=style_function_diff,
        tooltip=tooltip_diff,
        overlay=False,
        show=False,
    ).add_to(m)

    tooltip_groc = folium.GeoJsonTooltip(
        fields=["store_name", "address", "is_snap_map"],
        aliases=["Store Name:", "Address:", "SNAP Eligible:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
        """,
        max_width=800,
    )

    folium.GeoJson(
        grocery_df,
        name="Grocery Stores",
        marker=folium.Circle(
            radius=200,
            fill_color="#005AB5",
            fill_opacity=0.4,
            color="#005AB5",
            weight=2,
        ),
        tooltip=tooltip_groc,
        overlay=True,
        show=False,
    ).add_to(m)


def map_historic_settings(df, m):
    """
    Adds styles and layers for create_historic_map(). Takes a base map object that
    is return from create_base_map() m as input.

    No return
    """
    colors = ["#e34a33", "#fdbb84", "#fee8c8"]  # dark  # med  # light

    def style_function_2010_lowi(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }
        if feature["properties"]["lapophalfshare_2010"] is not None:
            if feature["properties"]["lapophalfshare_2010"] <= 1 / 3:
                default_style["fillColor"] = colors[0]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2015"] == 1:
                    default_style["fillPattern"] = stripes_lowa

            elif feature["properties"]["lapophalfshare_2010"] <= 2 / 3:
                default_style["fillColor"] = colors[1]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2015"] == 1:
                    default_style["fillPattern"] = stripes_meda
            else:
                default_style["fillColor"] = colors[2]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2015"] == 1:
                    default_style["fillPattern"] = stripes_higha
        else:
            default_style["fillPattern"] = circles

        return default_style

    def style_function_2010(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }
        if feature["properties"]["lapophalfshare_2010"] is not None:
            if feature["properties"]["lapophalfshare_2010"] <= 1 / 3:
                default_style["fillColor"] = colors[0]
                default_style["fillOpacity"] = 0.7

            elif feature["properties"]["lapophalfshare_2010"] <= 2 / 3:
                default_style["fillColor"] = colors[1]
                default_style["fillOpacity"] = 0.7
            else:
                default_style["fillColor"] = colors[2]
                default_style["fillOpacity"] = 0.7
        else:
            default_style["fillPattern"] = circles

        return default_style

    def style_function_2015_lowi(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }
        if feature["properties"]["lapophalfshare_2015"] is not None:
            if feature["properties"]["lapophalfshare_2015"] <= 1 / 3:
                default_style["fillColor"] = colors[0]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2015"] == 1:
                    default_style["fillPattern"] = stripes_lowa

            elif feature["properties"]["lapophalfshare_2015"] <= 2 / 3:
                default_style["fillColor"] = colors[1]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2015"] == 1:
                    default_style["fillPattern"] = stripes_meda
            else:
                default_style["fillColor"] = colors[2]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2015"] == 1:
                    default_style["fillPattern"] = stripes_higha
        else:
            default_style["fillPattern"] = circles

        return default_style

    def style_function_2015(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }
        if feature["properties"]["lapophalfshare_2015"] is not None:
            if feature["properties"]["lapophalfshare_2015"] <= 1 / 3:
                default_style["fillColor"] = colors[0]
                default_style["fillOpacity"] = 0.7

            elif feature["properties"]["lapophalfshare_2015"] <= 2 / 3:
                default_style["fillColor"] = colors[1]
                default_style["fillOpacity"] = 0.7
            else:
                default_style["fillColor"] = colors[2]
                default_style["fillOpacity"] = 0.7
        else:
            default_style["fillPattern"] = circles

        return default_style

    def style_function_2019_lowi(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }
        if feature["properties"]["lapophalfshare_2019"] is not None:
            if feature["properties"]["lapophalfshare_2019"] <= 1 / 3:
                default_style["fillColor"] = colors[0]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2019"] == 1:
                    default_style["fillPattern"] = stripes_lowa
            elif feature["properties"]["lapophalfshare_2019"] <= 2 / 3:
                default_style["fillColor"] = colors[1]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2019"] == 1:
                    default_style["fillPattern"] = stripes_meda
            else:
                default_style["fillColor"] = colors[2]
                default_style["fillOpacity"] = 0.7
                if feature["properties"]["LowIncomeTracts_2019"] == 1:
                    default_style["fillPattern"] = stripes_higha
        else:
            default_style["fillPattern"] = circles

        return default_style

    def style_function_2019(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }
        if feature["properties"]["lapophalfshare_2019"] is not None:
            if feature["properties"]["lapophalfshare_2019"] <= 1 / 3:
                default_style["fillColor"] = colors[0]
                default_style["fillOpacity"] = 0.7
            elif feature["properties"]["lapophalfshare_2019"] <= 2 / 3:
                default_style["fillColor"] = colors[1]
                default_style["fillOpacity"] = 0.7
            else:
                default_style["fillColor"] = colors[2]
                default_style["fillOpacity"] = 0.7
        else:
            default_style["fillPattern"] = circles

        return default_style

    stripes_lowa = folium.plugins.pattern.StripePattern(
        angle=-45, opacity=1, color=colors[0]
    ).add_to(m)
    stripes_meda = folium.plugins.pattern.StripePattern(
        angle=-45, opacity=1, color=colors[1]
    ).add_to(m)
    stripes_higha = folium.plugins.pattern.StripePattern(
        angle=-45, opacity=1, color=colors[2]
    ).add_to(m)

    circles = folium.plugins.pattern.CirclePattern(
        width=10,
        height=10,
        radius=3,
        fill_opacity=1,
        opacity=0.5,
        fill_color="#808080",
        color="#808080",
    ).add_to(m)

    tooltip_10 = folium.GeoJsonTooltip(
        fields=["GEOID_TRACT_20", "2010_prop_label"],
        aliases=["Tract ID:", "2010 Low-Access Proportion:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )
    tooltip_10_lowi = folium.GeoJsonTooltip(
        fields=["GEOID_TRACT_20", "2010_prop_label"],
        aliases=["Tract ID:", "2010 Low-Access Proportion:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    tooltip_15 = folium.GeoJsonTooltip(
        fields=["GEOID_TRACT_20", "2015_prop_label"],
        aliases=["Tract ID:", "2015 Low-Access Proportion:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    tooltip_15_lowi = folium.GeoJsonTooltip(
        fields=["GEOID_TRACT_20", "2015_prop_label"],
        aliases=["Tract ID:", "2015 Low-Access Proportion:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    tooltip_19 = folium.GeoJsonTooltip(
        fields=["GEOID_TRACT_20", "2019_prop_label"],
        aliases=["Tract ID:", "2019 Low-Access Proportion:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    tooltip_19_lowi = folium.GeoJsonTooltip(
        fields=["GEOID_TRACT_20", "2019_prop_label"],
        aliases=["Tract ID:", "2019 Low-Access Proportion:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    folium.GeoJson(
        df,
        name="2010 Access Proportion",
        style_function=style_function_2010,
        tooltip=tooltip_10,
        overlay=False,
        show=True,
    ).add_to(m)

    folium.GeoJson(
        df,
        name="2010 Access Proportion and Low-Income",
        style_function=style_function_2010_lowi,
        tooltip=tooltip_10_lowi,
        overlay=False,
        show=False,
    ).add_to(m)

    folium.GeoJson(
        df,
        name="2015 Access Proportion",
        style_function=style_function_2015,
        tooltip=tooltip_15,
        overlay=False,
        show=False,
    ).add_to(m)

    folium.GeoJson(
        df,
        name="2015 Access Proportion and Low-Income",
        style_function=style_function_2015_lowi,
        tooltip=tooltip_15_lowi,
        overlay=False,
        show=False,
    ).add_to(m)

    folium.GeoJson(
        df,
        name="2019 Access Proportion",
        style_function=style_function_2019,
        tooltip=tooltip_19,
        overlay=False,
        show=False,
    ).add_to(m)

    folium.GeoJson(
        df,
        name="2019 Access Proportion and Low-Income",
        style_function=style_function_2019_lowi,
        tooltip=tooltip_19_lowi,
        overlay=False,
        show=False,
    ).add_to(m)
