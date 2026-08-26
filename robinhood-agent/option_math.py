"""Option mispricing math -- the S7 "cheap contract before a catalyst" screen.

The question this answers: a contract costs $0.06. Is it cheap because the
market has not priced in a catalyst (an edge), or cheap because it is far
out-of-the-money and implied volatility is ALREADY elevated for a known
event (no edge, just low delta)? Those look identical by price. Only the
volatility number separates them.

  expected move  =  what the option market is currently pricing in
  historical move =  what this stock actually does on comparable events
  mismatch ratio  =  expected / historical

A ratio below 1.0 means the market is pricing LESS movement than this name
has historically delivered -- the only version of "cheap" that is an edge.
A ratio at or above 1.0 means implied volatility is doing its job and the
low dollar price is just low delta.

Worked live example that motivated this module (ENVX, 2026-08-12, earnings
that evening): the $6.50 call quoted $0.04 x $0.07 -- textbook "cheap
contract, real catalyst hours away" -- but carried 305% IV, and the ATM
straddle priced a ~15% move by Friday. Nothing was mispriced; the market
had already paid for an earnings-sized swing. See strategies.md S7.

Everything here is a PURE FUNCTION over numbers. No network, no SDK import,
so it is directly unit-testable -- same posture as regime.py, and the
reason the math does not live inside option_scanner.py.

Fail-closed throughout: malformed, missing, or nonsensical input returns
None (an unusable reading) rather than a number that looks authoritative.
Callers must treat None as exclusion, never as "assume fine".
"""

from __future__ import annotations

import datetime as dt
import math
import statistics
from dataclasses import dataclass
from typing import Any, Optional, Sequence

# The ATM straddle overprices the expected move slightly, because it carries
# time value beyond the pure expected range. ~0.85 is the standard haircut.
STRADDLE_TO_EXPECTED_MOVE = 0.85

DAYS_PER_YEAR = 365.0


def _as_float(value: Any) -> Optional[float]:
    """Coerce to float, or None. Rejects bools (True would become 1.0) and
    non-finite values, both of which would otherwise poison downstream math."""
    if isinstance(value, bool):
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    if out != out or out in (float("inf"), float("-inf")):  # NaN / inf
        return None
    return out


def _as_date(value: Any) -> Optional[dt.date]:
    """Parse a YYYY-MM-DD string (or pass through a date). None if unusable."""
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if not isinstance(value, str):
        return None
    try:
        return dt.date.fromisoformat(value.strip()[:10])
    except ValueError:
        return None


def mid_price(bid: Any, ask: Any) -> Optional[float]:
    """Midpoint of a quote. None when either side is missing or crossed.

    A zero bid is real and common on far-OTM contracts -- it means nobody is
    willing to buy it at any price, which is exactly the untradable condition
    worth excluding, so it is rejected rather than treated as $0.00.
    """
    b, a = _as_float(bid), _as_float(ask)
    if b is None or a is None:
        return None
    if b <= 0 or a <= 0 or a < b:
        return None
    return (a + b) / 2.0


def spread_pct(bid: Any, ask: Any) -> Optional[float]:
    """Quoted spread as a percent of the midpoint.

    Cheap options structurally show large PERCENTAGE spreads: the $0.01
    minimum tick is 20% of a $0.05 midpoint before anyone is being greedy.
    That is a genuine round-trip cost the trader eats, not a data artifact,
    which is why this is not papered over with an absolute-dollar escape
    hatch. It does mean the threshold for options has to be far looser than
    the 1% used for stocks in momentum_scanner.py -- comparing the two
    numbers directly is a category error.
    """
    b, a = _as_float(bid), _as_float(ask)
    m = mid_price(bid, ask)
    if m is None or b is None or a is None:
        return None
    return (a - b) / m * 100.0


def expected_move_from_straddle(
    call_mid: Any, put_mid: Any, multiplier: float = STRADDLE_TO_EXPECTED_MOVE
) -> Optional[float]:
    """Expected move in DOLLARS, from the at-the-money straddle price.

    This is the market-based read: what it costs to bet on a move in either
    direction, haircut for the straddle's extra time value.
    """
    c, p = _as_float(call_mid), _as_float(put_mid)
    mult = _as_float(multiplier)
    if c is None or p is None or mult is None:
        return None
    if c <= 0 or p <= 0 or mult <= 0:
        return None
    return (c + p) * mult


