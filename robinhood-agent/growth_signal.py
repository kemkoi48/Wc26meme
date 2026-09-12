"""Long-run growth-sleeve math -- entry screen and exit trail, held weeks
to months, not the 1-5 minute scalp horizon of scalp_signal.py.

Created 2026-08-18 after the user drew an explicit split, verbatim:
"you know what your strategy will be fast growing investment not the day
trading and option trading... I was your greater profit in long run...
day trading is not feasible with your situation... You will be help me
screen I will execute the day trade but you will trade yourself for long
run." Concretely: the user drives Surge Watch's day-trade fires by hand
from here on; this module is what I use to pick and manage this account's
own long-run positions.

NOTHING HERE IS BACKTESTED. Unlike scalp_signal.py (1,530 real minute
bars measured before any threshold was picked), the numbers below are
real, verified-live screener filters, not a measured edge. Say that
plainly whenever this module is quoted: it screens for what "growth
momentum" concretely means (real trend, real liquidity, not overbought,
not a micro-cap), it does not claim the screen predicts a return.

WHERE THE ENTRY SCREEN COMES FROM
==================================
Robinhood saved scan "Growth Momentum (long-run)"
(scan_id 2514847d-25cb-4628-9731-bb5b0ee7d246), built and verified live
2026-08-18 via get_scanner_filter_specs + create_scan/update_scan_filters,
iterating on real results until the filters actually matched something
(the first draft used % Change (1mo) > "5" and matched ZERO instruments
-- the underlying expression returns a decimal ratio, not a percentage,
so ">5" silently demanded a 500% monthly move. Caught by checking real
NVDA/AAPL/MSFT values, not by assuming the unit label was right):

  - Market cap > $1B          -- excludes the micro-caps Surge Watch
                                  screens; this sleeve wants companies
                                  with an actual balance sheet.
  - RSI(14, 1d) between 50-70 -- real momentum, not yet in overbought
                                  territory (70+) where a growth-momentum
                                  entry chases a top.
  - % change (1mo) > 5%        -- an established move, not today's noise.
  - ADX(14, 1d) > 20            -- a real trend by the standard textbook
                                  reading (ADX<20 = no trend / chop).
  - Average volume(30d) > 500k -- liquid enough to exit without moving
                                  the tape, irrelevant at this account's
                                  size today but the discipline is cheap.

381 real matches when last run 2026-08-18 (see sources.md). Re-run
`run_scan` on the scan_id above for fresh results -- this module does not
embed a symbol list, only the screen definition and the exit math.

THE EXIT: A WIDE TRAILING STOP, MANAGED BY HAND -- NOT A BROKER ORDER TYPE
===========================================================================
Verified 2026-08-16 (CLAUDE.md, "No OCO for equities"): `place_equity_order`
only offers market / limit / stop_market / stop_limit, no native trailing
type. A real trailing stop for this sleeve is therefore NOT a single
resting order -- it is a stop_market order that gets CANCELLED AND
REPLACED higher each time the position makes a new high, computed by
`trailing_stop_price` below and applied by whoever is running the
periodic check (see CLAUDE.md's growth-sleeve section for the cadence).

TRAIL_PCT = 18% -- the user chose "wide" over "scalp-style 2%" and over
"no stop at all" explicitly (2026-08-18 clarifying questions), wide
enough that an ordinary growth-stock pullback doesn't shake the position
out, tight enough to still cap a real thesis break. This is the midpoint
of the 15-20% range discussed, not independently backtested -- there is
no measured optimum here, only the user's stated risk tolerance. Revisit
once this sleeve has enough closed trades to look at real outcomes, the
same posture as scalp_signal.py's PROFIT_TRIGGER_PCT/PROFIT_TRAIL_PCT.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

# Real, verified-live screen (see module docstring). Kept here so a caller
# can see the numbers without re-reading create_scan's call history.
MIN_MARKET_CAP_USD = 1_000_000_000.0
RSI_LOW, RSI_HIGH = 50.0, 70.0
MIN_1MO_CHANGE_PCT = 5.0
MIN_ADX = 20.0
MIN_AVG_VOLUME = 500_000.0

# Wide trailing stop for the growth sleeve -- see module docstring for
# where 18% comes from (the user's stated tolerance, not a backtest).
TRAIL_PCT = 18.0


def _f(value: Any) -> Optional[float]:
    """Coerce to float or None. Rejects bools and non-finite values."""
    if isinstance(value, bool):
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    if out != out or out in (float("inf"), float("-inf")):
        return None
    return out


@dataclass(frozen=True)
class GrowthCandidate:
    """One row from the "Growth Momentum (long-run)" scan, as pulled from
    `run_scan`'s columns -- market_cap in dollars, pct_change_1mo as a
    PERCENTAGE (5.0 = 5%, already converted from the scan's raw decimal
    ratio -- see module docstring on that unit trap)."""

    symbol: str
    market_cap: float
    rsi: float
    pct_change_1mo: float
    adx: float
    avg_volume: float


@dataclass(frozen=True)
class ScreenResult:
    passed: bool
    reason: str


def check_candidate(c: GrowthCandidate) -> ScreenResult:
    """Re-verify a candidate against the same thresholds the saved scan
    filters on. Exists so a candidate pulled from a stale scan result
    (see scalp_signal.py's stale-signal lesson, CLAUDE.md 2026-08-18) gets
    re-checked against LIVE numbers before an order is placed, not just
    trusted from whenever the scan last ran."""
    if c.market_cap <= MIN_MARKET_CAP_USD:
        return ScreenResult(False, f"market cap ${c.market_cap:,.0f} <= ${MIN_MARKET_CAP_USD:,.0f} floor")
    if not (RSI_LOW <= c.rsi <= RSI_HIGH):
        return ScreenResult(False, f"RSI {c.rsi:.1f} outside {RSI_LOW:.0f}-{RSI_HIGH:.0f}")
    if c.pct_change_1mo <= MIN_1MO_CHANGE_PCT:
        return ScreenResult(False, f"1mo change {c.pct_change_1mo:+.2f}% <= {MIN_1MO_CHANGE_PCT:.1f}% floor")
    if c.adx <= MIN_ADX:
        return ScreenResult(False, f"ADX {c.adx:.1f} <= {MIN_ADX:.0f} (no real trend)")
    if c.avg_volume <= MIN_AVG_VOLUME:
        return ScreenResult(False, f"avg volume {c.avg_volume:,.0f} <= {MIN_AVG_VOLUME:,.0f} floor")
    return ScreenResult(
        True,
        f"RSI {c.rsi:.1f}, +{c.pct_change_1mo:.1f}% (1mo), ADX {c.adx:.1f}, "
        f"cap ${c.market_cap/1e9:.1f}B -- still passes live",
    )


def trailing_stop_price(peak_price: float, trail_pct: float = TRAIL_PCT) -> float:
    """The stop level for a given peak price since entry. Call this fresh
    on every periodic check with the real peak (max close since entry,
    not the entry price) and compare to the currently resting stop --
    only move the resting order UP, never down (see decide_stop_update)."""
    p = _f(peak_price)
    if p is None or p <= 0:
        raise ValueError(f"unusable peak price: {peak_price!r}")
    return p * (1 - trail_pct / 100.0)


@dataclass(frozen=True)
class StopUpdate:
    should_update: bool
    new_stop: Optional[float]
    reason: str


def decide_stop_update(
    current_stop: Optional[float],
    peak_price: float,
    trail_pct: float = TRAIL_PCT,
) -> StopUpdate:
    """Whether the resting protective stop needs to be cancelled and
    replaced higher. A trailing stop only ever ratchets UP -- if the
    computed level is below the current resting stop (peak hasn't made a
    new high since the stop was last set), do nothing. `current_stop` is
    None before any stop has been placed yet (right after entry)."""
    new_stop = trailing_stop_price(peak_price, trail_pct)
    if current_stop is None:
        return StopUpdate(True, new_stop, f"no stop resting yet -- place at {new_stop:.4f}")
    cur = _f(current_stop)
    if cur is None or cur <= 0:
        return StopUpdate(True, new_stop, f"current stop unusable ({current_stop!r}) -- replace at {new_stop:.4f}")
    if new_stop <= cur:
        return StopUpdate(
            False, None,
            f"no new high since last stop update: computed {new_stop:.4f} <= resting {cur:.4f}",
        )
    return StopUpdate(
        True, new_stop,
        f"new peak raises trail: {cur:.4f} -> {new_stop:.4f} ({trail_pct:.0f}% below peak)",
    )
