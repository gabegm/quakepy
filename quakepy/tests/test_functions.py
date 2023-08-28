import unittest

from shapely import Point
from quakepy import functions as func
import geopandas as gpd

class TestSum(unittest.TestCase):
    def test_calc_curve_distance(self):
        p = Point(40.730610, -73.935242)
        gdf = gpd.read_file("data/raw/all_month.geojson")

        gdf["distance"] = func.calc_curve_distance(gdf, p)

        assert len(gdf) == len(gdf)
        assert gdf["distance"].dtype == int

    def test_get_closest_n(self):
        n = 5
        p = Point(40.730610, -73.935242)

        gdf = gpd.read_file("data/raw/all_month.geojson")
        gdf["distance"] = func.calc_curve_distance(gdf, p)
        gdf_n = func.get_closest_n(gdf, n)

        assert len(gdf_n) == n
        assert int(gdf_n["distance"][:1]) < int(gdf_n["distance"][-1:])

    def test_get_data(self):
        columns = ["title", "geometry"]
        gdf = func.get_data(columns)
        n_duplicates = gdf.drop_duplicates(subset=["geometry"])

        assert gdf["geometry"].z.isna().all()
        assert len(n_duplicates) == len(gdf)

    def test_pretty_print(self):
        p = Point(40.730610, -73.935242)
        gdf_one = gpd.read_file("data/raw/all_month.geojson")
        gdf_two = gpd.read_file("data/raw/all_month.geojson")

        gdf_one["distance"] = func.calc_curve_distance(gdf_one, p)
        gdf_two["distance"] = func.calc_curve_distance(gdf_two, p)

        df_one_closest = func.get_closest_n(gdf_one, 10)
        df_two_closest = func.get_closest_n(gdf_two, 10)

        top_10_one_str = func.pretty_print(df_one_closest)
        top_10_two_str = func.pretty_print(df_two_closest)

        assert top_10_one_str == top_10_two_str