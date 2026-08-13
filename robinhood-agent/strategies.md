# Strategy playbook

Our own strategies. Built from the sources in `sources.md` plus findings from
live sessions — not a summary of any one book. Where a rule came from
somewhere, it says so; where we learned it ourselves the hard way, it says
that too.

Miner's claim is the reason this file exists: *"All consistently successful
traders have a written trade plan. Most unsuccessful traders do not."* A
scanner that finds candidates is one third of a plan. Each strategy below is
only complete when it has **setup conditions → entry trigger → stop → exit →
size**.

Status values: **LIVE** (can place orders) · **RESEARCH** (report only) ·
**BLOCKED** (complete but cannot run on this account) · **DRAFT** (written,
never run).

---

## Account constraints — these bind every strategy below

Not preferences. Structural facts about this account that eliminate whole
categories of setup:

1. **Long-only.** Cash account; shorting is impossible. Half of Miner's
   dual-timeframe 2x2 (both short rows) is permanently unusable, as is every
   bearish pattern in every source.
2. **Day trading IS allowed — with settled funds.** *(Corrected 2026-08-12;
   an earlier version of this file said "no same-day round trips," which was
   wrong and blocked S2 for no reason.)*

   A **good-faith violation** happens only when you buy with **unsettled**
   funds and sell before the original funds settle. Buying with settled cash
   and selling the same day is not a violation. Per current guidance: *"You
   can make unlimited day trades in a cash account as long as you use fully
   settled funds."* PDT never applied to cash accounts and was eliminated
   2026-06-04 regardless.

   **The real constraint is capital recycling speed.** Sale proceeds settle
   T+1. So each day you get roughly one pass through your settled balance:
   deploy $300 of settled cash, close the trade, and those proceeds are
   unusable until the next business day. Two $150 trades from settled cash
   are fine; re-trading the proceeds of the first is what trips a GFV.

   **Penalty ladder:** 3 GFVs in a rolling 12 months → account restricted to
   settled-cash-only for 90 days. That is the thing to avoid, and it takes
   three mistakes, not one.

3. **~$329 balance ($300 funded + ~$29 SLB), $150 per-order cap.** Spreads
   are large relative to position size, which is why the spread filter
   matters more here than on a bigger account. Whole shares are required —
   Robinhood will not place a stop-loss on a fractional position.

---

## Regime selector — decide this BEFORE picking a strategy

The gap that made today's session inefficient: every tool we ran was a
long-momentum tool, on a low-volatility grind day where that was the wrong
instrument. Classify first, then pick.

Inputs, one call each: `get_market_pulse` (VIX, breadth, fear/greed) and
SPY vs its own 20/50/200 SMA.

| Regime | Signals | Strategy | Notes |
| --- | --- | --- | --- |
| **Trending up, low vol** | VIX < 20, SPY above 50 & 200 SMA, breadth neutral-positive | **S1 Trend Follow** | Today (2026-08-11) was this: VIX 15.35, 90.7% of names neutral RSI |
| **Trending up, high vol** | VIX > 25, wide daily ranges, breadth extended | **S3 Momentum Scan** (research) | The regime the low-float scan is actually built for |
| **Range-bound / choppy** | **7/20/65 SMA filter NOT aligned** (see below), VIX mid, no breadth extreme | **S5 Range Trade** | DRAFT |
| **Trending down** | SPY below 50 SMA, breadth negative | **none from the daily-trend branch** | Long-only; S1/S3/S5 sit out, but see S2 row below |
| **Event day** | High-impact econ release, VIX spike | **sit out** | Investing.com calendar check pre-open. Overrides S2 too |
| **Volatile open (any daily regime)** | First completed 15m candle's range > 20% of ATR(14) | **S2 Opening Range Reversal** | **Fixed 2026-08-12** — `regime.py` now folds S2 in independent of trend/vol, per its own trigger. Stacks with whatever the trend branch above already allows (e.g. an uptrend-low-vol day with a volatile open returns both S1 and S2) |

**Two of five daily-trend regimes have a runnable strategy, plus S2 which
stacks on top of any of them** when the opening range is volatile enough.
That is the honest coverage number, and the down-day gap for S1/S3/S5 is
structural rather than something to build — S2 is the one that can still
fire on a down day.

### The trend/range test — 7/20/65 SMA alignment

From the DailyFX range guide, and the most useful thing in it. A concrete,
computable answer to "is this a trending or a ranging market," which the
regime table above otherwise hand-waves:

- **Uptrend:** 7 SMA > 20 SMA > 65 SMA
- **Downtrend:** 7 SMA < 20 SMA < 65 SMA
- **Neither (ranging):** any other ordering

> "The importance of the three-SMA filter does not lie in the specific SMA
> values, but rather in the interplay of the short-, intermediate- and
> long-term price trends."

So the alignment test is the point, not the periods — the periods are
tunable by Miner's procedure. Two independent uses:

1. **Aligned → trend regime.** Run S1/S4. Do **not** range trade; that is
   the guide's central warning.
