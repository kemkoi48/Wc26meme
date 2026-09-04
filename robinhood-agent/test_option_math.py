"""Tests for option_math.py.

Run: python3 test_option_math.py

The most important test in this file is test_envx_real_chain_is_rejected:
it replays the ACTUAL ENVX option chain pulled on 2026-08-12 (earnings that
evening) and asserts the screen rejects it. That contract looked exactly
like the setup this screen is meant to find -- pennies, real catalyst hours
away -- and was not an edge. A screen that cannot reject it is worthless.
"""

from __future__ import annotations

import datetime as dt

from option_math import (
    OptionScanConfig,
    SoftCatalystScanConfig,
    apply_filters_and_rank,
    apply_soft_filters_and_rank,
    as_pct_of,
    catalyst_direction_score,
    catalyst_effective_date,
    evaluate_candidate,
    decide_option_exit,
    evaluate_soft_candidate,
    expected_move_from_iv,
    expected_move_from_straddle,
    historical_move_pct,
    iv_cheap_vs_multi_window_hv,
    iv_hv_ratio,
    mid_price,
    mismatch_ratio,
    realized_volatility,
    spread_pct,
)

failures: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name} {detail}")
        failures.append(name)


def approx(a, b, tol=1e-6) -> bool:
    return a is not None and b is not None and abs(a - b) < tol


print("mid_price / spread_pct")
check("mid of 0.54/0.61", approx(mid_price(0.54, 0.61), 0.575))
check("zero bid rejected", mid_price(0, 0.07) is None)
check("crossed quote rejected", mid_price(0.10, 0.05) is None)
check("garbage rejected", mid_price("abc", 0.07) is None)
check("None rejected", mid_price(None, 0.07) is None)
check("bool rejected", mid_price(True, 0.07) is None)
# 0.54/0.61 -> spread 0.07 on mid 0.575 = 12.17%
check("spread 0.54/0.61 ~12.2%", approx(spread_pct(0.54, 0.61), 12.173913, 1e-4))
# the deep-OTM penny case: 0.04/0.07 -> 0.03 on 0.055 = 54.5%
check("spread 0.04/0.07 ~54.5%", approx(spread_pct(0.04, 0.07), 54.545454, 1e-4))

print("expected move")
# ENVX ATM straddle: call 0.575 + put 0.27 = 0.845 * 0.85 = 0.71825
check("straddle expected move", approx(expected_move_from_straddle(0.575, 0.27), 0.71825))
check("straddle rejects zero leg", expected_move_from_straddle(0, 0.27) is None)
check("straddle rejects None", expected_move_from_straddle(None, 0.27) is None)
# on $4.785 that is ~15.0%
check("ENVX expected move ~15%", approx(as_pct_of(0.71825, 4.785), 15.010449, 1e-4))
# IV formula: 4.785 * 2.93 * sqrt(2/365)
em_iv = expected_move_from_iv(4.785, 2.93, 2)
check("iv expected move computes", em_iv is not None and 0.9 < em_iv < 1.1)
check("iv rejects zero dte", expected_move_from_iv(4.785, 2.93, 0) is None)
check("iv rejects negative price", expected_move_from_iv(-1, 2.93, 2) is None)

print("historical_move_pct")
check("median of moves", approx(historical_move_pct([10, -20, 30]), 20.0))
check("abs applied", approx(historical_move_pct([-10, -10]), 10.0))
check("single observation rejected", historical_move_pct([15]) is None)
check("empty rejected", historical_move_pct([]) is None)
check("garbage filtered then rejected", historical_move_pct(["x", 5]) is None)
check("mixed garbage still works", approx(historical_move_pct(["x", 5, 15]), 10.0))

print("mismatch_ratio")
check("underpriced", approx(mismatch_ratio(5.0, 10.0), 0.5))
check("fairly priced", approx(mismatch_ratio(10.0, 10.0), 1.0))
check("rich", approx(mismatch_ratio(15.0, 10.0), 1.5))
check("zero historical rejected", mismatch_ratio(5.0, 0) is None)

print("catalyst_effective_date -- the off-by-one that kills contracts")
check(
    "pm earnings moves next day",
    catalyst_effective_date("2026-08-12", "pm") == dt.date(2026, 8, 13),
)
check(
    "am earnings moves same day",
    catalyst_effective_date("2026-08-12", "am") == dt.date(2026, 8, 12),
)
check(
    "unknown timing treated as pm (conservative)",
    catalyst_effective_date("2026-08-12", None) == dt.date(2026, 8, 13),
)
check("malformed date rejected", catalyst_effective_date("not-a-date") is None)