def expected_move_from_iv(
    underlying_price: Any, iv: Any, days_to_expiry: Any
) -> Optional[float]:
    """Expected move in DOLLARS, from implied volatility.

    price x IV x sqrt(DTE / 365). IV is annualized, hence the time scaling.
    Independent of the straddle calculation -- when the two disagree badly,
    that is a data-quality signal worth surfacing, not averaging away.

    `iv` is a decimal fraction (2.93 == 293%), matching what the Robinhood
    option quote returns.
    """
    price = _as_float(underlying_price)
    vol = _as_float(iv)
    dte = _as_float(days_to_expiry)
    if price is None or vol is None or dte is None:
        return None
    if price <= 0 or vol <= 0 or dte <= 0:
        return None
    return price * vol * ((dte / DAYS_PER_YEAR) ** 0.5)


def as_pct_of(move_usd: Any, underlying_price: Any) -> Optional[float]:
    """Convert a dollar move to a percent of the underlying price."""
    move = _as_float(move_usd)
    price = _as_float(underlying_price)
    if move is None or price is None or price <= 0 or move < 0:
        return None
    return move / price * 100.0


def historical_move_pct(moves: Sequence[Any]) -> Optional[float]:
    """Median ABSOLUTE percent move across past comparable catalyst events.

    Median rather than mean: one outlier gap (a buyout rumor, a halt) would
    drag a mean upward and make every option look underpriced by comparison,
    which is the exact false positive this whole module exists to prevent.

    Direction is discarded (abs) because the expected move is direction-less
    too -- the straddle prices magnitude, not sign. Requires at least two
    usable observations; a single past earnings move is an anecdote, and
    treating it as a base rate is how a screen manufactures false confidence.
    """
    if not moves:
        return None
    usable = []
    for m in moves:
        v = _as_float(m)
        if v is None:
            continue
        usable.append(abs(v))
    if len(usable) < 2:
        return None
    return statistics.median(usable)


def mismatch_ratio(
    expected_move_pct: Any, historical_move_pct_value: Any
) -> Optional[float]:
    """expected / historical. THE metric this module exists to produce.

      < 1.0  options price LESS movement than this name historically makes
             -> the genuine "cheap" case, worth a look
      ~ 1.0  market is pricing roughly what history suggests -> no edge
      > 1.0  market is pricing MORE than history -> options are rich, and a
             correct directional call can still lose to the post-event IV
             collapse

    Note the asymmetry: a low ratio is necessary but nowhere near sufficient.
    It says the option is cheap relative to this stock's own past behaviour;
    it says nothing about direction, and nothing about whether the upcoming
    catalyst resembles the past ones the historical figure was built from.
    """
    exp = _as_float(expected_move_pct)
    hist = _as_float(historical_move_pct_value)
    if exp is None or hist is None:
        return None
    if exp < 0 or hist <= 0:
        return None
    return exp / hist


def catalyst_effective_date(
    catalyst_date: Any, timing: Any = None
) -> Optional[dt.date]:
    """The first date the underlying can actually move on the catalyst.

    Earnings released AFTER the close ('pm') move the stock the NEXT session,
    so a contract expiring on the report date itself expires before the move
    it was bought for. This function encodes that off-by-one, which is the
    single easiest way to buy a structurally worthless option.

    Unknown/missing timing is treated as 'pm' -- the conservative reading,
    since assuming 'am' would wave through contracts that expire too early.

    Weekends are NOT adjusted for here: expiry comparison is against a real
    expiration date, which is always a trading day, so a Saturday effective
    date still correctly excludes a Friday expiry.
    """
    d = _as_date(catalyst_date)
    if d is None:
        return None
    t = str(timing).strip().lower() if timing is not None else ""
    if t == "am":
        return d
    return d + dt.timedelta(days=1)


def realized_volatility(
    daily_closes: Sequence[Any], trading_days_per_year: float = 252.0
) -> Optional[float]:
    """Annualized realized volatility, as a decimal fraction (0.42 == 42%),
    from close-to-close log returns. Same units as the `iv` field elsewhere
    in this module (Robinhood's option quote: 2.93 == 293%), so the two are
    directly comparable via iv_hv_ratio() below.

    Requires at least 10 usable closes (two trading weeks) -- fewer makes the
    stdev estimate too noisy to trust, same spirit as historical_move_pct's
    two-observation floor. Non-positive or unparseable closes are dropped
    rather than crashing; a gap-filled/interpolated bar (flat price, the WOLF
    failure mode from sources.md) silently produces a log return of exactly
    0.0 and is NOT specially detected here -- callers MUST discard
    interpolated=true bars before passing closes in, the same discipline
    option_scanner.py's SYSTEM_PROMPT already requires for historical_moves.
    """
    if not daily_closes:
        return None
    usable: list[float] = []
    for c in daily_closes:
        v = _as_float(c)
        if v is None or v <= 0:
            continue
        usable.append(v)
    if len(usable) < 10:
        return None
    log_returns = []
    for i in range(1, len(usable)):
        prev, cur = usable[i - 1], usable[i]
        if prev <= 0 or cur <= 0:
            continue
        log_returns.append(math.log(cur / prev))
    if len(log_returns) < 9:
        return None
    daily_stdev = statistics.stdev(log_returns)
    years = _as_float(trading_days_per_year)
    if years is None or years <= 0:
        return None
    return daily_stdev * (years ** 0.5)


