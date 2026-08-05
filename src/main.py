"""Little CLI that ties the utils together, mostly for manual poking."""

import argparse
import sys

from src import api, utils


def main(argv=None):
    parser = argparse.ArgumentParser(prog="playground")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_slug = sub.add_parser("slug", help="slugify some text")
    p_slug.add_argument("text", nargs="+")

    p_fetch = sub.add_parser("fetch", help="GET a URL and print JSON")
    p_fetch.add_argument("url")

    args = parser.parse_args(argv)

    if args.cmd == "slug":
        print(utils.slugify(" ".join(args.text)))
    elif args.cmd == "fetch":
        try:
            status, body = api.get(args.url)
            print(status, body)
        except api.ApiError as err:
            print(f"error: {err}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