print()
print("THE REGRESSION TEST -- real ENVX chain, 2026-08-12, must be REJECTED")
cfg = OptionScanConfig()
today = dt.date(2026, 8, 12)

# Real quotes pulled from the live chain. Underlying $4.785, earnings pm.
envx_otm_call = {
    "symbol": "ENVX",
    "underlying_price": 4.785,
    "strike": 6.5,
    "type": "call",
    "expiration_date": "2026-08-14",
    "catalyst_date": "2026-08-12",
    "catalyst_timing": "pm",
    "catalyst_type": "earnings",
    "bid": 0.04,
    "ask": 0.07,
    "iv": 3.045127,
    "delta": 0.119280,
    "open_interest": 593,
    "volume": 15,
    "atm_call_mid": 0.575,
    "atm_put_mid": 0.27,
    # REAL close-to-close moves on the session after each of ENVX's last six
    # pm earnings reports, computed from daily bars on 2026-08-12:
    #   2025-02-19 +2.55 | 2025-04-30 -8.36 | 2025-07-31 -20.11
    #   2025-11-05 -20.23 | 2026-02-25 -3.25 | 2026-05-13 -13.58
    # Median absolute move: 10.97%. These are looked up, NOT assumed -- an
    # earlier draft of this test invented plausible-looking numbers and
    # flipped the verdict, which is the exact failure mode this screen is
    # supposed to prevent.
    "historical_moves": [2.55, -8.36, -20.11, -20.23, -3.25, -13.58],
    "notes": "Looks like the classic cheap-catalyst setup. It is not.",
}
result, reason = evaluate_candidate(envx_otm_call, cfg, today=today)
check("ENVX $6.50 call rejected", result is None, f"got {result}")
print(f"       reason: {reason}")

# It fails on more than one gate; confirm the EDGE test rejects it too, with
# every tradability gate loosened. This is the load-bearing assertion: the
# contract must fail because it is not underpriced, not merely because its
# spread is wide. Market prices 15.0% vs a 10.97% median history -> 1.37.
loose = OptionScanConfig(max_spread_pct=99.0, min_delta=0.01, min_volume=0)
result2, reason2 = evaluate_candidate(envx_otm_call, loose, today=today)
check(
    "still rejected on the mismatch ratio alone",
    result2 is None and "mismatch ratio" in reason2,
    f"got {reason2}",
)
print(f"       reason: {reason2}")
check(
    "ENVX options are RICH vs history, not cheap",
    approx(mismatch_ratio(15.010449, historical_move_pct(envx_otm_call["historical_moves"])),
           1.368, 1e-3),
)

print()
print("a genuine mismatch DOES pass")
# Same structure, but the market prices a 6% move on a name that historically
# moves ~15%. That is the case worth surfacing.
good = dict(envx_otm_call)
good.update(
    {
        "symbol": "TEST",
        "atm_call_mid": 0.15,
        "atm_put_mid": 0.14,  # straddle 0.29 * 0.85 = 0.2465 -> 5.15% of 4.785
        # Hypothetical name that historically moves ~11% on earnings while
        # the market prices only ~5% -- the case worth surfacing.
        "historical_moves": [2.55, -8.36, -20.11, -20.23, -3.25, -13.58],
        "bid": 0.10,
        "ask": 0.11,
        "delta": 0.25,
        "volume": 50,
    }
)
res3, reason3 = evaluate_candidate(good, cfg, today=today)
check("genuine mismatch passes", res3 is not None, f"rejected: {reason3}")
if res3:
    check("ratio well below 1", res3["mismatch_ratio"] < 0.60, str(res3["mismatch_ratio"]))
    print(
        f"       expected {res3['expected_move_pct']:.1f}% vs history "
        f"{res3['historical_move_pct']:.1f}% -> ratio {res3['mismatch_ratio']:.2f}"
    )

print()
print("structural gates")
# Expiry BEFORE the catalyst can pay off -- the worst error this screen prevents.
early = dict(good)
early["expiration_date"] = "2026-08-12"  # pm earnings -> moves 8/13, too late
r, why = evaluate_candidate(early, cfg, today=today)
check("expiry before the move is rejected", r is None and "clear catalyst" in why, why)
print(f"       reason: {why}")

