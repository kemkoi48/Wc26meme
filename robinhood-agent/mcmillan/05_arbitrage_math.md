# Chapters 26-28: T-Bill/Option Strategy, Arbitrage, and Mathematical Applications

Source: *Options as a Strategic Investment*, 5th ed., McMillan. Extracted directly from
`ch_028.txt` (Ch. 26, "Buying Options and Treasury Bills"), `ch_029.txt` (Ch. 27, "Arbitrage"),
and `ch_030.txt` (Ch. 28, "Mathematical Applications" — file ends mid-section on "Computing a
Volatility Skew," so this note only covers what that file actually contains: the Black-Scholes
model, historical volatility, and composite/implied volatility through the start of the skew
calculation).

---

## Chapter 26: Buying Options and Treasury Bills

### Strategy/technique name & construction
**The Treasury bill/option strategy** (also called, in essence, a "synthetic convertible bond"
approach). Construction: put roughly **90% of one's money into risk-free, interest-bearing
instruments** (short-term T-bills, or when rates are too low, "AAA corporate bonds, or something
similar" — explicitly *not* junk bonds), and put the remaining **~10% into buying options**
(calls, puts, or both). McMillan states plainly: "Simply stated, the strategy consists of putting
90% of one's money in risk-free investments (such as short-term Treasury bills) and buying
options with the remaining 10% of one's funds."

He also describes, only to reject as inferior, a related idea: the **"synthetic convertible bond"**
— buying a debenture (bond) plus a call option on the same stock — which mimics a convertible
bond's shape but is "superior [in his view is the T-bill/option version]... since there is no risk
of price fluctuation in the largest portion of the investment."

### Market outlook or condition required
None specific — the text says the option-selection ranking method "completely ignores the outlook
for the underlying stock." He recommends selecting options by a ranking of "highest reward
opportunity" from volatility-based projections (cross-referencing Chapters 3 and 16), not by a
directional thesis. He notes that using only calls hurts in "both static and down markets," while
adding some puts means "only static markets could produce the worst results." He argues buying
both puts and calls is preferable "since the frequency of market rallies is smaller than the
combined frequency of market rallies and declines."

### Real numeric rules/formulas he gives
- **Base allocation:** 90% risk-free / 10% options.
- **Never exceed 20% annualized risk**, "no matter how small the actual dollar investment... To
  exceed this risk level would be to completely defeat the purpose of the fixed-income/option
  purchase strategy."
- **Annualized risk formula** (as given, with OCR garbling of the layout — reconstructed from the
  worked examples):
  > Annualized risk on entire portfolio = (Percent of total assets invested) × (360 / Holding
  > period [days])
  - 30-day purchases → 1,200% annualized risk (100% assumed loss × 12 periods/year).
  - 90-day purchases → 400% annualized risk.
  - 180-day purchases → 200% annualized risk.
  - "If one is able to diversify into several holding periods, the annualized risk is merely the
    sum of the risks for each holding period."
- **Worked example (large investor, $1,000,000):** ½ of 1% into 30-day purchases, ½ of 1% into
  90-day purchases, 1% into 180-day purchases:
  > Total annualized risk = .5% × (360/30) + .5% × (360/90) + 1% × (360/180) = .06 + .02 + .02 = 10%
  - In dollars: $5,000 to 30-day purchases, $5,000 to 90-day purchases, $10,000 to 180-day
    purchases, reinvested each cycle.
- **Rebalancing after gains example:** Start $90,000 T-bills / $10,000 options. Options grow to
  $30,000 (total assets $120,000 = 75%/25% split) → must sell $18,000 of options to bring the
  option position back down to $12,000 (10% of $120,000).
- **Rebalancing after losses example:** Lose the full $10,000 option stake in year one; T-bills
  plus ~$6,000 interest leave $90,000+interest; readjust back to a 90:10 ratio by selling some
  T-bills to buy options.
- **Position sizing at end of each holding period must use the new portfolio value, not the
  original dollar amount.** Example: portfolio falls to $990,000 after 30 days → next 30-day
  commitment is ½ of 1% of $990,000 = $4,950, not $5,000.
- **T-bill lot-size constraint:** "T-bills can be bought and sold only in amounts of at least
  $10,000 and in increments of $5,000 thereafter" ($10,000, $15,000, $20,000, $25,000... — not
  $5,000, $8,000, or $23,000).