2. **Not aligned → range regime.** S5 is eligible.

Applies to the index (SPY) for market regime and to an individual symbol for
per-name eligibility. `get_equity_technical_indicators` computes SMA at any
period, so this is three calls and no new infrastructure.

---

## House rules — apply to every strategy

Where the sources agree, we adopt. Where they conflict, that is stated
rather than silently resolved.

**Entry**
- **Limit orders, never market.** (Sincere: a market order in a fast tape can
  fill "10, 15, or 20 points lower than you anticipated.")
- **Require confirmation; never enter at a target price.** Buy-stop above a
  bar high or swing high — the market must move your way first. (Miner, and
  the single most transferable idea in any of these books.)
- Avoid the first ~10 minutes after the open unless the strategy is
  explicitly built for it. (Sincere, via a pro who conditions orders on
  10 minutes of session.)

**Stop**
- **Placed at the exact price that voids the setup, at the moment of entry —
  not later.** (Miner + Turner-via-Sincere agree precisely here.)
- Consequence worth stating: because entry and stop are both defined by the
  setup, **exposure is known before the order is placed.** That is what makes
  sizing computable at all.
- Never carry a hard stop overnight — gap risk fills it far below. (Sincere.)

**Size**
- **Risk ≤3% of account per trade, ≤6% across all open positions.** (Miner.)
- `size = (capital × 3%) ÷ (entry − stop)`.
- Note this is a *risk* cap, not a notional cap. `config.json`'s
  `max_order_notional_usd: 5` is notional and is a separate, additional
  ceiling. Both apply; the binding one is whichever is smaller.

**Exit**
- Never hold a loser overnight hoping it recovers. (Sincere.)
- "When in doubt, get out" — first serious thought of selling is the signal.
- Trail the stop up after a gain to lock profit.

**Circuit breaker**
- **10% account drawdown from closed trades within a month → stop trading
  for the rest of the month.** (Miner.) Nothing in the repo implements this
  yet; it belongs in `risk.py`.

**Unresolved conflict — do not pretend it is settled**
- *Minimum risk/reward ratio.* Sincere requires 1:2 min, prefers 1:3. Miner
  calls minimum-ratio rules "basically a bogus idea" and warns against
  educators who teach them. Both are credible. **Decidable by our own trade
  log**: tag each trade with its pre-trade ratio and compare realized
  outcomes. Until then, we record the ratio but do not gate on it.

**Our own disqualifier — from live data, not from any book**
- **Extreme relative volume + no confirmed catalyst = halt risk, not
  opportunity.** On 2026-08-11 this pattern hit twice out of two
  occurrences: WXM (614x rel. vol, no news) halted at 9:44am; PLAG (843x, no
  news, "under investigation" chatter) halted ~11:25am. Neither was callable
  in advance from price/volume alone; the catalyst check is what separated
  them. **No strategy below may take a position in a name with no verifiable
  catalyst, regardless of how many numeric pillars it clears.**

---

## S1 — Trend Follow  ·  **LIVE**

The only strategy on this account that can currently place an order.

- **Regime:** trending up, low volatility.
- **Universe:** `daily_allowlist.json`, written each morning by
  `screener.py` (liquidity, ATR band, price band filters).
- **Setup:** shorter-term MA above longer-term MA on the daily chart.
  Currently 20 vs 50 (`config.json` strategy prompt).
- **Entry:** buy when a non-held allowlisted symbol is in uptrend.
- **Exit:** sell a held symbol when the trend flips to downtrend.
- **Stop: MISSING.** This is the strategy's one real defect — it exits only
  on trend reversal, which can be far below entry. Until a stop exists,
  Miner-style sizing cannot be computed for it.
- **Size:** currently the flat $5 notional cap.

**Open questions worth testing rather than guessing**
- 20/50 vs **20/60/100** (daytrading.com's version, where the 100 sets trend
  bias and the 20/60 cross triggers) vs **8/13** (Sincere). `backtest.py`
  exists and can settle this on real data.
- Miner's lookback-selection procedure applies here and is concrete: test
  several settings across 2-3 different periods and keep the one where
  reversals land within a bar or two of actual swing highs/lows without
  false mid-range crosses.

---

## S2 — Opening Range Reversal (Pattern Scalp)  ·  **VIABLE** — top priority

**Status changed 2026-08-12.** Previously marked BLOCKED on a mistaken
reading of cash-account settlement (see constraint 2). It is not blocked:
one round trip per day from settled funds is exactly what this strategy
needs, and it is **the only strategy in this repo with a complete plan** —
entry trigger, stop, target, and time stop all specified.

Given the stated aim is day trading, **this is the strategy to run**, not
S1. S1 is a multi-day trend strategy and was never the right fit.

- **Regime:** volatile open.
- **Setup:** first completed 15m candle sets OR_high / OR_low. Valid only if
  `OR_range > 20% of daily ATR(14)` — a large liquidity-grabbing first
  candle. Long side requires that candle to have pushed *down* (close below
  open), i.e. a downside manipulation expected to reverse up.