# Same contract, am earnings -> the 8/12 expiry now needs 8/13 anyway (buffer 1)
early_am = dict(early)
early_am["catalyst_timing"] = "am"
r, why = evaluate_candidate(early_am, cfg, today=today)
check("am earnings still needs the 1-day buffer", r is None, why)

# Even with the catalyst buffer at 0, a same-day expiry is 0DTE and is
# excluded on its own separate rule -- the buffer must not become a back
# door into 0DTE.
r, why = evaluate_candidate(
    early_am, OptionScanConfig(min_days_after_catalyst=0), today=today
)
check("buffer 0 still cannot open a 0DTE back door", r is None and "0DTE" in why, why)
print(f"       reason: {why}")

premium = dict(good)
premium["bid"], premium["ask"] = 1.55, 1.60  # $157.50/contract, tight spread
r, why = evaluate_candidate(premium, cfg, today=today)
check("premium cap enforced", r is None and "premium" in why, why)

illiquid = dict(good)
illiquid["open_interest"] = 5
r, why = evaluate_candidate(illiquid, cfg, today=today)
check("open interest floor enforced", r is None and "open interest" in why, why)

lotto = dict(good)
lotto["delta"] = 0.02
r, why = evaluate_candidate(lotto, cfg, today=today)
check("pure lottery ticket excluded by delta floor", r is None and "delta" in why, why)

# The 0.25 floor was chosen 2026-08-21 to resolve real drift: strategies.md
# claimed 0.30 while the code enforced 0.10. `good` sits exactly ON the floor
# at delta 0.25, so pin both sides -- a silent drift back to 0.10, or a bump
# to 0.30, now breaks a test instead of quietly changing what gets traded.
assert good["delta"] == 0.25, "fixture moved off the delta floor; update these tests"
r, why = evaluate_candidate(dict(good, delta=0.25), cfg, today=today)
check("delta exactly at the 0.25 floor is accepted", r is not None, why)
r, why = evaluate_candidate(dict(good, delta=0.24), cfg, today=today)
check("delta just below the floor (0.24) is rejected", r is None and "delta" in why, why)

thin = dict(good)
thin["historical_moves"] = [20.0]
r, why = evaluate_candidate(thin, cfg, today=today)
check("single historical move gives no base rate", r is None and "historical" in why, why)

print()
print("apply_filters_and_rank")
passed, rejected = apply_filters_and_rank([good, envx_otm_call, {"symbol": "X"}], cfg, today=today)
check("one passes", len(passed) == 1 and passed[0]["symbol"] == "TEST")
check("two rejected with reasons", len(rejected) == 2)
check("rejections name the symbol", all(r["symbol"] and r["reason"] for r in rejected))
check("non-dict input rejected", apply_filters_and_rank(["nope"], cfg)[1][0]["reason"] == "not a mapping")

# ranking: lower ratio first
a = dict(good, symbol="AAA", atm_call_mid=0.20, atm_put_mid=0.20)  # ratio ~0.65
b = dict(good, symbol="BBB", atm_call_mid=0.10, atm_put_mid=0.10)  # ratio ~0.32
passed, _ = apply_filters_and_rank([a, b], cfg, today=today)
check("ranked most-underpriced first", [p["symbol"] for p in passed] == ["BBB", "AAA"],
      str([p["symbol"] for p in passed]))
check("top_n honored", len(apply_filters_and_rank([a, b], OptionScanConfig(top_n=1), today=today)[0]) == 1)

print()
print("realized_volatility")
# Hand-verified independently via statistics.stdev on log returns, then
# annualized by sqrt(252) -- see the comment this value was computed with.
closes_15 = [10.00, 10.15, 9.98, 10.22, 10.05, 10.30, 10.18, 10.45, 10.20,
             10.55, 10.40, 10.60, 10.35, 10.70, 10.50]
check("15 closes -> ~36.7% annualized", approx(realized_volatility(closes_15), 0.3666110, 1e-5))
check("fewer than 10 closes rejected", realized_volatility(closes_15[:9]) is None)
check("empty rejected", realized_volatility([]) is None)
check("non-positive closes dropped, still too few", realized_volatility([10, -5, 10, 0, 10, 10, 10, 10, 10, 10]) is None)
# a flat/interpolated run (the WOLF failure mode) has zero variance -- this
# function does NOT detect that on its own; callers must discard
# interpolated=true bars before calling it. Documented, not silently fixed.
flat = [5.0] * 15
check("flat series -> ~0 vol (documented caller responsibility, not auto-fixed)",
      approx(realized_volatility(flat), 0.0, 1e-9))

