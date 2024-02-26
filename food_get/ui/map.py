import folium
import geopandas as gpd
import pandas as pd
import numpy as np
import geopandas as gpd
from food_get.data.data_extract_census import tracts_2010_key


def create_base_map():
    """
    creates base folium map with tiles and zoom restrictions
    """
    m = folium.Map(
        location=[41.87491987636846, -87.62004994799588],
        zoom_start=10.5,
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
    folium.TileLayer(tiles="cartodb voyager").add_to(base_map)
    base_map.add_to(m)

    return m


def create_tracks_inclusion(name=None):
    """
    creates with tracks we are using and dropping as well as shoreline
    adjustments
    """
    # prep data
    geojson_data = gpd.GeoDataFrame(tracts_2010_key())
    lake = gpd.read_file(
        "/Users/austinsteinhart/Desktop/CAPP122/food.get/food_get/data/raw_data/Lake_Michigan_Shoreline.geojson"
    )

    tracts_keep = geojson_data[geojson_data["relation"] == "one"]
    tracts_drop = geojson_data[geojson_data["relation"] == "many"]

    tracts_keep_shore = tracts_keep.overlay(lake, how="difference")

    m = create_base_map()

    styleKeep = {"color": "blue"}
    styleDrop = {"color": "red"}
    styleLake = {"color": "green"}
    styleKeepShore = {"color": "purple"}

    folium.GeoJson(
        tracts_keep_shore,
        name="Keep Minus Shore",
        style_function=lambda x: styleKeep,
        overlay=False,
        show=True,
    ).add_to(m)
    folium.GeoJson(
        tracts_keep,
        name="Keeping Full",
        style_function=lambda x: styleKeepShore,
        overlay=False,
        show=False,
    ).add_to(m)

    folium.GeoJson(
        tracts_drop,
        name="Dropping",
        style_function=lambda x: styleDrop,
        overlay=True,
        show=False,
    ).add_to(m)

    folium.GeoJson(
        lake, name="Lake", style_function=lambda x: styleLake, overlay=True, show=False
    ).add_to(m)

    folium.LayerControl().add_to(m)

    if name:
        output = name + ".html"
        m.save(output)
    else:
        return m


def create_historic_map(name=None):
    m = create_base_map()

    if name:
        output = name + ".html"
        m.save(output)
    else:
        return m


def create_2022_map(name=None):
    m = create_base_map()

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