def iv_hv_ratio(implied_vol: Any, realized_vol: Any) -> Optional[float]:
    """implied / realized. THE edge test for catalysts with no single trigger
    date (insider buying, a sentiment spike, general hype) -- mismatch_ratio's
    counterpart for that case, same shape and same interpretation:

      < 1.0  the option market is pricing LESS movement than this stock has
             actually been making lately -- the interesting case, especially
             paired with a real directional signal (see catalyst_direction_score)
      ~ 1.0  IV is roughly tracking realized movement -- no edge
      > 1.0  IV already prices more movement than the stock has recently
             delivered -- no edge from volatility alone, regardless of how
             good the story sounds

    Looser to trust than mismatch_ratio: historical_move_pct is built from
    actual reactions to actual comparable events, while realized_vol is a
    blunter instrument (all recent price action, not isolated to any event).
    A soft-catalyst config should demand a wider margin than 0.85 as a result
    -- see SoftCatalystScanConfig.max_iv_hv_ratio.
    """
    iv = _as_float(implied_vol)
    hv = _as_float(realized_vol)
    if iv is None or hv is None:
        return None
    if iv < 0 or hv <= 0:
        return None
    return iv / hv


def iv_cheap_vs_multi_window_hv(
    implied_vol: Any,
    hv_10: Any,
    hv_20: Any,
    hv_50: Any,
    hv_100: Any,
    threshold: float = 0.8,
) -> Optional[bool]:
    """McMillan's Method 2 for judging cheap IV ("Options as a Strategic
    Investment", 5th ed., Ch. 39 -- read in full 2026-08-19, see
    mcmillan/07_volatility.md), quoted close to verbatim: "One should ensure
    that implied volatility is significantly different from all of the
    pertinent historical volatilities. For example, one might require that
    implied volatility is less than 80% of each of the 10-, 20-, 50-, and
    100-day historical volatility calculations."

    This is a MULTI-window AND -- IV must clear the 0.8x bar against every
    one of the four windows, not just one -- because a stock whose vol
    regime is actively shifting (accelerating or decelerating) can show a
    misleadingly cheap reading against a single stale window. iv_hv_ratio()
    above compares against exactly one realized-vol reading; this is the
    stricter, book-sourced version for when multiple windows are available.

    McMillan rates this Method 2 as inferior to his preferred Method 1 (IV
    PERCENTILE against the underlying's own ~600-day trailing history) --
    that method is NOT implemented here yet because it needs a real
    multi-year implied-volatility time series per symbol, which has not
    been verified as available from this account's data sources. Treat this
    function as a documented stand-in, not the book's actual first choice.

    Returns None (unusable, not "pass") if any input is missing/unusable --
    a partial multi-window read is not the same claim as this rule makes."""
    iv = _as_float(implied_vol)
    windows = [_as_float(hv_10), _as_float(hv_20), _as_float(hv_50), _as_float(hv_100)]
    if iv is None or iv < 0 or any(w is None or w <= 0 for w in windows):
        return None
    t = _as_float(threshold)
    if t is None or t <= 0:
        return None
    return all(iv < t * w for w in windows)


def catalyst_direction_score(
    ai_verdict: Any = None,
    insider_trend: Any = None,
    stocktwits_bull_pct: Any = None,
) -> Optional[float]:
    """Signed composite catalyst conviction, -10 (strongly bearish) to +10
    (strongly bullish), from up to three independent read-only signals:

      ai_verdict           Stocklake get_stock_research / get_stock ai_verdict
                            "bullish" -> +10, "neutral" -> 0, "bearish" -> -10
      insider_trend        Stocklake sentiment.insider_trend
                            "accumulation" -> +10, "neutral" -> 0,
                            "distribution" -> -10
      stocktwits_bull_pct  Stocktwits get_symbol_pulse sentiment.bull_pct,
                            0-100 -> linearly mapped so 50 (even split) is 0,
                            100 is +10, 0 is -10

    Equal-weighted mean of whichever signals are usable -- not a tuned/opaque
    weighting, because the module's whole point is that a human can check the
    number by hand. Requires at least 2 of the 3 -- one reading is an
    anecdote, same floor as historical_move_pct. An unrecognized string for
    ai_verdict or insider_trend is dropped as unusable, not coerced to 0
    ("neutral" must be said explicitly, not assumed from garbage input).

    This is a NECESSARY signal, not sufficient: a high score means multiple
    independent sources point the same direction, not that the direction is
    correct. Cross-check against get_stock_research's own tape/sentiment read
    before trusting a get_signals-only bullish call -- see CLAUDE.md's MLTX
    lesson (2026-08-13): a bullish headline the tape is rejecting is a trap.
    """
    signals: list[float] = []

    v = str(ai_verdict).strip().lower() if ai_verdict is not None else ""
    if v == "bullish":
        signals.append(10.0)
    elif v == "neutral":
        signals.append(0.0)
    elif v == "bearish":
        signals.append(-10.0)

    t = str(insider_trend).strip().lower() if insider_trend is not None else ""
    if t == "accumulation":
        signals.append(10.0)
    elif t == "neutral":
        signals.append(0.0)
    elif t == "distribution":
        signals.append(-10.0)

    bp = _as_float(stocktwits_bull_pct)
    if bp is not None and 0.0 <= bp <= 100.0:
        signals.append(max(-10.0, min(10.0, (bp - 50.0) / 5.0)))

    if len(signals) < 2:
        return None
    return statistics.mean(signals)


