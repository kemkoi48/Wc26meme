"""Premarket position sizer — enforces the $150 cap and the 6% risk budget.

The screening is done by eye (Rule 1: name the news). This does the arithmetic
that must not be done by eye: how many shares fit, and whether the trade fits
in what is left of today's risk budget.

Usage:
  python3 premarket.py --account 542.25 --open AEYE:19:7.70:7.08 --open HHS:33:4.37:4.14 \
      --candidate TRUG:1.67:1.45

  --open      SYMBOL:QTY:ENTRY:STOP     (a position already on)
  --candidate SYMBOL:PRICE:STOP         (something you are thinking about)

Prints remaining risk budget, then for each candidate the largest share count
that fits both constraints, with its target from Rule 4.
"""

from __future__ import annotations

import argparse

MAX_NOTIONAL_USD = 150.0
RISK_BUDGET_PCT = 0.06
TARGET_R_MULTIPLE = 1.25


def parse_open(spec: str) -> tuple[str, int, float, float]:
    symbol, qty, entry, stop = spec.split(":")
    return symbol.upper(), int(qty), float(entry), float(stop)


def parse_candidate(spec: str) -> tuple[str, float, float]:
    symbol, price, stop = spec.split(":")
    return symbol.upper(), float(price), float(stop)


def size_position(price: float, stop: float, risk_remaining: float) -> dict:
    """Largest share count fitting both the notional cap and the risk budget."""
    risk_per_share = price - stop
    if risk_per_share <= 0:
        return {"error": "stop must be below price"}

    qty_by_notional = int(MAX_NOTIONAL_USD // price)
    qty_by_risk = int(risk_remaining // risk_per_share)
    qty = min(qty_by_notional, qty_by_risk)

    return {
        "qty": qty,
        "binding": "notional cap" if qty_by_notional <= qty_by_risk else "risk budget",
        "risk_per_share": risk_per_share,
        "notional": qty * price,
        "risk_total": qty * risk_per_share,
        "target": price + TARGET_R_MULTIPLE * risk_per_share,
    }


def main():
    ap = argparse.ArgumentParser(description="Premarket position sizer")
    ap.add_argument("--account", type=float, required=True, help="Total account value USD")
    ap.add_argument("--open", action="append", default=[], metavar="SYM:QTY:ENTRY:STOP")
    ap.add_argument("--candidate", action="append", default=[], metavar="SYM:PRICE:STOP")
    args = ap.parse_args()

    budget = args.account * RISK_BUDGET_PCT
    print(f"\nAccount ${args.account:,.2f}   risk budget (6%) ${budget:.2f}")

    committed = 0.0
    if args.open:
        print("\nOpen positions")
        for spec in args.open:
            symbol, qty, entry, stop = parse_open(spec)
            risk = qty * (entry - stop)
            committed += risk
            target = entry + TARGET_R_MULTIPLE * (entry - stop)
            print(f"  {symbol:6} {qty:4d} @ ${entry:.2f}  stop ${stop:.2f}  "
                  f"risk ${risk:6.2f}  target ${target:.2f}")

    remaining = budget - committed
    print(f"\n  committed ${committed:.2f}   remaining ${remaining:.2f}")

    if remaining <= 0:
        print("\n  Risk budget is fully committed. No new position today.\n")
        return

    if args.candidate:
        print("\nCandidates")
        for spec in args.candidate:
            symbol, price, stop = parse_candidate(spec)
            r = size_position(price, stop, remaining)
            if "error" in r:
                print(f"  {symbol:6} {r['error']}")
                continue
            if r["qty"] == 0:
                print(f"  {symbol:6} does not fit — risk/share ${r['risk_per_share']:.2f} "
                      f"exceeds ${remaining:.2f} remaining")
                continue
            print(f"  {symbol:6} {r['qty']:4d} sh @ ${price:.2f}  stop ${stop:.2f}  "
                  f"target ${r['target']:.2f}")
            print(f"         notional ${r['notional']:.2f}   risk ${r['risk_total']:.2f}   "
                  f"limited by {r['binding']}")
    print()


if __name__ == "__main__":
    main()