print("iv_hv_ratio")
check("cheap: iv below hv", approx(iv_hv_ratio(0.30, 0.40), 0.75))
check("fair", approx(iv_hv_ratio(0.40, 0.40), 1.0))
check("rich: iv above hv", approx(iv_hv_ratio(0.60, 0.40), 1.5))
check("zero hv rejected", iv_hv_ratio(0.30, 0) is None)
check("negative iv rejected", iv_hv_ratio(-0.1, 0.40) is None)

print("iv_cheap_vs_multi_window_hv -- McMillan Ch. 39 Method 2 (IV < 0.8x every window)")
check(
    "cheap against all four windows -> True",
    iv_cheap_vs_multi_window_hv(0.20, 0.30, 0.30, 0.30, 0.30) is True,
)
check(
    "cheap against three windows but not the fourth (accelerating stock) -> False",
    iv_cheap_vs_multi_window_hv(0.20, 0.30, 0.30, 0.30, 0.24) is False,
)
check(
    "right at the 0.8x boundary on one window -> False (must be strictly below)",
    iv_cheap_vs_multi_window_hv(0.24, 0.30, 0.30, 0.30, 0.30) is False,
)
check(
    "custom threshold honored",
    iv_cheap_vs_multi_window_hv(0.28, 0.30, 0.30, 0.30, 0.30, threshold=0.95) is True,
)
check("missing window -> None", iv_cheap_vs_multi_window_hv(0.20, 0.30, 0.30, 0.30, None) is None)
check("zero window -> None", iv_cheap_vs_multi_window_hv(0.20, 0.30, 0.30, 0.30, 0) is None)
check("negative iv -> None", iv_cheap_vs_multi_window_hv(-0.1, 0.30, 0.30, 0.30, 0.30) is None)

print("catalyst_direction_score")
check("two bullish signals -> +10",
      approx(catalyst_direction_score("bullish", "accumulation", None), 10.0))
check("bullish + bearish -> 0",
      approx(catalyst_direction_score("bullish", "distribution", None), 0.0))
check("bull_pct 90 alone plus verdict -> positive",
      catalyst_direction_score("bullish", None, 90) > 5.0)
check("single signal rejected (needs >= 2)",
      catalyst_direction_score("bullish", None, None) is None)
check("no signals rejected", catalyst_direction_score(None, None, None) is None)
check("unrecognized verdict string dropped, not coerced to neutral",
      catalyst_direction_score("somewhat bullish i guess", "accumulation", 90) is not None)
check("bull_pct 50 (even split) -> 0 contribution",
      approx(catalyst_direction_score("neutral", None, 50), 0.0))
check("bull_pct clamped at extremes",
      approx(catalyst_direction_score("bullish", None, 100), 10.0))

print()
print("evaluate_soft_candidate -- structural + edge gates")
soft_cfg = SoftCatalystScanConfig()
today2 = dt.date(2026, 8, 17)

good_soft_call = {
    "symbol": "TEST2",
    "underlying_price": 20.00,
    "strike": 22.0,
    "type": "call",
    "expiration_date": "2026-09-25",  # ~39 days out from today2
    "bid": 0.45,
    "ask": 0.50,
    "iv": 0.30,
    "delta": 0.28,
    "open_interest": 500,
    "volume": 50,
    "daily_closes": closes_15,  # realized vol ~36.7%, iv 30% -> ratio ~0.82
    "ai_verdict": "bullish",
    "insider_trend": "accumulation",
    "stocktwits_bull_pct": 80,
    "ai_flag_score": 7,
    "notes": "synthetic -- exercises the pass path",
}
res, why = evaluate_soft_candidate(good_soft_call, soft_cfg, today=today2)
check("genuine soft mismatch passes", res is not None, why)
if res:
    # ai_verdict bullish (+10), insider accumulation (+10), bull_pct 80 (+6)
    # -- mean of all three usable signals, not just the first two.
    check("catalyst score ~8.67 (all three signals, mean)",
          approx(res["catalyst_score"], 8.6667, 1e-3))
    check("iv/hv ratio ~0.82", 0.75 < res["iv_hv_ratio"] < 0.90, str(res["iv_hv_ratio"]))