@dataclass(frozen=True)
class SoftCatalystScanConfig:
    """Thresholds for apply_soft_filters_and_rank -- the counterpart to
    OptionScanConfig for catalysts with no single dated trigger (insider
    accumulation, a sentiment spike, general hype/momentum with no scheduled
    event). Structural/tradability gates are shared in spirit with
    OptionScanConfig; the edge test and the days-to-expiry band differ,
    because there is no catalyst date to time an expiry against."""

    # Raised 2026-08-19 -> 2026-08-25 ($50 -> $150), user's explicit
    # instruction after 12/12 real checks (BMNR, AAOI x2, BABA, OXY) were
    # structurally rejected at $50: on any underlying trading much above
    # ~$50-60/share, $50 cannot reach the 0.30 delta floor at all. $150
    # was chosen because today's real rejections (AAOI $100p at $125/ct,
    # OXY $59p at $121.50/ct) needed roughly that much. Still a hard cap,
    # not a target -- same posture as the original $50.
    max_premium_usd: float = 150.0
    max_spread_pct: float = 15.0
    min_open_interest: float = 100.0
    min_volume: float = 10.0
    min_delta: float = 0.25
    max_delta: float = 0.55
    # Looser than OptionScanConfig's 0.85 -- see iv_hv_ratio()'s docstring on
    # why realized-vol-vs-IV is a blunter instrument than a real historical
    # event sample and needs a wider margin to trust.
    max_iv_hv_ratio: float = 0.90
    # Absolute value of catalyst_direction_score. 5.0 requires roughly
    # "two of two signals agree at moderate-or-better conviction" -- not a
    # coin flip, not unanimous-and-extreme either.
    min_catalyst_score: float = 5.0
    # Stocklake ai_flag_score floor (0-10 scale) -- a "worth attention" gate
    # independent of direction, mirroring Stocklake's own high_conviction
    # preset (flag_score >= 7). Set slightly looser here since flag_score and
    # catalyst_direction_score are cross-checking different things.
    min_flag_score: float = 6.0
    # No catalyst date to time against, so the floor exists instead to keep
    # premium from being pure theta-bleed on a thesis that needs weeks to
    # play out, not days.
    min_days_to_expiry: int = 10
    max_days_to_expiry: int = 90
    min_underlying_price: float = 2.0
    max_underlying_price: float = 100.0
    top_n: int = 10


