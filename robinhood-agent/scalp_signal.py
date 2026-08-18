"""Momentum-scalp signal math -- entry and exit rules for 1-5 minute holds.

Reverse-engineered from the user's own 2026-08-17 trading (six IPST round
trips, median hold 149 seconds, +$29.58) after that day's Investing account
made +36.29% while this repo's slower rules made +1.37% on the same tape.
See sources.md, "2026-08-17 The user's own scalping".

WHAT IS ACTUALLY ESTABLISHED, AND WHAT IS NOT
=============================================
Measured across 1,530 minute bars from five symbols on 2026-08-17
(IPST/WFF/OSRH/OABI/AIFC), entry modelled at the NEXT bar's open -- i.e.
only after a bar completes, which is the earliest a scanner can honestly
act:

  ESTABLISHED (and it is a negative result):
    Volume surge ALONE is worthless. Bars with >=4x median volume had a
    median 5-bar MFE of +0.95% against a +1.35% all-bars baseline -- i.e.
    WORSE than picking a bar at random. A volume spike with no price
    response is as likely to be a selling climax as a breakout.

  ESTABLISHED (and it is the useful part):
    Volume surge CONFIRMING an up move is materially better than the same
    up move without it. At bar_return >= 2%:
      no volume filter : median MFE +4.31%, MAE -3.76%, 61% reach +3%
      with surge >=3x  : median MFE +7.52%, MAE -2.84%, 71% reach +3%
      with surge <3x   : median MFE +3.57%, MAE -4.15%, 57% reach +3%
    Volume improves the upside, shrinks the drawdown, and lifts the hit
    rate -- but only as confirmation, never as the signal itself.

  NOT ESTABLISHED -- do not trust the magnitudes:
    Simulating the full rule (enter next open, -2% hard stop, trail out on
    close < prior bar's low) over the 41 signals that fired returns +709%
    total. That number is not real edge and must not be quoted as one:
      - 28 of 41 signals LOST money. Median outcome is -2.00%, the stop.
      - 3 trades produced 86% of the entire profit; the single best was 38%.
      - +699.6% of the +709.4% came from ONE symbol (WFF, which ran
        $4.49 -> $10.20 that day). IPST contributed +9.2%, OSRH -0.2%.
    Strip WFF out and the rule is flat. This is one stock's trend on one
    day, caught three times -- n=41 on a single session is not a backtest,
    and the repo has rejected far better-supported claims than this (see
    S2's 74-trade rejection in strategies.md).

  WHAT SURVIVES the honesty check is the SHAPE, not the size: most signals
  lose a little and a few win a lot. That matches the user's own day (three
  losers averaging -3.4%, one winner +23.9%) and it is the reason the exit
  rules below are asymmetric -- a fixed profit target would cap exactly the
  trades that pay for all the others. Applying this repo's own Rule 4
  (target = entry + 1.25R) to the user's +23.9% winner would have exited
  near $8.10 instead of $9.57, converting it to roughly +5% and throwing
  away three quarters of the day's profit.

So: treat the DIRECTION of these rules as evidence-backed and the EXPECTED
RETURN as unknown. Every signal this module emits carries `confidence`
saying which parts rest on measurement and which on a single day.

Everything here is a pure function over numbers -- no network, no SDK --
so it is unit-testable standalone (`python3 test_scalp_signal.py`), the same
posture as option_math.py and regime.py.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Any, Optional, Sequence

# --- thresholds, and where each number came from ---------------------------

# Volume must be this multiple of the trailing median to count as a surge.
# 3x measured better than 4x/5x on 2026-08-17 (median MFE +7.52% vs +9.58%
# at 4x, but 42 signals vs 26 -- 3x keeps more of the sample without giving
# up the effect). Below 3x the volume confirmation stops adding anything.
MIN_SURGE = 3.0

# The bar must actually move price up this much. THIS is the load-bearing
# filter: at >=2% the median MFE roughly triples versus surge alone. Set
# lower and the negative result above takes over.
MIN_BAR_RETURN_PCT = 2.0

# Trailing window for the volume median. 20 bars ~= the last 20 minutes,
# long enough to have a stable baseline and short enough to reflect today's
# regime rather than the pre-market lull.
VOLUME_LOOKBACK = 20

# Hard stop. -2% and -3% performed near-identically on the sample; -2%
# caps the loser faster, which is the half of the asymmetry actually under
# the trader's control.
DEFAULT_STOP_PCT = -2.0

# Give up if the move has not worked within this many bars. Median
# bars-to-peak was 11 and only 44% of signals peaked within 5, so this is
# deliberately NOT tight -- cutting at 2-3 bars truncated the winners that
# carry the strategy.
MAX_HOLD_BARS = 15


def _f(value: Any) -> Optional[float]:
    """Coerce to float or None. Rejects bools and non-finite values, both of
    which would otherwise silently poison the arithmetic."""
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
class Bar:
    """One OHLCV minute bar. `interpolated` bars must never reach here --
    a synthesized flat bar reports volume 0 and a 0% return, which silently
    suppresses every signal. Callers discard them (the WOLF lesson,
    sources.md 2026-08-12)."""

    o: float
    h: float
    l: float
    c: float
    v: float


def to_bars(raw: Sequence[dict[str, Any]]) -> list[Bar]:
    """Convert Robinhood `get_equity_historicals` bars to Bar objects,
    dropping anything unusable. Fails closed: a malformed bar is skipped,
    never coerced into a plausible-looking zero."""
    out: list[Bar] = []
    for b in raw:
        if b.get("interpolated"):
            continue
        o, h, l = _f(b.get("open_price")), _f(b.get("high_price")), _f(b.get("low_price"))
        c, v = _f(b.get("close_price")), _f(b.get("volume"))
        if None in (o, h, l, c, v):
            continue
        if o <= 0 or h <= 0 or l <= 0 or c <= 0 or v <= 0:
            continue
        if h < l:
            continue
        out.append(Bar(o=o, h=h, l=l, c=c, v=v))
    return out


def surge_ratio(bars: Sequence[Bar], lookback: int = VOLUME_LOOKBACK) -> Optional[float]:
    """Latest bar's volume as a multiple of the trailing median. None when
    there is not enough history or the median is zero -- both mean "no
    baseline", which is different from "no surge" and must not be reported
    as 1.0."""
    if len(bars) < lookback + 1:
        return None
    med = statistics.median([b.v for b in bars[-(lookback + 1):-1]])
    if med <= 0:
        return None
    return bars[-1].v / med


def bar_return_pct(bar: Bar) -> Optional[float]:
    """Open-to-close move of one bar, in percent."""
    if bar.o <= 0:
        return None
    return (bar.c - bar.o) / bar.o * 100.0


def close_position(bar: Bar) -> Optional[float]:
    """Where the bar closed inside its own range: 1.0 = at the high,
    0.0 = at the low. Reported for context; it did NOT separate winners
    from losers on the 2026-08-17 sample (adding close_pos>=0.7 on top of
    the surge+return filter changed the hit rate by ~1 point), so it is
    deliberately not a gate."""
    rng = bar.h - bar.l
    if rng <= 0:
        return None
    return (bar.c - bar.l) / rng


@dataclass(frozen=True)
class Signal:
    """An entry alert. `entry_hint` is the price the NEXT bar is expected to
    open near -- this module never claims a fill inside the signal bar,
    because a scanner cannot know a bar surged until it has closed."""

    fired: bool
    reason: str
    surge: Optional[float] = None
    bar_return: Optional[float] = None
    close_pos: Optional[float] = None
    entry_hint: Optional[float] = None
    stop_price: Optional[float] = None
    confidence: str = ""


def detect_entry(
    bars: Sequence[Bar],
    min_surge: float = MIN_SURGE,
    min_bar_return: float = MIN_BAR_RETURN_PCT,
    stop_pct: float = DEFAULT_STOP_PCT,
    lookback: int = VOLUME_LOOKBACK,
) -> Signal:
    """Decide whether the just-closed bar is an entry trigger.

    Both conditions must hold, and the ORDER of the checks encodes the
    finding: a surge with no price response is explicitly reported as a
    non-signal rather than a weak one, because that population underperformed
    a random bar."""
    if len(bars) < lookback + 1:
        return Signal(False, f"need {lookback + 1} bars, have {len(bars)}")

    last = bars[-1]
    s = surge_ratio(bars, lookback)
    if s is None:
        return Signal(False, "no usable volume baseline")
    r = bar_return_pct(last)
    if r is None:
        return Signal(False, "bar return not computable")
    cp = close_position(last)

    if r < min_bar_return:
        return Signal(
            False,
            f"price moved {r:+.2f}% (<{min_bar_return:.1f}%) -- volume {s:.1f}x "
            "without a price response is not a signal",
            surge=s, bar_return=r, close_pos=cp,
        )
    if s < min_surge:
        return Signal(
            False,
            f"up {r:+.2f}% but volume only {s:.1f}x (<{min_surge:.1f}x) -- "
            "unconfirmed move",
            surge=s, bar_return=r, close_pos=cp,
        )

    entry = last.c
    return Signal(
        True,
        f"volume {s:.1f}x median CONFIRMING a {r:+.2f}% bar",
        surge=s, bar_return=r, close_pos=cp,
        entry_hint=entry,
        stop_price=entry * (1 + stop_pct / 100.0),
        confidence=(
            "Direction is measurement-backed (surge+move beat surge alone and "
            "move alone on 1,530 bars). Expected return is NOT -- the sizing "
            "study was n=41 on one day with 86% of profit from 3 trades. "
            "Assume most signals lose ~2%; size for that."
        ),
    )


@dataclass(frozen=True)
class ExitDecision:
    exit_now: bool
    reason: str
    kind: str = ""  # "stop" | "trail" | "time" | ""


def decide_exit(
    entry_price: float,
    bars_since_entry: Sequence[Bar],
    stop_pct: float = DEFAULT_STOP_PCT,
    max_hold: int = MAX_HOLD_BARS,
) -> ExitDecision:
    """Exit logic, checked in priority order. Deliberately has NO profit
    target: on the 2026-08-17 sample every fixed target truncated the small
    number of large winners that produced all of the profit, and the same is
    true of the user's own +23.9% trade under this repo's Rule 4.

    Priority:
      1. Hard stop -- the loss is capped and nothing else matters.
      2. Trail -- close below the PREVIOUS bar's low means the up-move has
         structurally broken. This is what lets a winner run: it does not
         fire on an ordinary pullback, only on a lower close through prior
         support.
      3. Time -- the thesis was "this moves now"; after max_hold bars it
         did not, so the premise is stale.
    """
    e = _f(entry_price)
    if e is None or e <= 0:
        return ExitDecision(False, "unusable entry price")
    if not bars_since_entry:
        return ExitDecision(False, "no bars since entry yet")

    stop = e * (1 + stop_pct / 100.0)
    cur = bars_since_entry[-1]
    n = len(bars_since_entry)

    if cur.l <= stop:
        return ExitDecision(
            True, f"hard stop hit: low {cur.l:.4f} <= stop {stop:.4f}", "stop"
        )

    if n >= 2:
        prev = bars_since_entry[-2]
        if cur.c < prev.l:
            pnl = (cur.c - e) / e * 100.0
            return ExitDecision(
                True,
                f"structure broken: close {cur.c:.4f} < prior bar low "
                f"{prev.l:.4f} ({pnl:+.2f}%)",
                "trail",
            )

    if n >= max_hold:
        pnl = (cur.c - e) / e * 100.0
        return ExitDecision(
            True,
            f"time stop: {n} bars without resolving ({pnl:+.2f}%)",
            "time",
        )

    pnl = (cur.c - e) / e * 100.0
    return ExitDecision(False, f"holding, bar {n}/{max_hold}, {pnl:+.2f}%")
