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

## Glossary

Every acronym that actually appears in this file, `CLAUDE.md`, or
`sources.md` — not a general trading dictionary, just what's used here.

**Account & orders**
- **GFV** — Good-Faith Violation. Buying with unsettled funds and selling
  before those funds settle, in a cash account.
- **PDT** — Pattern Day Trader. A FINRA rule capping day trades in *margin*
  accounts under $25k. Does not apply here — this is a cash account, and
  the rule was eliminated for cash accounts regardless (see Account
  constraints below).
- **T+1** — Trade date plus one business day. How long a sale's proceeds
  take to settle before they're spendable again.
- **GTC** — Good-Till-Cancelled. An order stays open until it fills or is
  manually cancelled.
- **GFD** — Good-For-Day. An order expires unfilled at that session's close.
- **OCO** — One-Cancels-the-Other. A bracket order pairing an entry with a
  stop, where filling one cancels the other — referenced as a possible fix
  for S8's "naked for 11 minutes" gap, not yet confirmed available on this
  connector.
- **FINRA** — Financial Industry Regulatory Authority. Sets the PDT rule.
- **SEC** — U.S. Securities and Exchange Commission.
- **SLB** — Not an acronym in the account-value notes; it's the stock
  ticker for Schlumberger Limited. "$300 funded + ~$29 SLB" means ~$29 of
  pre-existing SLB share value, not a cash bonus.