def evaluate_soft_candidate(
    c: dict[str, Any], cfg: SoftCatalystScanConfig, today: Optional[dt.date] = None
) -> tuple[Optional[dict[str, Any]], str]:
    """Evaluate ONE candidate contract against the soft-catalyst edge test.
    Mirrors evaluate_candidate's shape and fail-closed posture; see that
    function's docstring for the general philosophy. Returns (result, reason)
    with the same convention: result is None with a named reason on
    rejection, never a silent drop.
    """
    today = today or dt.date.today()

    symbol = str(c.get("symbol", "")).upper().strip()
    if not symbol:
        return None, "missing symbol"

    underlying = _as_float(c.get("underlying_price"))
    if underlying is None or underlying <= 0:
        return None, "unusable underlying price"
    if not (cfg.min_underlying_price <= underlying <= cfg.max_underlying_price):
        return None, f"underlying ${underlying:.2f} outside price band"

    expiry = _as_date(c.get("expiration_date"))
    if expiry is None:
        return None, "missing or malformed expiration date"
    days_to_expiry = (expiry - today).days
    if days_to_expiry < 0:
        return None, f"expiry {expiry} has already passed"
    if days_to_expiry < cfg.min_days_to_expiry:
        return None, (
            f"{days_to_expiry}d to expiry below min {cfg.min_days_to_expiry}d -- "
            "no dated catalyst to time against; this needs room to work"
        )
    if days_to_expiry > cfg.max_days_to_expiry:
        return None, f"{days_to_expiry}d to expiry exceeds max {cfg.max_days_to_expiry}d"

    # --- tradability (identical gates to evaluate_candidate) ---
    bid, ask = c.get("bid"), c.get("ask")
    contract_mid = mid_price(bid, ask)
    if contract_mid is None:
        return None, "no usable two-sided quote on the contract"
    sp = spread_pct(bid, ask)
    if sp is None:
        return None, "spread not computable"
    if sp > cfg.max_spread_pct:
        return None, f"spread {sp:.1f}% exceeds max {cfg.max_spread_pct:.1f}%"

    ask_f = _as_float(ask)
    if ask_f is None:
        return None, "unusable ask"
    premium_usd = ask_f * 100.0
    if premium_usd > cfg.max_premium_usd:
        return None, (
            f"premium ${premium_usd:.0f}/contract exceeds max "
            f"${cfg.max_premium_usd:.0f}"
        )

    oi = _as_float(c.get("open_interest"))
    vol = _as_float(c.get("volume"))
    if oi is None or vol is None:
        return None, "missing open interest or volume"
    if oi < cfg.min_open_interest:
        return None, f"open interest {oi:.0f} below min {cfg.min_open_interest:.0f}"
    if vol < cfg.min_volume:
        return None, f"volume {vol:.0f} below min {cfg.min_volume:.0f}"

    delta = _as_float(c.get("delta"))
    if delta is None:
        return None, "missing delta"
    abs_delta = abs(delta)
    if not (cfg.min_delta <= abs_delta <= cfg.max_delta):
        return None, (
            f"|delta| {abs_delta:.2f} outside band "
            f"[{cfg.min_delta:.2f}, {cfg.max_delta:.2f}]"
        )

    # --- direction + conviction ---
    score = catalyst_direction_score(
        c.get("ai_verdict"), c.get("insider_trend"), c.get("stocktwits_bull_pct")
    )
    if score is None:
        return None, "fewer than 2 usable directional signals"
    if abs(score) < cfg.min_catalyst_score:
        return None, (
            f"catalyst score {score:+.1f} below min conviction "
            f"+/-{cfg.min_catalyst_score:.1f}"
        )
    contract_type = str(c.get("type", "")).lower().strip()
    if contract_type == "call" and score <= 0:
        return None, f"call contract but catalyst score is {score:+.1f} (not bullish)"
    if contract_type == "put" and score >= 0:
        return None, f"put contract but catalyst score is {score:+.1f} (not bearish)"
    if contract_type not in ("call", "put"):
        return None, f"unrecognized contract type {contract_type!r}"

    flag_score = _as_float(c.get("ai_flag_score"))
    if flag_score is None:
        return None, "missing ai_flag_score"
    if flag_score < cfg.min_flag_score:
        return None, f"flag score {flag_score:.1f} below min {cfg.min_flag_score:.1f}"

    # --- the edge test ---
    hv = realized_volatility(c.get("daily_closes") or [])
    if hv is None:
        return None, "fewer than 10 usable daily closes; realized vol not computable"
    ratio = iv_hv_ratio(c.get("iv"), hv)
    if ratio is None:
        return None, "iv/hv ratio not computable"
    if ratio > cfg.max_iv_hv_ratio:
        return None, (
            f"iv/hv ratio {ratio:.2f} > {cfg.max_iv_hv_ratio:.2f} -- implied "
            f"vol {_as_float(c.get('iv')) or 0:.0%} vs realized {hv:.0%}; "
            "not cheap relative to actual recent movement"
        )

    return {
        "symbol": symbol,
        "underlying_price": underlying,
        "strike": _as_float(c.get("strike")),
        "type": contract_type,
        "expiration_date": expiry.isoformat(),
        "days_to_expiry": days_to_expiry,
        "bid": _as_float(bid),
        "ask": ask_f,
        "premium_usd": premium_usd,
        "spread_pct": sp,
        "delta": delta,
        "iv": _as_float(c.get("iv")),
        "realized_vol": hv,
        "iv_hv_ratio": ratio,
        "open_interest": oi,
        "volume": vol,
        "catalyst_score": score,
        "ai_flag_score": flag_score,
        "notes": str(c.get("notes", ""))[:400],
    }, ""


