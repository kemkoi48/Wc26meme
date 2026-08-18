# Operating notes — read this first

My own standing instructions for this repo. Separate from `strategies.md`
(trading content) and `sources.md` (research log) — this file is about how
I work, not what I trade.

## RULE ZERO — real data, or say nothing. No guessing, ever.

Stated by the user on 2026-08-17 as **the core architecture of this
project**: *"there should be no guessing game while we are analyzing and
build."* This outranks every other rule in this file. When it conflicts
with being fast, being helpful, or having an answer ready, it wins.

**Every number that reaches the user, a file, or a decision must be
traceable to a tool call I actually made.** Not to a plausible estimate,
not to a remembered figure, not to what a number "should" be.

Concretely, and each of these has already gone wrong here at least once:

- **Never invent a threshold.** Derive it by measuring, then say what was
  measured. `scalp_signal.py`'s 3x surge / 2% return came from 1,530 real
  minute bars; the ENVX historical moves came from real daily bars. An
  early draft of `test_option_math.py` used *invented-but-plausible*
  historical moves and flipped the verdict from "reject" to "buy" — the
  exact failure this rule exists to prevent.
- **Never read a number off a screenshot and treat it as data.** Screenshots
  are a pointer to where the real data lives. On 2026-08-17 I reconstructed
  the user's trades from images, then re-pulled them from
  `get_equity_orders` — the second version had exact timestamps that
  changed the conclusion (median hold 149s, which no screenshot showed).
- **Never let a stale pull stand in for a live one.** Stocklake's movers
  returned byte-identical numbers 6.5 hours apart on 2026-08-17; quoting
  them as "current" would have been fabrication by omission. Cross-check
  against a second source before calling anything live.
- **Never report a computed result without the check that could break it.**
  A +709% backtest that is 86% three trades on one symbol is not a +709%
  backtest. Run the concentration/outlier check *before* reporting, not
  after being asked.
- **Discard synthesized bars before computing anything.** `interpolated:
  true` and zero-volume bars are fabricated gap-fill. WOLF returned 169 of
  331 such bars and turned a violently volatile name into a calm one.
- **"I don't have that data" is a complete and acceptable answer.** So is
  "that pull looks stale, let me verify." Guessing to avoid saying either
  is the failure mode.

When I state a number, I should be able to name the tool call it came from.
If I can't, I don't state it.

## A promise is not an action until a tool call backs it

On 2026-08-12 I told the user "next check ~3:15pm, flatten-or-hold at
~3:40pm" and then never called `send_later`. The sentence felt like
enough. It wasn't — nothing fires from prose. Rule: any time I say I'll
check back, follow up, or reassess at a later point, the scheduling tool
call happens in the same turn, before I say it's done. If I can't make
the call right then, I say "not yet scheduled" instead of implying it is.

Redundancy beats a single point of failure: for anything consequential
(an overnight position, a pending decision), book a second, independent
verification check rather than trusting the first one to re-arm itself.

## Strategy index — filter here before re-reading strategies.md in full

