"""Market regime classification -- decides WHICH strategy is eligible today.

The gap this fills: on 2026-08-11 every scan run was a long-momentum scan,
on a low-volatility grind day where that was the wrong instrument. Nothing
in the repo asked "what kind of day is this?" before picking a tool.

Two independent inputs, both cheap:

  1. Trend/range, via the 7/20/65 SMA alignment filter (DailyFX range guide).
     Aligned in order -> trending. Any other ordering -> ranging. The guide
     is explicit that the alignment is the rule and the specific periods are
     tunable, so the periods are parameters here, not constants.

  2. Volatility, via VIX (Stocklake get_market_pulse).

Everything here is a PURE FUNCTION over numbers already available from
get_equity_technical_indicators (SMA at any period) and get_market_pulse.
No network calls, no SDK import -- so it is directly unit-testable and can
be imported by any runner without pulling in the agent stack.

See strategies.md for what each regime means and which strategy it selects.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal, Optional

Trend = Literal["uptrend", "downtrend", "range"]

# Default SMA periods for the alignment filter. Tunable -- per the source,
# the interplay of short/intermediate/long matters, not these exact values.
FAST, MID, SLOW = 7, 20, 65

# VIX boundaries between volatility buckets.
VIX_LOW, VIX_HIGH = 20.0, 25.0

# S2's own trigger (strategies.md): the first completed 15m candle's range,
# as a fraction of ATR(14), must exceed this to count as a large enough
# liquidity-grabbing move to trade a reversal off of.
OR_ATR_THRESHOLD = 0.20


def classify_trend(
    sma_fast: float, sma_mid: float, sma_slow: float
) -> Trend:
    """7/20/65 SMA alignment test.

    uptrend   : fast > mid > slow
    downtrend : fast < mid < slow
    range     : any other ordering (the SMAs are tangled)

    Ties count as NOT aligned, i.e. range. Two equal SMAs mean the market is
    not cleanly ordered, which is exactly the condition the filter exists to
    detect -- treating a tie as a trend would be the optimistic reading and
    this filter's whole job is to keep range strategies out of trends.
    """
    if sma_fast > sma_mid > sma_slow:
        return "uptrend"
    if sma_fast < sma_mid < sma_slow:
        return "downtrend"
    return "range"


@dataclass(frozen=True)
class Regime:
    """A classified market regime and what it permits.

    `strategies` lists strategy IDs from strategies.md that are eligible.
    An EMPTY list is a real, correct answer -- "sit out" is a decision, and
    on a long-only cash account a downtrend has no valid strategy at all.
    """
    name: str
    trend: Trend
    vix: Optional[float]
    strategies: tuple[str, ...]
    rationale: str

    @property
    def should_trade(self) -> bool:
        return bool(self.strategies)


def classify_regime(
    sma_fast: float,
    sma_mid: float,
    sma_slow: float,
    vix: Optional[float] = None,
    event_day: bool = False,
    or_range_pct_of_atr: Optional[float] = None,
) -> Regime:
    """Classify the market and return the eligible strategies.

    `event_day` is a caller-supplied flag for a scheduled high-impact
    macro release (Investing.com economic calendar, per sources.md). It
    overrides everything: no strategy is eligible into a known event.

    `vix` may be None (Stocklake unavailable). Trend classification still
    works without it; only the high-volatility split is lost, so the result
    is downgraded conservatively rather than assumed benign.

    `or_range_pct_of_atr` is the first completed 15m candle's range as a
    fraction of ATR(14) -- S2's own trigger (strategies.md). S2 (Opening
    Range Reversal) is deliberately NOT part of the trend/vol branches
    below: per strategies.md its eligibility "doesn't depend on the daily
    trend regime" -- it is a same-day reversal off a volatile open and can
    fire during an uptrend, a downtrend, or a range day alike, so it is
    folded in afterward rather than gating it on `trend`. Omit this
    argument (or pass None) before the opening 15 minutes exist yet.
    """
    trend = classify_trend(sma_fast, sma_mid, sma_slow)

    if event_day:
        return Regime(
            name="event",
            trend=trend,
            vix=vix,
            strategies=(),
            rationale="Scheduled high-impact macro release; sit out.",
        )

    if trend == "downtrend":
        # Long-only cash account. This is structural, not a preference.
        regime = Regime(
            name="trending_down",
            trend=trend,
            vix=vix,
            strategies=(),
            rationale="Downtrend and this account is long-only; no daily-"
                      "trend strategy applies. Correct default is to sit "
                      "out.",
        )
    elif trend == "range":
        regime = Regime(
            name="range_bound",
            trend=trend,
            vix=vix,
            strategies=("S5",),
            rationale="SMAs not aligned -> ranging. Range strategy eligible; "
                      "trend strategies are the wrong instrument here.",
        )
    elif vix is None:
        # trend == "uptrend" -- split by volatility.
        regime = Regime(
            name="trending_up_unknown_vol",
            trend=trend,
            vix=None,
            strategies=("S1",),
            rationale="Uptrend confirmed but VIX unavailable. Allowing only "
                      "the low-volatility trend strategy, since the "
                      "high-volatility momentum scan is the more dangerous "
                      "of the two to run in the wrong conditions.",
        )
    elif vix >= VIX_HIGH:
        regime = Regime(
            name="trending_up_high_vol",
            trend=trend,
            vix=vix,
            strategies=("S3",),
            rationale=f"Uptrend with VIX {vix:.1f} >= {VIX_HIGH}. This is the "
                      "regime the low-float momentum scan is actually built "
                      "for.",
        )
    elif vix <= VIX_LOW:
        regime = Regime(
            name="trending_up_low_vol",
            trend=trend,
            vix=vix,
            strategies=("S1",),
            rationale=f"Uptrend with VIX {vix:.1f} <= {VIX_LOW}. Trend "
                      "following. Chasing extreme movers here is a known "
                      "mismatch (see 2026-08-11 session).",
        )
    else:
        regime = Regime(
            name="trending_up_mid_vol",
            trend=trend,
            vix=vix,
            strategies=("S1",),
            rationale=f"Uptrend, VIX {vix:.1f} between {VIX_LOW} and "
                      f"{VIX_HIGH}. Ambiguous volatility; defaulting to the "
                      "trend strategy rather than the momentum scan.",
        )

    if (
        or_range_pct_of_atr is not None
        and or_range_pct_of_atr > OR_ATR_THRESHOLD
        and "S2" not in regime.strategies
    ):
        regime = replace(
            regime,
            strategies=regime.strategies + ("S2",),
            rationale=regime.rationale + " Also: first-15m range is "
            f"{or_range_pct_of_atr:.0%} of ATR(14) (> {OR_ATR_THRESHOLD:.0%}) "
            "-- a volatile open, independent of the daily trend regime. S2 "
            "(Opening Range Reversal) is eligible.",
        )

    return regime


def close_strength(last: float, low: float, high: float) -> Optional[float]:
    """Where in the day's range a stock is trading, as a 0..1 fraction.

    From Tony Oz's Power scan: "the last trade must be in the top 13% of the
    day's trading range" -> close_strength >= 0.87.

    1.0 = trading at the high of day, 0.0 = at the low. This is a different
    axis from every filter currently in momentum_scanner.py, which all
    measure SIZE of move or volume and none of which measure QUALITY of
    close.

    Returns None when the range is degenerate (high == low, or malformed
    inputs) -- an unusable reading rather than a misleading number. Callers
    should treat None as fail-closed, consistent with the rest of the repo.
    """
    try:
        last_f, low_f, high_f = float(last), float(low), float(high)
    except (TypeError, ValueError):
        return None
    if high_f <= low_f:
        return None
    if not (low_f <= last_f <= high_f):
        # Last outside today's range means one of the three is stale or
        # from a different session. Refuse rather than clamp.
        return None
    return (last_f - low_f) / (high_f - low_f)