- **Small-investor example ($50,000 portfolio):** Given 30-day purchases carry 1,200% annualized
  risk, "it does not make much sense to even consider purchases that are so short-term for assets
  of this size." He models 1% into a 90-day purchase and 3% into a 180-day purchase, then
  concludes in practice the investor would "probably just invest 5% of his assets in 180-day
  purchases, also a 10% annualized risk" — i.e., $2,500 into a single 180-day options list, rebalanced
  roughly every 90–180 days.
- **Very small investor example ($5,000):** "5% of the money invested every 180 days is only $250
  in each investment period." He notes many at-/near-the-money calls that rank well in this
  strategy "will cost more than 2½ points for one option" (i.e., $250+ per contract), directly
  conflicting with a $250 budget.

### Risk/reward profile
Predefined, capped downside (limited to the amount committed to options, kept to a strict 10%
annualized ceiling, never above 20%) with theoretically unlimited upside from the option leg. "Its
true advantage lies in the fact that it has predefined risk and does not have a limit on potential
profits." It's structurally similar to owning a convertible bond (has a "floor") but McMillan
argues it's strictly better because the fixed-income portion carries zero price-fluctuation risk.

### McMillan's own caveats
- It is *not* effortless: "the investor... must not be deluded into thinking that it is so simple
  that it does not take any work at all." Ongoing work includes disciplined option selection and
  periodic rebalancing to keep risk at ~10% annualized.
- When interest rates are very low, the "risk-free" 90% may earn "no income... or very little," so
  the investor must find a still-safe but higher-yielding substitute (AAA bonds) and actively
  manage that portion too.
- Explicitly warns against reaching for yield in the "safe" 90% (GNMAs, corporate/convertible/
  municipal bonds, "high-yield stock or covered call writing") — these carry more risk/less
  liquidity than T-bills and would "assume risk with the portion of his money that was not
  intended to have any risk at all."
- The risk-per-holding-period assumption is deliberately conservative/simplistic: "assumption...
  that the risk in each option purchase was 100% for the holding period," which he defends as
  "far safer" even though real losses are usually less than 100% over 30 days.
- Explicitly calls out the **small-investor problem** (see below).
- No margin account or collateral computations are needed — "the strategy can be operated
  completely from a cash account" and has no short options, so no early-assignment risk.

### Capital/margin size — honesty check for a $100–500 account
This chapter is the most explicit in the whole set about small-account limitations, and McMillan's
own numbers make the verdict clear-cut:
- T-bills require a **minimum $10,000 purchase**, in $5,000 increments. A $100–500 account cannot
  buy T-bills at all — full stop, per the text.
- McMillan's own "truly small investor" example uses **$5,000** and he still calls it a "double
  disadvantage" — too small to buy the option list's better selections, and too small even to buy
  T-bills (forced into money market funds instead), with a warning that risk could creep toward
  the 20% annualized ceiling just to make it workable.
- At $100–500, the *10% annualized* target commitment to options would be roughly **$10–50/year**,
  which cannot buy any of the at-/slightly-out-of-the-money options the ranking method favors —
  McMillan's own text notes those regularly cost "more than 2½ points" (i.e., $250+) even for his
  $5,000 example.
- **Conclusion: this chapter's strategy, as McMillan describes it, is not implementable at
  $100–500.** The mechanism (a fixed-income anchor plus small option allocation) is conceptually
  simple, but the T-bill minimum lot size and the dollar cost of qualifying options make it a
  structural mismatch for this account size. A retail investor at this level could only loosely
  approximate the *spirit* of the idea (e.g., keep most cash in a money-market fund and cap total
  option-buying dollars), but that is a departure from, not an application of, McMillan's actual
  rules.

---

## Chapter 27: Arbitrage

McMillan opens by narrowing the intended audience immediately: "The public customer cannot
generally operate arbitrage-like strategies because of the commission costs involved. Arbitrageurs
are firm traders or floor traders who are trading through a seat on the appropriate securities
exchange, and therefore have only minimal transaction costs." He adds that this chapter "is
directed at the strategist who is actually going to be participating in arbitrage," and that public
customers benefit mainly from *understanding* it, not deploying it.

### 1. Basic call/put arbitrage ("discounting")

