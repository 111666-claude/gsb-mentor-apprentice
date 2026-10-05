"""命令行入口。"""

import argparse
import json

from . import core, report


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="mentor")
    ap.add_argument("--sample", choices=["days", "cap", "boost", "replay", "work"])
    sub = ap.add_subparsers(dest="cmd")
    report_parser = sub.add_parser("report")
    report_parser.add_argument("--pairs", required=True)
    report_parser.add_argument("--req-id", required=True)
    report_parser.add_argument("--cap", type=int, default=3)
    report_parser.add_argument("--boost", action="store_true")
    args = ap.parse_args(argv)

    if args.sample:
        from . import samples
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    decisions = list(core.iter_decisions(_load(args.pairs), args.boost, args.cap, core.Counter()))
    print(report.render(decisions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
