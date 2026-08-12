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
2. **No same-day round trips.** Cash settlement causes good-faith violations.
   T+1 changed when capital frees up, not this. Any strategy that buys and
   sells the same name the same day is blocked regardless of merit.
   (PDT is *not* the constraint — that rule was eliminated 2026-06-04; see
   `sources.md`. Settlement is.)
3. **~$28 balance, $5 per-order cap.** Spreads and commissions are large
   relative to position size, which is why the spread filter matters more
   here than it would on a larger account.

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
| **Volatile open, no daily trend** | Large first-15m range vs ATR | **S2 Opening Range Reversal** | BLOCKED — needs same-day round trip |
| **Range-bound / choppy** | **7/20/65 SMA filter NOT aligned** (see below), VIX mid, no breadth extreme | **S5 Range Trade** | DRAFT |
| **Trending down** | SPY below 50 SMA, breadth negative | **none possible** | Long-only. Correct action is sit out |
| **Event day** | High-impact econ release, VIX spike | **sit out** | Investing.com calendar check pre-open |

**Two of six regimes have a runnable strategy.** That is the honest coverage
number, and the down-day gap is structural rather than something to build.

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

## S2 — Opening Range Reversal (Pattern Scalp)  ·  **BLOCKED**

The most complete plan in the repo — and it cannot run. Kept because the
blocker is account structure, not strategy quality.

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
- **Blocker:** requires a same-day round trip → good-faith violation.

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
5. Only then: S4 as running code, or a range-bound strategy for the
   uncovered regime.