- **Entry:** on 5m bars near/below OR_low, either a hammer that pokes below
  OR_low and closes back above it (enter on the break of that candle's high),
  or a bullish engulfing recovering ≥50% of the prior down candle.
- **Stop:** just below the wick low / manipulation extreme.
- **Target:** return toward OR_high.
- **Time stop:** exit by end of the entry window; never hold into afternoon.
- **Capital:** uses settled cash for one round trip per day. At ~$329 with a
  $150 order cap that is one or two positions, closed same day.
- **Config:** `config.pattern-scalp.json` — needs its risk block updated to
  match the $300 funding (still carries the old $5 cap).

---

## S3 — Low-Float Momentum Scan  ·  **RESEARCH ONLY**

`momentum_scanner.py`. Never writes an allowlist, never feeds `run.py`.

- **Regime:** trending up, high volatility. Explicitly the wrong tool on a
  low-vol day.
- **Window:** 9:30–11:30am ET (Warrior Trading). **Caveat from our own
  testing: this did not hold.** The acceleration signal decayed just as fast
  inside the window as outside it — WXM put 1.22M shares through the 9:35
  bar then 90,878 through 9:40, a 93% collapse, round-tripping to its open
  price. Treat the window as necessary, not sufficient.
- **Numeric pillars (config.json):** rel. vol ≥5x · % change ≥10% ·
  price $2–20 · float ≤20M · **spread ≤1%** (added 2026-08-11).
- **5th pillar — catalyst — is not numeric and cannot be automated.** It is
  checked by hand via Stocktwits + Stocklake news. This is the pillar that
  caught both halts. See the disqualifier in House Rules.
- **Known defect:** the relative-volume metric is cumulative-day-volume ÷
  daily-average, a ratchet that only climbs. A name qualifying at 11am stays
  qualified all afternoon whether or not buyers remain. BNR passed on 16,473
  shares traded all day.
- **Known defect:** `min_price: 2.0` is a liquidity proxy that the spread
  filter now measures directly. The floor hid PLAG for two full scan cycles
  while it ran from $1.14 to $2.57. Candidate for removal.

---

## S4 — Dual Timeframe Momentum  ·  **DRAFT, never run**

From Miner, adapted to this account. Written out because it is the most
directly implementable idea from any of the four sources, and because it
addresses S1's weakness: S1 has no concept of *when* within a trend to enter.

- **Regime:** any trending regime — its own filter handles direction.
- **Timeframes:** any adjacent pair. For this account, daily/60m (setup
  visible in the evening, order placed for the next day, no intraday
  monitoring required) is the only pair that respects the settlement
  constraint. 15m/5m is the day-trade pair and is blocked.
- **Setup — long only** (the two short rows of Miner's table are unusable):

  | Higher TF momentum | Action |
  | --- | --- |
  | Bull, not overbought | **Long** after a smaller-TF bullish reversal made *below* the OB zone |
  | Bull, overbought | No new long. (Not a reason to exit an existing one.) |
  | Bear, not oversold | No trade — short setup, unusable |
  | Bear, oversold | **Long** after a smaller-TF bullish reversal |

- **Entry:** trailing one-bar high — buy-stop one tick above the prior bar's
  high. Does not execute unless the market confirms.
- **Stop:** the price that voids the setup (below the reversal swing low).
- **Size:** 3% risk rule, computable because entry and stop are both known.
- **Indicator:** any oscillator with OB/OS zones. `get_equity_technical_
  indicators` provides RSI, stochastic, MACD. Lookback to be selected by
  Miner's procedure, not assumed.
- **Status:** nothing built. Would need a new runner; `run.py`'s prompt is
  single-timeframe.

---

## S5 — Range Trade  ·  **DRAFT, never run**

Fills the range-bound regime, previously uncovered. Source: DailyFX/FXCM
*Range Trade Guide*. **That guide is about forex, and a large part of it does
not transfer** — see the exclusions at the end of this section.

- **Regime:** range-bound. Eligibility test is the 7/20/65 SMA filter
  **not** aligned, on both SPY and the symbol.
- **Range definition:** price makes a significant high, retests and fails to
  break it, makes a significant low, retests and fails to break it. Both
  failures are required — one touch does not establish a level. "The longer
  the indecision point remains, the more significant the support or
  resistance level."
- **Setup (long only on this account):** price at/near established support
  with RSI oversold.
- **Entry:** **RSI(14) crossing back up through 30** — the cross, not the
  reading. The guide is explicit that RSI can sit oversold for many periods
  in a trend, so the cross is what makes it an entry. This is the same
  confirmation principle as Miner's trailing-one-bar entry: require the
  market to move your way first.
- **Stop:** below the swing low, plus slippage room. (Guide uses 10 pips in
  FX; the equity analogue is a small fixed buffer or a fraction of ATR, to be
  set — do not copy "10 points" literally, the units are not comparable.)
- **Target:** RSI reaching overbought (70), or price reaching the top of the
  established range. The short half of the guide's cycle (sell at resistance)
  is unusable here — long-only.
- **Size:** house 3% risk rule. Range stops are tight, so this permits a
  larger share count than S1 would; the notional cap still binds.

**Two rules from this guide that are more valuable than the strategy itself**

1. **"Only Take One Stop."** When a range breaks, take one loss and do not
   re-enter. Re-entering a broken range to "get it back" is how the strategy
   turns a small loss into an account event. This is an explicit
   anti-martingale rule and we have nothing else like it written down.
2. **Stops are non-negotiable here specifically.** Range trading is
   profitable right up until the breakout, and breakouts out of long
   consolidations are violent — the guide's own example ranged for 11 months
   then broke hard. The strategy's entire risk is concentrated in the one
   event that ends it.

**Indicator calibration rule** (a concrete test, same spirit as Miner's):
for Bollinger Bands used on a range, the band should hold the *second*,
higher low. If that second low pierces the lower band, the moving average is
**too short**; if it stays well above, **too long**.

**Avoid trading into scheduled news.** Guide's window for North America is
**8–10am ET**. Our own equivalent is the Investing.com economic calendar
check already logged in `sources.md` — same idea, better source for equities.

### What does NOT transfer from this guide
The whole instrument-selection half is forex-specific and should not be
adapted by analogy:
- Avoid-the-majors / trade-the-crosses. Rests on the dollar being one side
  of ~90% of FX transactions. **No equity analogue exists.**
- Interest-rate differentials predicting range width. Meaningless for a
  single stock.
- Tick volume as a support/resistance proxy — exists because FX has no
  central volume. Equities have real volume; use it directly.
- DailyFX's proprietary reports and their Range Breakout Barometer.

**The open question this leaves:** the guide's core selection insight is
"trade the instrument that has no dominant trending driver." What the equity
analogue is — low beta? no upcoming earnings? no active catalyst? — is
genuinely unanswered, and inventing one and attributing it to this guide
would be false. Needs its own testing before S5 is more than a draft.

---

## S6 — Tony Oz scan family  ·  **DRAFT** (four scans, directly scannable)

Source: Tony Oz, *The Stock Trader: How I Make a Living Trading Stocks*
(Goldman Brown, 2000). Unlike every other source logged, Oz publishes
**literal scan formulas**, which is exactly what this repo needs. Read this
section as scanner specs, not as reading notes.

**Read the caveats before implementing any threshold.** This is a 2000 book
and two of its numbers are not portable.

### The four scans, as published

| Scan | Avg volume | Rel. volume | Net change | Price | Extra condition |
| --- | --- | --- | --- | --- | --- |
| **Volume Spike** | > 750,000 | > 1.5× | ≥ 5/8 | $40–200 | — |
| **Breakout** | > 400,000 | > 1.7× | ≥ 5/8 | $40–200 | last trade = **4-week high** |
| **Pullback Swing** | > 750,000 | — | — | $40–200 | down 3 days, trading above yesterday's low |
| **Power** | > 350,000 | > 1.5× | ≥ 5/8 | $40–200 | last trade in **top 13% of day's range** |

### Pullback Swing — exact formula as printed in the text

The only one for which the book prints the raw formula syntax:

```
VolAvg20    > 350,000
Last        > P Low          # last trade above yesterday's low
P1Close     < P2Close        # three consecutive
P2Close     < P3Close        #   lower closes
P3Close     < P4Close
```
`VolAvg20` = 20-day average volume; `P Low` = previous day's low;
`P1Close` = previous close, `P2Close` the day before, etc.

**Discrepancy — flagged, not silently resolved.** The in-text formula
(Chapter 2, the scan he actually ran that day) uses **VolAvg20 > 350,000**.
The Appendix version of the same scan says **"more than 750,000 shares on
average"** and adds the $40–200 price band, which the in-text formula does
not contain. Both are in the same book. The Appendix notes its formulas
"were published in the book, *Stock Trading Wizard*" — a different, later
title — so the likeliest explanation is that the Appendix is a revised
version. **Do not treat either as canonical.** If implemented, pick one
deliberately and record which.

### Portability caveats — two numbers do NOT transfer

1. **"Net change of 5/8" is a fraction, not a percentage.** The book predates
   decimalization (2001). 5/8 = **$0.625**. On a $40–200 stock that is
   0.3%–1.5% — a much weaker move requirement than it looks. It is an
   absolute dollar move, and it is not comparable to our `min_pct_change`
   of 10%.
2. **The $40–200 price band is 2000-era pricing** and would need inflation
   and market-structure adjustment before use. Do not copy the numbers
   literally; the *intent* — liquid, higher-priced, institutionally traded
   names — is what carries.

Obsolete and ignored: the book's Level II / SOES / SelectNet material
describes a market structure that no longer exists.

### The genuinely new scannable idea: close strength

**"Last trade in the top 13% of the day's trading range."** Computable
directly:

```
(last - low) / (high - low) >= 0.87
```

This measures *where in its range a stock is closing* — a name finishing at
its high is under accumulation; one finishing mid-range is not. **We have no
equivalent filter.** It is cheap to compute from `get_equity_fundamentals`
(which already returns today's high, low, and last) and it is a genuinely
different axis from anything currently in `momentum_scanner.py`, which
measures size of move and volume but never *quality of close*.

Same for the **4-week high** condition and the **three-consecutive-lower-
closes** pullback pattern — both computable from `get_equity_historicals`
daily bars, neither currently implemented.

### The convergence worth acting on

Three independent sources now point away from this repo's current scan
universe, and our own live data agrees with them:

| Source | On price / liquidity |
| --- | --- |
| Oz (2000) | $40–200, avg volume 350K–750K minimum |
| Sincere (2011) | avoid stocks under $3; "you need liquid stocks" |
| **Our data (2026-08-11)** | every extreme-relvol cheap pass halted or faded; TISI 4.5% spread |

`config.json` currently scans **$2–20, float ≤20M, rel. vol ≥5×** — the
opposite universe on every axis. That is not automatically wrong; low-float
momentum is a real strategy and Warrior Trading targets exactly it. But it
should be a **deliberate choice between two coherent universes**, not an
unexamined default. The spread filter added 2026-08-11 is the first step
toward measuring which universe we are actually in.

### Structural note from Oz worth more than the scans

He states that **most of his trades came from a curated "Constant watch
list" of 35 stocks he follows daily**, not from scans — scans are the
supplementary source, and he says explicitly that in a trending bull market
they generate more of his trades. He also warns: *"You will get numerous
candidates using each one of these scans... not every result is a high
probability candidate. You must study the charts."*

That is the same structure we arrived at independently: the scan produces
candidates; a human/judgment pass (our 5th pillar) decides. It also suggests
a piece we do not have — a **stable curated watchlist as the primary
source**, with scans as the secondary one. `screener.py` builds a daily
allowlist from a fixed `candidate_universe`, which is closer to this than
the momentum scanner is.

---

---

## S7 — Options (long calls / long puts)  ·  **DRAFT — not yet traded live**

Source: Dan Passarelli, *Trading Options Greeks* (Bloomberg Financial
Series). A Greeks-first options text — deltas, theta, vega, spread
construction, volatility trading. Read the parts relevant to what this
account can actually execute; the rest is logged as out of scope, not
adopted.

### Two blockers, checked directly rather than assumed

1. **Corrected 2026-08-12: this is NOT blocked.** `get_accounts` now shows
   `option_level: "option_level_2"` for account 432805174 — the account was
   already approved (or was upgraded since the note below was written; the
   point is it was checked live, not assumed). `option_level_2` covers long
   calls, long puts, covered calls, and cash-secured puts, which is exactly
   what survives blocker 2 below. No upgrade action needed.
2. **Multi-leg orders are not supported by this MCP connector, even at
   level 3.** Per the tool's own description: *"multi-leg orders are not yet
   supported here."* This is a hard tooling limit, not an approval-level
   problem, and it doesn't get fixed by upgrading further.

**Consequence: most of this book's content is not executable on this
account through these tools, regardless of approval level or funding.**
Verticals (Ch. 9), wing spreads / condors / butterflies (Ch. 10), calendars
and diagonals (Ch. 11), ratio spreads (Ch. 16) all require several legs
filled as one order. **Logged as read, not adopted** — same treatment as
Miner's Elliott/Fibonacci chapters. If this connector ever supports
multi-leg orders, or if manual multi-leg entry becomes available, this
section should be revisited; the strategies themselves are sound, the
blocker is purely mechanical.

**What survives the two blockers:** single-leg long options — long calls,
long puts. These need only `option_level_2` and one order. A long straddle
or strangle *can* be approximated as two separate single-leg buys (a call
and a put), but that is two fills at two prices, not one simultaneous spread
fill — real legging risk that the book's straddle chapter assumes away.
Worth knowing, not worth pretending it's the same trade.

### S7 mechanics — long calls/puts only, adapted to this account

- **Direction comes from the existing regime/momentum signals** (S1's trend
  read, S3/S6's scan output, the catalyst check). Options here are a
  different *instrument* for the same directional read, not a new signal
  source.
- **Moneyness is a lever, not a free choice:**
  - **ATM** — most balanced exposure to price movement vs. time decay;
    roughly even mix of delta, theta, and vega risk. Reasonable default.
  - **OTM** — cheaper premium, more leverage per dollar, but decays faster
    and needs a bigger move to pay off. Higher variance, matches this
    account's small size only if position sizing accounts for a higher
    probability of the premium going to zero.
  - **ITM** — pricier, behaves more like the underlying stock, slower decay.
    Lower leverage; not obviously suited to a small account's capital limit.
- **Delta doubles as a rough odds estimate.** A ~0.20 delta option is
  loosely read as ~20% odds of finishing in-the-money; ~0.75 delta as ~75%.
  Approximate, not exact, but useful for sizing intuition alongside the
  house 3%-risk rule (the risk here is the full premium if held to a
  worthless expiry, not a stop-defined loss).
- **Theta accelerates as expiration nears, fastest for at-the-money
  options.** For a day-trade approach (in and out same day or within a few
  days), this cuts the other way from a typical premium-selling book's
  framing — it doesn't call for staying in through decay, it's the reason
  **not** to hold a losing long option hoping for a rebound. Same "cockroach
  theory" instinct as Sincere's stock rule, just faster on options.
- **Implied vs. realized volatility.** IV is what the market is currently
  pricing in via supply and demand for the option, not a measure of what the
  stock has actually done. **Do not buy options into a known IV-elevating
  event** (earnings, a scheduled catalyst) expecting a directional move to
  pay for itself — a correct direction call can still lose money if IV
  collapses after the event (an "IV crush") faster than the stock moves.
  This is a real risk for a scanner tuned to catalyst-driven names; check
  whether a candidate has a same-day or next-day earnings date
  (`get_earnings_calendar`) before choosing options over the underlying.
- **Expiration choice is a tradeoff the book frames around avoiding the
  worst of theta decay** while still having enough duration for the setup to
  play out — commonly discussed in the 2–6 week range rather than the
  final days, where decay is steepest and a stalled setup has the least
  room to recover before theta erases it.

### Cheap-contract catalyst plays — the mismatch has to be in IV, not in dollars

Added 2026-08-12 after the account asked specifically about buying
sub-$2 (sometimes sub-$0.10) contracts ahead of a catalyst, on the theory
that a real move is coming and the market hasn't caught up. That pattern
is real and has a name (sources below call it a "lotto ticket" or
"catalyst play"), but it has one failure mode that swallows most attempts
at it: **a contract can be cheap in dollars for two completely different
reasons, and only one of them is an edge.**

- Cheap because it's far OTM and **IV is normal** — the market hasn't
  priced in unusual movement, so if a real under-the-radar catalyst sits in
  the expiry window, the option is genuinely underpriced. This is the real
  version of the strategy.
- Cheap because it's far OTM and **IV is already elevated** into a known
  event (earnings, a scheduled catalyst) — the market has priced in a big
  move, the option's dollar price just looks small because delta is low.
  This is not a mismatch. It looks identical to the first case by price
  alone; only the IV number tells them apart.

**How to actually tell them apart — the expected move.** ATM straddle
price × 0.85 ≈ the market's expected move by expiry (the 0.85 corrects for
the straddle including extra time value beyond the pure expected range).
Equivalently: `stock_price × IV × sqrt(days_to_expiry / 365)`. Compare that
expected move to the stock's own historical earnings-day (or catalyst-day)
moves via `get_earnings_results` / `get_equity_historicals`:
  - Priced move noticeably **below** the stock's own history on comparable
    events → possible genuine mismatch, options may be cheap relative to
    what this name actually tends to do.
  - Priced move at or **above** history → no mismatch. IV is doing its job.
  - No dated catalyst in the window at all, IV still low → far OTM decay
    risk with nothing to catalyze it into the money. The bad kind of cheap.

**Live worked example (not a mismatch) — ENVX, 2026-08-12, reports after
today's close:**

| Contract (exp 2026-08-14) | Price | IV | Delta |
| --- | --- | --- | --- |
| $4.50 call (ATM) | $0.54×$0.61 | 293% | 0.65 |
| $4.50 put (ATM) | $0.26×$0.28 | 279% | -0.35 |
| $6.50 call (36% OTM) | $0.04×$0.07 | 305% | 0.12 |
| $3.50 put (27% OTM) | $0.02×$0.05 | 303% | -0.07 |

Stock $4.785. ATM straddle mid ≈ $0.575 + $0.27 = $0.845 → expected move ≈
$0.845 × 0.85 ≈ **$0.72, ~15% by Friday**.

Now the half that actually decides it — **what ENVX really does on
earnings.** Its last six reports were all `pm`, so each move landed the
next session. Close-to-close, computed from daily bars:

| Report | Move next session |
| --- | --- |
| 2025-02-19 | +2.55% |
| 2025-04-30 | −8.36% |
| 2025-07-31 | −20.11% |
| 2025-11-05 | −20.23% |
| 2026-02-25 | −3.25% |
| 2026-05-13 | −13.58% |

**Median absolute move: 10.97%.** Market is pricing **15.01%**.

**Mismatch ratio = 15.01 / 10.97 = 1.37.** The options are *rich* — the
market is pricing 37% MORE movement than this name typically delivers.
Buying that $6.50 call is paying above the historical rate for a move,
then needing a 36% rally on top of it. **This is what a non-mismatch looks
like** — the pattern to screen out, not screen for.

Worth flagging how this conclusion was reached, because the first version
of this section got there by the wrong route: it argued "IV is 305%, so
it's not cheap." High IV alone does not prove that — a high-IV name that
historically moves *even more* would still be underpriced. The verdict
only became sound after pulling the six real historical moves. A draft of
the regression test that used invented-but-plausible historical numbers
flipped the verdict to "genuine mismatch." **The historical leg is not
optional, and it must be looked up, never assumed.**

**The honest base rate.** Multiple sources checked this session
independently report that retail investors buying far-OTM options lose
roughly 91% of the time on average. That number is for the category as a
whole, undifferentiated by IV mismatch — it is the reason position sizing
for this strategy should assume most individual tickets go to zero and
should be sized as a batch of small bets, not evaluated ticket-by-ticket
on hope.

### The screener — `option_scanner.py` + `option_math.py`  ·  **RESEARCH ONLY**

Built 2026-08-12. Same structure as the other scanners: a read-only
gathering session with **no order tool present at all**, and selection done
afterward by a pure function in code, not by model judgment. Writes
`option_candidates.json`, which nothing else reads — it is not an allowlist
and never feeds `run.py`.

The math lives in `option_math.py` with no SDK import, so it is testable
standalone (`python3 test_option_math.py`, 48 assertions). Its central
regression test replays the real ENVX chain above and **asserts the screen
rejects it** — with every tradability gate loosened, so the rejection has
to come from the edge test itself, not from the wide spread. A screen that
can't reject ENVX would be worthless.

**Gates, in the order they bind:**

| Gate | Default | Why |
| --- | --- | --- |
| Expiry clears the catalyst | ≥1 day past the effective move date | A `pm` report on D moves the stock on **D+1**; an option expiring D is structurally worthless. Unknown timing is treated as `pm` (the conservative read) |
| 0DTE | excluded outright | Separate rule, so relaxing the catalyst buffer can't open a back door into it |
| Premium | ≤ $50/contract | Premium *is* max loss on a long option, so this is a true risk cap. The house 3% rule still applies on top; smaller binds |
| Spread | ≤15% | Far looser than the stock scanner's 1% — a $0.01 tick is 20% of a $0.05 mid. Calibrated on the live ENVX chain: admits the ATM strikes, excludes the deep-OTM pennies |
| Open interest / volume | ≥100 / ≥10 | Thin-contract exclusion, same instinct as the GSIW/BNR stock rejections |
| \|Delta\| | 0.10–0.55 | Below the floor is a pure lottery ticket (~91% base-rate loser); above it the leverage is gone and stock is the better expression |
| **Mismatch ratio** | **≤0.85** | The actual edge test. Demands a real margin, not a rounding error |
| Historical sample | ≥2 usable moves | One past move is an anecdote; treating it as a base rate manufactures false confidence |

Ranked by mismatch ratio ascending. **Rejections are reported with reasons,
never silently dropped** — "nothing passed" and "the data was malformed"
look identical otherwise, and on this repo's history (BNR, GSIW, PLAG) that
difference has mattered.

**What it still cannot do:** verify that a catalyst is real. Earnings dates
are confirmable via `get_earnings_calendar`; everything else the account
raised as a signal — news, sentiment, insider activity, a stock "about to
break" — is not machine-verifiable here. Same unsolved gap as S3's 5th
pillar. Those go in `notes` for a human to read and are **never** a
pass/fail gate. A perfect mismatch ratio on an imagined catalyst is still a
losing trade. Stocklake Pro ($20/mo) would partly close this; not yet
evaluated.

**Expect it to return nothing most days.** A genuine volatility mismatch is
rare, and the screen is built to say no. An empty result is the screen
working, not the screen failing.

### First live run — 2026-08-12, 11 contracts, 0 passed

Hand-run against the real earnings calendar as an end-to-end check. 14
names cleared the $2–100 price band; 5 with liquid chains were carried
through in full (ONDS, STNE, LUNR, WOLF, NKTR), all on the 2026-08-21
expiry, which clears every one of their catalysts.

| Symbol | Priced move | Historical median | Ratio | Read |
| --- | --- | --- | --- | --- |
| ONDS | 13.90% | 13.70% (n=6) | 1.01 | Fairly priced |
| STNE | 7.80% | 8.89% (n=6) | 0.88 | Near-miss; just above the 0.85 gate |
| WOLF | 16.93% | 17.61% (n=3) | 0.96 | Fairly priced, thin sample |
| NKTR | 6.91% | 2.94% (n=6) | 2.35 | Rich |
| LUNR | 14.46% | 4.35% (n=6) | 3.32 | Very rich |

Nothing passed. Contract-level gates also did real work independently:
LUNR's ATM call was $151/contract (premium cap), and STNE/WOLF/NKTR all
quoted 20–36% spreads (spread cap) — the same round-trip friction the
stock scanner's 1% rule catches, at the scale options actually trade at.

**A real defect this run exposed.** WOLF's first pass showed three
earnings moves of exactly +0.0%, which is not a plausible reading.
`get_equity_historicals` returned **169 synthesized bars out of 331** —
`interpolated: true`, volume 0, flat at $1.54 — the pre-reorganization
stub from its Chapter 11. Half the price history was fabricated, and it
made a violently volatile name look calm. Recomputed with those bars
discarded, WOLF's median move is 17.61% across the 3 surviving reports,
not 4.85%. `option_scanner.py`'s prompt now requires discarding
`interpolated`/zero-volume bars before computing anything, and requires
skipping reports whose surrounding bars were discarded rather than
measuring a "move" across a months-long hole. **Nothing in the repo
checked this flag before; the momentum side may have the same exposure
and has not been audited for it.**

Two honest caveats on the run itself: WOLF passes the ≥2-observation
minimum with only 3, and all 3 are post-reorganization, so it is
arguably a different company than the ticker's earlier history; and
STNE at 0.88 is close enough to the 0.85 gate that the threshold — not
the market — is what excluded it.

### First live run — results (graded 2026-08-13)

ONDS and LUNR both reported `am` on 2026-08-13, so their moves are now
measurable against what the screen predicted the day before. Baselines are
the 8/12 closes; "actual" is measured in regular hours on 8/13.

| | 8/12 close | 8/13 | **actual move** | market priced | own history | ratio | screen said |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ONDS | $9.77 | $9.31 | **−4.71%** | 13.90% | 13.70% | 1.01 | "fairly priced, no edge" |
| LUNR | $16.95 | $17.05 | **+0.60%** | 14.46% | 4.35% | 3.32 | "very rich, AVOID" |

**LUNR: the screen was decisively right.** It flagged the options as very
rich (ratio 3.32) and refused them. The market priced a 14.46% move; the
stock moved **0.60%** — the options were overpriced by roughly **24x** the
realized move. A long call or put bought into that print would have been
close to a total loss on IV crush alone. This is exactly the failure mode
S7 exists to prevent, and the mismatch ratio caught it a day early.

**ONDS: right outcome, but for shakier reasons than the ratio implies.**
The screen said "fairly priced, no edge" and declined to buy — correct, since
the stock moved 4.71% against a 13.90% priced move, i.e. options were
overpriced about **3x**. But the ratio only read 1.01 ("fair") because the
historical median (13.70%) happened to be close to the priced move. The
stock then moved far less than *either* number. **The ratio understated how
rich those options were**, and got the no-buy call by luck of the baseline
rather than by measuring the right thing.

**What this actually teaches, stated carefully:**

1. **Both names' options were overpriced versus the realized move** — 3x and
   24x. That is one day and two observations, but it is consistent with the
   IV-crush literature in `sources.md`: buying premium into a scheduled
   catalyst is structurally hard, and the screen's default posture of
   rejecting almost everything looks correct rather than merely timid.
2. **The historical median is a noisy proxy for the coming move.** ONDS has a
   13.70% median across six prior reports and delivered 4.71%. When realized
   volatility undershoots a name's own history, the mismatch ratio reads
   "fair" on options that are in fact very rich. The ratio is a filter
   against buying, not a valuation.
3. **This does not validate the ratio as a signal.** Zero contracts passed on
   2026-08-12, so nothing was risked and nothing was earned. The screen was
   graded on two rejections, both of which it got right on outcome. A
   rejection being correct is far weaker evidence than a *selection* being
   correct, and no selection has yet been made or tested.

STNE and NKTR reported `pm` on 8/13 and are graded separately once their
moves are visible.

### What this changes about the existing playbook
Nothing about S1–S6 changes. This is an execution-layer option once the
account is approved: the same regime call and the same candidate list can be
expressed as stock (defined risk = position size × stop distance) or as a
long option (defined risk = premium paid, no stop needed since max loss is
capped by construction) — a genuine alternative, not a replacement. Decide
per-trade based on IV level and how much leverage the setup's conviction
justifies.

---

## What to build next, in order

1. **Regime classifier** — `get_market_pulse` plus the **7/20/65 SMA
   alignment test** on SPY, outputs the table above. The SMA filter is what
   makes this concrete rather than a judgment call, and it is three
   indicator calls. Highest value per line of code.
2. **A stop for S1** — the only live strategy is missing the one thing every
   source agrees on.
3. **Trade log** — Miner: no successful trader lacks one. Also the only way
   to settle the risk/reward conflict above with our own data.
4. **10% monthly drawdown halt** in `risk.py`.
5. **Close-strength filter** `(last−low)/(high−low)` from Oz's Power scan —
   cheapest genuinely new scan axis available. Every field needed is already
   returned by `get_equity_fundamentals`; no new data source.
6. **Decide the scan universe deliberately** — low-float momentum ($2–20,
   float ≤20M) or liquid higher-priced (Oz/Sincere). Currently the former by
   default rather than by decision, and three sources plus our own halt data
   argue for at least testing the latter.
7. Only then: S4/S5/S6 as running code.
