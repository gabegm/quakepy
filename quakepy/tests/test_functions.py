import unittest
from argparse import ArgumentTypeError

from shapely import Point
from quakepy import functions as func
import geopandas as gpd

class TestSum(unittest.TestCase):
    def test_calc_curve_distance(self):
        """Ensure that calculated distance has the
        same length as the original dataframe.
        """
        p = Point(-73.935242, 40.730610)
        gdf = gpd.read_file("data/raw/all_month.geojson")[:1]

        s_distance = func.haversine(gdf["geometry"].values, p, 6371)

        assert len(gdf) == len(s_distance)
        assert s_distance.dtype == int
        assert s_distance[0] == 4003

    def test_get_closest_n(self):
        """Ensure that a length of N is retruned
        and the ordering is correct.
        """
        n = 5
        p = Point(40.730610, -73.935242)

        gdf = gpd.read_file("data/raw/all_month.geojson")
        gdf["distance"] = func.haversine(gdf["geometry"].values, p, 6371)
        gdf_n = func.get_closest_n(gdf, n)

        assert len(gdf_n) == n
        assert gdf_n["distance"][:1].values[0] < gdf_n["distance"][-1:].values[0]

    def test_get_data(self):
        """Ensure that the geometry does not contain a z
        coordinate and no duplicate geometries remain.
        """
        columns = ["title", "geometry"]
        gdf = func.get_data(columns)
        n_duplicates = gdf.drop_duplicates(subset=["geometry"])

        assert gdf["geometry"].z.isna().all()
        assert len(n_duplicates) == len(gdf)

    def test_pretty_print(self):
        """Ensure the same nearest N earthquakes 
        are always returned.
        """
        p = Point(40.730610, -73.935242)
        gdf_one = gpd.read_file("data/raw/all_month.geojson")
        gdf_two = gpd.read_file("data/raw/all_month.geojson")

        gdf_one["distance"] = func.haversine(gdf_one["geometry"].values, p, 6371)
        gdf_two["distance"] = func.haversine(gdf_two["geometry"].values, p, 6371)

        df_one_closest = func.get_closest_n(gdf_one, 10)
        df_two_closest = func.get_closest_n(gdf_two, 10)

        top_10_one_str = func.pretty_print(df_one_closest)
        top_10_two_str = func.pretty_print(df_two_closest)

        assert top_10_one_str == top_10_two_str

    def test_argparse(self):
        """Ensure arguments are of type float 
        and within range.
        """
        float_range = func.float_range(-90, 90)
        assert float_range(40.730610)
        assert float_range(-73.935242)

        with self.assertRaises(ArgumentTypeError):
                float_range(200)
