"""Offline backtester for the moving-average trend rule the live agent follows.

This validates the *rule*, not the LLM agent. The agent reasons over Robinhood's
live tools and can't be replayed deterministically; the SMA-crossover rule it is
based on can be. Use this to sanity-check a symbol/parameter choice on history
before pointing the live agent at it.

Long/flat, one symbol, no leverage, no shorting — matching the cautious posture
of the live bot. Costs are modeled as a per-trade fee in basis points.

    python backtest.py --demo                       # synthetic random-walk data
    python backtest.py --csv AAPL.csv               # your own data
    python backtest.py --csv AAPL.csv --short 20 --long 50 --fee-bps 1

CSV format: a header row, then rows of `date,close` (extra columns ignored).
Pure standard library — no dependencies.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass


@dataclass
class Result:
    n_days: int
    start_equity: float
    end_equity: float
    total_return_pct: float
    buy_hold_return_pct: float
    annualized_pct: float
    max_drawdown_pct: float
    n_trades: int
    win_rate_pct: float
    sharpe: float


def load_prices(path: str) -> list[tuple[str, float]]:
    rows: list[tuple[str, float]] = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        # Locate the close column (default to last) and a date column (default first).
        close_idx, date_idx = -1, 0
        if header:
            lower = [h.strip().lower() for h in header]
            if "close" in lower:
                close_idx = lower.index("close")
            if "date" in lower:
                date_idx = lower.index("date")
        for row in reader:
            if not row:
                continue
            try:
                close = float(row[close_idx].replace("$", "").replace(",", ""))
            except (ValueError, IndexError):
                continue
            date = row[date_idx] if date_idx < len(row) else str(len(rows))
            rows.append((date, close))
    if len(rows) < 2:
        raise ValueError(f"{path}: need at least 2 usable price rows, got {len(rows)}")
    return rows


def synthetic_prices(n: int = 750, seed: int = 7) -> list[tuple[str, float]]:
    """Geometric random walk with a slight upward drift — for smoke-testing."""
    rng = random.Random(seed)
    price = 100.0
    out: list[tuple[str, float]] = []
    for i in range(n):
        price *= math.exp(rng.gauss(0.0003, 0.012))
        out.append((f"D{i:04d}", round(price, 2)))
    return out


def _sma(values: list[float], window: int, end: int) -> float | None:
    """SMA of `values` over the `window` days ending at index `end` (inclusive)."""
    if end + 1 < window:
        return None
    return sum(values[end + 1 - window : end + 1]) / window


def backtest(
    prices: list[tuple[str, float]],
    *,
    short: int,
    long: int,
    start_cash: float,
    fee_bps: float,
) -> Result:
    if short >= long:
        raise ValueError("short window must be smaller than long window")
    closes = [p for _, p in prices]
    fee = fee_bps / 10_000.0

    cash = start_cash
    shares = 0.0
    invested = False
    entry_price = 0.0
    n_trades = 0
    wins = 0

    equity_curve: list[float] = []
    for i, price in enumerate(closes):
        s = _sma(closes, short, i)
        l = _sma(closes, long, i)
        if s is not None and l is not None:
            uptrend = s > l
            if uptrend and not invested:
                # Buy full position at close.
                shares = (cash * (1 - fee)) / price
                cash = 0.0
                invested = True
                entry_price = price
                n_trades += 1
            elif not uptrend and invested:
                # Sell full position at close.
                cash = shares * price * (1 - fee)
                shares = 0.0
                invested = False
                n_trades += 1
                if price > entry_price:
                    wins += 1
        equity_curve.append(cash + shares * price)

    # Close any open position at the final price for accounting.
    if invested:
        final = closes[-1]
        cash = shares * final * (1 - fee)
        if final > entry_price:
            wins += 1
        shares = 0.0
        equity_curve[-1] = cash

    end_equity = equity_curve[-1]

    # Metrics.
    total_return = (end_equity / start_cash - 1) * 100
    buy_hold = (closes[-1] / closes[0] - 1) * 100
    years = max(len(closes) / 252.0, 1e-9)
    annualized = ((end_equity / start_cash) ** (1 / years) - 1) * 100

    peak = -math.inf
    max_dd = 0.0
    for v in equity_curve:
        peak = max(peak, v)
        if peak > 0:
            max_dd = max(max_dd, (peak - v) / peak)

    daily_rets = [
        equity_curve[i] / equity_curve[i - 1] - 1
        for i in range(1, len(equity_curve))
        if equity_curve[i - 1] > 0
    ]
    sharpe = 0.0
    if len(daily_rets) > 1:
        mean = sum(daily_rets) / len(daily_rets)
        var = sum((r - mean) ** 2 for r in daily_rets) / (len(daily_rets) - 1)
        sd = math.sqrt(var)
        if sd > 0:
            sharpe = (mean / sd) * math.sqrt(252)

    # win_rate is over completed round-trips (each round-trip = 2 trades).
    round_trips = n_trades // 2 + (n_trades % 2)
    win_rate = (wins / round_trips * 100) if round_trips else 0.0

    return Result(
        n_days=len(closes),
        start_equity=start_cash,
        end_equity=end_equity,
        total_return_pct=total_return,
        buy_hold_return_pct=buy_hold,
        annualized_pct=annualized,
        max_drawdown_pct=max_dd * 100,
        n_trades=n_trades,
        win_rate_pct=win_rate,
        sharpe=sharpe,
    )


def _print_report(r: Result, *, short: int, long: int, label: str) -> None:
    print(f"Backtest — {label}  (SMA {short}/{long})")
    print("-" * 48)
    print(f"  Days                : {r.n_days}")
    print(f"  Start equity        : ${r.start_equity:,.2f}")
    print(f"  End equity          : ${r.end_equity:,.2f}")
    print(f"  Strategy return     : {r.total_return_pct:+.2f}%")
    print(f"  Buy & hold return   : {r.buy_hold_return_pct:+.2f}%")
    print(f"  Annualized (strat)  : {r.annualized_pct:+.2f}%")
    print(f"  Max drawdown        : {r.max_drawdown_pct:.2f}%")
    print(f"  Trades              : {r.n_trades}")
    print(f"  Win rate (r-trips)  : {r.win_rate_pct:.1f}%")
    print(f"  Sharpe (annualized) : {r.sharpe:.2f}")
    print("-" * 48)
    edge = r.total_return_pct - r.buy_hold_return_pct
    verdict = "beat" if edge > 0 else "lagged"
    print(f"  vs buy & hold       : {verdict} by {abs(edge):.2f} pts")
    print("\nNote: past performance does not predict future results. This "
          "validates the rule, not the live LLM agent.")


def main() -> None:
    p = argparse.ArgumentParser(description="Backtest the SMA trend rule.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--csv", help="Path to a date,close CSV.")
    src.add_argument("--demo", action="store_true", help="Use synthetic data.")
    p.add_argument("--short", type=int, default=20, help="Short SMA window.")
    p.add_argument("--long", type=int, default=50, help="Long SMA window.")
    p.add_argument("--cash", type=float, default=10_000.0, help="Starting cash.")
    p.add_argument("--fee-bps", type=float, default=1.0, help="Per-trade fee in bps.")
    args = p.parse_args()

    if args.demo:
        prices = synthetic_prices()
        label = "synthetic random walk"
    else:
        prices = load_prices(args.csv)
        label = args.csv

    result = backtest(
        prices,
        short=args.short,
        long=args.long,
        start_cash=args.cash,
        fee_bps=args.fee_bps,
    )
    _print_report(result, short=args.short, long=args.long, label=label)


if __name__ == "__main__":
    main()
