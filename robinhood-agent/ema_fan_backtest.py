"""Backtest of the '13/48/200 EMA fan-out' trend-momentum claim from a
trading-room marketing thread the user showed me: EMAs stacked in order
(13>48>200 for bullish) = trend, and the WIDER the fan (spacing) between
them, the stronger the momentum -- versus bunched-up EMAs = chop, avoid.

Real 5-minute bars, SPY + QQQ, 2026-06-22 through 2026-08-21 (44 trading
days, regular session only), pulled live via get_equity_historicals. No
synthesized data, no cherry-picking -- same posture as every other
backtest in this repo (see S2's negative result in strategies.md).

Method:
  1. Compute EMA13/EMA48/EMA200 continuously over each symbol's full bar
     series (first ~5 trading days are warm-up, excluded from results
     since EMA200 needs ~200 bars ~ 2.5 days to stabilize and a wider
     buffer is safer).
  2. Classify each remaining bar into a regime:
       bullish = EMA13 > EMA48 > EMA200 (stacked up)
       bearish = EMA13 < EMA48 < EMA200 (stacked down)
       mixed   = anything else (not cleanly stacked -- the "chop" the
                 thread says to avoid)
  3. For bullish/bearish bars, compute fan width = |EMA13 - EMA200| /
     EMA200 (normalized spacing), and split into terciles: narrow /
     mid / wide.
  4. Forward return over N bars (N=6 -> 30 minutes at 5-min bars) in the
     direction the trend implies (up for bullish, down for bearish).
  5. Compare: (a) regime bars (bullish+bearish) vs mixed/chop bars --
     does avoiding chop actually improve forward returns? (b) wide-fan
     vs narrow-fan bars within a regime -- does wider spacing predict
     BETTER forward continuation, or is it just confirming a move
     that's already priced in?

Everything here is descriptive statistics on real historical bars, not a
trading system with a stop/entry rule -- this tests the THREAD'S CLAIM,
not a tradable strategy on its own.
"""
from __future__ import annotations

import json
import statistics as stats
from typing import Any

FWD_BARS = 6  # 30 minutes at 5-min bars
WARMUP_BARS = 400  # ~5 trading days, well past EMA200 stabilization


def ema_series(closes: list[float], period: int) -> list[float]:
    k = 2.0 / (period + 1)
    out = [closes[0]]
    for c in closes[1:]:
        out.append(c * k + out[-1] * (1 - k))
    return out


def load_bars(path: str, symbol: str) -> list[dict[str, Any]]:
    d = json.load(open(path))
    for r in d["data"]["results"]:
        if r["symbol"] == symbol:
            return [b for b in r["bars"] if not b.get("interpolated")]
    raise KeyError(symbol)


def analyze(symbol: str, bars: list[dict[str, Any]]) -> None:
    closes = [float(b["close_price"]) for b in bars]
    e13 = ema_series(closes, 13)
    e48 = ema_series(closes, 48)
    e200 = ema_series(closes, 200)

    n = len(closes)
    regime_returns: dict[str, list[float]] = {"bullish": [], "bearish": [], "mixed": []}
    fan_bucketed: dict[str, list[tuple[float, float]]] = {"bullish": [], "bearish": []}

    for i in range(WARMUP_BARS, n - FWD_BARS):
        c13, c48, c200 = e13[i], e48[i], e200[i]
        px_now = closes[i]
        px_fwd = closes[i + FWD_BARS]

        if c13 > c48 > c200:
            regime = "bullish"
            fwd_ret = (px_fwd - px_now) / px_now * 100.0
        elif c13 < c48 < c200:
            regime = "bearish"
            fwd_ret = (px_now - px_fwd) / px_now * 100.0  # favorable direction = down
        else:
            regime = "mixed"
            # mixed/chop has no defined trend direction, so signed return
            # would be meaningless as a "favorable direction" number -- keep
            # it signed (plain price change) for a mean/median read, but
            # NEVER compute a directional hit_rate for this bucket below.
            fwd_ret = (px_fwd - px_now) / px_now * 100.0

        regime_returns[regime].append(fwd_ret)
        if regime in ("bullish", "bearish"):
            width = abs(c13 - c200) / c200 * 100.0
            fan_bucketed[regime].append((width, fwd_ret))

    print(f"\n=== {symbol} ===")
    print(f"total usable bars: {n - WARMUP_BARS - FWD_BARS}")
    for regime in ("bullish", "bearish", "mixed"):
        rs = regime_returns[regime]
        if not rs:
            print(f"  {regime:8s}: n=0")
            continue
        mean = stats.mean(rs)
        med = stats.median(rs)
        abs_mean = stats.mean(abs(x) for x in rs)  # magnitude, direction-agnostic
        if regime == "mixed":
            print(f"  {regime:8s}: n={len(rs):5d}  mean_signed_ret={mean:+.4f}%  "
                  f"median={med:+.4f}%  mean_|ret|={abs_mean:.4f}% (no defined direction, "
                  f"hit_rate not meaningful here)")
        else:
            hit = sum(1 for x in rs if x > 0) / len(rs) * 100.0
            print(f"  {regime:8s}: n={len(rs):5d}  mean_fwd_ret={mean:+.4f}%  "
                  f"median={med:+.4f}%  mean_|ret|={abs_mean:.4f}%  hit_rate={hit:.1f}%")

    # Fan-width tercile comparison, combined across both regimes (favorable-direction return)
    combined = fan_bucketed["bullish"] + fan_bucketed["bearish"]
    combined.sort(key=lambda t: t[0])
    n_c = len(combined)
    if n_c >= 30:
        third = n_c // 3
        narrow = combined[:third]
        mid = combined[third:2 * third]
        wide = combined[2 * third:]
        print(f"  fan-width terciles (n={n_c} regime bars, favorable-direction fwd return):")
        for label, bucket in (("narrow", narrow), ("mid", mid), ("wide", wide)):
            rets = [r for _, r in bucket]
            widths = [w for w, _ in bucket]
            mean = stats.mean(rets)
            hit = sum(1 for x in rets if x > 0) / len(rets) * 100.0
            print(f"    {label:6s}: n={len(rets):5d}  width_range=[{min(widths):.3f}%,{max(widths):.3f}%]"
                  f"  mean_fwd_ret={mean:+.4f}%  hit_rate={hit:.1f}%")


if __name__ == "__main__":
    path = "/root/.claude/projects/-home-user-Wc26meme/765d6f61-b995-5466-8187-9a1ba3fcf877/tool-results/mcp-Robinhood-get_equity_historicals-1787552399079.txt"
    for sym in ("SPY", "QQQ"):
        analyze(sym, load_bars(path, sym))
