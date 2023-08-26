import logging
import argparse
from typing import List

import geopandas as gpd
from geopandas import GeoDataFrame
from pandas import Series, DataFrame
from shapely import Point, wkb
from pyproj import Transformer

import requests
from requests.exceptions import HTTPError, Timeout

logging.basicConfig(level=logging.INFO)

def pretty_print(df: DataFrame) -> str:
    """Pretty print DataFrame in the following format
    title || distance
    title || distance
    title || distance

    Args:
        df (DataFrame): DataFrame with top N earthquakes

    Returns:
        str: String representation of DataFrame
    """
    x_title = df["title"].to_list()
    y_distance = df["distance"].to_list()

    return ''.join([str(x) + " || " + str(y) + '\n' for x,y in zip(x_title, y_distance)])

def calc_curve_distance(gdf: GeoDataFrame, p: Point) -> Series:
    """Reproject both geometries from degrees into 
    metres and calculate the distance between the 
    point and all  points in the GeoDataFrame. 
    The distance is then converted into kilometres 
    and rounded to a whole number.

    Args:
        gdf (GeoDataFrame): List of earthquakes
        p (Point): Inpur coordinates

    Returns:
        Series: Calculated distance for each earthquake.
    """
    logging.info("Reprojecting geometry")
    gdf = gdf.to_crs(epsg=32663)

    transformer = Transformer.from_crs("EPSG:4979", "EPSG:32663")
    p = Point(transformer.transform(p.x, p.y))

    logging.info("Calculating distance in KM")
    s_distance = gdf.distance(p).divide(1000).round(0).astype(int)
    s_distance.name = "distance"

    return s_distance

def get_closest_n(df: DataFrame, n: int) -> DataFrame:
    """Sort rows by distance in ascending 
    order and return the top n rows.

    Args:
        df (DataFrame): DataFrame with list of earthquakes
        n (int): top N rows used for slicing

    Returns:
        DataFrame: Sorted by distance in ascending order
    """
    logging.info(f"Retrieving nearest {n} earthquakes")

    return df.sort_values(by="distance", ascending=True)[:n]

def get_data(columns: List[str]) -> GeoDataFrame:
    """Call the earthquake API to get the list 
    of earthquakes in the last 30 days and drop 
    the x coordinate as this is not needed. 
    Remove duplicate rows based on the geometry.

    Args:
        columns (List[str]): List of columns to slice.

    Returns:
        GeoDataFrame: DataFrame with list of earthquakes
    """
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

    response = call_api(url)

    gdf = gpd.read_file(response)[columns]

    logging.info(f"Finished processing {len(gdf)} rows")

    _drop_z = lambda geom: wkb.loads(wkb.dumps(geom, output_dimension=2))
    gdf.geometry = gdf.geometry.transform(_drop_z)

    logging.info("Dropped z coordinate from geometry")

    gdf_depublicated = gdf.drop_duplicates(subset=["geometry"])

    logging.info(f"Depublicated {len(gdf) - len(gdf_depublicated)} rows")

    return gdf_depublicated

def call_api(url:str) -> str:
    """Make a GET request based on the provided URL. 
    In case of a timeout requests will automatically retry.

    Args:
        url (str): Used to make the API call

    Returns:
        str: response text
    """
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

    logging.info(f"Response {response.status_code}")
    return response.text

def float_range(mini: float, maxi: float):
    """Return function handle of an argument type function for
       ArgumentParser checking a float range: mini <= arg <= maxi

    Args:
        mini (float): minimum acceptable argument
        maxi (float): maximum acceptable argument

    Raises:
        argparse.ArgumentTypeError: Not a floating point number
        argparse.ArgumentTypeError: Not in range specified

    Returns:
        _type_: type of float within specified range
    """
    # Define the function with default arguments
    def float_range_checker(arg):
        """New Type function for argparse - a float within predefined range."""

        try:
            f = float(arg)
        except ValueError:
            raise argparse.ArgumentTypeError("must be a floating point number")
        if f < mini or f > maxi:
            raise argparse.ArgumentTypeError("must be in range [" + str(mini) + " .. " + str(maxi)+"]")
        return f

    # Return function handle to checking function
    return float_range_checker