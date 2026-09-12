"""Backtester for the Pattern Scalp (opening-range reversal) rule.

Faithful to the strategy's logic, with two honest simplifications noted up front
so you don't over-trust the output:

  * LONG-ONLY. Only "first 15-min candle pushed DOWN -> reverse UP" setups are
    taken, matching what's executable in a cash account (no shorting).
  * The 5-minute entry trigger ("John Wick" / bullish engulfing) is approximated
    by an OR_low RECLAIM: the first 5-min bar that trades below OR_low but closes
    back above it. This captures the reversal idea; it is not a candle-by-candle
    reproduction of the exact patterns.

Per trading day it: builds the opening range from the first 15 min, checks the
manipulation filter (OR range > atr-frac x daily ATR), and if it's a valid long
setup, simulates entry (reclaim), a stop below the wick low, and a target back at
OR_high, with a time stop at the end of the entry window.

    python backtest_pattern_scalp.py --demo
    python backtest_pattern_scalp.py --csv SPY_5min.csv
    python backtest_pattern_scalp.py --csv SPY_5min.csv --atr-frac 0.2 --fee-bps 1

CSV format: header row, then `timestamp,open,high,low,close` with ISO timestamps
(e.g. 2026-01-05T09:30:00) for regular-session 5-minute bars across many days.
Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import math
import random
from dataclasses import dataclass


@dataclass
class Bar:
    ts: dt.datetime
    o: float
    h: float
    l: float
    c: float


@dataclass
class Trade:
    day: dt.date
    entry: float
    stop: float
    target: float
    exit: float
    outcome: str  # "target", "stop", "time"
    r_multiple: float
    pct: float


def load_bars(path: str) -> list[Bar]:
    bars: list[Bar] = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        idx = {"timestamp": 0, "open": 1, "high": 2, "low": 3, "close": 4}
        if header:
            lower = [h.strip().lower() for h in header]
            for k in idx:
                if k in lower:
                    idx[k] = lower.index(k)
        for row in reader:
            if not row:
                continue
            try:
                ts = dt.datetime.fromisoformat(row[idx["timestamp"]].strip())
                bars.append(Bar(
                    ts,
                    float(row[idx["open"]]),
                    float(row[idx["high"]]),
                    float(row[idx["low"]]),
                    float(row[idx["close"]]),
                ))
            except (ValueError, IndexError):
                continue
    bars.sort(key=lambda b: b.ts)
    if not bars:
        raise ValueError(f"{path}: no usable bars")
    return bars


def group_by_day(bars: list[Bar]) -> dict[dt.date, list[Bar]]:
    days: dict[dt.date, list[Bar]] = {}
    for b in bars:
        days.setdefault(b.ts.date(), []).append(b)
    return days


def daily_atr(days: dict[dt.date, list[Bar]], period: int) -> dict[dt.date, float]:
    """Simple ATR of the reconstructed daily bars, using days *before* each day."""
    ordered = sorted(days)
    daily = []  # (date, high, low, close)
    for d in ordered:
        bs = days[d]
        daily.append((d, max(b.h for b in bs), min(b.l for b in bs), bs[-1].c))
    trs: list[float] = []
    atr_for: dict[dt.date, float] = {}
    for i, (d, h, l, c) in enumerate(daily):
        if i == 0:
            tr = h - l
        else:
            pc = daily[i - 1][3]
            tr = max(h - l, abs(h - pc), abs(l - pc))
        # ATR available for THIS day is the mean of the prior `period` TRs.
        if len(trs) >= period:
            atr_for[d] = sum(trs[-period:]) / period
        trs.append(tr)
    return atr_for


def simulate_day(
    bars: list[Bar],
    atr: float,
    *,
    or_minutes: int,
    atr_frac: float,
    entry_window_min: int,
    stop_buffer: float,
    fee_bps: float,
) -> Trade | None:
    day = bars[0].ts.date()
    open_time = bars[0].ts
    or_end = open_time + dt.timedelta(minutes=or_minutes)
    window_end = open_time + dt.timedelta(minutes=entry_window_min)

    or_bars = [b for b in bars if b.ts < or_end]
    if len(or_bars) < 1:
        return None
    or_high = max(b.h for b in or_bars)
    or_low = min(b.l for b in or_bars)
    or_range = or_high - or_low

    # Step 2: manipulation filter.
    if or_range <= atr_frac * atr:
        return None
    # Long setup only: the opening 15-min candle must have pushed DOWN.
    if or_bars[-1].c >= or_bars[0].o:
        return None  # upside manipulation -> short setup -> skip (can't short)

    # Step 3: entry via OR_low reclaim within the entry window.
    post = [b for b in bars if or_end <= b.ts < window_end]
    entry_bar = None
    wick_low = or_low
    for b in post:
        wick_low = min(wick_low, b.l)
        if b.l <= or_low and b.c > or_low:
            entry_bar = b
            break
    if entry_bar is None:
        return None

    entry = entry_bar.c
    stop = wick_low * (1 - stop_buffer)
    target = or_high
    if entry <= stop or target <= entry:
        return None  # degenerate geometry

    # Simulate remaining bars to the end of the day. Conservative: within a bar,
    # check the stop before the target.
    rest = [b for b in bars if b.ts > entry_bar.ts]
    exit_price, outcome = entry_bar.c, "time"
    for b in rest:
        if b.l <= stop:
            exit_price, outcome = stop, "stop"
            break
        if b.h >= target:
            exit_price, outcome = target, "target"
            break
    else:
        if rest:
            exit_price, outcome = rest[-1].c, "time"

    fee = fee_bps / 10_000.0
    pct = (exit_price / entry - 1) - 2 * fee
    r = (exit_price - entry) / (entry - stop)
    return Trade(day, entry, stop, target, exit_price, outcome, r, pct)


def run(
    bars: list[Bar],
    *,
    or_minutes: int,
    atr_period: int,
    atr_frac: float,
    entry_window_min: int,
    stop_buffer: float,
    fee_bps: float,
    label: str,
) -> None:
    days = group_by_day(bars)
    atr_for = daily_atr(days, atr_period)

    trades: list[Trade] = []
    for d in sorted(days):
        if d not in atr_for:
            continue
        t = simulate_day(
            days[d], atr_for[d],
            or_minutes=or_minutes, atr_frac=atr_frac,
            entry_window_min=entry_window_min, stop_buffer=stop_buffer, fee_bps=fee_bps,
        )
        if t:
            trades.append(t)

    print(f"Pattern Scalp backtest — {label}")
    print(f"  (long-only, OR={or_minutes}m, ATR{atr_period} x {atr_frac:.0%} filter, "
          f"entry window {entry_window_min}m, fee {fee_bps}bps)")
    print("-" * 60)
    print(f"  Trading days with ATR : {sum(1 for d in days if d in atr_for)}")
    print(f"  Trades taken          : {len(trades)}")
    if not trades:
        print("  No setups triggered on this data.")
        print("-" * 60)
        return

    wins = [t for t in trades if t.r_multiple > 0]
    gross_win = sum(t.r_multiple for t in wins)
    gross_loss = -sum(t.r_multiple for t in trades if t.r_multiple <= 0)
    total_r = sum(t.r_multiple for t in trades)
    total_pct = sum(t.pct for t in trades) * 100
    by_outcome = {o: sum(1 for t in trades if t.outcome == o) for o in ("target", "stop", "time")}

    print(f"  Win rate              : {len(wins) / len(trades) * 100:.1f}%")
    print(f"  Total R (risk mult.)  : {total_r:+.2f}R")
    print(f"  Avg R per trade       : {total_r / len(trades):+.2f}R")
    print(f"  Sum of trade returns  : {total_pct:+.2f}%  (not compounded, before position sizing)")
    print(f"  Profit factor (R)     : {gross_win / gross_loss:.2f}" if gross_loss > 0 else "  Profit factor (R)     : inf (no losers)")
    print(f"  Exits                 : {by_outcome['target']} target / {by_outcome['stop']} stop / {by_outcome['time']} time")
    print("-" * 60)
    print("Indicative only: long-only, reclaim-based entry approximation, and\n"
          "sensitive to intraday data quality. A positive result here is a reason\n"
          "to test further, not to trade real money.")


def synthetic_bars(days: int = 40, seed: int = 11) -> list[Bar]:
    """5-min regular-session bars with occasional engineered down-manipulation
    mornings that reverse, so the machinery has something to trigger on."""
    rng = random.Random(seed)
    bars: list[Bar] = []
    price = 100.0
    start_date = dt.date(2026, 1, 5)
    d = start_date
    made = 0
    while made < days:
        if d.weekday() < 5:  # weekdays only
            t = dt.datetime.combine(d, dt.time(9, 30))
            manip = rng.random() < 0.4
            for i in range(78):  # 9:30-16:00 in 5-min bars
                o = price
                if manip and i == 0:  # big down first candle (over ~3 bars of range)
                    drift = -0.9
                    vol = 0.6
                elif manip and 1 <= i <= 6:  # reversal back up
                    drift = 0.28
                    vol = 0.25
                else:
                    drift = rng.gauss(0.0, 0.0)
                    vol = 0.12
                c = o + drift + rng.gauss(0, vol)
                hi = max(o, c) + abs(rng.gauss(0, vol))
                lo = min(o, c) - abs(rng.gauss(0, vol))
                bars.append(Bar(t, round(o, 2), round(hi, 2), round(lo, 2), round(c, 2)))
                price = c
                t += dt.timedelta(minutes=5)
            price += rng.gauss(0, 0.3)  # overnight gap
            made += 1
        d += dt.timedelta(days=1)
    return bars


def main() -> None:
    p = argparse.ArgumentParser(description="Backtest the Pattern Scalp opening-range reversal.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--csv", help="Path to a timestamp,open,high,low,close 5-min CSV.")
    src.add_argument("--demo", action="store_true", help="Use synthetic intraday data.")
    p.add_argument("--or-minutes", type=int, default=15, help="Opening-range length.")
    p.add_argument("--atr-period", type=int, default=14, help="Daily ATR period.")
    p.add_argument("--atr-frac", type=float, default=0.20, help="Manipulation threshold (OR range / ATR).")
    p.add_argument("--entry-window-min", type=int, default=90, help="Minutes after open to look for entry.")
    p.add_argument("--stop-buffer", type=float, default=0.001, help="Stop distance below the wick low (fraction).")
    p.add_argument("--fee-bps", type=float, default=1.0, help="Round-trip fee in basis points.")
    args = p.parse_args()

    if args.demo:
        bars, label = synthetic_bars(), "synthetic intraday"
    else:
        bars, label = load_bars(args.csv), args.csv

    run(
        bars,
        or_minutes=args.or_minutes,
        atr_period=args.atr_period,
        atr_frac=args.atr_frac,
        entry_window_min=args.entry_window_min,
        stop_buffer=args.stop_buffer,
        fee_bps=args.fee_bps,
        label=label,
    )


if __name__ == "__main__":
    main()