| ID | Name | Status | Source | Note |
| --- | --- | --- | --- | --- |
| S1 | Trend Follow | WIRED BUT NEVER INVOKED | Miner + DailyFX SMA filter | Multi-day. **Has no stop** — that is its real defect, and it must not be funded until it has one. 2026-08-16: verified `daily_allowlist.json` does not exist, so its universe is empty by construction; nothing has ever been scheduled. It has not failed, it has not run. Wrong fit for the stated day-trade aim regardless. |
| S2 | Opening Range Reversal | **TESTED — NEGATIVE, do not fund** | Sincere / Miner | Best-written spec in the repo and it still loses. Backtested 2026-08-16 on real 5-min bars, 29 days, 12 underlyings: 74 trades, 27% win rate, **−20.84R**, avg −0.28R. Fails on SPY/QQQ/IWM too (QQQ 0-for-8), so it was never an underlying problem. **0 of 20 parameter sets positive**, and raising the ATR filter monotonically worsens results — the premise is inverted. Never traded live; the cap blocker was protective. |
| S3 | Low-Float Momentum Scan | RESEARCH ONLY — **do not modify without an explicit request** | Warrior Trading | 5 pillars: relative volume, % change, price range, float, catalyst (non-numeric, hand-checked). `momentum_scanner.py` structurally cannot place an order. Keep separate from ad hoc day-trade screening even when they overlap. |
| S4 | Dual Timeframe Momentum | DRAFT, never run | Miner | |
| S5 | Range Trade | DRAFT | DailyFX | |
| S6 | Oz scan family | Logged; close-strength adopted elsewhere | Tony Oz | |
| S7 | Options (long calls/puts) | DRAFT, option_level_2 confirmed live | Passarelli + own catalyst-mismatch research | `option_math.py` + `option_scanner.py` built, unit-tested (`test_option_math.py`). Six contracts graded across three live runs (ONDS, LUNR, STNE, NKTR, ZIM, BULL), all six rejections, zero trades placed. 2026-08-17: added a second track for catalysts with no dated trigger (insider activity, sentiment, general hype) — `SoftCatalystScanConfig`/`evaluate_soft_candidate`/`apply_soft_filters_and_rank`, edge test is IV vs. this stock's own realized volatility rather than vs. a historical-event sample. Not yet run live; see strategies.md S7. |
| S8 | Verified Catalyst Momentum | DRAFT, n=1 live trades, catalyst gate backtested | Not a book — reverse-engineered from this week's own trades and rejections | Written 2026-08-15 after noticing S1–S7 had contributed zero trades while the ad hoc screen carried the account. 2026-08-16: the float-turnover disqualifier was backtested (single day, n=11, not independent) and **demoted** — turnover magnitude didn't predict outcome and was actively suppressed on the one name that was halting. The catalyst check is the real gate now; turnover is secondary. See S8's "Float-turnover backtest" subsection. |
| — | Day-trade equity screening (SMWB/RSKD picks) | Ad hoc, hand-run each time | Saved Robinhood scans + Stocktwits catalyst check | NOT S3. Don't conflate a finding here into a reason to edit S3. This is what S8 is trying to formalize — but S8 is not yet proven, so this ad hoc process stays the working method until S8 earns LIVE status on its own results. |

Read this table before re-deriving a strategy's status from scratch.

## "It doesn't work" vs "it never ran" — check which one first

2026-08-16. The account's entire P&L came from ad hoc screening while S1–S7
contributed nothing, and the obvious reading was that the formal strategies
had no edge. That reading was wrong. S1's allowlist file does not exist and
S2 cannot place a single share of a $600 ETF under a $150 cap — **neither
has ever placed an order.** Before concluding a strategy underperforms,
verify it executed: look for its universe file, its state/log artifacts, and
real fills in the order history. Absence of trades is far more often a
plumbing failure than a signal failure, and the two call for opposite fixes.

Related: this file's own strategy notes drifted. `strategies.md` claimed
both S1 and S2 still carried "the old $5 notional cap" when both configs
have read `max_order_notional_usd: 150` for some time. Re-read the config
before repeating a number from prose.

## Monday morning plan (2026-08-17) — hot potato strategy

This week: test the "hot potato" effect from trader data (see premarket.py). Key insight: when the #1 leading gainer gets extended (up >20%), trader attention flows to #2-3 gainer with fresh catalyst. This is where the cleanest entry happens, 8:40am-9:15am.

