"""Tests for intraday_edge.py.

Run: python3 test_intraday_edge.py

The most important test in this file is test_qqq_real_0dte_is_rejected: it
replays the ACTUAL QQQ 5-minute bar history pulled live on 2026-08-21 (44
real trading days, 2026-06-22 through 2026-08-21) against the ACTUAL 0DTE
decision on the table that afternoon -- a $714 call needing +0.15% with 108
minutes left, priced by Robinhood's own model at a 24.4% chance of profit.
The position was already down 35% when this was built and went on to expire
worthless. A module that cannot reject it, using only data that existed
before market close that day, is worthless.
"""

from __future__ import annotations

from intraday_edge import (
    IntradayEdgeConfig,
    daily_close_window_moves,
    edge_ratio,
    evaluate_intraday_edge,
    realized_move_frequency,
    required_move_pct,
)

failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    status = "ok  " if condition else "FAIL"
    print(f"{status} {name}" + (f"\n       {detail}" if detail and not condition else ""))
    if not condition:
        failures.append(name)


print("required_move_pct")
check("up move", abs(required_move_pct(713.27, 714.33) - 0.14863) < 0.001,
      str(required_move_pct(713.27, 714.33)))
check("down move (put breakeven below current)", required_move_pct(713.27, 700.0) < 0,
      str(required_move_pct(713.27, 700.0)))
check("zero current price rejected", required_move_pct(0, 714.33) is None)
check("negative current price rejected", required_move_pct(-5, 714.33) is None)
check("non-numeric rejected", required_move_pct("nope", 714.33) is None)
check("bool rejected", required_move_pct(True, 714.33) is None)

print("\nrealized_move_frequency")
below_floor = [0.1] * 19  # one short of MIN_HISTORICAL_DAYS
check("below the 20-day floor is rejected", realized_move_frequency(below_floor, 0.0) is None)
at_floor = [0.5] * 15 + [-0.5] * 5  # 20 days, 15 hit a +0.0% threshold
check("at the floor computes", realized_move_frequency(at_floor, 0.0) == 0.75,
      str(realized_move_frequency(at_floor, 0.0)))
check("garbage entries are dropped, not counted as hits",
      realized_move_frequency(list(at_floor) + ["nan-ish", None, True], 0.0) == 0.75,
      str(realized_move_frequency(list(at_floor) + ["nan-ish", None, True], 0.0)))
mixed_sign = [-0.2] * 12 + [0.2] * 8  # 20 days
# threshold -0.1: a put needing the underlying to fall at least 0.1%.
# The 12 days at -0.2% cleared it (fell MORE than needed); the 8 days at
# +0.2% did not (rose instead of falling) -- hit rate is 12/20, not the
# 8/20 a naive ">= -0.1" literal comparison would give.
check("negative threshold (put breakeven) counts bigger falls as hits",
      realized_move_frequency(mixed_sign, -0.1) == 0.60,
      str(realized_move_frequency(mixed_sign, -0.1)))

print("\nedge_ratio")
check("historical beats implied -> ratio > 1", abs(edge_ratio(0.30, 0.20) - 1.5) < 1e-9)
check("historical worse than implied -> ratio < 1", edge_ratio(0.182, 0.244) is not None
      and abs(edge_ratio(0.182, 0.244) - 0.7459) < 0.001)
check("None historical propagates", edge_ratio(None, 0.20) is None)
check("implied_prob of 0 rejected", edge_ratio(0.30, 0) is None)
check("implied_prob > 1 rejected (caller passed percent, not a fraction)",
      edge_ratio(0.30, 24.4) is None)
check("negative implied_prob rejected", edge_ratio(0.30, -0.1) is None)

print("\ndaily_close_window_moves -- synthetic bars")


def bar(begins_at: str, close: float, interpolated: bool = False) -> dict:
    d = {"begins_at": begins_at, "close_price": str(close)}
    if interpolated:
        d["interpolated"] = True
    return d


