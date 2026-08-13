# Parabolic move forensics — what is actually visible before the run

**This is a RESEARCH document, not a strategy.** Nothing here is wired into
any scanner or order path. It exists to answer one question with data
rather than folklore: when a stock goes up several hundred percent, what
was observable beforehand, and could we have acted on it?

Method: pick a stock that already ran, pull daily price/volume from
Robinhood, pull social message volume from Stocktwits, align the two
timelines, and look for what led versus what lagged. Retrospective by
construction — see "Why this is not a strategy" at the bottom.

---

## Case 1 — ZTG (Zenta Group), 2026

The move: **$1.23 close (2026-04-07) → $12.25 intraday (2026-08-12), +896%.**
The violent part: **$2.65 → $10.02 close, +278% in 11 sessions.**

Baseline for comparison: median daily volume 2026-07-01 to 07-28 was
**23,533 shares**. Price drifted $1.70 → $2.65 over that stretch.

### The launch sequence

| Date | Close | Day % | Volume | x median | Stocktwits msg vol |
| --- | --- | --- | --- | --- | --- |
| 07-28 | 2.65 | — | 12,268 | 0.5x | Extremely Low (22) |
| **07-29** | **2.72** | **+2.6%** | **549,716** | **23x** | **Extremely Low (24)** |
| 07-30 | 3.39 | +24.6% | 1,041,688 | 44x | Slightly High (72) |
| 07-31 | 4.40 | +29.8% | 896,241 | 38x | Extremely High (89) |
| 08-03 | 4.96 | +12.7% | 893,186 | 38x | Extremely High (98) |
| 08-04 | 5.68 | +14.5% | 1,781,565 | 76x | Extremely High (97) |
| 08-05 | 6.80 | +19.7% | 1,594,763 | 68x | Extremely High (96) |
| 08-06 | 10.05 | +47.8% | 2,320,516 | 99x | Extremely High (97) |
| 08-07 | 9.20 | -8.5% | 1,313,499 | 56x | Extremely High (97) |
| 08-12 | 10.02 | +8.1% | 4,110,257 | 175x | Extremely High (88) |

### Finding 1 — volume led price by one day, and social by two

On **07-29** volume was **23x** the 20-day median while price moved only
**+2.6%** and social chatter was still **"Extremely Low."** That is the
signature of a buyer absorbing available supply without chasing the offer.
The price broke out the *next* session (+24.6%), and the crowd arrived
with it — Stocktwits went 24 → 72 on 07-30, by which point the entry was
already 25% worse.

**This is the only genuinely early, genuinely observable signal in the
entire dataset:** an unusual-volume day where price does NOT yet move and
nobody is talking about it.

### Finding 2 — the same signal failed twice on this same stock

This is the part that matters more than Finding 1.

| Date | Volume | x median | What happened next |
| --- | --- | --- | --- |
| 04-14 | 3,189,320 | **135x** | $1.65 → $1.86, then faded and chopped $1.5–2.0 for six weeks |
| 06-08 | 6,384,058 | **271x** | — |
| 06-09 | 12,444,372 | **529x** | **Closed DOWN.** Next session opened $1.74, **−28%** |
| 07-29 | 549,716 | 23x | **The real launch** |

The **largest volume print of the entire period (529x, 06-09) was
distribution, not accumulation** — the stock fell 28% the following day.
And it was 23x, the *smallest* of the four spikes, that preceded the real
move.

**Volume reveals size. It never reveals direction.** On a raw
unusual-volume trigger this stock produced roughly a 1-in-3 hit rate, and
the two failures included the single most dramatic-looking signal.

### Finding 3 — social sentiment is a lagging indicator, and a trap

Stocktwits message volume hit **98 ("Extremely High") on 06-22** — the
stock went nowhere and drifted lower for weeks. During the actual launch
it was still "Extremely Low" (24) on 07-29 and only spiked on 07-30, the
day *after* the informed volume, and simultaneously with a +24.6% candle.

By the time chatter is extreme, the move is public and you are late.
Compare FXHO on 2026-08-12 (rejected by our own screen): sentiment 98.99%
bullish, posts openly saying "lets pump this" and "squeeze it" — that is
the terminal phase, not the entry.

---

## What this implies for tracking, honestly

The **candidate** signal, stated precisely so it can be tested rather than
believed:

> Daily volume ≥ ~20x the 20-day median, **while** the day's price change
> stays small (say under ±5%), **and** social message volume is still
> low/normal. Direction unknown — confirm on the following session.

Everything about that is falsifiable, and all three inputs are available
today (Robinhood `get_equity_historicals` for volume, Stocktwits
`get_message_volume_history` for chatter).

**What it cannot do:**
- Tell you direction. 06-09 had 529x volume and fell 28%.
- Work without confirmation. The entry has to wait for the next session,
  which sacrifices the first move — on ZTG that was +24.6%.
- Be assumed to generalize. **This is n=1.** One stock, three signals, one
  success. That is an anecdote, not a base rate.

## Why this is not a strategy (yet)

**Survivorship bias is the whole problem.** ZTG was selected *because it
already ran 896%*. The honest test is the reverse: take every stock that
printed ≥20x median volume on a flat-price day over some period, then
measure what fraction subsequently ran. Nobody shows you the dozens with
identical footprints that went nowhere — including, on this very ticker,
April and June.

Until that reverse test is run, the correct status is: **interesting
hypothesis, unmeasured base rate, not tradable.**

## On "do they know something we don't?"

Partly yes, and it is worth being precise about which parts:

- **Sometimes genuinely yes** — material non-public information exists,
  and trading on it is illegal. Not a strategy, a felony.
- **Sometimes purchased** — real-time order flow, dark-pool prints, and
  options-flow feeds are commercially available to those who pay. That is
  an information asymmetry we simply do not have.
- **Sometimes just earlier** — the 07-29 buyer left a footprint anyone
  watching volume could see. No secret required, only attention.
- **Mostly survivorship** — for every whale who "timed it perfectly,"
  many took the same position and lost. We only hear about the winners,
  and the 06-09 print is a concrete local example of a large player
  getting it wrong on this exact stock.

The tractable edge is the third one. The first two are unavailable, and
the fourth is a story we tell ourselves after the fact.
