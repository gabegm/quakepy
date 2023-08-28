from argparse import ArgumentParser
import logging

from shapely import Point
from quakepy import functions as func

logging.basicConfig(level=logging.INFO)

def init_argparse() -> ArgumentParser:
    """Adds two run time arguments for the user to 
    pass the latitude and longitude coorindates.

    Returns:
        ArgumentParser: Parses the runtime arguments.
    """
    parser = ArgumentParser(
        usage="%(prog)s [LAT] [LON]",
        description="Get nearest 10 earthquakes in the last month"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 0.1.0"
    )
    parser.add_argument("lat", type=func.float_range(-90, 90), nargs=1)
    parser.add_argument("lon", type=func.float_range(-180, 180), nargs=1)

    return parser

def get_top_n(p: Point):
    """Returnes the nearest 10 earthquakes
    based on the distance to the point provided.

    Args:
        p (Point): Coordinates entered at runtime

    Returns:
        _type_: Pretty printed results of nearest 10 earthquakes
    """
    columns = ["title", "geometry"]
    gdf = func.get_data(columns)

    gdf["distance"] = func.calc_curve_distance(gdf, p)
    df_closest = func.get_closest_n(gdf, 10)
    top_10_str = func.pretty_print(df_closest)

    return top_10_str

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    logging.info(f"Received coordinates: {args.lat[0]}, {args.lon[0]}")

    p = Point(args.lat, args.lon)

    s = get_top_n(p)

    print(s)

if __name__ == "__main__":
    main()