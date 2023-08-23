import logging
from typing import List

import pandas as pd
import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame
from pandas import Series, DataFrame
from shapely import Point, wkb
from pyproj import Transformer

import requests
from requests.exceptions import HTTPError, Timeout

logging.basicConfig(level=logging.INFO)

def pretty_print(df: DataFrame) -> str:
    x_title = df["title"].to_list()
    y_distance = df["distance"].to_list()

    return ''.join([str(x) + " || " + str(y) + '\n' for x,y in zip(x_title, y_distance)])

def calc_curve_distance(gdf: GeoDataFrame, p: Point) -> Series:
    logging.info("Reprojecting geometry")
    gdf = gdf.to_crs(epsg=32663)

    transformer = Transformer.from_crs("EPSG:4979", "EPSG:32663")
    p = Point(transformer.transform(p.x, p.y))

    s_distance = gdf.distance(p).divide(1000).round(0).astype(int)
    s_distance.name = "distance"

    return s_distance

def get_closest_n(df: DataFrame, n: int) -> DataFrame:
    return df.sort_values(by="distance", ascending=True)[:n]

def get_data(columns: List[str]) -> GeoDataFrame:
    # path_to_data = "data/raw/all_month.geojson"
    # gdf = gpd.read_file(path_to_data)
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

    response = call_api(url)

    gdf = gpd.read_file(response)[columns]

    logging.info(f"Finished processing {len(gdf)} rows")

    _drop_z = lambda geom: wkb.loads(wkb.dumps(geom, output_dimension=2))
    gdf.geometry = gdf.geometry.transform(_drop_z)

    gdf_depublicated = gdf.drop_duplicates(subset=["geometry"])

    logging.info(f"Depublicated {len(gdf) - len(gdf_depublicated)} rows")

    return gdf_depublicated

def call_api(url:str) -> str:
    try:
        logging.info(f"GET {url}")
        response = requests.get(
            url,
            params={'q': 'requests+language:python'},
            timeout=10
        )

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except Timeout as http_timeout:
        logging.info("The request timed out (might be retried)")
    except HTTPError as http_err:
        logging.info(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.info(f"Other error occurred: {err}")

    return response.text