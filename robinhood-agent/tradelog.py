#!/usr/bin/env python3
"""Trade log — the record that lets strategies be compared on our own data.

Every fill goes in `trades.csv` tagged with the strategy that produced it.
The CSV stores only observed facts (entry, qty, initial stop, exit, realized
dollars); everything derived — planned risk, R-multiple, win/loss — is
computed here so the file can never carry a stale calculation.

Why R-multiples: this account funds strategies unequally and always will.
A $28 legacy position and a $150 momentum position are not comparable in
dollars, but they are comparable in R (realized / planned risk). R is the
only unit in which S1, S2 and S8 can be ranked against each other.

Usage:
    python3 tradelog.py report          per-strategy stats
    python3 tradelog.py open            open positions and their risk
    python3 tradelog.py add --help      append a new trade
"""

import argparse
import csv
import os
import statistics
import sys

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trades.csv")

FIELDS = [
    "trade_id", "strategy", "symbol", "open_date", "open_time_et", "entry",
    "qty", "stop_initial", "stop_latency_sec", "close_date", "close_time_et",
    "exit", "realized_usd", "exit_reason", "catalyst", "notes",
]


def _f(row, key):
    """Parse a float field, returning None when blank or unparseable."""
    val = (row.get(key) or "").strip()
    if not val:
        return None
    try:
        return float(val)
    except ValueError:
        return None


def load():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        entry, qty = _f(row, "entry"), _f(row, "qty")
        stop, realized = _f(row, "stop_initial"), _f(row, "realized_usd")

        # Planned risk is what we said we'd lose if the stop filled at its price.
        row["_risk"] = (entry - stop) * qty if None not in (entry, qty, stop) else None
        row["_realized"] = realized
        row["_open"] = realized is None
        # R only means something when both a stop and an outcome exist.
        row["_r"] = (
            realized / row["_risk"]
            if realized is not None and row["_risk"] not in (None, 0)
            else None
        )
        row["_latency"] = _f(row, "stop_latency_sec")
    return rows


def _stats(rows):
    """Aggregate a set of closed trades."""
    realized = [r["_realized"] for r in rows if r["_realized"] is not None]
    rs = [r["_r"] for r in rows if r["_r"] is not None]
    wins = [x for x in realized if x > 0]
    losses = [x for x in realized if x < 0]
    gross_loss = abs(sum(losses))
    return {
        "n": len(realized),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": len(wins) / len(realized) * 100 if realized else None,
        "total": sum(realized),
        "avg_win": sum(wins) / len(wins) if wins else None,
        "avg_loss": sum(losses) / len(losses) if losses else None,
        # Profit factor is undefined, not infinite, with no losing trade yet.
        "pf": (sum(wins) / gross_loss) if gross_loss else None,
        "avg_r": sum(rs) / len(rs) if rs else None,
        "total_r": sum(rs) if rs else None,
        "best_r": max(rs) if rs else None,
        "worst_r": min(rs) if rs else None,
        "n_r": len(rs),
    }


def _fmt(val, spec="+.2f", dash="—"):
    return dash if val is None else format(val, spec)


def report(rows):
    closed = [r for r in rows if not r["_open"]]
    open_rows = [r for r in rows if r["_open"]]

    print("=" * 74)
    print("TRADE LOG — per-strategy results")
    print("=" * 74)

    if not closed:
        print("\nNo closed trades logged yet.\n")
        return

    strategies = sorted({r["strategy"] for r in closed})
    print(f"\n{'Strat':<8}{'n':>3}{'W':>3}{'L':>3}{'Win%':>7}"
          f"{'Total $':>10}{'Avg R':>8}{'Tot R':>8}{'PF':>7}")
    print("-" * 74)
    for name in strategies:
        s = _stats([r for r in closed if r["strategy"] == name])
        print(f"{name:<8}{s['n']:>3}{s['wins']:>3}{s['losses']:>3}"
              f"{_fmt(s['win_rate'], '.0f'):>6}%"
              f"{_fmt(s['total']):>10}"
              f"{_fmt(s['avg_r']):>8}"
              f"{_fmt(s['total_r']):>8}"
              f"{_fmt(s['pf'], '.2f'):>7}")

    total = _stats(closed)
    print("-" * 74)
    print(f"{'ALL':<8}{total['n']:>3}{total['wins']:>3}{total['losses']:>3}"
          f"{_fmt(total['win_rate'], '.0f'):>6}%"
          f"{_fmt(total['total']):>10}"
          f"{_fmt(total['avg_r']):>8}"
          f"{_fmt(total['total_r']):>8}"
          f"{_fmt(total['pf'], '.2f'):>7}")

    # The headline number. Positive avg R means the process makes money per
    # unit of risk taken; below +1.00R means no trade has yet earned back
    # the distance it was risking.
    print(f"\nExpectancy: {_fmt(total['avg_r'])}R per closed trade "
          f"(n={total['n_r']} with a recorded stop)")
    if total["best_r"] is not None:
        print(f"Best {_fmt(total['best_r'])}R   Worst {_fmt(total['worst_r'])}R")
        if total["best_r"] < 1.0:
            print("  ! No trade has reached +1.00R. Winners are being cut "
                  "shorter than the risk taken to get them.")

    print("\nStop-placement latency (fill -> protective stop live):")
    lat = [(r["symbol"], r["_latency"]) for r in rows if r["_latency"] is not None]
    if lat:
        vals = [v for _, v in lat]
        print(f"  median {statistics.median(vals):.0f}s   "
              f"max {max(vals):.0f}s")
        for sym, val in sorted(lat, key=lambda x: -x[1]):
            flag = "  <-- UNPROTECTED WINDOW" if val > 60 else ""
            print(f"    {sym:<6}{val:>7.0f}s{flag}")

    if open_rows:
        print(f"\n{len(open_rows)} position(s) still open — see `open`.")
    print()


def show_open(rows):
    open_rows = [r for r in rows if r["_open"]]
    print("=" * 74)
    print("OPEN POSITIONS")
    print("=" * 74)
    if not open_rows:
        print("\nFlat.\n")
        return
    total_risk = 0.0
    for r in open_rows:
        risk = r["_risk"]
        if risk:
            total_risk += risk
        print(f"\n{r['symbol']}  [{r['strategy']}]  {r['qty']} @ {r['entry']}")
        print(f"  stop {r['stop_initial']}   planned risk {_fmt(risk, '.2f')}")
        if r["notes"]:
            print(f"  {r['notes']}")
    print(f"\nTotal open risk: ${total_risk:.2f}\n")


def add(args):
    rows = load()
    next_id = max((int(r["trade_id"]) for r in rows if r["trade_id"].isdigit()),
                  default=0) + 1
    record = {f: "" for f in FIELDS}
    record["trade_id"] = str(next_id)
    for field in FIELDS[1:]:
        val = getattr(args, field, None)
        if val is not None:
            record[field] = str(val)
    write_header = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(record)
    print(f"Logged trade {next_id}: {record['strategy']} {record['symbol']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("report", help="per-strategy results")
    sub.add_parser("open", help="open positions and their risk")

    p_add = sub.add_parser("add", help="append a trade")
    for field in FIELDS[1:]:
        p_add.add_argument(f"--{field}")

    args = parser.parse_args()
    if args.cmd == "add":
        add(args)
    elif args.cmd == "open":
        show_open(load())
    elif args.cmd == "report":
        report(load())
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