**Construction (call arbitrage):** buy a deeply in-the-money call trading at a discount to parity,
simultaneously sell (as an "irrevocable exercise," not a true short sale — no uptick required)
the stock, then exercise the call to buy stock back at the strike.
- Example: XYZ at 58, July 50 call at 7.90 (parity would be 8.00 → 10-cent discount).
  1. Buy call at 7.90; 2. Sell stock at 58; 3. Exercise to buy stock at 50.
  - Profit = 8 points on stock (58−50) − 7.90 paid for call = **10-cent profit**, matching exactly
    the discount.

**Construction (put arbitrage):** buy stock, buy an in-the-money put at a discount, exercise the
put.
- Example: XYZ at 58, July 70 put at 11.90 (parity 12.00 → 10-cent discount). Buy stock at 58, buy
  put at 11.90, exercise put to sell stock at 70. Stock profit = 12 points − 11.90 put cost = **10
  cents**.

**Alternative when the stock leg isn't available in size:** sell a *different* in-the-money option
at parity instead of trading the stock itself (a synthetic stock-position substitute). Worked with
the same 58/50-call example using a July 40 call sellable at parity (18).

**Condition required:** discount options "generally either are quite deeply in-the-money or have
only a short time remaining until expiration, or both." Call arbitrage opportunities are more
common "after market rallies"; put arbitrage opportunities more common "after market declines,"
and near expiration when public buying interest in deep ITM options dries up.

**Risk/reward:** essentially riskless once locked in — profit equals exactly the discount amount,
locked in immediately via simultaneous trades and exercise.

**Caveat:** "The arbitrageur obviously wants to establish these positions in as large a size as
possible, since there is no risk in the position if it is established at a discount" — this is a
professional, size-driven, seat-holder game; the profit per unit (dimes) only matters at scale with
near-zero commissions.

### 2. Dividend arbitrage

**Construction:** buy the stock and buy an in-the-money put whose time value premium is *less*
than the upcoming dividend; hold through the ex-dividend date, collect the dividend, then exercise
the put.
- Rule of thumb: "on the day before a stock goes ex-dividend, all puts should have a time value
  premium at least as large as the dividend amount." If not, arbitrage exists.
- Example: XYZ closes 45, going ex-div $1 tomorrow; July 50 put trades at 5.90 (parity+time value
  should be ≥6). Buy put 5.90 + buy stock 45 → exercise put to sell at 50 (+5) + collect $1
  dividend = 6 inflow − 5.90 cost = **10-cent profit**.

**Carrying cost matters a lot here.** Example: 6% annual carrying rate, position held 2 months
before ex-div → carrying cost on the $50.90 outlay = 0.5075 points, which **exceeds** the 10-cent
theoretical profit. "This is more than 50 cents in costs — clearly more than the 10-cent potential
profit." His conclusion: only worthwhile close to the ex-dividend date, where carrying cost is
small.

**Dividend risk arbitrage variant:** speculate on the *size* of an expected special dividend using
a put + stock combo, where loss is capped at the (excess) time value premium minus the guaranteed
regular dividend. Worked example: XYZ at 55, buy stock + Jan 60 put at 7.50 (2.50 time value);
break-even needs a special dividend ≥ $1.50 (on top of the known $1.00 regular dividend); "the most
that the arbitrageur would lose would be 1.50 points."

**No equivalent direct call-side dividend arbitrage** is described — the text explicitly says there
isn't one, though dividend-driven call selling by holders can occasionally create discount calls
that feed into strategy #1.

**Caveat:** "his records must be accurate, so that he exercises all his long options on the day
before the ex-dividend date" — a careless arbitrageur who is still short stock on the ex-date can
have the dividend payout wipe out the discount profit entirely.

### 3. Conversions and reversals

**Conversion construction:** buy the underlying + buy a put + sell a call, same strike/terms.
Profitable if total cost < strike price.
- Formula given: **Conversion profit = Striking price + Call price − Underlying price − Put price
  + Dividends to be received − Carrying cost of position**
- Simplified fixed-cost formula: **Conversion fixed cost = Carrying rate × Time held × Striking
  price − Dividend to be received**
- Example: stock 55, Jan 50 call 6.50, Jan 50 put 1 → cost = 55 + 1 − 6.50 = 49.50 < strike 50 →
  locked-in 50-cent profit regardless of where stock finishes.
- Carrying-cost example: 3 months held, 6% rate, $0.50 dividend, strike 50 → fixed cost = .06 ×
  (3/12) × 50 − .50 = .75 − .50 = **.25**; only profitable if the simplistic profit exceeds this 25
  cents.

