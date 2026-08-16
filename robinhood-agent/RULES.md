# The rules — one page

Plain English. This is the whole method. Everything in `strategies.md`,
`sources.md` and the PDF is *evidence for* these rules, not extra rules.
If those files ever disagree with this page, this page is what we do.

---

## First, what a stop is

A stop is a standing order: **"if the price falls to X, sell me out
automatically."** An automatic seatbelt. Not a strategy.

AEYE, real numbers: 19 shares bought at $7.70, stop at $7.08. If AEYE hits
$7.08 the broker sells all 19 automatically, at 3am if need be. Worst case
loss is 19 × ($7.70 − $7.08) = **$11.78**. Without it, a drop to $4 costs
$70 instead. The stop turns an unknown loss into a known one.

**GTC** = "good till cancelled", stays until it fires. **GFD** = "good for
day", **dies at 4pm every day** and must be re-placed each evening. Always
use GTC.

---

## Before you buy

**1. Name the news out loud.** If you can't say what specifically happened
to this company, don't buy. No exceptions, however good the numbers look.

> Why: on 2026-08-11 two stocks had enormous volume and no news — WXM (614×
> normal) halted at 9:44am, PLAG (843×) halted at 11:25am. Nothing in the
> price or volume predicted it. Only the news check caught both.

**2. Check there's room.** Max **$150** per buy. Total risk across
everything open stays under **6% of the account** (~$32 today).

---

## When you buy

**3. Place the stop within a minute, GTC.** Our record is a median of 16
seconds, which is good. The one trade that took 11 minutes (HHS) is the one
that sat unprotected.

**4. Write down three numbers before you place anything:**

```
Risk per share  =  entry price  −  stop price
Target price    =  entry price  +  1.25 × risk per share
```

That's the only arithmetic in the method.

| | Entry | Stop | Risk/share | **Target** |
| --- | --- | --- | --- | --- |
| AEYE | $7.70 | $7.08 | $0.62 | **$8.48** |
| HHS | $4.37 | $4.14 | $0.23 | **$4.66** |

---

## While you hold

**5. Sell at the target. Don't wait for more.**

> Why: across four trades the moves offered an average of +1.32R and we
> captured +0.28R — **21%**. SMWB was sold at 09:34; its high came at 15:15
> the same day.

**6. Never move the stop up to breakeven.** Leave it where you set it.

> Why: tested both ways. Moving to breakeven returned +0.17R, and moving it
> earlier returned −0.03R — both *worse* than doing nothing (+0.28R). It
> turns normal dips into pointless exits on exactly the trades that go on to
> work. This is common advice and it loses money here.

**7. If it hasn't hit target or stop by the close, sell it.** Don't let a
day trade quietly become a position.

---

## Two things the broker can't do for you

**A stop and a target can't both wait on the same shares.** Robinhood's API
places one order at a time — whichever is placed first holds the shares.
This is why Friday's $7.80 AEYE stop was rejected: the older $7.08 stop
already held all 19. To have a target waiting, place the bracket by hand in
the Robinhood app (the app supports it, the API doesn't).

**A stop does not work in a halt.** If a stock stops trading there is
nothing to sell into. It reopens wherever it reopens — sometimes far lower
— and only then does the stop fire. This is the real risk in cheap, volatile
names, and rule 1 is the only defence against it.

---

## What we run

Only one thing: **buy a stock with verifiable news, with a stop, sized to
the rules above.** One new position at a time until the account is bigger.

Not running, and why:

- **S1 (trend follow)** — has no stop rule. Parked until it does.
- **S2 (opening range)** — tested on 74 real trades, lost money at every
  setting. Rejected.
- **S7 (options)** — graded four contracts, all four too expensive. Nothing
  bought, correctly.

---

## Log every trade

`python3 tradelog.py report`. A trade that isn't logged didn't teach us
anything. The initial stop is the field that matters most and the one most
easily lost — write it down at entry, not afterwards.