**Price action & indicators**
- **OR** — Opening Range. The high/low of the first completed candle after
  the market opens (S2's core input).
- **ATR** — Average True Range. A volatility measure in dollars.
- **SMA / EMA / MA** — Simple / Exponential / (generic) Moving Average.
- **RSI** — Relative Strength Index. Momentum oscillator, 0–100.
- **MACD** — Moving Average Convergence Divergence. Trend/momentum
  indicator built from two EMAs.
- **ADX** — Average Directional Index. Measures trend strength (not
  direction).
- **VWAP** — Volume-Weighted Average Price.
- **TF** — Timeframe (e.g. "higher-TF trend").
- **OB / OS — ambiguous, means two different things in this repo:**
  - In **S4** (Dual Timeframe Momentum): **Overbought / Oversold** zones on
    an oscillator.
  - In **S7/S8** (options, and the "SMT+IDM+FVG+OB" chart tested
    2026-08-15): **Order Block** — a candle presumed to mark institutional
    positioning before a strong move. Read the section you're in.
- **FVG** — Fair Value Gap. A 3-candle price gap (candle 3's low above
  candle 1's high). Tested against real data 2026-08-15 — see `sources.md`.
  No measurable edge found.
- **IDM** — Inducement. A stop-hunt before the "real" move, per the same
  SMC chart as FVG/OB. Not independently testable with available tools —
  see `sources.md`.
- **SMT** — Smart Money Technique/divergence — comparing two correlated
  instruments for a divergence. Same chart, same caveat as IDM.
- **HOD** — High Of Day (appears in quoted Stocktwits chatter, not in our
  own rules).

**Options (S7)**
- **IV** — Implied Volatility. What the options market is currently pricing
  in, not a measure of the stock's actual past movement.
- **ATM / OTM / ITM** — At-the-money / Out-of-the-money / In-the-money.
- **DTE** — Days To Expiration.
- **OI** — Open Interest (contracts outstanding).

**Market context**
- **VIX** — CBOE Volatility Index. The market's overall fear/complacency
  gauge, used in the regime table.
- **SKEW** — CBOE SKEW Index. A tail-risk gauge — can run high even while
  VIX is calm.
- **MOVE** — ICE BofA MOVE Index. Bond-market equivalent of VIX.
- **SPY / QQQ / IWM** — ETFs tracking the S&P 500 / Nasdaq-100 / Russell
  2000, used for regime classification.

**Other**
- **M&A** — Mergers and Acquisitions (the HHS trade's catalyst type).
- **FDA** — U.S. Food and Drug Administration.
- **R:R** — Risk-to-Reward ratio.
- **MCP** — Model Context Protocol — how this session talks to Robinhood,
  Stocklake, and Stocktwits.

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

## Trade log — the only source of our own data

`trades.csv` (the record) + `tradelog.py` (the arithmetic). Added
2026-08-16, seeded from the broker's own order history rather than memory.
`python3 tradelog.py report` prints per-strategy results;
`tradelog.py open` prints live risk.

Every fill is tagged with the strategy that produced it. The CSV stores
only observed facts — entry, qty, initial stop, exit, realized dollars —
and all derived numbers are computed at read time so the file can never
carry a stale calculation.

**Results are reported in R, not dollars.** R = realized ÷ planned risk,
where planned risk is `(entry − initial stop) × qty`. This account funds
strategies unequally and always will; a $28 legacy position and a $150
momentum position are incomparable in dollars but directly comparable in R.
R is the only unit in which S1, S2 and S8 can ever be ranked against
each other.

### What n=5 already shows (2026-08-16)

| Strategy | n | W | L | Win% | Total $ | Avg R | Total R |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADHOC | 4 | 3 | 1 | 75% | +10.16 | +0.28 | +1.13 |
| LEGACY (SLB) | 1 | 1 | 0 | 100% | +0.39 | — | — |
| **All** | **5** | **4** | **1** | **80%** | **+10.55** | **+0.28** | **+1.13** |

Three findings, none of which needed a big sample:

1. **Expectancy is positive but thin: +0.28R per trade.** The process makes
   money per unit of risk. It is not broken.
2. **No trade has reached +1.00R.** Best was LNSR at +0.71R. Every winner
   was closed for less than the distance it was risking to earn. This is
   the single largest correctable leak — not entry selection, exits.
3. **Stop latency is excellent everywhere except S8.** Median 16 seconds
   from fill to live protective stop across five trades. HHS took **675
   seconds** (11m15s). The one S8 trade is the one unprotected window, which
   confirms the structural defect already flagged in S8's own section.

**What this log cannot tell us yet, and won't for a long time.** At roughly
five closes a month, splitting across three strategies yields ~1.7 trades
per strategy per month. Separating a 45% from a 55% win rate needs n in the
hundreds; even detecting a large difference between two strategies needs
n≈20–30 *each*, i.e. a year or more at this rate. **Do not expect the log to
rank S1 vs S2 vs S8 on edge this quarter.** What it detects within one to
three trades is mechanical: does the strategy fire, can it place an order,
does the stop land, is the cap respected. Fix mechanics first; edge
comparison is a later, slower payoff.

---

## Exits — the measured leak, and what actually fixes it

Tested 2026-08-16 on the four closed trades that have a recorded initial
stop, using real 5-minute bars. The earlier claim in this file was that
"winners are being cut short." That needed testing, because a sub-1R average
has two possible causes with **opposite** fixes: exits taken too early, or
stops set too wide for the move that was ever available. It is the first.

### Maximum favourable excursion vs what was captured

Walking each trade forward from its fill until its stop would have been hit:

| Trade | Risk/sh | MFE | MFE in R | MFE occurred | Actual | Captured |
| --- | --- | --- | --- | --- | --- | --- |
| SMWB | 0.6599 | +0.790 | **+1.20R** | 08/13 15:15 | +0.21R | 18% |
| RSKD | 0.2899 | +0.640 | **+2.21R** | 08/14 14:40 | +0.50R | 23% |
| LNSR | 0.5199 | +0.790 | **+1.52R** | 08/14 09:30 | +0.71R | 47% |
| AIRO | 0.8838 | +0.326 | +0.37R | 08/14 09:30 | −0.29R | — |
| HHS (open) | 0.2300 | +0.130 | +0.57R | 08/14 10:10 | — | — |
| AEYE (open) | 0.6199 | +0.490 | +0.79R | 08/14 12:25 | — | — |

**Average MFE available: +1.32R. Average captured: +0.28R. Capture
efficiency: 21%.** Three of four trades offered ≥1.0R. The move was there
and the stops were not too wide — the exits gave back four fifths of it.
SMWB was sold at 09:34 on 08/13; its high came at 15:15 the same day.

### Which exit rule would have captured it

Simulated with an explicit time stop so no rule benefits from holding
forever. Stop wins within-bar ties (conservative).

| Rule | Same-session stop | Next-session stop |
| --- | --- | --- |
| **Actual (hand exit)** | **+0.28R** | **+0.28R** |
| Target 0.75R | +0.49R | +0.31R |
| Target 1.0R | +0.68R | +0.50R |
| Target 1.25R | **+0.74R** | +0.64R |
| Target 1.5R | +0.56R | **+0.77R** |
| Target 2.0R | +0.56R | +0.55R |
| Target 2.5R | +0.56R | +0.55R |

Any fixed target in the **1.0–1.5R band roughly doubles expectancy** under
either horizon. Do not read the exact peak as the answer — it moves from
1.25R to 1.5R just by changing the time stop, which is what n=4 noise looks
like. The band is the finding; the peak is not.

### Two counter-findings worth more than the headline

**1. Breakeven and trailing stops made things actively worse.** Tested with
a fall-through to end-of-data, so these are directly comparable to each
other: break-even at +1R then trail 1R gave **+0.17R**, and arming earlier
at +0.5R gave **−0.03R** — both *below* the +0.28R of doing it by hand.
Moving the stop to breakeven converts ordinary pullbacks into scratch exits
and taxes exactly the trades that later work. "Move to breakeven once you're
up" is common advice; on this sample it is the worst rule tested.

**2. The discretionary exit helped on the loser.** AIRO was closed by hand
at −0.29R; every mechanical rule that let it run took the full −1.00R. So
the fix is asymmetric: **mechanise the upside, keep the time stop on the
downside.** A same-session time stop is what preserves AIRO's −0.29R, and it
is why the same-session column beats the next-session one at small targets.

### Recommended exit block, and the constraint that shapes it

Stop (already placed well — median 16s from fill) · limit target at
**~1.25R** · same-session time stop. On this sample: **+0.74R vs +0.28R.**

**The constraint: `place_equity_order` has no bracket or OCO.** Types are
market / limit / stop_market / stop_limit, single-leg only. There is a
`get_advanced_orders` *read* tool for OCO, but no placement tool. So a
resting stop and a resting limit target **cannot coexist on the same
shares** — whichever is placed first holds them. This is not theoretical:
it is exactly why Friday's $7.80 AEYE stop was rejected while the older
$7.08 GTC stop held all 19 shares.

Three ways to run the target given that, in order of preference:

1. **Place the bracket manually in the Robinhood app.** The app supports
   real OCO; `get_advanced_orders` can then read it back. This is the only
   option that gives a genuinely *resting* target needing no supervision.
2. **Agent-monitored target.** Leave the stop resting, and when price
   reaches the target during a session, cancel the stop and sell with a
   marketable limit. Requires the agent to be invoked during market hours —
   the same scheduling gap that blocks S2, so it is not free.
3. **Time-stop only.** Weakest, but still beats the current hand exit,
   and needs no intraday presence.

### Limits of this test

n=4 closed trades, one week, one regime, all from the same ad hoc screen.
Within-bar sequencing on 5-minute bars is assumed, not observed. The target
side is realistic — limit orders fill at the limit or better — but stop
fills can slip worse than modelled. Treat the 1.0–1.5R band as a working
hypothesis to be re-tested at n≥15, not as a settled parameter.

---

## Capital allocation — what is actually fundable

Account state 2026-08-16: **total $540.50** · equity $292.30 (HHS, AEYE) ·
**free cash $248.20**.

Open risk right now is **$19.37** (HHS $7.59 + AEYE $11.78) = **3.58% of
account**. House rules cap total open risk at 6% ($32.43), so **$13.06 of
risk budget remains**, and the 3%-per-trade cap ($16.22) is not the binding
constraint — the 6% total is.

**Running S1 + S2 + S8 in parallel is not fundable this week.** Three slots
at the $150 cap is $450 of notional against $248.20 free, and three new
positions would need roughly $25–35 of risk against $13.06 remaining. Both
constraints fail independently. The honest capacity is **one new position**,
sized to ≤$13.06 of risk.

The way to get parallel data on a small account is *sequential trades,
consistently tagged* — not simultaneous positions. One slot, filled by
whichever strategy has a valid setup that day, logged by strategy. Over
months that accumulates the same comparison without over-leveraging a $540
account into three concurrent bets.

**Slot priority when a slot is free:**

1. **S8** — the only strategy with a live, verified process and a positive
   logged expectancy. Gets first claim on a free slot.
2. **S1** — **does not get funded until it has a stop rule and a real
   allowlist.** A stopless multi-day trend position is the one structure on
   this account that can produce a loss larger than the whole risk budget in
   a single gap. Parking it is a risk decision, not a verdict on trend
   following.
3. **S2** — **do not fund. Backtested negative on real data 2026-08-16**
   (see its section). It is not in the allocation queue.

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
- **Size:** `config.json` sets `max_order_notional_usd: 150`. (Corrected
  2026-08-16 — this file previously claimed a "$5 notional cap", which the
  config has not carried for some time. Verified by reading the file.)

**Why S1 has never traded — verified 2026-08-16, and it is not the signal.**
Its universe is `daily_allowlist.json`, written by `screener.py`. **That file
does not exist in this repo.** S1's universe is therefore empty by
construction: the loop runs, finds nothing allowlisted, and buys nothing.
`deploy/crontab.example` is an example — nothing is scheduled, there is no
service running, and there are no run logs or state files. S1 is not a
strategy that was tried and failed. It is a strategy that has never been
invoked. The same is true of S2.

That reframes any comparison against S8: **S8 is not beating S1 and S2 on
results, it is beating them on having executed at all.** Do not read the
trade log as evidence about S1's or S2's edge until they have actually run.

**Open questions worth testing rather than guessing**
- 20/50 vs **20/60/100** (daytrading.com's version, where the 100 sets trend
  bias and the 20/60 cross triggers) vs **8/13** (Sincere). `backtest.py`
  exists and can settle this on real data.
- Miner's lookback-selection procedure applies here and is concrete: test
  several settings across 2-3 different periods and keep the one where
  reversals land within a bar or two of actual swing highs/lows without
  false mid-range crosses.

---

## S2 — Opening Range Reversal (Pattern Scalp)  ·  **TESTED — NEGATIVE. Do not fund.**

**Status changed 2026-08-16, from "VIABLE — top priority" to do-not-fund.**
It was never run live, and backtesting it on real bars before funding it is
the reason no money was lost on it. The full plan below is retained because
the *specification* is still the best-written one in this repo — the problem
is that the specification loses money.

### The test that killed it

`backtest_pattern_scalp.py` (already in the repo) run against **real
5-minute Robinhood bars**, 2026-06-15 → 2026-08-14, 29 trading days with a
valid ATR, across **12 underlyings**: SPY, QQQ, IWM, TLT, EEM, ARKK, KRE,
SOXL, TQQQ, XLF, SLV, GDX. Zero interpolated bars (checked, per the WOLF
precedent).

At the strategy's own default settings (OR 15m, ATR-frac 0.20, 90m window):

| Underlying | Trades | Win% | Total R |
| --- | --- | --- | --- |
| SLV | 3 | 100% | +10.24 |
| EEM | 6 | 67% | +1.87 |
| SPY | 5 | 60% | +1.35 |
| SOXL | 6 | 33% | +0.44 |
| XLF | 5 | 40% | −0.37 |
| TLT | 3 | 33% | −0.84 |
| KRE | 4 | 25% | −1.70 |
| IWM | 9 | 22% | −3.81 |
| ARKK | 7 | 14% | −5.61 |
| GDX | 10 | 20% | −6.72 |
| QQQ | 8 | **0%** | −7.69 |
| TQQQ | 8 | **0%** | −8.00 |
| **Total** | **74** | **27%** | **−20.84R** |

Exits: 20 target / 51 stop / 3 time. Average **−0.28R per trade**.

Only four of twelve were positive, and SLV's +10.24R came from **three**
trades — remove it and the remaining 71 trades total −31.08R. QQQ and TQQQ
went **0-for-8 each**.

### Two findings that make this decisive rather than suggestive

**1. It fails on the instruments it was designed for.** This is not a
wrong-underlying problem that a cheaper ticker would fix. SPY is marginally
positive on n=5; QQQ is 0-for-8 and IWM is −3.81R. The search for a sub-$100
underlying was therefore the wrong fix to the wrong problem.

**2. The core premise is inverted in the data.** A 5×4 sweep of
`atr_frac` ∈ {0.10, 0.15, 0.20, 0.30, 0.40} × entry window ∈ {30, 60, 90,
120} min, pooled across all 12 underlyings:

| atr_frac | 30m | 60m | 90m | 120m |
| --- | --- | --- | --- | --- |
| 0.10 | −0.29 | −0.33 | −0.31 | −0.29 |
| 0.15 | −0.28 | −0.31 | −0.29 | −0.28 |
| 0.20 | **−0.25** | −0.29 | −0.28 | −0.26 |
| 0.30 | −0.41 | −0.47 | −0.49 | −0.44 |
| 0.40 | −1.00 | −0.84 | −0.80 | −0.68 |

**0 of 20 parameter combinations is positive.** Best case is −0.25R. And
note the direction: the strategy's thesis is that a *larger* opening range
means a *bigger* liquidity grab and therefore a *better* reversal. The data
says the opposite — raising `atr_frac` from 0.20 to 0.40 degrades average R
from −0.25 to −1.00, monotonically. The filter that is supposed to select
the best setups selects the worst ones. That is a premise failure, not a
tuning failure, and tuning cannot fix it.

### Honest limits of this test

- Entry is a **reclaim approximation** (first 5m bar that trades below
  OR_low and closes back above), not a candle-by-candle hammer/engulfing
  match. A faithful pattern implementation could differ.
- Long-only, which is a real account constraint, so this part is fair.
- 29 trading days is one regime, and per-symbol n runs 3–10.

What it does *not* prove: that opening-range reversal never works. What it
does establish: **this specification, on real bars, at every setting tested,
loses — and its central filter works backwards.** That is more than enough
to keep it away from a $540 account. Reviving it requires a faithful pattern
entry and a fresh test, not a new ticker.

### Original plan, retained for reference

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
- **Capital:** uses settled cash for one round trip per day. At $540 account
  value with $248 free and a $150 order cap, that is one position, closed
  same day.
- **Config:** `config.pattern-scalp.json` already carries
  `max_order_notional_usd: 150`. (Corrected 2026-08-16 — this file previously
  said it "still carries the old $5 cap". It does not; verified by reading it.)
- **Universe problem, unresolved.** The strategy is written for a single
  liquid equity/ETF. SPY/QQQ/IWM are all >$150/share, so with a $150 order
  cap and no fractional-share support on stop orders, **S2 cannot place a
  single share.** It needs a sub-$100 underlying with a real opening range
  before it can run at all. This is the blocking defect, not the logic.
- **Blocker:** nothing invokes it. S2 must be called about every 5 minutes
  through the open. There is no scheduler; this container is ephemeral and
  cron dies with the session. In practice the agent has to be the scheduler,
  run interactively during the 9:30–11:30 window.

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

**STNE and NKTR — not yet gradable as of 2026-08-14 00:09 ET.** Both
reported `pm` on 8/13 (`get_earnings_results`, `verified: true`: STNE
$0.47 vs $0.46 est.; NKTR −$1.23 vs −$2.04 est.). By this section's own
rule — a `pm` report on D moves the stock on **D+1** — the move that
grades them lands in the **8/14 regular session, which has not opened
yet**. The after-hours tape is not a substitute, and this pair is a clean
demonstration of why.

**Corrected baselines.** The 8/13 closes are **STNE $10.23** and **NKTR
$75.92** (`get_equity_quotes` → `close`, `interpolated: false`, source
`sip-list-exchange-close`). The $10.25 / $75.89 figures in circulation
are `last_trade_price`, stamped 19:59:59.6Z and 19:59:56.1Z — the last
prints *before* the bell, not the closing auction. The errors are small
(+0.20% and −0.04%) but they are the denominator of the realized move,
so grade against the official closes.

**A known data gotcha recurred.** The 8/13 *daily* bars for both names
return `interpolated: true`, volume 0, flat at the 8/12 close ($10.00
STNE, $76.03 NKTR) — the day bar had not settled at pull time. Anything
differenced off the daily series would have measured a **0.00% move on
both** and graded the screen against a fabricated number. Same class of
defect as the WOLF synthesized-bar corruption; `get_equity_quotes`'s
`close` block is the sound source. **Check `interpolated` before
differencing anything.**

**Why after-hours cannot settle either name.** STNE's post-session was
liquid — 1.28M shares in the 4:00pm ET half-hour — but wildly unstable:
a $9.66 low and a $10.36 high inside that single bar, then a drift back
to $10.15 by 11:24pm ET. Against the $10.23 close that is anywhere from
**−5.57%** (spike low) to **−0.78%** (late print), implying the 7.80%
priced move was overpriced by somewhere between **1.4x and 10x**. A grade
that swings sevenfold on which timestamp you read is not a grade.

NKTR's post-session is worse and should not be used at all. After the
4:00pm bar the tape is a 2,000-share print at $71.555, then 200-, 100-
and 800-share prints near $75.05, with three `interpolated` volume-0 bars
filling the gaps. The quoted spread is **$73.62 × $77.14 = 4.67%** —
wider than the entire move being measured (−1.15% from the close). The
~5.9x-overpriced read after-hours suggests is arithmetically reproducible
but rests on ~3,100 shares and a spread that swamps the signal.

**Graded 2026-08-15 against the 8/14 regular session.** Baselines are the
official 8/13 closes; "actual" is the 8/14 settled close taken from the
daily bar with `interpolated: false` and real volume (STNE 11,366,249
shares, NKTR 828,396) — `get_equity_quotes` was still serving the 8/13
close a full day later, so the quote feed could not be used here.

| | 8/13 close | 8/14 close | **actual move** | market priced | own history | ratio | screen said |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STNE | $10.23 | $9.55 | **−6.65%** | 7.80% | 8.89% | 0.88 | "near-miss reject" |
| NKTR | $75.92 | $73.02 | **−3.82%** | 6.91% | 2.94% | 2.35 | "rich, AVOID" |

**Both rejections were correct on outcome** — but by far less than the
after-hours tape implied. STNE's options were overpriced **1.17x** the
realized move, NKTR's **1.81x**.

**STNE is the one worth studying, because the margin — not the signal — is
what saved it.** A ratio of 0.88 means the market priced *below* this
name's own history (7.80% vs an 8.89% median). Directionally the ratio was
pointing at "cheap, consider buying"; the only thing that prevented a
purchase was the requirement to clear **0.85**, rather than merely fall
under 1.00. The stock then moved 6.65% — less than the priced move *and*
less than the historical median — so a long option bought there would have
lost. **Had the gate been 0.90, this screen would have bought and lost
money.** That is the clearest evidence yet for keeping a real margin on the
edge test instead of gating at parity.

**NKTR is the case where the ratio measured the right thing.** It priced
6.91% against a 2.94% median, read 2.35, and the realized 3.82% came in
slightly *above* the name's own history while still landing far under the
priced move. Unlike ONDS on 8/13 — which got a correct no-buy from a "fair"
1.01 reading by luck of the baseline — NKTR's verdict and its mechanism
agree.

**The after-hours tape was wrong by roughly 3x on both, in the same
direction.** After-hours suggested ~3.2x (STNE) and ~5.9x (NKTR)
overpriced; the regular-session answers are 1.17x and 1.81x. The
overstatement is traceable: STNE's post-session put a $9.66 low and a
$10.36 high inside a single bar, and NKTR's rested on ~3,100 shares behind
a 4.67% spread. Refusing to grade off that tape was not excessive caution —
doing so would have overstated the screen's success threefold.

**Running tally, stated with the same caution as before.** Four contracts
graded across two days — ONDS 3x, LUNR 24x, STNE 1.17x, NKTR 1.81x — and
every one had options overpriced relative to the realized move, consistent
with the IV-crush literature in `sources.md`. But the spread between 1.17x
and 24x is enormous, and **all four are rejections.** Zero selections have
been made or tested. A screen that says no to everything scores 4-for-4 on
a tape where premium was uniformly rich; that is not the same as having an
edge, and it will not be until a contract passes and is held to a result.

### What this changes about the existing playbook
Nothing about S1–S6 changes. This is an execution-layer option once the
account is approved: the same regime call and the same candidate list can be
expressed as stock (defined risk = position size × stop distance) or as a
long option (defined risk = premium paid, no stop needed since max loss is
capped by construction) — a genuine alternative, not a replacement. Decide
per-trade based on IV level and how much leverage the setup's conviction
justifies.

---

## S8 — Verified Catalyst Momentum  ·  **DRAFT — n=1, not yet proven**

Source: **not a book.** Every rule below was pulled from a trade or a
rejection that actually happened this week (2026-08-11 through 2026-08-15),
not from Miner, Sincere, Passarelli, Oz, Warrior Trading, or DailyFX. It
exists because a gap showed up in the account's own results: four days of
trading, and every dollar of realized P&L came from the ad hoc day-trade
equity screen (SMWB/RSKD/LNSR/AIRO, +$10.16) while S1–S7 — the actual
book-sourced strategies — contributed zero trades between them. S7 racked
up four rejections and no fills; S2 was flagged top-priority for days and
turned out to be unrunnable on any major ETF at this account's size before
it ever placed an order. S8 is an attempt to write down, as a real Miner-
format plan, what the informal process that's been carrying the account was
actually doing right, so it can be tested and improved deliberately instead
of staying implicit.

**Setup.** A verified, named catalyst: a signed/definitive agreement, an
SEC filing, an FDA action, or a wire-confirmed news item with a source that
can be checked (Stocktwits linking to a primary source, `get_stock_news`
with a real article, `get_earnings_results`). Chatter, "partnerships
coming," unexplained relative volume, and newsletter/promoter picks do not
count, no matter how clean the numeric pillars look.

**Disqualifier — revised 2026-08-16 after backtesting the original
threshold, see below.** Elevated float turnover with no catalyst is a
*secondary* warning sign, not the numeric gate the first draft made it.
**The catalyst check is the actual disqualifier; turnover only supports
it.** The full-day evidence for this correction is in the backtest section
immediately below — the short version is that turnover magnitude doesn't
predict outcome severity, and turnover is actively suppressed (and
therefore misleading) on the exact names that are halting the most.

**Entry.** Stop-limit above the pre-move resistance / bar high — never a
market order, never bought into the target price. Confirmation first, per
Miner and per what actually filled HHS at $4.37 against a $4.35 breakout
level.

**Stop.** Below the pre-breakout swing low, placed **the instant the
position fills**, not on the next scheduled check. This is the one place
S8 already knows it has a bug: HHS sat naked for 11 minutes between fill
(10:06am) and stop placement (10:17am) because the entry was conditional
and got monitored on a timer instead of continuously. A conditional entry
needs either a bracket/OCO order (if this connector supports one) or
continuous monitoring through the fill — a scheduled check-in cannot
deliver "at the moment of entry."

**Exit.** Two different endings depending on the catalyst type, not yet
both tested:
- **Capped catalyst** (M&A, tender offer) — target is the deal price itself,
  discounted for deal risk and consideration type (HHS is cash *and*
  preferred stock, not all-cash, which is why it trades under $5.00 rather
  than converging to it). Not an open-ended momentum hold.
- **Uncapped catalyst** (earnings beat, FDA approval, contract win) — trail
  the stop up per house rules once a real gain shows. Not yet tested live
  under S8; no example this week was this type.

**Size.** Unchanged house rule: risk ≤3% of account per trade, ≤6% across
all open positions, notional ≤$150 per order.

### Float-turnover backtest (2026-08-16) — the threshold didn't survive, the catalyst check did

**What was actually available to test.** `run_scan` only evaluates live
market data — it cannot be replayed against a past date, and it was the
weekend when this ran, so no fresh independent scan population existed.
The honest test available with real data: pull the full 8/14 daily bar
(open/high/low/close, real volume) for the 11 names flagged that day and
check whether elevated turnover actually predicted what the rule assumes —
that the move fails to hold. This is **one day, n=11, all names already
selected by the same screen** — a real test, not a toy, but not an
independent out-of-sample backtest either. That caveat matters for how
much weight to put on what follows.

| Symbol | Turnover (day vol ÷ float) | Giveback from day's high | vs. day's open |
| --- | --- | --- | --- |
| CGTL | 1,171.6× | −18.6% | −12.3% |
| LBGJ | 788.0× | −23.7% | −15.9% |
| ONFO | 731.0× | −57.4% | −4.1% |
| WETO | 95.8× | −36.5% | −22.8% |
| STKH | 49.3× | −44.1% | −33.2% |
| SXTC | 30.2× | −10.9% | −5.9% |
| AKAN | 26.1× | −25.4% | −17.4% |
| DFSC | 10.2× | −8.8% | +15.8% |
| LFS | 2.5× | −41.4% | −0.4% |
| AEHL | 2.0× | −37.2% | +10.5% |
| NMAX | 0.8× | −6.2% | +9.9% |
| **HHS** (kept, real catalyst) | 0.7× | −4.4% | +1.7% |

**Finding 1 — the threshold number is not supported.** Turnover magnitude
does not predict giveback magnitude. CGTL ran 1,172× its float and gave
back "only" 18.6%; STKH ran a comparatively modest 49× and gave back
44.1%. There is no monotonic relationship in this sample, so picking 20×
vs. 30× vs. 50× as *the* cutoff was arbitrary from the start — it fit the
eight examples on hand, not a real distribution.

**Finding 2 — turnover is actively unreliable exactly when it matters
most.** AEHL — the name that was *observed halting live* on Stocktwits —
shows the second-lowest turnover in the table (2.0×). Halts cap how many
shares can trade, which suppresses the metric precisely on the riskiest
names. A rule that goes quiet during a halt is worse than no rule.

**Finding 3 — the catalyst check is the one doing the real work.** LFS
(2.5× turnover — would not have tripped even the loosest version of the
threshold) still failed exactly like the high-turnover names: −41.4% from
its high, finishing the day essentially flat (−0.4% vs. open) despite an
intraday spike to $4.13. It was caught by "$LFS news??" going unanswered
on Stocktwits, not by any number. Turnover would have missed it entirely.

**Finding 4 — one real miss, and it's instructive.** NMAX gave back only
6.2% from its high and finished **up** 9.9% vs. its open — better than
several names that passed the numeric pillars. It was rejected purely on
"zero news in 3 days," and the price action didn't clearly vindicate that
call the way it did for the other nine. Worth remembering the disqualifier
isn't infallible even on its stronger leg.

**What changed as a result:** the Disqualifier section above now reads
"catalyst check is the gate, turnover is supporting evidence" instead of
treating them as two co-equal numeric pillars. This is a demotion, not a
removal — elevated turnover with no catalyst is still worth noticing, it
just isn't a number to trust on its own, and it should never substitute
for the catalyst check the way a bright-line gate might tempt someone to
use it.

**What is not yet true about this strategy, stated plainly:**
1. **n=1 on live trades.** HHS is the only trade run under something
   resembling these rules, and it was still open (unrealized −$2.81 as of
   the 8/14 close) when this was written. One trade proves nothing.
2. **The turnover backtest above is one day, not independent samples.**
   All 11 names came from the same screen on the same day — it cannot rule
   out that day's specific conditions shaping the result. A durable answer
   needs this same check repeated on independent future days, accumulated
   over time, the way the FVG test used a full year of independent daily
   bars (`sources.md`, 2026-08-15: 43 bullish FVGs, no edge over baseline).
3. **The ad hoc screen's 4-for-4 record (SMWB/RSKD/LNSR/AIRO) was not run
   under this exact rule set.** It's the reason S8 exists, but it wasn't
   S8 — so that record cannot be cited as S8's track record, only as its
   motivation.
4. **The exit rule is asymmetric and only half-tested.** Nothing this week
   exercised the uncapped-catalyst trailing-stop path.

**Status: still DRAFT.** The float-turnover threshold has now been tested
and demoted rather than validated — that is real progress, not a setback,
since a wrong number sitting in a "gate" position was a bigger risk than
an honest "we don't fully trust this yet." Promotion to LIVE waits on live
trades accumulating under the corrected rule set. Do not treat this as
validated by this week's account performance; the account was profitable
this week because of the process this formalizes, not because of this
document.

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
