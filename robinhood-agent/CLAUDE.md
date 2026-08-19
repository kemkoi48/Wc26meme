# Operating notes — read this first

My own standing instructions for this repo. Separate from `strategies.md`
(trading content) and `sources.md` (research log) — this file is about how
I work, not what I trade.

## Scalp scanner is now live-trading authorized — Agentic account only

User, 2026-08-18 ~09:31 ET, verbatim: **"you do your trading in your
agentic account."** This is a standing authorization, not a one-off: when
the two-scanner market scan (`scalp_signal.detect_entry`, see
`scalp_scan.py`) fires — on the core four OR a fresh market-scan
candidate — place the trade for real in account `432805174` (Agentic,
`agentic_allowed: true`). Do not just report a fire on the dashboard and
wait for the user to act; execute it, following the existing risk rules
in `RULES.md` that aren't strategy-specific:

- **Rule 2 sizing**: max $150 per buy. Checked 2026-08-18: account cash
  $544.74, zero open positions, so a $150 buy is affordable and leaves
  room for the 6% total-risk cap across positions.
- **Rule 3**: GTC stop placed within 60 seconds of the fill, at the
  signal's `stop_price` (entry − 2%, from `scalp_signal.py`).
- **No fixed target** — this is the scalp exit, deliberately different
  from S8's Rule 4/5. Exit on `decide_exit`'s trail trigger (close below
  the prior bar's low) or the 15-bar time stop. Re-check `decide_exit`
  each refresh while a scalp position is open.
- Log every fill to `trades.csv` immediately, same as any other strategy.

Verified same session: a fire that goes stale before it's acted on
un-fires — SGLY fired at 8:40 ET ($7.44, stop $7.29) and by 9:31 ET had
fallen to $6.25, well past where the stop would have triggered. Never
trade a signal off a timestamp older than the refresh that's about to
place the order; re-run `detect_entry` on fresh bars immediately before
buying, not on what the dashboard last showed.

**First live trade, 2026-08-18 10:18 ET (IPST, 13 sh @ $10.75):** stop
landed 105 seconds after the fill, missing Rule 3's 60-second target —
several `get_equity_orders` polls were spent confirming the fill before
the stop went in. `place_equity_order` returns `state: unconfirmed` or
`confirmed` immediately; it does NOT mean filled. Next time: poll faster
and tighter (don't interleave dashboard/quote work between fill checks),
and consider whether a marketable limit that's virtually certain to fill
(deep book, tight spread) can go straight to placing the stop order
provisionally rather than polling to confirm first — worth testing, not
yet decided.

## RULE — a placed stop is not a real stop until its state is verified

**The failure that made the above lesson worse, same trade, same day.**
The GTC stop for the IPST trade was placed at 14:20:26 ET (`stop_price:
10.54`) and I moved on, treating "order submitted" as "position
protected" — exactly the gap Rule Zero exists to prevent, and I made it
anyway. The stop was actually **rejected** by the broker seconds after
submission (`state: rejected`, no resting order, no protection at all).
Nobody caught it — not me, not a scheduled refresh — until the user
asked, ~3 minutes later, "make sure to sell it on time." By then the
price had already fallen from $10.75 to $9.61-9.87, past where the -2%
stop would have triggered. Sold at market for -$14.56 (-5.33R) instead
of the ~$2.73 (-1R) the stop was supposed to cap it at. Root cause of
the rejection itself is still undiagnosed — flagged in trades.csv row 9,
needs checking before the next live scalp trade.

**Standing rule now: after placing ANY protective order (stop, GTC
sell), re-check its state within the same turn before considering the
position protected.** `place_equity_order` returning a response is not
confirmation the order is live — `confirmed` can still flip to
`rejected` moments later, silently, with no separate notification. A
stop that isn't verified resting is not a stop; it's a belief.

## The Agentic account is a CASH account — proceeds don't settle same-day

Discovered 2026-08-18 10:49 ET, mid-session, real money: a 4th scalp trade
(XOS, freshly fired) was rejected with "Not enough buying power," even
though `get_portfolio` showed `cash: $524.38`. The real spendable figure
was `buying_power: $110.65` — proceeds from that morning's three closed
trades (IPST, SXTC, WFF) hadn't settled yet. This account is `type: cash`
per `get_accounts`, not margin, so a sell's proceeds are not spendable
until settlement (typically T+1), regardless of the cash balance shown.

**Before sizing a buy at the $150 Rule 2 cap, check `buying_power` from
`get_portfolio`, not `cash`.** If a position closed earlier the same
session, assume its proceeds are NOT available for the next buy until
confirmed otherwise. This will keep recurring on any day with multiple
round-trip scalp trades — it is not a one-off. By the time this was
diagnosed, XOS had fallen from its $4.70 signal to $4.35 (past its own
stop level) and was correctly skipped rather than chased — but a faster
buying-power check would have caught this before the signal went stale,
not after.

## Profit-lock trail added to `decide_exit` — 2026-08-18

User: "we are happy at 5% profit but if the momentum is there sell it at
high." `scalp_signal.decide_exit` now arms a trailing exit once a trade
has PEAKED at +5% or more, then exits on a 2%+ pullback from that peak —
not a fixed target, still lets a running trade keep running. See the
module docstring's "ADDED 2026-08-18" section and `PROFIT_TRIGGER_PCT` /
`PROFIT_TRAIL_PCT` for the numbers, which are the user's stated comfort
level and the stop's distance, not independently backtested. Tests added
in `test_scalp_signal.py`; two pre-existing tests were adjusted because
their bar values happened to cross the new +5% trigger, changing which
rule fired first — not a regression, the new rule firing there is correct.

## Long-run growth sleeve — new, 2026-08-18, agent-executed

User, verbatim: *"you know what your strategy will be fast growing
investment not the day trading and option trading... day trading is not
feasible with your situation... You will be help me screen I will
execute the day trade but you will trade yourself for long run."* Split
of responsibility, effective immediately:

- **Day trading (Surge Watch, scalp_signal.py)**: screening only from
  here on. The dashboard still refreshes and reports fires, but the
  autonomous 5-minute self-chained trading loop is OFF (user: "stop
  surge watch screening for now" — the recurring `send_later` chain was
  cancelled). The user executes any day-trade fire by hand.
- **Long-run growth (growth_signal.py, new)**: agent-executed, same
  Agentic account (432805174), same capital, funded as it settles —
  no separate account or carve-out requested.

**Entry screen**: Robinhood saved scan "Growth Momentum (long-run)"
(scan_id `2514847d-25cb-4628-9731-bb5b0ee7d246`) — market cap >$1B, RSI
50-70, 1-month change >5%, ADX>20, avg volume >500k. See
`growth_signal.py`'s module docstring for the full derivation, including
the unit-conversion bug caught before trusting the filter (the % Change
expression returns a decimal ratio, not a percentage — an early draft
demanded a 500% monthly move and matched zero instruments).

**Exit**: a wide 18% trailing stop from the peak price since entry
(`growth_signal.TRAIL_PCT`) — user chose "wide" over scalp-style 2% and
over no stop at all. This is the user's stated risk tolerance, not a
backtested number.

**RULE — fractional-share equity orders cannot carry ANY stop trigger.**
Discovered live 2026-08-18, the growth sleeve's first trade (trades.csv
row 12). Tried a GTC stop_market on a 0.607998-share PLTR position:
rejected, `"Invalid time in force for fractional order"`. Tried GFD
instead: rejected again, `"Invalid trigger for fractional order"` — so
it is not a time-in-force problem, fractional orders reject the `stop`
trigger outright, confirming and sharpening the existing "Fractional
shares: only on type=market" line in `place_equity_order`'s own
parameter docs. **Consequence: a fractional buy for this sleeve cannot
have a real resting stop.** Prefer a WHOLE-SHARE buy sized to whatever
buying power is actually available, even if that means picking a
cheaper name from the scan than the single best candidate, so
`decide_stop_update`'s trailing stop can actually rest as a broker
order. If a fractional buy is unavoidable, say so explicitly — "no
resting stop, monitored by hand" — never imply broker-side protection
that does not exist.

**RULE — a same-day round trip does not return buying power to where it
started, even in a cash account, even at zero net exposure.** Same
trade: reversing the unprotectable PLTR fractional position (sold
immediately, -$0.08 round-trip cost) dropped buying power from $110.65
to $5.65 for the rest of the day — the sell's proceeds are unsettled
same as any other sale (T+1), regardless of how recently the shares
were bought. This should have been checked BEFORE reversing, not
discovered after. **Before undoing any position to fix a mistake, check
whether the undo itself is affordable in the same way a fresh trade
would be** — an "instant fix" that costs the day's remaining buying
power is not actually free.

## Watchlist hygiene pass — 2026-08-18 night

User asked to prune the "August 11" watchlist (a dated, single-day
catalyst pick list — see its own pre-existing description) and check
the others. Real methodology used: today's volume vs 2-week average
volume (still active vs faded), proximity to 52-week high/low (still
running vs reverted), and `financial_status_indicator` (exchange
compliance flags) via `get_equity_fundamentals`. Result on "August 11"
(16 -> 6 items): kept TISI (new 52w high same day), OABI/ABCL (both
made new 52w highs within the prior 24h), SE/RIOT (durable, liquid,
not really "stale catalyst" material), KPLT (merger catalyst still
presumably pending, flagged caution same as the list's own original
note). Removed EYPT (made a new 52-WEEK LOW the day before — thesis
inverted), AIFC/BIOX (`financial_status_indicator` = noncompliant),
VG/CNTB/ITP/DYAI (no elevated activity, no cited catalyst), WXM/BW
(the list's own original note already said "no catalyst"/"halted,
unconfirmed" at creation, both down further since).

Also removed NAK from "Cryptos to Watch" — a mining stock, wrong asset
class for a crypto list, correctly still lives in "penny".

**Deliberately left "penny" and "timothy" untouched** despite being
asked to filter them too — checked every name (fundamentals, 52w
range, compliance flags), found real weakness in several (IGC, DJT,
TLRY, GME all well off their highs) but none with an objective red
flag comparable to August 11's noncompliance/52w-low/already-flagged-
no-catalyst reasons. Those two lists are undated and not framed as
single-day catalyst picks the way "August 11" explicitly is, so
"off its highs" alone isn't a real basis to remove something from
what might be a deliberate standing watch list — said so directly to
the user rather than guessing at intent and pruning anyway.

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
| S7 | Options (long calls/puts) | DRAFT, option_level_2 confirmed live | Passarelli + own catalyst-mismatch research + McMillan (2026-08-19, full-book read) | `option_math.py` + `option_scanner.py` built, unit-tested (`test_option_math.py`). Six contracts graded across three live runs (ONDS, LUNR, STNE, NKTR, ZIM, BULL), all six rejections, zero trades placed. 2026-08-17: added a second track for catalysts with no dated trigger — `SoftCatalystScanConfig`/`evaluate_soft_candidate`/`apply_soft_filters_and_rank`, edge test is IV vs. realized volatility. 2026-08-19: read McMillan's *Options as a Strategic Investment* in full (`mcmillan/`, 8 chapter-group notes files) — confirms independently, from capital math rather than tooling, that this account is structurally limited to long calls/puts/straddles/strangles; added `iv_cheap_vs_multi_window_hv()` (his Ch.39 Method 2: IV < 0.8x each of 10/20/50/100-day HV) to `option_math.py`. His preferred IV-percentile method (600-day lookback) and the 80%-probability entry filter are NOT yet implemented — both need real data/formula work not done tonight. See strategies.md S7's "Second source added" subsection. |
| S8 | Verified Catalyst Momentum | DRAFT, n=1 live trades, catalyst gate backtested | Not a book — reverse-engineered from this week's own trades and rejections | Written 2026-08-15 after noticing S1–S7 had contributed zero trades while the ad hoc screen carried the account. 2026-08-16: the float-turnover disqualifier was backtested (single day, n=11, not independent) and **demoted** — turnover magnitude didn't predict outcome and was actively suppressed on the one name that was halting. The catalyst check is the real gate now; turnover is secondary. See S8's "Float-turnover backtest" subsection. |
| — | Day-trade equity screening (SMWB/RSKD picks) | Ad hoc, hand-run each time | Saved Robinhood scans + Stocktwits catalyst check | NOT S3. Don't conflate a finding here into a reason to edit S3. This is what S8 is trying to formalize — but S8 is not yet proven, so this ad hoc process stays the working method until S8 earns LIVE status on its own results. |
| S9 | Growth sleeve (long-run, agent-executed) | LIVE, n=2 (1 reversed same-day, 1 open with a real resting stop) | User's own risk split, 2026-08-18 | `growth_signal.py`. Screen: Robinhood scan `2514847d-25cb-4628-9731-bb5b0ee7d246`. Exit: 18% trail from peak, user's stated tolerance not a backtest. First trade (PLTR, row 12, 2026-08-18) reversed same-day after discovering fractional orders can't carry a stop. Second trade (BTG, row 13, 2026-08-19): buying power fully settled overnight ($5.65 → $524.30, confirming T+1 works as expected), bought 85 whole shares ($5.2599 avg) specifically so the 18% trail could rest as a real GTC stop_market ($4.31) — verified `state: confirmed`, not rejected. First growth position with actual broker-side protection. Daily stop check (2026-08-19 ~4:05pm ET): real peak close since entry was $5.39 (30-min bars), `decide_stop_update` said ratchet — cancelled the $4.31 stop (verified `state: cancelled`), placed a new one at $4.42 (18% below $5.39). New order shows `state: queued` (market closed at 4pm ET, regular_hours stop orders queue for next open — not a rejection, will rest live at tomorrow's open). |

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