def apply_soft_filters_and_rank(
    candidates: Sequence[dict[str, Any]],
    cfg: SoftCatalystScanConfig,
    today: Optional[dt.date] = None,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """apply_filters_and_rank's counterpart for the soft-catalyst track.
    Survivors are ranked by iv_hv_ratio ascending (cheapest relative to
    actual recent movement first, ties broken by lower premium_usd), capped
    at top_n. Same non-judgment of the
    catalyst itself: a high catalyst_direction_score means multiple sources
    agree, not that they are right."""
    passed: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    for c in candidates:
        if not isinstance(c, dict):
            rejected.append({"symbol": "?", "reason": "not a mapping"})
            continue
        result, reason = evaluate_soft_candidate(c, cfg, today=today)
        if result is None:
            rejected.append(
                {"symbol": str(c.get("symbol", "?")).upper(), "reason": reason}
            )
            continue
        passed.append(result)
    # Best edge first; cheaper premium breaks ties among equally-qualified
    # candidates (2026-08-19, user: "keep $50 but try to find cheaper if
    # possible" -- edge quality still decides, this only orders ties).
    passed.sort(key=lambda r: (r["iv_hv_ratio"], r["premium_usd"]))
    return passed[: max(0, cfg.top_n)], rejected


@dataclass(frozen=True)
class OptionScanConfig:
    """Thresholds for apply_filters_and_rank. Mirrors the option_scan block
    in config.json; kept here as a frozen dataclass so the pure math module
    has no dependency on the YAML/JSON loader."""

    # Max premium per contract in dollars (price x 100). The account's 3%
    # house risk rule still applies on top -- both caps apply and the
    # smaller one binds. Premium IS the max loss on a long option, so this
    # is a true risk cap, not a notional cap.
    # Raised 2026-08-19 -> 2026-08-25 ($50 -> $150), user's explicit
    # instruction after 12/12 real checks were structurally rejected at
    # $50 -- see SoftCatalystScanConfig's comment for the full rationale.
    max_premium_usd: float = 150.0
    # See spread_pct() on why this is far looser than the stock scanner's 1%.
    # 15% admits the ATM contracts and excludes the deep-OTM penny strikes,
    # calibrated against the live ENVX chain on 2026-08-12.
    max_spread_pct: float = 15.0
    min_open_interest: float = 100.0
    min_volume: float = 10.0
    # Delta band. Below the floor is a pure lottery ticket whose base rate
    # (~91% of far-OTM buyers lose, per sources.md) is not worth screening
    # for; above the ceiling the leverage that makes this strategy work is
    # gone and buying the stock is usually the better expression.
    min_delta: float = 0.25
    max_delta: float = 0.55
    # The actual edge test. Below 1.0 means underpriced vs. this name's own
    # history; 0.85 demands a real margin rather than a rounding error.
    max_mismatch_ratio: float = 0.85
    # Expiry must clear the catalyst by at least this many days. 0 permits an
    # expiry on the effective move date itself (razor thin); 1+ buys room.
    min_days_after_catalyst: int = 1
    max_days_to_expiry: int = 45
    min_underlying_price: float = 2.0
    max_underlying_price: float = 100.0
    top_n: int = 10


def evaluate_candidate(
    c: dict[str, Any], cfg: OptionScanConfig, today: Optional[dt.date] = None
) -> tuple[Optional[dict[str, Any]], str]:
    """Evaluate ONE candidate contract. Returns (result, reason).

    On a pass, result is the enriched candidate and reason is "". On a
    rejection, result is None and reason names the failing gate -- rejections
    are reported, not silently dropped, because "everything was filtered out"
    and "the data was malformed" look identical otherwise, and on this repo's
    history (BNR, GSIW, PLAG) the difference mattered.
    """
    today = today or dt.date.today()

    symbol = str(c.get("symbol", "")).upper().strip()
    if not symbol:
        return None, "missing symbol"

    underlying = _as_float(c.get("underlying_price"))
    if underlying is None or underlying <= 0:
        return None, "unusable underlying price"
    if not (cfg.min_underlying_price <= underlying <= cfg.max_underlying_price):
        return None, f"underlying ${underlying:.2f} outside price band"

    # --- structural: does this contract survive to see the catalyst? ---
    effective = catalyst_effective_date(c.get("catalyst_date"), c.get("catalyst_timing"))
    if effective is None:
        return None, "missing or malformed catalyst date"
    expiry = _as_date(c.get("expiration_date"))
    if expiry is None:
        return None, "missing or malformed expiration date"
    required = effective + dt.timedelta(days=cfg.min_days_after_catalyst)
    if expiry < required:
        return None, (
            f"expiry {expiry} does not clear catalyst (needs >= {required}); "
            "contract would expire before or too close to the move"
        )
    days_to_expiry = (expiry - today).days
    if days_to_expiry < 0:
        return None, f"expiry {expiry} has already passed"
    if days_to_expiry == 0:
        # Excluded deliberately, not incidentally. On expiration day the
        # contract still trades, but theta is at its most violent and the
        # position has no room to recover from being early -- a different
        # game with a different skill set. This screen is for buying a
        # catalyst with time to work, so 0DTE is out regardless of how good
        # the mismatch ratio looks.
        return None, f"expires today ({expiry}); 0DTE is excluded by design"
    if days_to_expiry > cfg.max_days_to_expiry:
        return None, f"{days_to_expiry}d to expiry exceeds max {cfg.max_days_to_expiry}d"

    # --- tradability ---
    bid, ask = c.get("bid"), c.get("ask")
    contract_mid = mid_price(bid, ask)
    if contract_mid is None:
        return None, "no usable two-sided quote on the contract"
    sp = spread_pct(bid, ask)
    if sp is None:
        return None, "spread not computable"
    if sp > cfg.max_spread_pct:
        return None, f"spread {sp:.1f}% exceeds max {cfg.max_spread_pct:.1f}%"

    ask_f = _as_float(ask)
    if ask_f is None:
        return None, "unusable ask"
    premium_usd = ask_f * 100.0
    if premium_usd > cfg.max_premium_usd:
        return None, (
            f"premium ${premium_usd:.0f}/contract exceeds max "
            f"${cfg.max_premium_usd:.0f}"
        )

    oi = _as_float(c.get("open_interest"))
    vol = _as_float(c.get("volume"))
    if oi is None or vol is None:
        return None, "missing open interest or volume"
    if oi < cfg.min_open_interest:
        return None, f"open interest {oi:.0f} below min {cfg.min_open_interest:.0f}"
    if vol < cfg.min_volume:
        return None, f"volume {vol:.0f} below min {cfg.min_volume:.0f}"

    delta = _as_float(c.get("delta"))
    if delta is None:
        return None, "missing delta"
    abs_delta = abs(delta)
    if not (cfg.min_delta <= abs_delta <= cfg.max_delta):
        return None, (
            f"|delta| {abs_delta:.2f} outside band "
            f"[{cfg.min_delta:.2f}, {cfg.max_delta:.2f}]"
        )

    # --- the edge test ---
    em_usd = expected_move_from_straddle(c.get("atm_call_mid"), c.get("atm_put_mid"))
    if em_usd is None:
        return None, "ATM straddle not usable; expected move not computable"
    em_pct = as_pct_of(em_usd, underlying)
    if em_pct is None:
        return None, "expected move percent not computable"

    hist_pct = historical_move_pct(c.get("historical_moves") or [])
    if hist_pct is None:
        return None, (
            "fewer than 2 usable historical catalyst moves; no base rate to "
            "compare against"
        )

    ratio = mismatch_ratio(em_pct, hist_pct)
    if ratio is None:
        return None, "mismatch ratio not computable"
    if ratio > cfg.max_mismatch_ratio:
        return None, (
            f"mismatch ratio {ratio:.2f} > {cfg.max_mismatch_ratio:.2f} -- "
            f"market prices a {em_pct:.1f}% move vs {hist_pct:.1f}% history; "
            "not underpriced"
        )

    # Cross-check the straddle read against the IV read. Not a gate -- the
    # two legitimately differ -- but a large gap means one of the inputs is
    # stale, and a human should see that before risking money on it.
    em_iv_usd = expected_move_from_iv(underlying, c.get("iv"), days_to_expiry)
    em_iv_pct = as_pct_of(em_iv_usd, underlying) if em_iv_usd is not None else None
    iv_disagreement = None
    if em_iv_pct is not None and em_pct > 0:
        iv_disagreement = abs(em_iv_pct - em_pct) / em_pct * 100.0

    return {
        "symbol": symbol,
        "underlying_price": underlying,
        "strike": _as_float(c.get("strike")),
        "type": str(c.get("type", "")).lower().strip(),
        "expiration_date": expiry.isoformat(),
        "days_to_expiry": days_to_expiry,
        "catalyst_date": str(c.get("catalyst_date")),
        "catalyst_type": str(c.get("catalyst_type", "unspecified")),
        "catalyst_effective_date": effective.isoformat(),
        "bid": _as_float(bid),
        "ask": ask_f,
        "premium_usd": premium_usd,
        "spread_pct": sp,
        "delta": delta,
        "iv": _as_float(c.get("iv")),
        "open_interest": oi,
        "volume": vol,
        "expected_move_pct": em_pct,
        "historical_move_pct": hist_pct,
        "mismatch_ratio": ratio,
        "expected_move_pct_from_iv": em_iv_pct,
        "iv_disagreement_pct": iv_disagreement,
        "notes": str(c.get("notes", ""))[:400],
    }, ""


def apply_filters_and_rank(
    candidates: Sequence[dict[str, Any]],
    cfg: OptionScanConfig,
    today: Optional[dt.date] = None,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """THE safety-critical function. Reported numbers are UNTRUSTED input.

    Returns (passed, rejected). Survivors are ranked by mismatch ratio
    ascending -- most underpriced relative to the name's own history first,
    ties broken by lower premium_usd -- and capped at top_n.

    What this function deliberately does NOT do: judge the catalyst. Whether
    a real, dated, market-moving event exists is not verifiable by any
    connected tool (the same unsolved gap as S3's 5th pillar), so it stays in
    `notes` for a human to read and is never a pass/fail gate here. A perfect
    mismatch ratio on an imaginary catalyst is still a losing trade.
    """
    passed: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    for c in candidates:
        if not isinstance(c, dict):
            rejected.append({"symbol": "?", "reason": "not a mapping"})
            continue
        result, reason = evaluate_candidate(c, cfg, today=today)
        if result is None:
            rejected.append(
                {"symbol": str(c.get("symbol", "?")).upper(), "reason": reason}
            )
            continue
        passed.append(result)
    # Best edge first; cheaper premium breaks ties among equally-qualified
    # candidates (2026-08-19, user: "keep $50 but try to find cheaper if
    # possible" -- edge quality still decides, this only orders ties).
    passed.sort(key=lambda r: (r["mismatch_ratio"], r["premium_usd"]))
    return passed[: max(0, cfg.top_n)], rejected


@dataclass(frozen=True)
class OptionExitDecision:
    exit_now: bool
    reason: str
    kind: str = ""  # "stop" | "profit" | "time" | ""


# Interim exit rule for the first live S7 trades, added 2026-08-19 when the
# strategy went from watch-only to agent-executed. NOT from McMillan and NOT
# backtested -- unlike scalp_signal.py's thresholds (measured against 1,530
# real bars) or growth_signal.py's (at least the user's own stated
# tolerance), these three numbers are simply a conservative starting point
# chosen because a long option has no stop-order equivalent (the position IS
# the defined risk) and S7 had no coded exit rule at all before this. Revisit
# once real trades exist to look at outcomes -- same posture this repo
# applies to every other new threshold.
OPTION_STOP_LOSS_PCT = 50.0    # exit if premium has lost half its value
OPTION_PROFIT_LOCK_PCT = 100.0  # exit if premium has doubled
OPTION_TIME_STOP_DAYS = 5       # exit with this many days left, to stay out
                                 # of the steepest theta-decay zone (Ch. 3's
                                 # decay-accelerates-under-8-weeks finding,
                                 # sharper still in the final days)


def decide_option_exit(
    entry_premium: Any,
    current_premium: Any,
    days_to_expiry: Any,
    stop_loss_pct: float = OPTION_STOP_LOSS_PCT,
    profit_lock_pct: float = OPTION_PROFIT_LOCK_PCT,
    time_stop_days: int = OPTION_TIME_STOP_DAYS,
) -> OptionExitDecision:
    """Exit logic for a single-leg long call/put position, checked in
    priority order. A long option has no broker-side stop-order equivalent
    for a naked long (the premium paid already IS the max loss) -- this is a
    periodic-check rule, not a resting order, so it must be re-evaluated on
    whatever cadence the position is actually monitored.

    Priority:
      1. Stop-loss -- premium has fallen to stop_loss_pct or more below
         entry. Cut it; a long option that has lost half its value rarely
         recovers before expiry finishes the job.
      2. Profit-lock -- premium has risen to profit_lock_pct or more above
         entry (a "double"). Bank it. Unlike scalp_signal's profit-lock
         trail, this is a flat target, not a trailing one -- there is no
         equivalent of "ride the peak" implemented yet for options, so this
         is deliberately the more conservative of the two designs.
      3. Time stop -- fewer than time_stop_days remain. Close regardless of
         P&L rather than hold into the fastest-decay window.
    """
    entry = _as_float(entry_premium)
    cur = _as_float(current_premium)
    dte = _as_float(days_to_expiry)
    if entry is None or entry <= 0 or cur is None or cur < 0 or dte is None or dte < 0:
        return OptionExitDecision(False, "unusable input")

    pnl_pct = (cur - entry) / entry * 100.0

    if pnl_pct <= -stop_loss_pct:
        return OptionExitDecision(
            True,
            f"stop-loss: premium {cur:.2f} is {pnl_pct:.1f}% below entry {entry:.2f}",
            "stop",
        )
    if pnl_pct >= profit_lock_pct:
        return OptionExitDecision(
            True,
            f"profit-lock: premium {cur:.2f} is {pnl_pct:+.1f}% above entry {entry:.2f}",
            "profit",
        )
    if dte <= time_stop_days:
        return OptionExitDecision(
            True,
            f"time stop: {dte:.0f} days to expiry ({pnl_pct:+.1f}%)",
            "time",
        )
    return OptionExitDecision(
        False, f"holding, {dte:.0f} days to expiry, {pnl_pct:+.1f}%"
    )
