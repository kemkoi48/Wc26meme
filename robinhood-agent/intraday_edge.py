"""Same-day index/equity move edge test -- the 0DTE counterpart to
option_math.py's mismatch_ratio.

The question this answers, for a same-day option with T minutes left in the
session: the market (via delta / "chance of profit") is pricing in some
probability that the underlying clears breakeven by the close. Is that
probability actually supported by how this underlying has moved in this
exact closing window on real past days, or is the option just charging for
optimism the tape doesn't back up?

  implied probability  =  what the option's own pricing says (delta or the
                           broker's own chance-of-profit figure)
  historical frequency  =  how often THIS underlying actually cleared that
                           size of move, in the same number of minutes
                           before close, on real past trading days
  edge ratio            =  historical frequency / implied probability

A ratio at or above 1.0 means real history clears the bar at least as often
as the option is pricing in -- a genuine, checkable edge. A ratio below 1.0
means the option is pricing in more optimism than the tape has ever
delivered in this window -- the real-money analog of S7's "IV already paid
for the move" rejection.

Worked live example that motivated this module (QQQ, 2026-08-21, ~1:57pm ET,
108 minutes left in the session): the $714 0DTE call needed a +0.15% move to
breakeven. Robinhood's own model priced that at a 24.4% chance of profit.
The real answer, from 44 actual trading days' worth of 5-minute bars on
this exact underlying: QQQ cleared +0.15% in the closing 108 minutes on
only 8 of 44 days (18.2%). Edge ratio 0.75 -- rejected, and correctly so;
the position went on to expire worthless. See strategies.md.

Everything here is a PURE FUNCTION over numbers/bars. No network, no SDK
import -- same posture as option_math.py, directly unit-testable.

Fail-closed throughout: too little history, malformed bars, or a
non-positive price returns None rather than a number that looks
authoritative. Callers must treat None as "cannot evaluate", never as
"assume fine".
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Any, Optional, Sequence

# Below this many real trading days of history, the frequency estimate is
# too noisy to trust -- same spirit as option_math.realized_volatility's
# 10-close floor, tuned tighter here because this counts discrete days
# (a binomial rate), not a continuous return series.
MIN_HISTORICAL_DAYS = 20


def _as_float(value: Any) -> Optional[float]:
    """Coerce to float, or None. Rejects bools and non-finite values."""
    if isinstance(value, bool):
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if f != f or f in (float("inf"), float("-inf")):  # NaN / inf
        return None
    return f


def required_move_pct(current_price: Any, breakeven_price: Any) -> Optional[float]:
    """Percent move (signed) needed to go from current_price to
    breakeven_price. Positive means price must rise; negative means it must
    fall. Returns None on a non-positive or unusable current_price."""
    cur = _as_float(current_price)
    be = _as_float(breakeven_price)
    if cur is None or cur <= 0 or be is None:
        return None
    return (be - cur) / cur * 100.0


def daily_close_window_moves(
    bars: Sequence[dict[str, Any]], window_minutes: int
) -> list[float]:
    """From raw intraday bars (Robinhood's get_equity_historicals shape --
    each bar a dict with begins_at, close_price, and optionally
    interpolated), compute the real percent move from `window_minutes`
    before each trading day's close to that day's actual close.

    This is the historical base-rate builder: run it once per underlying
    per window size, then compare its output against whatever move an
    option needs today via realized_move_frequency() below.

    Interpolated (gap-filled) bars are dropped before grouping -- a flat,
    synthetic bar would silently produce a 0.0% move and pollute the
    distribution, the same failure mode option_math.py's docstrings warn
    about for daily closes. Bars are grouped into trading days by the UTC
    calendar date of `begins_at`, which is safe for US equities/index ETFs
    since the regular session (13:30-20:00 UTC) never crosses a UTC
    midnight. One move per day; days with no bar at or before the window
    cutoff are skipped rather than guessed at.
    """
    if window_minutes <= 0:
        return []
    by_day: dict[dt.date, list[tuple[dt.datetime, float]]] = {}
    for b in bars:
        if not isinstance(b, dict) or b.get("interpolated"):
            continue
        px = _as_float(b.get("close_price"))
        ts = b.get("begins_at")
        if px is None or px <= 0 or not isinstance(ts, str):
            continue
        try:
            t = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            continue
        by_day.setdefault(t.date(), []).append((t, px))

    moves: list[float] = []
    window = dt.timedelta(minutes=window_minutes)
    for day_bars in by_day.values():
        day_bars.sort(key=lambda p: p[0])
        close_t, close_px = day_bars[-1]
        mark_t = close_t - window
        candidates = [p for p in day_bars if p[0] <= mark_t]
        if not candidates:
            continue
        _, mark_px = candidates[-1]
        if mark_px <= 0:
            continue
        moves.append((close_px - mark_px) / mark_px * 100.0)
    return moves


def realized_move_frequency(
    historical_moves_pct: Sequence[Any], threshold_pct: float
) -> Optional[float]:
    """Fraction of real historical days whose move (signed, same convention
    as required_move_pct) cleared threshold_pct in the needed direction.

    Direction follows the SIGN of threshold_pct, not a literal ">=":
    a positive threshold (a call's breakeven is above the current price)
    asks "how often did it rise at least this much" (m >= threshold_pct);
    a negative threshold (a put's breakeven is below the current price)
    asks "how often did it FALL at least this much" (m <= threshold_pct,
    i.e. at least as negative). A literal ">=" on a negative threshold
    would get this backwards -- a bigger fall (more negative) would fail
    to count as a hit, which is the opposite of what a put buyer needs.
    threshold_pct of exactly 0 is treated as the upside case (m >= 0).

    Returns None with fewer than MIN_HISTORICAL_DAYS usable observations --
    a rate estimated from a handful of days is not a base rate, it is noise
    dressed up as one.
    """
    usable = [m for m in (_as_float(x) for x in historical_moves_pct) if m is not None]
    if len(usable) < MIN_HISTORICAL_DAYS:
        return None
    if threshold_pct >= 0:
        hits = sum(1 for m in usable if m >= threshold_pct)
    else:
        hits = sum(1 for m in usable if m <= threshold_pct)
    return hits / len(usable)


def edge_ratio(historical_freq: Optional[float], implied_prob: Any) -> Optional[float]:
    """historical_freq / implied_prob. None if either input is unusable, or
    if implied_prob is not a valid (0, 1] probability -- a value outside
    that range is a caller bug (wrong units, e.g. passing 24.4 instead of
    0.244), not a real edge reading."""
    if historical_freq is None:
        return None
    p = _as_float(implied_prob)
    if p is None or p <= 0 or p > 1:
        return None
    return historical_freq / p


@dataclass(frozen=True)
class IntradayEdgeConfig:
    """Thresholds for evaluate_intraday_edge."""

    # Reject below this many real historical days -- see MIN_HISTORICAL_DAYS.
    min_historical_days: int = MIN_HISTORICAL_DAYS
    # Require history to clear the bar at least this often relative to what
    # is priced in. 1.0 means "at least as good as priced, no worse" -- the
    # neutral floor. Not yet validated against outcomes (this module has
    # zero trades behind it as of the day it was built); revisit once real
    # decisions have been graded against it, same posture as every other
    # untested gate in this repo.
    min_edge_ratio: float = 1.0


@dataclass(frozen=True)
class IntradayEdgeResult:
    required_move_pct: float
    historical_freq: float
    implied_prob: float
    edge_ratio: float
    sample_days: int
    passed: bool
    reason: str


def evaluate_intraday_edge(
    current_price: Any,
    breakeven_price: Any,
    implied_prob: Any,
    historical_moves_pct: Sequence[Any],
    cfg: IntradayEdgeConfig = IntradayEdgeConfig(),
) -> tuple[Optional[IntradayEdgeResult], str]:
    """Evaluate ONE same-day option decision. Returns (result, reason) with
    the same convention as option_math.evaluate_candidate: result is None
    with a named reason on a data problem; on real data, result is always
    populated (passed True/False) so a rejection is a graded verdict, not a
    missing one.
    """
    req = required_move_pct(current_price, breakeven_price)
    if req is None:
        return None, "unusable current_price or breakeven_price"

    p = _as_float(implied_prob)
    if p is None or p <= 0 or p > 1:
        return None, "implied_prob must be a (0, 1] probability"

    usable = [m for m in (_as_float(x) for x in historical_moves_pct) if m is not None]
    n = len(usable)
    if n < cfg.min_historical_days:
        return None, (
            f"only {n} usable historical days, need >= {cfg.min_historical_days} "
            "to trust a base rate"
        )

    freq = realized_move_frequency(usable, req)
    ratio = edge_ratio(freq, p)
    passed = ratio is not None and ratio >= cfg.min_edge_ratio
    reason = "" if passed else (
        f"edge ratio {ratio:.2f} < {cfg.min_edge_ratio:.2f} -- real history clears "
        f"the {req:+.2f}% bar {freq:.0%} of the time ({n} real days), option prices "
        f"a {p:.0%} chance"
    )
    return IntradayEdgeResult(
        required_move_pct=req,
        historical_freq=freq,
        implied_prob=p,
        edge_ratio=ratio,
        sample_days=n,
        passed=passed,
        reason=reason,
    ), reason
