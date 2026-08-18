"""Unit tests for growth_signal.py. Run: python3 test_growth_signal.py"""

from __future__ import annotations

from growth_signal import (
    GrowthCandidate,
    check_candidate,
    decide_stop_update,
    trailing_stop_price,
)

passed = 0
failed = 0


def check(name: str, cond: bool) -> None:
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {name}")


# --- check_candidate -- re-verifies live numbers against the saved scan's
# own thresholds -------------------------------------------------------

good = GrowthCandidate(
    symbol="PLTR", market_cap=4.15e11, rsi=66.7, pct_change_1mo=40.5,
    adx=29.4, avg_volume=4.35e7,
)
r = check_candidate(good)
check("passing candidate: passes", r.passed)
check("passing candidate: reason cites real numbers", "66.7" in r.reason)

low_cap = GrowthCandidate(
    symbol="MICRO", market_cap=5e8, rsi=60.0, pct_change_1mo=10.0,
    adx=25.0, avg_volume=1e6,
)
r = check_candidate(low_cap)
check("below market cap floor: fails", not r.passed)
check("below market cap floor: reason names it", "market cap" in r.reason)

overbought = GrowthCandidate(
    symbol="HOT", market_cap=2e9, rsi=78.0, pct_change_1mo=30.0,
    adx=25.0, avg_volume=1e6,
)
r = check_candidate(overbought)
check("RSI over 70: fails", not r.passed)
check("RSI over 70: reason names RSI", "RSI" in r.reason)

no_trend = GrowthCandidate(
    symbol="CHOP", market_cap=2e9, rsi=60.0, pct_change_1mo=10.0,
    adx=12.0, avg_volume=1e6,
)
r = check_candidate(no_trend)
check("ADX below 20 (no trend): fails", not r.passed)

flat = GrowthCandidate(
    symbol="FLAT", market_cap=2e9, rsi=60.0, pct_change_1mo=1.0,
    adx=25.0, avg_volume=1e6,
)
r = check_candidate(flat)
check("1mo change too small: fails", not r.passed)

illiquid = GrowthCandidate(
    symbol="THIN", market_cap=2e9, rsi=60.0, pct_change_1mo=10.0,
    adx=25.0, avg_volume=1e4,
)
r = check_candidate(illiquid)
check("avg volume too thin: fails", not r.passed)


# --- trailing_stop_price -----------------------------------------------

check("trailing stop 18% below a $100 peak", trailing_stop_price(100.0) == 82.0)
check("trailing stop scales with peak", trailing_stop_price(200.0) == 164.0)
check("trailing stop honors a custom trail_pct", trailing_stop_price(100.0, trail_pct=10.0) == 90.0)

try:
    trailing_stop_price(0)
    check("trailing stop rejects a zero peak", False)
except ValueError:
    check("trailing stop rejects a zero peak", True)

try:
    trailing_stop_price(-5)
    check("trailing stop rejects a negative peak", False)
except ValueError:
    check("trailing stop rejects a negative peak", True)


# --- decide_stop_update -- only ever ratchets UP ------------------------

u = decide_stop_update(current_stop=None, peak_price=100.0)
check("no stop resting yet: should update", u.should_update)
check("no stop resting yet: new stop is 18% below peak", u.new_stop == 82.0)

u = decide_stop_update(current_stop=82.0, peak_price=110.0)
check("new higher peak: should update", u.should_update)
check("new higher peak: new stop is 18% below the NEW peak", abs(u.new_stop - 90.2) < 1e-9)

u = decide_stop_update(current_stop=82.0, peak_price=100.0)
check("same peak as last update: should NOT update", not u.should_update)
check("same peak as last update: no new stop returned", u.new_stop is None)

u = decide_stop_update(current_stop=90.0, peak_price=100.0)
check(
    "peak higher than entry but trail level still below resting stop: should NOT update",
    not u.should_update,
)

u = decide_stop_update(current_stop=None, peak_price=50.0)
check("custom entry, no stop yet: computes correctly", u.new_stop == 41.0)


print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
