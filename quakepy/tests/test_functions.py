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
        p = Point(40.730610, -73.935242)
        gdf = gpd.read_file("data/raw/all_month.geojson")

        s_distance = func.calc_curve_distance(gdf, p)

        assert len(gdf) == len(s_distance)
        assert s_distance.dtype == int

    def test_div_rounding(self):
        #p = Point(40.730610, -73.935242)
        p = Point(34.028622, -117.810333)
        gdf = gpd.read_file("data/raw/all_month.geojson")

        s_distance = func.calc_curve_distance(gdf[:1], p)

        assert s_distance[0] == 157

    def test_get_closest_n(self):
        """Ensure that a length of N is retruned
        and the ordering is correct.
        """
        n = 5
        p = Point(40.730610, -73.935242)

        gdf = gpd.read_file("data/raw/all_month.geojson")
        gdf["distance"] = func.calc_curve_distance(gdf, p)
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

        gdf_one["distance"] = func.calc_curve_distance(gdf_one, p)
        gdf_two["distance"] = func.calc_curve_distance(gdf_two, p)

        df_one_closest = func.get_closest_n(gdf_one, 10)
        df_two_closest = func.get_closest_n(gdf_two, 10)

        top_10_one_str = func.pretty_print(df_one_closest)
        top_10_two_str = func.pretty_print(df_two_closest)

        assert top_10_one_str == top_10_two_str

    def test_argparse(self):
       float_range = func.float_range(-90, 90)
       assert float_range(40.730610)
       assert float_range(-73.935242)

       with self.assertRaises(ArgumentTypeError):
            float_range(200)