synthetic = [
    bar("2026-08-17T13:30:00Z", 100.0),
    bar("2026-08-17T18:30:00Z", 100.0),  # 90 min before a 20:00 close
    bar("2026-08-17T19:59:00Z", 101.0),  # actual close
    bar("2026-08-18T13:30:00Z", 200.0),
    bar("2026-08-18T18:30:00Z", 200.0, interpolated=True),  # should be ignored
    bar("2026-08-18T18:25:00Z", 200.0),  # real bar just before the interpolated one
    bar("2026-08-18T19:59:00Z", 198.0),
]
moves = daily_close_window_moves(synthetic, window_minutes=90)
check("two trading days extracted", len(moves) == 2, str(moves))
check("day 1 move computed off the real mark bar",
      len(moves) == 2 and abs(moves[0] - 1.0) < 1e-6, str(moves))
check("day 2 falls back past the interpolated bar to a real one",
      len(moves) == 2 and abs(moves[1] - (-1.0)) < 1e-6, str(moves))
check("zero window_minutes returns empty", daily_close_window_moves(synthetic, 0) == [])
check("empty input returns empty", daily_close_window_moves([], 90) == [])

print("\nevaluate_intraday_edge -- input validation")
r, why = evaluate_intraday_edge(0, 714.33, 0.244, [0.1] * 25)
check("bad price rejected with a reason", r is None and "current_price" in why, why)
r, why = evaluate_intraday_edge(713.27, 714.33, 1.5, [0.1] * 25)
check("implied_prob out of (0,1] rejected", r is None and "implied_prob" in why, why)
r, why = evaluate_intraday_edge(713.27, 714.33, 0.244, [0.1] * 19)
check("insufficient history rejected", r is None and "historical days" in why, why)

print("\nTHE REGRESSION TEST -- real QQQ 0DTE decision, 2026-08-21 ~1:57pm ET")
# The ACTUAL 44 real trading days of QQQ 5-minute-bar closes, mark->close
# moves over the closing 108 minutes of each regular session, pulled live
# via get_equity_historicals (2026-06-22 through 2026-08-21) and computed
# with this exact module's daily_close_window_moves(). Not synthesized --
# this is what the tape actually did.
qqq_108min_moves_real = [
    0.068, -0.303, 0.238, -0.153, -0.805, 0.138, -0.026, -0.356, 0.214, -0.046,
    -0.478, 0.176, -0.106, -0.047, -0.147, -0.263, -0.055, -0.048, -0.385, -0.701,
    -0.117, -0.291, 0.216, -0.583, 0.338, -0.093, -1.857, 0.210, -0.095, -0.183,
    0.119, -0.539, -0.137, 0.309, -0.082, 0.098, -0.166, -0.007, 0.077, 0.007,
    0.103, 0.073, 0.234, -0.041,
]
check("real dataset has 44 days", len(qqq_108min_moves_real) == 44)

freq = realized_move_frequency(qqq_108min_moves_real, 0.15)
check("real historical frequency of a +0.15% close-window move is 18.2%",
      abs(freq - 8 / 44) < 1e-6, str(freq))

result, reason = evaluate_intraday_edge(
    current_price=713.27,
    breakeven_price=714.33,
    implied_prob=0.244,  # Robinhood's own "chance_of_profit_long" on the $714 call
    historical_moves_pct=qqq_108min_moves_real,
)
check("real trade is REJECTED", result is not None and result.passed is False, reason)
check("edge ratio matches hand-computed 0.746",
      result is not None and abs(result.edge_ratio - 0.7459) < 0.001,
      str(result.edge_ratio if result else None))
check("rejection reason names the real required move and the real odds",
      result is not None and "0.15" in reason and "18%" in reason and "24%" in reason,
      reason)

# The far-OTM $717 call the same afternoon: delta 0.04, chance_of_profit_long
# 3.5%, needing +0.53% instead of +0.15%. Real history never once produced a
# move that size in this window across all 44 days -- 0% frequency.
required_717 = required_move_pct(713.27, 717.03)
freq_717 = realized_move_frequency(qqq_108min_moves_real, required_717)
check("the far-OTM leg needed roughly +0.53%", abs(required_717 - 0.5273) < 0.001, str(required_717))
check("real history never cleared that bar in 44 days", freq_717 == 0.0, str(freq_717))
result_717, reason_717 = evaluate_intraday_edge(713.27, 717.03, 0.035, qqq_108min_moves_real)
check("the far-OTM leg is rejected even harder", result_717 is not None and result_717.passed is False)

print()
if failures:
    print(f"{len(failures)} FAILURE(S): {failures}")
    raise SystemExit(1)
print("all tests passed")
