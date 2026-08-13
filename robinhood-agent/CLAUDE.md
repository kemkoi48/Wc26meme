# Operating notes — read this first

My own standing instructions for this repo. Separate from `strategies.md`
(trading content) and `sources.md` (research log) — this file is about how
I work, not what I trade.

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
| S1 | Trend Follow | LIVE | Miner + DailyFX SMA filter | Multi-day, has a protective stop. Wrong fit for the stated day-trade aim. |
| S2 | Opening Range Reversal | VIABLE, top priority | Sincere / Miner | Day-trade, only strategy with a complete entry/stop/target/time-stop plan. Not yet run live. |
| S3 | Low-Float Momentum Scan | RESEARCH ONLY — **do not modify without an explicit request** | Warrior Trading | 5 pillars: relative volume, % change, price range, float, catalyst (non-numeric, hand-checked). `momentum_scanner.py` structurally cannot place an order. Keep separate from ad hoc day-trade screening even when they overlap. |
| S4 | Dual Timeframe Momentum | DRAFT, never run | Miner | |
| S5 | Range Trade | DRAFT | DailyFX | |
| S6 | Oz scan family | Logged; close-strength adopted elsewhere | Tony Oz | |
| S7 | Options (long calls/puts) | DRAFT, option_level_2 confirmed live | Passarelli + own catalyst-mismatch research | `option_math.py` + `option_scanner.py` built, unit-tested (`test_option_math.py`), hand-run once live 2026-08-12 (0/11 passed, expected). |
| — | Day-trade equity screening (SMWB/RSKD picks) | Ad hoc, hand-run each time | Saved Robinhood scans + Stocktwits catalyst check | NOT S3. Don't conflate a finding here into a reason to edit S3. |

Read this table before re-deriving a strategy's status from scratch.

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

## Verify before writing a conclusion into strategies.md

Two live corrections this repo has already needed: the ENVX
"not-a-mismatch" call was first argued from IV alone and was wrong until
the real historical earnings moves were pulled; the WOLF historical-move
calculation was corrupted by 169 synthesized bars until `interpolated`
was checked. Default to pulling real data over reasoning from a plausible
number, especially before a conclusion gets committed to the repo.