**Workflow:**
1. **Sunday evening:** Print premarket-checklist.html, review RULES.md
2. **7:00am - 8:30am:** Scan top 5 gainers. Fill in the checklist. Identify which one looks "obvious" to most traders.
3. **8:40am - 9:15am:** Enter on breakout or bounce of freshest gainer (not extended #1)
4. **Place stop within 60sec (Rule 3).** Pre-calculate target (Rule 4).
5. **9:15am - 10:00am:** Exit at target or stop (Rule 5/7). Close by bell if no hit.
6. **10:00am+:** Avoid high-risk zone (trader data shows big losses cluster here)

**Log all fields** in trades.csv, especially: entry_time, extension_level (fresh_5%, extended_20%, etc.), float_millions, catalyst_source. After 10 trades, this data will show whether 8:40-9:15am is real for your method.

## Results go in trades.csv, in R, or they don't count

`trades.csv` + `tradelog.py` (added 2026-08-16, seeded from broker order
history). Every fill gets logged with the strategy that produced it, and
comparisons are made in R (realized ÷ planned risk), never in dollars —
strategies on this account are funded unequally, so dollars cannot rank
them. Log at entry time, not by reconstruction: the initial stop is what
makes R computable, and it is the field most easily lost after the fact.

## Strategies stay separate unless told to merge

A problem noticed while running one strategy (e.g. S3's float cap looking
wrong for a day-trade equity pick) does not get fixed by editing that
strategy. It gets parked, or becomes its own thing, only on explicit
instruction. 2026-08-13 precedent: the WEN float-cap question came from
day-trade screening, not S3, and stays off S3.

## Research posture

The user supplies source material (books, guides) when they have it. I
have standing permission to WebSearch for how real/expert practice
handles a specific question — expected-move mechanics, IV rank, lotto-play
base rates — rather than waiting to be handed a source. Log findings in
`sources.md` the same way as book-derived material: attributed, not
guessed, cross-checked against more than one source before treating a
claim as fact (see the 2026-08-12 GFV correction — verify regulatory or
mechanical claims before writing them into a strategy file).

## Stocklake Pro — available, but check coverage before relying on it

Pro tier went live on the account 2026-08-13. Unlocks the AI-pipeline
tools: `get_stock_research` (full bundle: AI summary, verdict, flag score,
news sentiment, insider/institutional signal), `get_insider_activity`,
`get_stock` pro blocks (rating, stance_signals, relative_strength vs
SPY/QQQ/sector), `get_screener`, `get_indicator_history`. The server is
connected at the platform level in this session — there is nothing to
install in this repo, and the bearer token must NEVER be written into any
committed file. It belongs in `.env` (gitignored) if it is needed at all.

**Coverage limit, verified 2026-08-13, not assumed:** the universe is
~3,501 symbols and is NOT complete. Both of that day's live positions —
RSKD and SMWB — returned `symbol_not_found` from `get_stock`,
`get_stock_research`, AND `get_insider_activity`. AAPL returns full data.
So Pro covers large/mid caps well and misses exactly the small-cap
day-trade names our momentum screening actually surfaces.

Consequence: Pro does NOT close S3's 5th-pillar catalyst gap or S7's
catalyst-verification gap for small caps. Stocktwits + Robinhood
fundamentals remain the working catalyst check for those. Always try the
symbol before assuming Pro has it; treat `symbol_not_found` as a routine
coverage miss, not a tool failure.

## Robinhood's own saved scanners — prefer these over a third-party screener

The account has real saved scanners (`get_scans` / `run_scan`, built in
Legend, not created by this agent). Verified live 2026-08-18: "Early
Momentum Ignition" (scan_id `9d3566de-aca8-4b0e-8099-304a3e474d92` — price
$2-20, float <20M, 1h relative volume >3x) independently surfaced IPST and
WFF, the user's own traded symbols, and its top mover (XOS) checked out
against real 5-minute bars. User's own words, 2026-08-18: "robinhood has
everything. you can refine it thats all."

Use `run_scan` on this scan_id as the primary momentum coarse filter —
it's sourced directly from the broker (same feed orders execute against,
no second vendor that can go stale), and it already has float + hourly
relative volume built in, which Stocklake's `get_screener` doesn't. A
looser secondary net exists too: "Warrior Trading Style - Low Float
Volume Movers" (scan_id `32ff11e9-065f-40b0-99a0-c5971241c435`). Stocklake
still has a job downstream of this — `get_stock_research` and
`get_insider_activity` for catalyst/insider verification once a candidate
is found — just not as the scanner itself. See sources.md for the full
test.

