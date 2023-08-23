import argparse
import logging

from shapely import Point
from quakepy import functions as func

logging.basicConfig(level=logging.INFO)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [LAT] [LON]",
        description="Get nearest 10 earthquakes in the last month"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument("lat", type=float_range(-90, 91), nargs=1)
    parser.add_argument("lon", type=float_range(-90, 91), nargs=1)

    return parser

def float_range(mini,maxi):
    """Return function handle of an argument type function for
       ArgumentParser checking a float range: mini <= arg <= maxi
         mini - minimum acceptable argument
         maxi - maximum acceptable argument"""

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

def get_top_n(p: Point):
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