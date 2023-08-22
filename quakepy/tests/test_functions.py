from shapely import Point
from quakepy import functions as func

def test_calc_curve_distance():
    lat = 40.730610
    lon = -73.935242

    p = Point(lat, lon)

    dist = func.calc_curve_distance(p)