**2026-08-18 overnight: checked every remaining saved scan and both
accounts' positions/orders directly** (user: "check my other saved scans
too... anything that is similar and seems important do it"). Account
safety confirmed real, not assumed — Agentic account flat, real account's
only resting-looking orders were rejected, never live. One dead position
found (`ACETQZZ`, inactive/delisted, confirmed via `get_equity_quotes`
erroring `inactive_instruments`) — informational, nothing to act on.
Added "Warrior Trading Style" (scan_id `32ff11e9-065f-40b0-99a0-c5971241c435`)
as a second scan net alongside Early Momentum Ignition — found real new
candidates (AUUD, IVF) the first scan missed. Two more real, working
scans found (options IV/volume — S7's territory; RSI/ADX trend — could
unblock S1's missing allowlist someday) but deliberately NOT wired into
the scalp dashboard — different strategies, logged in sources.md only.
Full detail: sources.md, "All saved Robinhood scans checked" entry.

## Using Stocklake tools for trade screening

Stocklake is available as a connector at the platform level (authentication handled
by Claude, no local config needed). Use these tools to verify catalysts and detect
insider trading signals:

**For insider activity check:**
```
mcp__Stocklake__get_insider_activity(symbol="AEYE")
```
Returns recent insider buys/sells/exercises with insider names, titles, amounts.
Look for a **trend** (accumulation/distribution) — distribution by officers often
precedes halts or reversals in small caps.

**For research verdict + sentiment:**
```
mcp__Stocklake__get_stock_research(symbol="AEYE")
```
Returns verdict (BULLISH/BEARISH/NEUTRAL), tape sentiment, relative strength vs
SPY/QQQ/sector. When this contradicts `get_signals`, research wins — it includes
tape response to the catalyst.

**For signals (headlines + news sentiment):**
```
mcp__Stocklake__get_signals(symbol="AEYE")
```
Returns headlines and AI-scored conviction. But NEVER trade off this alone —
always cross-check with `get_stock_research` first (see MLTX example below).

**For quick watchlist/data:**
```
mcp__Stocklake__get_stock(symbol="AEYE")
```
Returns fundamentals, relative strength, insider/institutional signal flags.

**Manual control:** Call these tools only when you need fresh data. There is no
auto-refresh hammer. The connector resets daily (midnight UTC), same quota as the
ChatGPT screener was using. Use them deliberately: daily pre-market check on open
positions (batch `get_insider_activity`), weekly deep dive on candidates
(`get_stock_research`), never mindlessly refresh.

**Coverage note:** Same limit as before — large caps return full data, small caps
often return `symbol_not_found`. RSKD and SMWB (our live trades) were both missing
2026-08-13. Fall back to Stocktwits + Robinhood fundamentals for small-cap catalyst
verification.

## NEVER trade off get_signals alone — cross-check get_stock_research

Verified 2026-08-13 on MLTX. `get_signals` returned LONG, conviction 9/10,
flag_score 9/10, sourced from the news pipeline: "Sonelokimab met primary
endpoint in Phase 3." Same symbol, same day, `get_stock_research` returned
**verdict BEARISH, near_term BEARISH**, headline "Positive Ph3 data can't
stop the bleeding — insiders selling, tape rejecting catalysts."

The reconciling facts: the stock FELL 5% on the Phase 3 headline; CEO, CFO
and CSO sold $6.1M in clustered June-July sales with zero insider buys;
negative relative performance vs SPY across every window; down 72.5% from
its 52-week high.

`get_signals` reads a headline and scores the NEWS, not the market's
response to it. `get_stock_research` adds tape, insider flow, and relative
strength. When they disagree, the research bundle is the one that
incorporates whether the catalyst actually worked. Standing rule: any
candidate sourced from `get_signals` must be cross-checked with
`get_stock_research` (and insider_trend) before it goes anywhere near a
trade. A bullish catalyst that the tape is rejecting is a trap, not an
opportunity.

## No OCO for equities — a stop and a target cannot both rest

Verified 2026-08-16 against the tool schema. `place_equity_order` offers
market / limit / stop_market / stop_limit, **single-leg only**. There is a
`get_advanced_orders` read tool for OCO, but nothing that *places* one. So
two resting sell orders cannot cover the same shares — whichever lands
first holds them and the second is rejected.

This already bit us: Friday's attempt to put a $7.80 stop on AEYE failed
because the older $7.08 GTC stop held all 19 shares. Do not plan any
strategy around a resting stop-plus-target bracket placed through this
interface. Either the user places the bracket in the Robinhood app (which
does support real OCO), or the agent has to monitor intraday and swap
orders — and monitoring needs the agent invoked during market hours, which
is the same gap that blocks S2.

## Verify before writing a conclusion into strategies.md

Two live corrections this repo has already needed: the ENVX
"not-a-mismatch" call was first argued from IV alone and was wrong until
the real historical earnings moves were pulled; the WOLF historical-move
calculation was corrupted by 169 synthesized bars until `interpolated`
was checked. Default to pulling real data over reasoning from a plausible
number, especially before a conclusion gets committed to the repo.
