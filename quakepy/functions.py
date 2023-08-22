import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
from pandas import Series, DataFrame
from shapely import Point

import requests
from requests.exceptions import HTTPError, Timeout

def pretty_print(df: DataFrame) -> str:
    x = df["title"].to_list()
    y = df["distance"].to_list()

    return lambda x, y: str(x) + " || " + str(y)

def calc_curve_distance(gdf: GeoDataFrame, p: Point) -> Series:
    s = gdf.distance(p).sort_values(ascending=False)
    s.name = "distance"

    return s

def get_closest_n(s: Series, n: int) -> Series:
    s = s.sort_values(ascending=False)

    s = s[:n]

    return s

def get_joined_data(gs_title: Series, gs_distance: Series) -> DataFrame:
    df = pd.merge(gs_title, gs_distance, left_index=True, right_index=True)

    return df

def get_data() -> GeoDataFrame:
    # path_to_data = "data/raw/all_month.geojson"
    # gdf = gpd.read_file(path_to_data)
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

    response = call_api(url)

    gdf = gpd.read_file(response)

    return gdf

def call_api(url:str) -> str:
    try:
        response = requests.get(
            url,
            params={'q': 'requests+language:python'},
            timeout=10
        )

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except Timeout as http_timeout:
        print('The request timed out')
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return response.text