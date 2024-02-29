import folium
from folium import plugins
import geopandas as gpd
import pandas as pd
import numpy as np
import geopandas as gpd
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
    creates with tracks we are using and dropping as well as shoreline
    adjustments
    """
    # create_data
    tracts_keep, tracts_drop, tracts_keep_shore, lake = track_comparison_df()

    m = create_base_map()

    styleKeep = {"color": "blue"}
    styleDrop = {"color": "red"}
    styleLake = {"color": "green"}
    styleKeepShore = {"color": "purple"}

    tooltip1 = folium.GeoJsonTooltip(
        fields=["geoid10"],
        aliases=["Tract Name:"],
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
        tracts_keep_shore,
        name="Keep Minus Shore",
        style_function=lambda x: styleKeep,
        overlay=False,
        show=True,
        tooltip=tooltip3,
    ).add_to(m)

    folium.GeoJson(
        tracts_keep,
        name="Keeping Full",
        style_function=lambda x: styleKeepShore,
        overlay=False,
        show=False,
        tooltip=tooltip1,
    ).add_to(m)

    folium.GeoJson(
        tracts_drop,
        name="Dropping",
        style_function=lambda x: styleDrop,
        overlay=True,
        show=True,
        tooltip=tooltip2,
    ).add_to(m)

    folium.GeoJson(
        lake,
        name="Lake",
        style_function=lambda x: styleLake,
        overlay=True,
        show=False,
    ).add_to(m)

    folium.LayerControl().add_to(m)

    if name:
        output = name + ".html"
        m.save(output)
    else:
        return m


def create_historic_map(df, name=None):
    m = create_base_map()

    # styles
    stripes = folium.plugins.pattern.StripePattern(angle=-45, opacity=0.5).add_to(m)

    colors_2010 = ["#e34a33", "#fdbb84", "#fee8c8"]  # dark  # med  # light
    colors_2015 = ["#8856a7", "#9ebcda", "#e0ecf4"]  # dark  # med  # light
    colors_2019 = ["#2ca25f", "#99d8c9", "#e5f5f9"]  # dark  # med  # light

    def style_function_2010(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }
        if feature["properties"]["lapophalfshare_2010"] is not None:
            if feature["properties"]["lapophalfshare_2010"] <= 1 / 3:
                default_style["fillColor"] = colors_2010[0]
                default_style["fillOpacity"] = 0.7
            elif feature["properties"]["lapophalfshare_2010"] <= 2 / 3:
                default_style["fillColor"] = colors_2010[1]
                default_style["fillOpacity"] = 0.7
            else:
                default_style["fillColor"] = colors_2010[2]
                default_style["fillOpacity"] = 0.7
        else:
            default_style["fillPattern"] = stripes

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
                default_style["fillColor"] = colors_2010[0]
                default_style["fillOpacity"] = 0.7
            elif feature["properties"]["lapophalfshare_2015"] <= 2 / 3:
                default_style["fillColor"] = colors_2010[1]
                default_style["fillOpacity"] = 0.7
            else:
                default_style["fillColor"] = colors_2010[2]
                default_style["fillOpacity"] = 0.7
        else:
            default_style["fillPattern"] = stripes

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
                default_style["fillColor"] = colors_2010[0]
                default_style["fillOpacity"] = 0.7
            elif feature["properties"]["lapophalfshare_2019"] <= 2 / 3:
                default_style["fillColor"] = colors_2010[1]
                default_style["fillOpacity"] = 0.7
            else:
                default_style["fillColor"] = colors_2010[2]
                default_style["fillOpacity"] = 0.7
        else:
            default_style["fillPattern"] = stripes

        return default_style

    tooltip_10 = folium.GeoJsonTooltip(
        fields=["GEOID_TRACT_20", "lapophalfshare_2010"],
        aliases=["Tract Name:", "2010 Low Access Proportion:"],
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
        fields=["GEOID_TRACT_20", "lapophalfshare_2015"],
        aliases=["Tract Name:", "2015 Low Access Proportion:"],
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
        fields=["GEOID_TRACT_20", "lapophalfshare_2019"],
        aliases=["Tract Name:", "2019 Low Access Proportion:"],
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
        name="2015 Access Proportion",
        style_function=style_function_2015,
        tooltip=tooltip_15,
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

    folium.LayerControl().add_to(m)

    if name:
        output = name + ".html"
        m.save(output)
    else:
        return m


def create_2022_map(df, name=None):
    m = create_base_map()

    # styles
    stripes = folium.plugins.pattern.StripePattern(angle=-45, opacity=0.5).add_to(m)

    colors_2022 = ["#e34a33", "#fdbb84", "#fee8c8"]  # dark  # med  # light

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
            default_style["fillPattern"] = stripes

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
        fields=["GEOID_TRACT_20", "lapophalfshare_2022"],
        aliases=["Tract Name:", "2022 Low Access Proportion:"],
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
        name="2022 Access Proportion",
        style_function=style_function_2022,
        tooltip=tooltip_22,
        overlay=False,
        show=True,
    ).add_to(m)

    tooltip_diff = folium.GeoJsonTooltip(
        fields=[
            "GEOID_TRACT_20",
            "lapophalfshare_2010",
            "lapophalfshare_2022",
            "10_22_diff",
        ],
        aliases=[
            "Tract Name:",
            "2010 Low Access Proportion:",
            "2022 Low Access Proportion:",
            "Change in Food Access 2010-2022:",
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
        df,
        name="Change in Food Access",
        style_function=style_function_diff,
        tooltip=tooltip_diff,
        overlay=False,
        show=False,
    ).add_to(m)

    folium.LayerControl().add_to(m)

    if name:
        output = name + ".html"
        m.save(output)
    else:
        return m


def create_total_map(name=None):
    m = create_base_map()

    if name:
        output = name + ".html"
        m.save(output)
    else:
        return m
