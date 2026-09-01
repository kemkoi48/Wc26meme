"""Generalized dated-catalyst historical-move engine -- extends S7's edge
test (option_math.py) beyond earnings to ANY symbol's recurring or
one-off dated event: product launches, Fed decisions, regulatory
rulings, investor days, etc. Earnings already have a real source
(get_earnings_calendar / get_earnings_results, used by option_scanner.py)
-- this module exists for everything that isn't earnings but still has a
real, knowable date.

RULE ZERO applies here exactly as everywhere else in this repo: every
date in EVENT_CATALOG must be a real, verified date -- confirmed via a
real news source or the user directly, never assumed from memory or
pattern-matched ("it's usually the second Tuesday"). Built 2026-09-01,
seeded with AAPL's fall product event after the user asked for the real
historical pre-event trend; each of the eight past dates below was
cross-checked against a real AAPL close via get_equity_historicals the
same day this file was written -- see sources.md "AAPL Sept-event trend".
No tool here can confirm a FUTURE calendar date is real, so adding a new
upcoming_date without independent confirmation (the user, or a fresh
news check) is exactly the kind of guess this repo's Rule Zero exists to
forbid -- do not add one from memory alone.

Pure math, no network, same posture as option_math.py:
historical_moves_from_bars() takes REAL daily bars the caller already
fetched (get_equity_historicals) and returns the same historical_moves
list shape option_math.evaluate_candidate expects. It does not fetch
data itself, and it does not average away a bad bar -- it discards
interpolated/zero-volume bars before computing anything, the same WOLF-
shaped failure mode option_scanner.py's SYSTEM_PROMPT already warns
about by hand.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Sequence


@dataclass(frozen=True)
class EventSeries:
    """One symbol's recurring or notable dated event type. catalyst_type
    is a free label (e.g. "product_event", "fomc", "regulatory_ruling",
    "investor_day") -- not restricted to a fixed enum, since "everything"
    was the point."""

    symbol: str
    catalyst_type: str
    # "am" or "pm" -- when the market can first react, same convention as
    # option_math.catalyst_effective_date's am/pm split. "am": the event
    # lands before/during the session (most keynotes are morning Pacific,
    # i.e. still premarket or early session ET) -- compare the close on
    # the event's own trading day against the PRIOR close. "pm": the
    # event lands after the close -- compare the NEXT trading day's close
    # against the event day's close.
    timing: str
    # Real, verified past occurrence dates (YYYY-MM-DD), oldest first.
    past_dates: tuple[str, ...]
    upcoming_date: Optional[str] = None
    source_note: str = ""


# Seeded 2026-09-01. See sources.md "AAPL Sept-event trend" for the real
# 8-year price verification these dates are built on (get_equity_historicals,
# 2018-2025 daily bars, no interpolated bars used).
EVENT_CATALOG: dict[tuple[str, str], EventSeries] = {
    ("AAPL", "product_event"): EventSeries(
        symbol="AAPL",
        catalyst_type="product_event",
        timing="am",
        past_dates=(
            "2018-09-12",
            "2019-09-10",
            "2020-09-15",  # Watch/iPad event; that year's iPhone event
                            # was delayed to 2020-10-13 (COVID) -- flagged
                            # in source_note, not silently treated as
                            # equivalent to a normal year.
            "2021-09-14",
            "2022-09-07",
            "2023-09-12",
            "2024-09-09",
            "2025-09-09",
        ),
        upcoming_date="2026-09-09",
        source_note=(
            "User-confirmed 2026-09-09 fall event date (2026-09-01). "
            "Historical dates are Apple's real publicly-announced fall "
            "keynote dates. 2020 was a Watch/iPad-only event -- the iPhone "
            "launch that year was delayed to 2020-10-13, so its move is not "
            "directly comparable to the other seven flagship-iPhone years."
        ),
    ),
}


def get_event_series(symbol: str, catalyst_type: str) -> Optional[EventSeries]:
    return EVENT_CATALOG.get((symbol.upper().strip(), catalyst_type))


def list_event_series(symbol: Optional[str] = None) -> list[EventSeries]:
    """All catalogued series, optionally filtered to one symbol."""
    out = list(EVENT_CATALOG.values())
    if symbol:
        sym = symbol.upper().strip()
        out = [e for e in out if e.symbol == sym]
    return out


def _real_bar(bar: dict[str, Any]) -> bool:
    """True if a bar is real traded market data, not synthesized gap-fill.
    Same check option_scanner.py's SYSTEM_PROMPT already requires by hand
    -- codified here so a caller cannot silently skip it."""
    if bar.get("interpolated"):
        return False
    try:
        vol = float(bar.get("volume", 0) or 0)
    except (TypeError, ValueError):
        return False
    return vol > 0


def historical_moves_from_bars(
    series: EventSeries, daily_bars: Sequence[dict[str, Any]]
) -> list[float]:
    """One real close-to-close percent move per past occurrence in
    `series`, from a REAL daily-bar series the caller already fetched
    (get_equity_historicals, interval='day', spanning from before
    series.past_dates[0] through today). Bars must carry 'begins_at'
    (a date string, UTC), 'close_price', 'interpolated', and 'volume' --
    the exact shape get_equity_historicals returns.

    Skips (never fabricates) any occurrence whose needed bars are missing
    or were discarded as synthesized -- returns fewer moves rather than a
    wrong one. Feed the result straight into
    option_math.historical_move_pct(), which already enforces a
    two-observation floor and returns None below it.
    """
    real = [b for b in daily_bars if _real_bar(b)]
    dated: list[tuple[str, float]] = []
    for b in real:
        begins = str(b.get("begins_at", ""))[:10]
        try:
            close_f = float(b.get("close_price"))
        except (TypeError, ValueError):
            continue
        if not begins or close_f <= 0:
            continue
        dated.append((begins, close_f))
    dated.sort(key=lambda t: t[0])

    timing = (series.timing or "pm").strip().lower()
    moves: list[float] = []
    for target in series.past_dates:
        # index of the latest trading day at-or-before target
        i = -1
        for idx, (d, _) in enumerate(dated):
            if d <= target:
                i = idx
            else:
                break
        if i < 0:
            continue  # no real data reaches back this far
        if timing == "am":
            if i - 1 < 0:
                continue
            before_close = dated[i - 1][1]
            event_close = dated[i][1]
            pct = (event_close - before_close) / before_close * 100.0
        else:
            if i + 1 >= len(dated):
                continue
            event_close = dated[i][1]
            after_close = dated[i + 1][1]
            pct = (after_close - event_close) / event_close * 100.0
        moves.append(pct)
    return moves
