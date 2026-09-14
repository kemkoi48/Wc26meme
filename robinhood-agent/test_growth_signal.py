"""Unit tests for growth_signal.py. Run: python3 test_growth_signal.py"""

from __future__ import annotations

from growth_signal import (
    PROFIT_TRAIL_PCT,
    PROFIT_TRIGGER_PCT,
    GrowthCandidate,
    check_candidate,
    decide_profit_exit,
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


# ---------------------------------------------------------------------------
# Profit lock (added 2026-09-14). The thresholds are the user's own stated
# numbers, so they are pinned on BOTH sides here -- same discipline the S7
# delta floor got, so the value cannot drift back out of the code silently.
# ---------------------------------------------------------------------------

check("trigger pinned at 5%", PROFIT_TRIGGER_PCT == 5.0)
check("trail pinned at 2%", PROFIT_TRAIL_PCT == 2.0)

# not armed: peak never reached +5%
r = decide_profit_exit(entry_price=100.0, peak_price=104.0, current_price=100.0)
check("peak +4% does not arm the lock", not r.should_exit)
check("not-armed reason names the gap", "not armed" in r.reason)

# armed exactly at the boundary, no pullback yet -> hold
r = decide_profit_exit(entry_price=100.0, peak_price=105.0, current_price=105.0)
check("peak exactly +5% arms but does not exit at the high", not r.should_exit)
check("armed-and-running reason says still running", "still running" in r.reason)

# armed, pullback exactly 2% -> exit
r = decide_profit_exit(entry_price=100.0, peak_price=105.0, current_price=102.9)
check("armed + exactly 2% pullback exits", r.should_exit)
check("exit reason names the profit lock", "profit lock" in r.reason)

# armed, pullback 1.9% -> hold (boundary pinned from below)
r = decide_profit_exit(entry_price=100.0, peak_price=105.0, current_price=103.0)
check("armed + 1.9% pullback does NOT exit", not r.should_exit)

# a big winner keeps running: rides the PEAK, not the entry
r = decide_profit_exit(entry_price=100.0, peak_price=150.0, current_price=148.0)
check("+50% peak, 1.3% off it: keeps running", not r.should_exit)
r = decide_profit_exit(entry_price=100.0, peak_price=150.0, current_price=147.0)
check("+50% peak, 2% off it: exits near the high, not at breakeven", r.should_exit)

# never peaked above entry -- must not divide by a peak below entry
r = decide_profit_exit(entry_price=100.0, peak_price=95.0, current_price=90.0)
check("peak below entry: never arms, no exit", not r.should_exit)

# garbage in -> no exit, never an exception
for bad in (0, -1, None, "abc", True, float("nan")):
    r = decide_profit_exit(entry_price=bad, peak_price=105.0, current_price=100.0)
    check(f"unusable entry {bad!r}: no exit, no raise", not r.should_exit)
    r = decide_profit_exit(entry_price=100.0, peak_price=105.0, current_price=bad)
    check(f"unusable current {bad!r}: no exit, no raise", not r.should_exit)

# ---------------------------------------------------------------------------
# REAL closed trades from trades.csv, as regression fixtures. These record
# what the rule WOULD have done -- including the two cases where it changes
# nothing, so the fix is not oversold.
# ---------------------------------------------------------------------------

# SMR: entry 10.00, real peak 11.37 (09-08), stopped out at 9.32 for -$0.68.
r = decide_profit_exit(entry_price=10.00, peak_price=11.37, current_price=9.32)
check("SMR (+13.7% peak) would have armed and exited in profit", r.should_exit)

# BTG: entry 5.2599, real peak 5.7005. Only booked because the user forced it.
r = decide_profit_exit(entry_price=5.2599, peak_price=5.7005, current_price=5.50)
check("BTG (+8.4% peak, 3.5% off) would have auto-exited without being told", r.should_exit)

# SMCI: peak 39.47 on a 38.00 entry is only +3.87% -- the lock never arms.
r = decide_profit_exit(entry_price=38.00, peak_price=39.47, current_price=36.4822)
check("SMCI peak was only +3.87%: lock does NOT arm (fix does not help here)", not r.should_exit)

# HL: peak 21.18 on a 20.62 entry is only +2.72% -- also never arms.
r = decide_profit_exit(entry_price=20.62, peak_price=21.18, current_price=18.975)
check("HL peak was only +2.72%: lock does NOT arm (fix does not help here)", not r.should_exit)


print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
