import argparse
from shapely import Point
from quakepy import functions as func

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [LAT] [LON]",
        description="Get nearest 10 earthquakes in the last month"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument("lat", nargs=1)
    parser.add_argument("lon", nargs=1)

    return parser

def get_top_n(p: Point):
    gdf = func.get_data()
    s = func.calc_curve_distance(gdf, p)
    s_closest = func.get_closest_n(s, 10)
    df_joined = func.get_joined_data(gdf["title"], s_closest)
    top_10_str = func.pretty_print(df_joined)

    return top_10_str

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    while (not args.lat or not args.lon):
        print("Please enter two coordinates.")
        args = parser.parse_args()

    p = Point(args.lat, args.lon)

    s = get_top_n(p)

    print(s)

if __name__ == "__main__":
    main()