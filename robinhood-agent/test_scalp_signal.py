"""Tests for scalp_signal.py.  Run: python3 test_scalp_signal.py

The load-bearing tests are the two that replay REAL 2026-08-17 IPST minute
bars: the 10:57 bar (which preceded the user's +23.9% trade) must fire, and
the 10:31 bar (which preceded the -5.6% loser, entered one bar after the
surge had passed) must NOT. A module that cannot tell those two apart has
learned nothing from the day it was built from.
"""

from __future__ import annotations

from scalp_signal import (
    Bar,
    decide_exit,
    detect_entry,
    surge_ratio,
    bar_return_pct,
    close_position,
    to_bars,
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


def flat(n: int, vol: float = 1000.0, price: float = 10.0) -> list[Bar]:
    """n quiet baseline bars."""
    return [Bar(o=price, h=price * 1.001, l=price * 0.999, c=price, v=vol) for _ in range(n)]


print("to_bars -- fails closed on unusable input")
check("interpolated bar dropped",
      to_bars([{"open_price": 1, "high_price": 1, "low_price": 1,
                "close_price": 1, "volume": 5, "interpolated": True}]) == [])
check("zero-volume bar dropped",
      to_bars([{"open_price": 1, "high_price": 1, "low_price": 1,
                "close_price": 1, "volume": 0}]) == [])
check("missing field dropped",
      to_bars([{"open_price": 1, "high_price": 1, "low_price": 1}]) == [])
check("high<low dropped",
      to_bars([{"open_price": 1, "high_price": 0.5, "low_price": 1,
                "close_price": 1, "volume": 5}]) == [])
check("good bar kept",
      len(to_bars([{"open_price": 1, "high_price": 2, "low_price": 0.9,
                    "close_price": 1.5, "volume": 5}])) == 1)

print("primitives")
b = Bar(o=10.0, h=11.0, l=9.5, c=10.8, v=5000)
check("bar_return_pct", approx(bar_return_pct(b), 8.0))
check("close_position ~0.867", approx(close_position(b), (10.8 - 9.5) / 1.5, 1e-9))
check("close_position None on zero range", close_position(Bar(5, 5, 5, 5, 10)) is None)
bars = flat(20) + [Bar(o=10, h=10.5, l=10, c=10.4, v=4000)]
check("surge_ratio 4x", approx(surge_ratio(bars), 4.0))
check("surge_ratio None without history", surge_ratio(flat(5)) is None)

print()
print("detect_entry -- the negative result is enforced, not just documented")
# Volume surge with NO price response must be reported as a non-signal.
quiet_surge = flat(20) + [Bar(o=10.0, h=10.05, l=9.95, c=10.0, v=10000)]
sig = detect_entry(quiet_surge)
check("10x volume with a flat bar does NOT fire", not sig.fired, sig.reason)
check("  ...and says why", "without a price response" in sig.reason, sig.reason)

# Price move with no volume confirmation also must not fire.
lonely_move = flat(20) + [Bar(o=10.0, h=10.4, l=10.0, c=10.35, v=1200)]
sig = detect_entry(lonely_move)
check("+3.5% bar on 1.2x volume does NOT fire", not sig.fired, sig.reason)
check("  ...and says why", "unconfirmed" in sig.reason, sig.reason)

# Both together -> fires.
both = flat(20) + [Bar(o=10.0, h=10.4, l=10.0, c=10.35, v=4000)]
sig = detect_entry(both)
check("surge + move fires", sig.fired, sig.reason)
check("  stop is 2% under entry", approx(sig.stop_price, 10.35 * 0.98, 1e-9))
check("  entry hint is the signal bar close", approx(sig.entry_hint, 10.35))
check("  confidence names the WETO out-of-sample check",
      "WETO" in sig.confidence and "-4.4%" in sig.confidence)

check("insufficient history does not fire", not detect_entry(flat(5)).fired)
check("down bar does not fire",
      not detect_entry(flat(20) + [Bar(o=10, h=10.1, l=9.0, c=9.2, v=9000)]).fired)

print()
print("REGRESSION -- real IPST bars, 2026-08-17")
# Real volumes from get_equity_historicals, 10:37-10:57 ET, in order.
# Trailing median of the 20 bars before 10:57 is 62,551*... computed live:
# the 10:57 bar (vol 251,916, open 7.475 -> close 7.685, +2.81%) is the one
# the user bought into at 7.7174 and sold 2m08s later at 9.5654 (+23.9%).
ipst_vols_before_1057 = [
    79361, 50366, 27008, 95763, 89054, 86295, 45680, 36730, 39176, 33016,
    39313, 128761, 163110, 96699, 154494, 96697, 76606, 64846, 140137, 62551,
]
hist = [Bar(o=7.3, h=7.4, l=7.2, c=7.3, v=v) for v in ipst_vols_before_1057]
bar_1057 = Bar(o=7.475, h=7.750, l=7.4437, c=7.685, v=251916)
sig = detect_entry(hist + [bar_1057])
check("IPST 10:57 surge bar FIRES", sig.fired, sig.reason)
if sig.fired:
    print(f"       {sig.reason}")
    check("  surge ~3.3x", 3.0 <= sig.surge <= 3.6, f"{sig.surge}")
    check("  bar return ~+2.8%", 2.5 <= sig.bar_return <= 3.1, f"{sig.bar_return}")

# The loser: user bought at 10:31, one bar AFTER the 10:30 surge. The 10:31
# bar itself was 149,480 on a falling close (7.6338 -> 7.58) -- must not fire.
vols_before_1031 = [
    45819, 54565, 117859, 170878, 147059, 161768, 111651, 368036,
    79361, 50366, 27008, 95763, 89054, 86295, 45680, 36730, 39176, 33016,
    39313, 128761,
]
hist2 = [Bar(o=7.3, h=7.4, l=7.2, c=7.3, v=v) for v in vols_before_1031]
bar_1031 = Bar(o=7.6338, h=7.660, l=7.4001, c=7.580, v=149480)
sig2 = detect_entry(hist2 + [bar_1031])
check("IPST 10:31 (the -5.6% loser's bar) does NOT fire", not sig2.fired, sig2.reason)
print(f"       {sig2.reason}")

print()
print("decide_exit -- no FIXED profit target, but a profit-lock trail")
entry = 10.0
check("no bars yet -> hold", not decide_exit(entry, []).exit_now)

d = decide_exit(entry, [Bar(o=10, h=10.1, l=9.75, c=9.8, v=100)])
check("hard stop fires on the low", d.exit_now and d.kind == "stop", d.reason)

d = decide_exit(entry, [Bar(o=10, h=10.3, l=9.95, c=10.25, v=100)])
check("first bar up -> hold", not d.exit_now, d.reason)

# close below PRIOR bar's low -> structure broken. Kept under the +5%
# profit-lock trigger so this isolates the trail rule specifically.
d = decide_exit(entry, [
    Bar(o=10, h=10.3, l=10.0, c=10.2, v=100),
    Bar(o=10.2, h=10.25, l=9.9, c=9.95, v=100),
])
check("trail fires on close < prior low", d.exit_now and d.kind == "trail", d.reason)

# an ordinary pullback that holds above prior low, and stays under the
# profit-lock trigger, must NOT exit
d = decide_exit(entry, [
    Bar(o=10, h=10.3, l=10.0, c=10.2, v=100),
    Bar(o=10.2, h=10.3, l=10.05, c=10.15, v=100),
])
check("ordinary pullback does NOT exit (this is what lets winners run)",
      not d.exit_now, d.reason)

# a big winner must be allowed to keep running -- no target anywhere
running = [Bar(o=10 + i, h=11 + i, l=9.9 + i, c=10.9 + i, v=100) for i in range(6)]
d = decide_exit(entry, running)
check("+50% and still holding (no profit target exists)", not d.exit_now, d.reason)

# time stop
long_hold = [Bar(o=10, h=10.2, l=9.95, c=10.05, v=100) for _ in range(15)]
d = decide_exit(entry, long_hold)
check("time stop fires at max_hold", d.exit_now and d.kind == "time", d.reason)

check("stop takes priority over time",
      decide_exit(entry, [Bar(o=10, h=10.1, l=9.7, c=9.75, v=100)] * 15).kind == "stop")

print()
print("decide_exit -- profit-lock trail (2026-08-18, user-requested)")

# peak never reaches +5% -> profit lock does not arm, even on a pullback
d = decide_exit(entry, [
    Bar(o=10, h=10.3, l=10.2, c=10.25, v=100),   # peak +3%
    Bar(o=10.25, h=10.28, l=10.05, c=10.1, v=100),  # pulls back, but never armed
])
check("pullback below +5% peak does NOT trigger profit lock",
      not d.exit_now or d.kind != "profit", d.reason)

# peak reaches +5%, then pulls back 2%+ from that peak -> profit lock fires
d = decide_exit(entry, [
    Bar(o=10, h=10.6, l=10.4, c=10.55, v=100),   # peak +6%, arms
    Bar(o=10.55, h=10.58, l=10.2, c=10.35, v=100),  # closes ~2.4% off the $10.6 peak
])
check("profit lock fires on pullback from an armed peak",
      d.exit_now and d.kind == "profit", d.reason)
check("  ...and the reason cites the real peak, not the entry",
      "peak +6.00%" in d.reason, d.reason)

# armed, but pullback stays under the trail distance -> keep holding
d = decide_exit(entry, [
    Bar(o=10, h=10.6, l=10.4, c=10.55, v=100),   # peak +6%, arms
    Bar(o=10.55, h=10.57, l=10.45, c=10.5, v=100),  # only ~0.9% off the peak
])
check("small pullback under the trail distance does NOT exit",
      not d.exit_now, d.reason)

# THE POINT: a trade that keeps making new highs keeps running past +5%,
# same as before -- profit-lock chases the peak, it does not cap it.
still_running = [
    Bar(o=10, h=10.6, l=10.4, c=10.55, v=100),    # peak +6%, arms
    Bar(o=10.55, h=11.5, l=10.5, c=11.4, v=100),  # new high, +15%
    Bar(o=11.4, h=12.5, l=11.3, c=12.4, v=100),   # new high again, +25%
]
d = decide_exit(entry, still_running)
check("still making new highs past +5% -> keeps running, no cap",
      not d.exit_now, d.reason)

# hard stop still wins even if the trade was once up past the profit trigger
d = decide_exit(entry, [
    Bar(o=10, h=10.6, l=10.4, c=10.55, v=100),   # peak +6%, arms
    Bar(o=10.55, h=10.55, l=9.7, c=9.75, v=100), # crashes through the -2% stop
])
check("hard stop takes priority even after profit-lock armed",
      d.exit_now and d.kind == "stop", d.reason)

print()
print("OUT-OF-SAMPLE -- real WETO bars, 2026-08-17, NOT one of the 5 symbols")
print("the thresholds were derived from. This is a negative result and it")
print("is pinned here on purpose so the module cannot silently drift into")
print("being oversold later. See scalp_signal.py's module docstring.")
# 21 real one-minute bars ending 16:09 UTC (12:09 ET), pulled from
# get_equity_historicals and transcribed by script (not by eye -- Rule 0).
# The last bar is a genuine surge+move signal bar.
weto_window = [
    dict(o=16.95, h=16.95, l=16.7, c=16.7181, v=2504),
    dict(o=16.76, h=16.9999, l=16.76, c=16.7602, v=2696),
    dict(o=16.77, h=16.9188, l=16.71, c=16.81, v=8694),
    dict(o=16.9163, h=17.25, l=16.8219, c=17.185, v=28327),
    dict(o=17.2364, h=17.2364, l=16.79, c=16.9214, v=9229),
    dict(o=16.9294, h=17.0, l=16.52, c=16.7058, v=26697),
    dict(o=16.72, h=16.7999, l=16.701, c=16.7999, v=3115),
    dict(o=16.701, h=16.8, l=16.6632, c=16.7, v=2664),
    dict(o=16.83, h=16.83, l=16.55, c=16.56, v=6492),
    dict(o=16.59, h=16.69, l=16.3, c=16.51, v=10118),
    dict(o=16.481, h=16.6, l=16.37, c=16.48, v=8771),
    dict(o=16.59, h=16.59, l=16.02, c=16.1155, v=8084),
    dict(o=16.105, h=16.2839, l=16.05, c=16.25, v=8692),
    dict(o=16.25, h=16.38, l=16.16, c=16.2535, v=5807),
    dict(o=16.2714, h=16.4699, l=16.2714, c=16.37, v=5145),
    dict(o=16.4, h=16.4, l=16.2, c=16.29, v=4006),
    dict(o=16.2771, h=16.34, l=16.2, c=16.22, v=5933),
    dict(o=16.2267, h=16.3399, l=16.14, c=16.2501, v=9270),
    dict(o=16.36, h=16.41, l=16.165, c=16.205, v=6499),
    dict(o=16.2086, h=16.66, l=16.1, c=16.4914, v=8295),
    dict(o=16.58, h=17.09, l=16.435, c=17.0405, v=25774),
]
weto_bars = to_bars([
    {"open_price": b["o"], "high_price": b["h"], "low_price": b["l"],
     "close_price": b["c"], "volume": b["v"]}
    for b in weto_window
])
sig = detect_entry(weto_bars)
check("WETO bar (17.04, vol 25774, 3.5x/+2.8%) DOES fire -- it is a real "
      "volume-confirmed breakout, same as IPST's", sig.fired, sig.reason)

# The next two real bars: price stalls and rolls over into the stop.
weto_followup = to_bars([
    dict(open_price=16.965, high_price=17.0, low_price=16.6601, close_price=16.855, volume=17472),
    dict(open_price=16.7569, high_price=16.95, low_price=16.75, close_price=16.7844, volume=16731),
])
entry = sig.entry_hint
d1 = decide_exit(entry, weto_followup[:1])
check("...but the very next real bar hits the hard stop (this is the "
      "honest outcome for 8 of WETO's 11 signals that day)",
      d1.exit_now and d1.kind == "stop", d1.reason)
if d1.exit_now:
    pnl = (weto_followup[0].c - entry) / entry * 100
    print(f"       real outcome on this signal: {pnl:+.2f}%")

print()
if failures:
    print(f"{len(failures)} FAILURE(S): {failures}")
    raise SystemExit(1)
print("all tests passed")