**Reversal construction:** sell underlying short + sell a put + buy a call, same terms. Profitable
if credit received > strike.
- Formula: **Reversal profit = Underlying + Put − Strike − Call + Carrying cost − Dividends**
- Example: stock 55, Jan 60 call 2, Jan 60 put 7.50 → credit = 55 + 7.50 − 2 = 60.50 > strike 60 →
  50-cent locked-in profit.
- Reversal fixed-cost formula: **Reversal fixed cost = Dividend to be paid − (Interest rate per
  month × Months held × Striking price)**. Example with a 30-strike, .50 dividend, 3 months, ½%/mo
  → .50 − (.005×3×30) = .50 − .045 = **.005** (near zero — "often possible... that there will be a
  fixed credit, not a fixed cost, in a reversal arbitrage").

**More rigorous carrying-cost formula (compounding/present value):** Strike / (1+r)^t, vs. the
simple **Carrying cost = Strike × r × t**. McMillan: the simple version is "generally acceptable...
common practice," accurate when r and t are small, but should be double-checked with the exact
formula "in periods of high interest rates when longer-term options are being analyzed."

**"Box stock" / stock-loan cost:** to short stock for a reversal you must borrow it. If you don't
have "box" stock (margin-account stock a firm can lend internally) you pay a stock-loan fee,
typically "10 to 20% of the prevailing carrying cost rate" — e.g., at a 10% annual carry rate,
expect to pay 1–2% to the lender, which "reduces the profitability of the reversal slightly." He
notes this literally segments arbitrageurs by their cost of capital: one needing only 50 cents,
another 55 cents, another 65 cents for "the same" reversal.

**Four risks in reversals** (per McMillan, verbatim list): "An extra dividend is declared, the
interest rate falls while the reversal is in place, an early assignment is received, or the stock
is exactly at the striking price at expiration." Mirror risks for conversions: "a dividend cut, an
increase in the interest rate, early assignment, or the stock closing at the strike at expiration."
- **Extra dividend:** usually large enough to wipe the profit; a reversal that looks "overly
  profitable" up front may be pricing in an anticipated extra dividend — treat as a red flag.
- **Rate risk:** build in a margin (e.g., price the reversal to break even at 2–3 points below/above
  current rates — the "effective rate"); optionally hedge by parking the credit balance in CDs/paper
  maturing near the reversal's expiration.
- **Early assignment (reversal):** forces buying stock/incurring a debit, reducing interest earned;
  can flip to a net loss if assignment comes early. Partial mitigation: structure with the call
  in-the-money and put out-of-the-money.
- **Pin risk (stock exactly at strike at expiration):** McMillan calls this "the most common" risk
  and not "minute." Can leave an unhedged long or short position Monday morning. Mitigations
  described: exercise only half the calls if genuinely undecided; or roll the reversal to a later
  expiration or a different strike (e.g., a 3-way spread order moving the strike 5 points for a
  matching 5-point credit, "costing the arbitrageur nothing except a small transaction charge").

**Public-customer caveat, verbatim intent:** "He may sometimes be able to find conversions or
reversals... that appear to have profit potentials that exceed commission costs. Such positions do
exist from time to time, but the rate of return to the public customer will almost assuredly be
less than the short-term cost of money. If it were not, arbitrageurs would be onto the position
very quickly."

### 4. The "interest play"

**Construction:** short the underlying + buy an in-the-money call trading slightly over parity (no
put leg) — essentially a reversal without the short put, designed mainly to harvest interest on the
short-sale credit.
- Example 1: short XYZ at 60, buy Jan 50 call at 10.25, 1% monthly rate, 1 month to expiry, no
  dividend. Credit = $4,975 → interest = $49.75; loss on securities = $25 (time value paid) → net
  profit **$24.75**.
- Example 2 (real-world, early 1979): IBM at 300, April 240 calls (60+ points ITM) trading 3.50
  over parity at 63.50 purely because prevailing interest rates were high (~1%/month) with 6 weeks
  to expiry. Credit from the trade = $23,700 → interest ≈ $365.50 over 1.5 months vs. $350 lost on
  time value → net profit. McMillan uses this to show directly why "interest rates affect option
  prices."

### 5. The box spread

**Construction:** simultaneously buy a call bull spread and buy a put bear spread using the same
two strikes (or the credit-side mirror: sell a call bear spread + sell a put bull spread). Value at
expiration is fixed at exactly the strike differential.
- Example ("buying" the box): XYZ 55; Jan 50 call 7 / Jan 50 put 1 / Jan 60 call 2 / Jan 60 put
  5.50. Bull spread (buy 50c, sell 60c) = net 5 debit; bear spread (buy 60p, sell 50p) = net 4.50
  debit → total cost **9.50**, box always worth **10** at expiry → locked-in **50-cent profit**
  (before carrying cost, e.g. 6% for 3 months on 9.50 ≈ 14 cents drag, "still leaves room for a
  profit").
- Example ("selling" the box): XYZ 75; April 70 call 8.50 / put 1 / April 80 call 3 / put 6 → total
  credit **10.50** vs. fixed liquidation value 10 → locked-in **50-cent profit**, and the seller
  *earns* interest on the credit while holding.
- **Two-question evaluation test he gives:**
  1. Buying both spreads: is total cost < strike differential + carrying cost? If yes, arbitrage
     exists.
  2. Selling both spreads: is total credit + interest earned > strike differential? If yes,
     arbitrage exists.
- **Risks:** same pin risk as conversions/reversals (stock closing at either strike creates
  exercise/assignment ambiguity); early assignment can trigger unplanned carrying costs (short put
  assigned) or lost dividends (short call assigned near ex-div).
- **Caveat on availability:** "These box spreads are not easy to find. If one does appear, the act
  of doing the arbitrage will soon make the arbitrage impossible... this is true of any type of
  arbitrage; it cannot be executed indefinitely."

### 6. Variations on equivalence arbitrage (mentioned, not detailed)

Butterfly-vs-butterfly (calls vs. puts), listed straddle vs. synthetic straddle (short stock + long
2 calls), listed straddle vs. ratio write (long stock + short 2 calls). McMillan's own verdict:
these are "relatively complicated and probably not worth the arbitrageur's time to analyze,"
useful only opportunistically when one leg has unusually large size/liquidity relative to another.

### 7. Risk arbitrage (mergers, tender offers, pairs trading)

Unlike the riskless categories above, McMillan flags this bucket as **more accessible to public
customers** because per-share profit can be large enough to absorb commissions: "Since the
potential profits in risk arbitrage situations may be quite large, perhaps 3 or 4 points per 100
shares, the public can participate in this strategy... Although the public cannot normally
participate in arbitrage strategies because of the small profit potential, risk arbitrages may
often offer exceptions."

- **Stock-swap mergers:** short the acquirer (XYZ), buy the target (LMN) in the announced ratio, to
  capture the spread between current LMN price and implied deal value. Example: XYZ buys LMN at
  1-for-2; LMN trades ~22 pre-close vs. implied 25; profit is the closing of that spread.
  - **Option substitute for shorting the acquirer:** buy in-the-money puts on XYZ instead of
    shorting it (useful when the stock is hard/impossible to borrow) — worked example shows this
    can actually *outperform* the all-stock version if the acquirer rallies (put loss capped, LMN
    gain isn't), at the cost of foregone short-sale interest.
  - Selling options (short puts on target, short ITM calls on acquirer) is called "generally...
    inferior" because it caps profit without capping risk, though selling ITM calls can help when
    the stock is hard to borrow/short (uptick issues).
  - **Collared/"hooked" mergers** (deal value fixed within an acquirer price band, e.g. worth $25 as
    long as XYZ is between 45 and 55): McMillan shows how to derive the min/max exchange ratio
    (25/45 = 0.556 max shares, 25/55 = 0.455 min shares) and recommends buying **puts on the
    acquirer near the lower "hook" strike** instead of trying to time a partial short hedge, to
    avoid ratio-mismatch losses if the acquirer whipsaws around the collar boundary.
- **Tender offers:** "any and all" cash tenders → buy protective puts on the target as insurance if
  the deal breaks; selling naked options here is flagged as risky ("may often seem like easy
  money" but a competing bid or deal collapse can cause large losses).
  - **Two-tier partial tender offers** (e.g., XYZ offers $70 for half its own stock, remainder
    expected to trade at $40): buy the stock + buy a proportionate number of puts near the
    post-tender expected price, to lock in the tendered-share gain while insuring the un-tendered
    remainder. Worked numeric example: 200 shares at 52 + 1 July 50 put at 10 = $11,400 cost; if
    100 shares accepted at 70 (=$7,000) and 100 sold via put exercise at 50 (=$5,000), profit is
    locked in regardless of where the stock opens post-tender.
  - Explicit legal warning: **"Short tendering is against the law"** — you must be net long all
    shares you tender as of the expiration date, and shares must be reduced by any in-the-money
    calls written against the position.
- **Pairs trading:** long one historically-cheap stock, short its historically-related pair,
  betting on reversion; can be replicated with ITM puts (in place of the short) and ITM calls (in
  place of the long) to cap risk (e.g., against surprise takeover bids on the shorted name) while
  keeping similar profit potential, minus time value premium and carrying cost of the (now-debit)
  options position.

### General caveats for Chapter 27 — who can realistically use these
McMillan's summary is unambiguous and directly answers the "who can use this" question: "Arbitrage
involving options can be very profitable, but unless the profit potential is sufficiently large, it
is generally a strategy that is for professional traders who are exchange members — who pay little
or no commissions." He splits the chapter's strategies into:
- **Riskless (or near-riskless) arbitrage** — discount, dividend, conversion/reversal, interest
  plays, boxes, equivalence arbitrage: profits are typically **fractions of a point per share**
  (10–50 cents in his examples), which only work at institutional size with minimal commissions and
  often require **borrowing stock, margin/"box" accounts, and access to exercise mechanics
  (irrevocable exercise) not available to a standard cash retail account.**
- **Risk arbitrage** (mergers/tenders/pairs) — the one category he explicitly says the public can
  sometimes use, because per-trade profit (3-4 points/100 shares) can exceed commission costs.

### Capital/margin size for $100–500
- The riskless arbitrage strategies (discounting, dividend arbitrage, conversions/reversals,
  interest plays, box spreads) are **not realistically accessible** at this size: they require
  stock-loan/margin infrastructure, exchange-member-level commission costs to be profitable on
  dime-sized edges, and — critically — capital to buy/carry full underlying share lots (e.g. 100+
  shares of stock per contract, as in every worked example) alongside the option legs. A box spread
  alone in the worked examples ties up ~$950–$1,050 per box (9.50–10.50 points × 100 shares) before
  even considering the stock legs in conversions/reversals, which involve buying or shorting 100
  shares of underlying (thousands of dollars) per position. None of this fits in $100–500.
- **Risk arbitrage is the one sub-strategy in this chapter with a plausible, if still stretched, fit
  at very small size** — but only the pure option-substitution versions (buying a single put or
  call instead of the full stock position), since McMillan's own profit figures ("3 or 4 points per
  100 shares" = $300-$400 per 100-share lot) imply position sizes still well beyond $100-500 once
  you include the paired stock leg (e.g., buying LMN shares in the merger example, or 200 shares of
  XYZ in the tender example). A single deep ITM put/call on a merger target, sized to a $100-500
  budget, is conceivable in principle, but McMillan never presents an example at this scale, and
  commission costs (his stated reason retail is usually excluded) bite proportionally harder on a
  smaller ticket.
- **Bottom line: this chapter is written for and about professional/exchange-member arbitrageurs.
  At $100-500, essentially nothing in it is directly executable; at most, a trader could take away
  the conceptual lesson (e.g., understanding why puts/calls price the way they do relative to
  strike and interest rates) without being able to run any of the actual arbitrage constructions.**

---

## Chapter 28: Mathematical Applications (partial — file covers Black-Scholes through the start of volatility-skew computation)

This chapter is presented by McMillan as **analytical/evaluative infrastructure**, not a
freestanding trading strategy: "Although the average investor... normally has a limited grasp of
advanced mathematics, the information in this chapter should still prove useful. It will allow the
investor to see what sorts of strategy decisions could be aided by the use of mathematics [and] to
evaluate techniques of an information service." There is no discrete "buy/sell" strategy here in
the same sense as the previous chapters — it is pricing and volatility machinery meant to *support*
strategy decisions made elsewhere in the book.

### Technique 1: The Black-Scholes model

**Construction/purpose:** compute a theoretical fair value for an option (and its delta) from five
inputs: stock price, strike price, time to expiration, risk-free rate, and volatility.

**Formula as given (verbatim, OCR-cleaned):**
> Theoretical option price = pN(d₁) − se^(−rt)N(d₂)
>
> where d₁ = [ln(p/s) + (r + v²/2)t] / (v√t)
>
> d₂ = d₁ − v√t

Variables per the text: p = stock price; s = striking price; t = time remaining until expiration
(as a percent of a year); r = current risk-free interest rate; v = volatility (annual standard
deviation); ln = natural logarithm; N(x) = cumulative normal density function.

**Delta formula given:** Delta = N(d₁) — "the amount by which the option price can be expected to
change for a small change in the stock price... more formally known as the hedge ratio."

**Cumulative normal approximation formula given** (for hand/programmable-calculator use instead of
table lookups):
> x = 1 − z(1.330274y⁵ − 1.821256y⁴ + 1.781478y³ − .356538y² + .3193815y)
>
> where y = 1/(1 + .2316419|d|) and z = .3989423 × e^(−d²/2)

**Fully worked example (numbers as given):** XYZ at 45, July 50 call, 60 days to expiration,
volatility 30%, risk-free rate 10%.
- t = 60/365 = .16438
- d₁ = [ln(45/50) + (.10 + .3×.3/2)×.16438] / (.3×√.16438) = [−.10536 + (.145×.16438)] /
  (.3×.40544) = **−.67025**
- d₂ = −.67025 − .3×.40544 = **−.79189**
- N(d₁) = 1 − x, computed via the approximation → **N(d₁) = .25134**
- (N(d₂) computed similarly, not shown in full)
- **Theoretical value = 45×.25134 − 50×e^(−.10×.16438)×.21421 = 45×.25134 − 50×.9837×.21421 =
  .7746** — "the theoretical value of the July 50 call is just slightly over ¾ of a point."
- **Delta = N(d₁) ≈ .25** — "the July 50 call will change price about ¼ as fast as the stock for a
  small price change by the stock."

### Characteristics/caveats of the Black-Scholes model (McMillan's own critique)
- **Dividends are not in the base model.** "Direct application of the model will tend to give
  inflated call prices, especially on stocks that pay relatively large dividends." Fisher Black's
  suggested fix (as relayed by McMillan): (1) subtract the present worth of expected dividends from
  the stock price before pricing, and separately (2) price the option as if it expired just before
  the last pre-expiration ex-dividend date; use whichever of the two calculated prices is higher.
  A cruder alternative: apply a dividend-based weighting factor, heavier for higher-yield stocks.
  McMillan notes that for many strategy applications the exact price isn't needed, so "the dividend
  'correction' might not have to be applied."
- **Lognormal, not normal, distribution of prices.** The model implies stock prices range only (0,
  ∞) and have an upward bias, "since a stock can drop only 100% but can rise in price by more than
  100%." McMillan's critique of critics: the model "tends to overprice in-the-money calls and
  underprice out-of-the-money calls" per some critics — "this criticism is true in some cases, but
  does not materially subtract from many applications of the model in strategy decisions," except
  if you're trading purely off computed theoretical value.
- **Volatility is the hard, critical input.** "Since the volatility is a very crucial element of the
  pricing model, it is important that the modeler use a reasonable estimate of the current
  volatility... The problem of accurately computing the volatility is critical, because the model
  is so sensitive to it."

### Technique 2: Computing (lognormal) historical volatility

**Naive standard-deviation formula given:**
> V = σ/P̄, where σ² = Σ(Pᵢ − P̄)² / (n−1)

But McMillan flags this as *not* the correct input for Black-Scholes, because the model assumes
**log price changes**, not price levels, are normally distributed — so Pᵢ must be replaced by
ln(Pᵢ/Pᵢ₋₁).

**Worked 10-day example (numbers as given, from the table in the text):**
- Daily ln(price ratio) values computed for 11 closes (e.g., day 2: ln(153.625/153.875) ≈ −.0016;
  day 10: ln(158.625/152.5) ≈ .0394; etc.)
- Average of the 10 daily ln-values ≈ **0.00288**
- Sum of squared deviations from that mean ≈ **0.004455**
- **D (10-day volatility) = √(0.004455/9) = 0.022249**
- **Annualization: V = D × √(number of trading days/year) = 0.022249 × √260 = 0.3587**, i.e.,
  "the volatility of XYZ is 36% on an annualized basis." (He notes ~260 trading days/year is used.)
- Notes this same process generalizes to 10-, 20-, 50-day, or annual windows as desired.

### Technique 3: Composite implied volatility

**Concept:** instead of estimating volatility from historical prices, back it out of current market
option prices (assuming near-the-money, actively-traded options are fairly priced), by solving
Black-Scholes for volatility given the observed option price (iteratively), separately for each
listed option on a stock, then combining ("weighting") those individual implied volatilities into
one number for the underlying.

**Weighting scheme given:**
- **Volume weight** = that option's daily volume ÷ total volume across all options on the stock.
- **Distance-from-strike weight**: a parabolic (non-linear) function of percentage distance between
  stock price and strike, of the form:
  > Weighting factor = 1 − (x/a)² [as reconstructed from the OCR'd fragment "1(x−a)... if x is
  > less than a"] — where x = percentage distance between stock price and strike, and a = the
  > maximum percentage distance the modeler will assign any weight to at all. (The exact exponent
  > is garbled in the OCR; the worked numeric table below is what actually carries the intended
  > values.)
- **Combining formula given:**
  > Implied volatility = Σ(Volume factor × Distance factor × Implied volatility) / Σ(Volume factor
  > × Distance factor)

**Fully worked example (numbers as given):** XYZ at 33, with a = .25 (discard strikes >25% away
from stock price).

| Option | Price | Volume | Implied Vol | Volume Factor | Distance Factor |
|---|---|---|---|---|---|
| Jan 30 call | 4.50 | 50 | .34 | .25 (50/200) | .41 |
| Jan 35 call | 1.50 | 90 | .28 | .45 (90/200) | .57 |
| Apr 35 call | 2.50 | 55 | .30 | .275 (55/200) | .57 |
| Apr 40 call | 1.50 | 5 | .38 | .025 (5/200) | .02 |

> Implied volatility = [.25×.41×.34 + .45×.57×.28 + .275×.57×.30 + .025×.02×.38] / [.25×.41 +
> .45×.57 + .275×.57 + .025×.02] = **.298** (29.8%)

**Smoothing note:** implied volatility can be noisy day-to-day for thinly-traded names; McMillan
suggests a moving average, or a simpler momentum/EWMA approach: "today's final volatility might be
computed by adding 5% of today's implied volatility to 95% of yesterday's final volatility" (needs
only one stored prior value).

**Where the provided file cuts off:** The text begins describing "Computing a Volatility Skew" —
(1) compute each option's individual implied volatility, (2) take the standard deviation of that
set (unweighted, but excluding options trading with little/no time value premium), (3) divide by
the composite implied volatility computed above. **The file ends mid-step-3, before showing a
worked skew example or any further sections** (e.g., no content on option evaluation/ranking
formulas, position-sizing math, or risk/reward ranking tools of the kind referenced back in Chapter
26 appears in this file). Anything beyond this point should not be assumed present in this source.

### Market outlook or condition required
None — this is analytical machinery applicable regardless of directional view. It supports
*evaluating* options (over/underpriced relative to a model or relative to each other) rather than
prescribing a market stance.

### Risk/reward profile
Not applicable in the position-level sense — this chapter provides valuation and volatility
*tools*, not a position construction with a risk/reward payoff diagram of its own.

### McMillan's own caveats
- Explicitly acknowledges the model's known biases (over/under-pricing ITM/OTM calls under the
  lognormal assumption) and says this matters "if one is going to buy or sell calls solely on the
  basis of their computed value" but "small differentials will not matter" when other factors
  dominate the strategy decision.
- Says dividend adjustment can often be skipped depending on the strategy application.
- Flags volatility estimation itself as the weak link: "an annual standard deviation is not
  accurate, because it encompasses too long a period of time," and that more complex recency
  weighting schemes "may introduce as much error as using the annual standard deviation does."
- No statement in this file about who can/cannot realistically use these tools — but implicit in
  the framing ("the investor who does have a knowledge of mathematics and also has access to a
  computer will be able to directly use the techniques") is that meaningful independent use
  requires programming/spreadsheet capability, not just capital.

### Capital/margin size
Not applicable — nothing in this chapter (as captured in this file) is a position or trade
construction requiring capital. It is calculation methodology only. The relevant "size" constraint
for a $100–500 trader isn't dollars but **tooling**: doing this by hand (as McMillan's worked
examples do) is realistic for a single trade evaluation, but running it across a watchlist requires
a spreadsheet or programmed calculator, which McMillan flags as the differentiator ("access to a
computer") rather than account size.
