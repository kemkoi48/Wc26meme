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
    apply_filters_and_rank,
    as_pct_of,
    catalyst_effective_date,
    evaluate_candidate,
    expected_move_from_iv,
    expected_move_from_straddle,
    historical_move_pct,
    mid_price,
    mismatch_ratio,
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
premium["bid"], premium["ask"] = 0.85, 0.90  # $90/contract, tight spread
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
if failures:
    print(f"{len(failures)} FAILURE(S): {failures}")
    raise SystemExit(1)
print("all tests passed")