rich = dict(good_soft_call, iv=0.50)  # 0.50/0.3666 ~ 1.36, above the 0.90 cap
r, why = evaluate_soft_candidate(rich, soft_cfg, today=today2)
check("iv/hv ratio cap enforced", r is None and "iv/hv ratio" in why, why)

mismatched_direction = dict(good_soft_call, type="put")  # bullish score, put contract
r, why = evaluate_soft_candidate(mismatched_direction, soft_cfg, today=today2)
check("put contract rejected against a bullish score", r is None and "not bearish" in why, why)

weak_conviction = dict(good_soft_call, ai_verdict="neutral", insider_trend="neutral",
                        stocktwits_bull_pct=55)
r, why = evaluate_soft_candidate(weak_conviction, soft_cfg, today=today2)
check("weak conviction rejected", r is None and "conviction" in why, why)

low_flag = dict(good_soft_call, ai_flag_score=3)
r, why = evaluate_soft_candidate(low_flag, soft_cfg, today=today2)
check("flag score floor enforced", r is None and "flag score" in why, why)

too_soon = dict(good_soft_call, expiration_date="2026-08-20")  # 3 days out
r, why = evaluate_soft_candidate(too_soon, soft_cfg, today=today2)
check("min days-to-expiry enforced (no dated catalyst to time against)",
      r is None and "below min" in why, why)

too_far = dict(good_soft_call, expiration_date="2027-06-18")  # >90 days out
r, why = evaluate_soft_candidate(too_far, soft_cfg, today=today2)
check("max days-to-expiry enforced", r is None and "exceeds max" in why, why)

thin_signals = dict(good_soft_call, insider_trend=None, stocktwits_bull_pct=None)
r, why = evaluate_soft_candidate(thin_signals, soft_cfg, today=today2)
check("single directional signal rejected", r is None and "directional signals" in why, why)

print()
print("apply_soft_filters_and_rank")
cheaper = dict(good_soft_call, symbol="CHEAPER", iv=0.20)  # ratio ~0.55, better than good_soft_call's ~0.82
passed, rejected = apply_soft_filters_and_rank(
    [good_soft_call, rich, cheaper], soft_cfg, today=today2
)
check("two pass, one rejected on iv/hv", len(passed) == 2 and len(rejected) == 1)
check("ranked cheapest iv/hv first", [p["symbol"] for p in passed] == ["CHEAPER", "TEST2"],
      str([p["symbol"] for p in passed]))

print("decide_option_exit -- interim S7 exit rule (2026-08-19)")
check("holding, well inside all thresholds", decide_option_exit(1.00, 1.10, 20).exit_now is False)
check(
    "stop-loss at exactly -50% fires",
    decide_option_exit(1.00, 0.50, 20).kind == "stop",
)
check(
    "just above -50% (-49%) does not fire the stop",
    decide_option_exit(1.00, 0.51, 20).exit_now is False,
)
check(
    "profit-lock at exactly +100% (a double) fires",
    decide_option_exit(1.00, 2.00, 20).kind == "profit",
)
check(
    "just below a double (+99%) does not fire profit-lock",
    decide_option_exit(1.00, 1.99, 20).exit_now is False,
)
check(
    "time stop at exactly 5 days fires even flat P&L",
    decide_option_exit(1.00, 1.00, 5).kind == "time",
)
check("6 days does not trigger the time stop", decide_option_exit(1.00, 1.00, 6).exit_now is False)
check(
    "stop-loss takes priority over time stop when both would fire",
    decide_option_exit(1.00, 0.40, 2).kind == "stop",
)
check("zero entry premium rejected", decide_option_exit(0, 1.00, 20).exit_now is False)
check("negative entry premium rejected", decide_option_exit(-1, 1.00, 20).exit_now is False)
check("negative current premium rejected", decide_option_exit(1.00, -0.1, 20).exit_now is False)
check("negative dte rejected", decide_option_exit(1.00, 1.00, -1).exit_now is False)
check(
    "custom thresholds honored",
    decide_option_exit(1.00, 0.70, 20, stop_loss_pct=25.0).kind == "stop",
)

print()
if failures:
    print(f"{len(failures)} FAILURE(S): {failures}")
    raise SystemExit(1)
print("all tests passed")
