# McMillan — *Options as a Strategic Investment* (5th ed.)
## Notes: Definitions, Covered Call Writing, Call Buying, Other Call Buying Strategies, Naked Call Writing, Ratio Call Writing

Source files (OCR'd from epub, minor artifacts left as-is):
`ch_005.txt` (Introduction), `ch_006.txt` (Ch.1 Definitions), `ch_009.txt` + `ch_010.txt` (Ch.2 Covered Call Writing), `ch_011.txt` (Ch.3 Call Buying / Ch.4 Other Call Buying Strategies), `ch_012.txt` (end of Ch.4, Ch.5 Naked Call Writing, Ch.6 Ratio Call Writing).

All figures below are quoted or closely paraphrased directly from the text McMillan wrote — no outside/training-data knowledge has been added. Where the book gives no number for a requested item, that is stated explicitly rather than filled in.

---

## Front Matter (ch_005.txt) — Introduction

This file is only the book's Introduction (roughly one paragraph). It contains no strategy content. It explains the book's structure: "Each chapter in this book presents information in a logically sequential fashion... call buying is discussed initially in Chapter 3; and mathematical applications, as they apply to call purchases, are described in Chapter 28." No numeric rules, no strategy detail — this file is genuinely thin, as expected for front matter.

---

## Chapter 1 — Definitions (ch_006.txt)

This chapter has no "strategy" per se (no market outlook, no risk/reward table) — it is pure mechanics/vocabulary that underpins everything else. Captured here because later chapters assume it.

### Key definitions relevant to strategy construction
- **Call option**: "gives the owner (or holder) the right to buy the underlying security." **Put**: right to sell.
- **Exercise/striking price**: price at which stock may be bought/sold; "exercise price" and "striking price" are synonymous on listed markets.
- One option contract = right to buy/sell "100 shares (normally)."
- Quoted price is per-share: an option quoted at $5 costs $500 (×100) plus commissions.

### Time value premium — exact formula given
> "Call time value premium = Call option price + Striking price − Stock price" (for an in-the-money call)

If out-of-the-money, "the premium and the time value premium are the same" (i.e., 100% of the price is time value).

- Time value premium is **largest when stock price = strike**, and shrinks as the option moves deep ITM or OTM (Table 1-1 in the text demonstrates this).
- McMillan flags "time value premium" as **a misnomer** even in Chapter 1 (a theme he repeats in Ch. 3 and Ch. 5): "The volatility of the underlying stock has a great deal to do with how much 'time premium' is in the option. So, really, 'time premium' is something of a misnomer, but it's the standard term."

### Time decay — explicit rule of thumb
> "The rate of decay is actually related to the square root of the time remaining. Thus, a 3-month option decays (loses time value premium) at twice the rate of a 9-month option, since the square root of 9 is 3. Similarly, a 2-month option decays at twice the rate of a 4-month option."
- Caveat: this is a **simplification** — a 9-month option does not necessarily cost twice a 3-month option, because volatility and the other pricing factors also matter.

### The six price determinants (four major, two minor)
Major: (1) stock price, (2) striking price, (3) time remaining, (4) volatility of underlying.
Minor: (5) risk-free interest rate, (6) dividend rate of underlying.
- "More volatile underlying stocks have higher option prices."
- Dividends **lower** call premiums; "the call buyer... discount[s] the upcoming dividends of the stock when they bid for the calls," with the **nearest** dividend discounted more heavily than later ones.
- At expiration, only stock price and striking price matter — option worth exactly its intrinsic value.

### Exercise/assignment mechanics (capital-relevant)
- Exercise notices are irrevocable, processed once daily after the close; OCC assigns short firms/customers at random, FIFO, or another exchange-approved method.
- **Automatic exercise**: OCC automatically exercises any option one penny in-the-money at expiration unless the customer instructs otherwise. Caution given: "This is why some brokerage firms do not allow option buying in retirement accounts (IRAs, for example), because one cannot just routinely add money into an IRA to fulfill the requirements of an automatic exercise" — relevant for a small account since an unplanned exercise creates a stock purchase obligation that may trigger a margin call if cash is insufficient.
- **Early exercise via discount/dividend arbitrage**: explained with worked numeric examples (arbitrageur buys discount call, shorts stock, exercises for ~20-cent profit net of commissions). McMillan's explicit caution: "A dividend payment that exceeds the time premium in the call, therefore, does not imply that the writer will be assigned" — a common misunderstanding he corrects directly.

### Order types and mechanics
- Options trade in **1-cent increments up to $3.00, then 5-cent increments** for stock options; liquid ETFs/indices can trade in pennies at any price.
- Expiration cycles: Jan/Apr/Jul/Oct, Feb/May/Aug/Nov, Mar/Jun/Sep/Dec, plus near-term months; "regular" expiration = Saturday after third Friday, but the effective last trading day is the third Friday, with the customer required to instruct the broker by 5:30 p.m. NY time.
- Weeklys expire on Friday itself, not the Saturday after.
- **Position limits**: largest stocks have limits of 250,000 contracts; smaller stocks 5,000–200,000, depending on liquidity. Not usually relevant at a $100–500 account size, but shows the strategist should check limits before scaling.
- Order types covered: Market, Market Not Held, Limit, Stop, Stop-Limit, Good-Until-Canceled (valid 6 months). McMillan explicitly warns: "one should be cautious about using stop orders with illiquid options," because some exchanges elect stops off the option's *bid*, not last sale, so they can trigger in illiquid, wide markets unintentionally.

### Split/dividend adjustments
- Round-lot splits (2-for-1, 3-for-1, etc.): number of contracts increases, strike decreases, each contract stays 100 shares.
- Non-round-lot splits (e.g., 3-for-2): strike is adjusted by the ratio, contract count unchanged, but each contract now represents a non-standard number of shares (e.g., 150) and gets a **new ticker symbol**. McMillan's caveat: "you must be sure that you are trading the exact contract you intend to... In general, it is a good idea, after a split or similar adjustment, to establish opening positions solely with the standard contracts and to leave the split-adjusted contracts alone" — direct warning against an easy, costly mistake.

---

## Chapter 2 — Covered Call Writing (ch_009.txt + ch_010.txt)

### Strategy name & construction
**Covered call write**: long 100 shares of stock + short 1 call (same underlying), same or fewer calls than round lots of stock owned. "One always decreases the risk of owning the stock" by writing against it.

### Market outlook required
> "The covered writer should be mildly bullish, or at least neutral, toward the underlying stock." Explicitly: "If one is truly bearish on a stock he owns, he should sell the stock instead of establishing a covered write." An out-of-the-money write requires a **bullish** outlook; an in-the-money write is appropriate if "neutral or moderately bearish."

### Numeric formulas (verbatim)
> "Maximum profit potential = Strike price − Stock price + Call price"
> "Downside break-even point = Stock price − Call price"

Worked example: buy XYZ at 48, sell July 50 call at 3 → downside protection of 3 points; if stock stays below 50 at expiration, writer keeps the $300 premium.

### Risk/reward profile
- **Max profit**: occurs at all stock prices at or above the strike at expiration; capped regardless of how high stock rises (writer is obligated to sell at strike).
- **Max loss**: stock falls to zero, offset only by the premium received (i.e., stock cost minus premium).
- "The strategy of owning the stock and writing the call will outperform outright stock ownership if the stock falls, remains the same, or even rises slightly. In fact, the only time that the outright owner of the stock will outperform a covered writer is if the stock increases in price by a relatively substantial amount."
- In-the-money vs out-of-the-money tradeoff, worked numeric example: XYZ at 45, July 40 call at 8 (ITM) gives "8 points, or nearly 18% protection down to price of 37," max profit $300 above 40. July 50 call at 1 (OTM) gives only 1 point downside protection, max profit $600 above 50. "The maximum potential profit of an out-of-the-money covered write is generally greater than that of an in-the-money write" — but ITM has the more conservative/defensive profile.

### Return computations — explicit formulas & worked numbers (Table 2-3 to 2-12, cash and margin examples with 500 shares of XYZ at 43, July 45 calls at 3)
Three statistics McMillan says the writer should **always** compute before entering:
1. **Return if exercised** = Net profit if exercised ÷ Net investment. Cash example: $2,945 / $20,040 = **14.7%**.
2. **Return if unchanged** (a.k.a. "static return"; McMillan notes it is "sometimes incorrectly referred to as the 'expected return'"). Cash example: $1,960 / $20,040 = **9.8%**.
3. **Downside break-even point** — cash example computed as $39.08 (net investment less dividends, divided by shares).

Margin version (50% margin rate) of the same trade: net investment $9,283; return if exercised **25.6%**; return if unchanged **15.3%**; break-even 40.16 (higher than cash breakeven because of margin interest). McMillan's rule of thumb: "unless a fairly deep in-the-money write is being considered, the return on margin will always be higher than the return from cash."

**Margin interest compounding formula** (given but described as a refinement rarely needed):
> "Margin interest charge = Debit [(1 + r)^t − 1]" where r = monthly rate, t = months to expiration.

**Brokerage margin loan cap on covered writes**: "the brokerage firm will loan you only half of the strike price amount as a maximum." Example given: a stock at 20 with a deep ITM call struck at 10 cannot be financed for free; the broker will loan only 5 (half of 10). But McMillan also notes a **zero-margin** covered write is possible: stock at 38, LEAPS call struck at 40 selling at 19 → margin requirement is zero, though risk is still 19 points and margin interest still accrues.

### McMillan's minimum-return guideline (explicit numeric target)
> "A general rule used in deciding what is a minimally acceptable return is to con[sider that a] write would have to have a return if unchanged of at least 6%" [for the holding period, not necessarily annualized — text is slightly garbled by OCR but the surrounding context makes clear this is a per-position floor]. He also states: "In a conservative option writing strategy, one should be looking for minimum returns if unchanged of **1% per month, with downside protection of at least 10%**, as general guidelines." During periods of rich premiums, raise the target to "1½% or 2% per month." Alternative rule: "require that the write be a certain percent in-the-money, say **5%**."

### Downside protection — standard benchmark
> "A standard figure that is often used is the **10% level of protection**."

### Combined (half in-the-money / half out-of-the-money) writing — worked example
Buying 1,000 XYZ at 42, writing 5 April 40 calls (ITM, 4 pts) + 5 April 45 calls (OTM, 2 pts) blends return and protection: combined return if exercised 11.2% vs. 7.6% (all-ITM) or 14.7% (all-OTM); combined protection 9.3% vs. 11.7% (all-ITM) or 7.0% (all-OTM). "By writing both calls, the writer may be able to acquire the return and protection diversification that he is seeking."

### Capital/margin size (directly relevant to a $100–500 account)
- **Minimum contract size caution**: "Buying too few shares for covered writing purposes can lower returns considerably, if the minimum commission charge comes into play." He shows a real numeric effect: a 10-cent worse fill on both legs (stock 43→43.10, call 3→2.90) meaningfully cuts return if unchanged and return if exercised across the Table 2.13 comparisons — i.e. execution slippage of dimes materially matters at small size.
- A single 100-share covered write on even a modest stock (e.g., $40–50/share) requires **$4,000–5,000 of capital** to buy the shares (minus the premium received), which is **far above a $100–500 account**. McMillan doesn't discuss sub-$1,000 accounts at all — this strategy as described assumes at least several thousand dollars of buying power for even one contract. The text does note that low-priced, high-volatility stocks with 1-point strike spacing exist, which would lower the dollar entry point somewhat, but no specific low-capital covered-write example is given.
- "Net" order execution (simultaneous stock+option) is recommended, and some brokers require a minimum share count (500–1,000 shares) to accept a net/contingent covered-write order, though "there are... brokerage firms that will take net orders even for 100-share covered writes."

### Caveats / pitfalls McMillan explicitly warns against
1. **"A serious but all-too-common mistake"**: writing calls against stock you have no real intention of selling. "In essence, writing calls against stock that you have no intention of selling is tantamount to writing naked calls!" He describes writers who keep rolling up for debits chasing a rising stock, "wear[ing] down emotionally," eventually either eating a huge debit to buy back calls or — worse — selling naked puts to fund the rolls, "leveraged tremendously," risking "enough to wipe out the entire account." His fix: "allow the stock to be called away at some point."
2. Rolling down to "lock in a loss" is sometimes still the mathematically correct move — but he cautions this should be weighed against technical support levels and only be done as a full or **partial roll-down** depending on conviction of a rebound.
3. Do not roll up for a large debit unless the position "can withstand at least a 10% correction" — otherwise stay put.
4. Avoid the accidental **uncovered** position: writing a replacement call on the same day the old one expires (before Monday) leaves you naked over the weekend for margin purposes, because the exchange doesn't recognize the worthless option as closed until settlement.
5. Downside protection quoted as a raw percentage is "somewhat misleading" without accounting for the underlying's volatility — 10% protection on a volatile stock is not equivalent to 10% on a low-volatility one (formula deferred to Ch. 28, not covered in these files).
6. Low-priced, non-volatile stocks are the worst candidates for repeated roll-downs because strikes are spaced far apart in percentage terms, forcing the writer to "lock in a loss."

### Follow-up actions catalogued
1. **Protective action if stock declines**: roll down (buy back written call, sell lower-strike call), either fully or as a **partial roll-down** (roll only some contracts) to retain upside optionality while still gaining some downside credit.
2. **Aggressive action if stock rises**: roll up (debit transaction — raises break-even, raises max profit) or close early near parity.
3. **Action near expiration**: roll forward if in-the-money and time premium is gone; for out-of-the-money, compare "return per day" of current vs. longer-dated option and roll forward only if the longer-term option offers a higher return per day (worked numeric example: $8.33/day vs. $9.58/day).
4. **Partial extraction strategy**: sell a portion of shares to fund buying back the written calls at zero net cost, freeing the rest of the position from imminent assignment — useful for low-cost-basis stock the holder doesn't want assigned away (tax reasons).
5. **Incremental return concept ("rolling for credits")**: for large stockholders with a long-term target sale price, write against only part of the position at the nearest strike, then roll up (in size) for credits as the stock climbs toward the target, capturing full appreciation to the target plus cumulative option credits. Explicitly framed for "large stockholders, both individuals and institutions" — not really a small-account strategy.

### Special variants noted (not deeply relevant to a small account but mentioned)
- Covered writing against **convertible securities** (bonds/preferred) — often higher yield than the common; conversion-ratio math given, and a rule of thumb: "Any convertible premium greater than **15%** above computed value might be considered to be too large."
- Covered writing against **warrants** — smaller cash investment since no dividend and lower cost basis, but thin/illiquid market for warrants generally.
- Covered writing via **LEAPS** (diagonal spread variant) — deferred to Chapter 25.

---

## Chapter 3 — Call Buying (ch_011.txt)

### Strategy name & construction
Simple **long call** (buy 1+ calls, no stock). "Call buying is not a strategy in the same sense of the word as most of the other strategies discussed in this text… success… depends primarily on one's ability to select stocks that will go up and to time the selection reasonably well."

### Market outlook required
> "One must be bullish on the underlying stock in order to consider buying calls on that stock." Certainty of timing matters: high conviction/near-term → short-term, higher-delta (even slightly OTM or ITM) calls; low conviction/long horizon → longer-dated calls to "allow room for error in timing."

### Numeric rules / formulas
- **Position-sizing rule of thumb (directly relevant to a small account)**:
> "One should normally not invest more than **15%** of his risk capital in call buying, because of the relatively large percentage risks involved."
- Worked leverage example: XYZ at 48, July 50 call at 3 (6 months); a ~20% stock move can produce a **167%** call profit — illustrating the leverage/risk tradeoff, with max loss capped at the $300 premium paid.
- **Delta** defined as "the amount by which the call will increase or decrease in price if the underlying stock moves by 1 point." Deep ITM delta ≈ 1; deep OTM delta ≈ 0; ATM delta typically "between .50 and .60."
- **Delta-by-holding-period guidance** (explicit, tiered):
  - Day trading: don't use options at all — "trade the stock, not an option" — because of wide bid/ask spreads; if forced to use an option, use short-term ITM with delta "approaching .90 or higher."
  - Short-term (days to ~2 weeks): short-term ITM call, delta "usually in excess of .80."
  - Intermediate-term (weeks to a couple months, less exact timing): at-the-money option (lower delta).
  - Long-term (vague timing, fundamentals-based): "something slightly out-of-the-money, or at least a fairly long-term at-the-money option," or LEAPS.
- **Ranking calls for purchase** — McMillan gives an explicit 6-step method (not a canned formula but a procedure):
  1. Assume each stock advances per its own volatility over a fixed horizon (30/60/90 days).
  2. Estimate call prices after the advance.
  3. Rank by highest percentage reward (aggressive list).
  4. Assume each stock declines per its own volatility.
  5. Estimate call prices after the decline.
  6. Rank by reward/risk ratio = (% gain from step 2) ÷ (% loss from step 5) — this is the "less speculative" list.
  He explicitly warns that ranking calls by simple percentage stock-price targets **without adjusting for volatility is "quite misleading"** — worked example shows a nonvolatile stock's call looking like the "better buy" on a naive 10%-move ranking while the volatile stock's call is actually superior once realistic (volatility-scaled) move sizes are used.
- **Holding-period realism**: "most call purchases are made for holding periods of from 30 to 90 days" — even a 6-month call is usually sold, not held to expiration.

### Risk/reward profile
- Max loss = 100% of premium paid (fixed, known in advance).
- Max gain = theoretically unlimited (stock can rise indefinitely).
- ITM vs OTM tradeoff, worked example: XYZ at 65, July 60 (ITM) at 7 vs July 70 (OTM) at 3; if stock only creeps to 68, "the buyer of the July 70... may actually experience a loss... However, the holder of the in-the-money July 60 will definitely have a profit." Rule stated generally: "an in-the-money call will offer better rewards for a modest stock gain, and an out-of-the-money call is better for larger stock gains."

### McMillan's caveats / pitfalls
- "Absolute dollar price should in no way be a deciding factor for the call buyer. If one's funds are so limited that he can only afford to buy the cheapest calls, he should not be speculating in this strategy." — **directly relevant warning for a very small account**: buying the cheapest (most OTM) calls purely because they're affordable is explicitly discouraged.
- "Time value premium is a misnomer" repeated here too: volatility, not just time, drives that portion of price; a quick change in volatility expectations can swing an option's price heavily even on a day with negligible time decay.
- On over/undervalued calls (relative to a fair-value formula): the mispricing "may be only a small fraction of a point... this information is most useful only to market-makers or firm traders who pay little or no commissions... The general public cannot benefit directly from the knowledge that such a small discrepancy exists, because of commission costs." He explicitly says: "One should not base his call buying decisions merely on the fact that a call is underpriced."
- Follow-up: cut losses using a technical ("mental") stop rather than an actual stop order, because "stop orders for options result in poor executions."
- On taking profits: he explicitly criticizes the psychological asymmetry of readily taking a double on a $5→$10 call but being reluctant to take a double on a $1→$2 call ("we only made a point") — calls this an inconsistency the investor should correct.
- "Every time one takes partial profits, rolls up, or takes other measures, he is doing something bearish to his position" — i.e., adjustment itself has a cost if the trend continues; sometimes a trailing stop and "do nothing" outperforms active management of winners.

### Capital/margin size
- Calls "must be paid for in full; they have no margin value" (except LEAPS, marginable since 1999).
- No cash outlay beyond the premium — this is the **most capital-accessible strategy of the group** for a $100–500 account, since a single call can cost well under $100 depending on strike/stock (though McMillan gives no sub-$500 worked example specifically).
- The 15%-of-risk-capital guideline above is the only explicit sizing rule given.

---

## Chapter 4 — Other Call Buying Strategies (ch_011.txt cont'd, ch_012.txt start)

Two "synthetic" strategies, both built by combining a **short stock position** with **long calls**. McMillan notes these are generally inferior to using listed puts directly when puts are available and liquid — described here mainly for markets where puts are illiquid or unavailable.

### Strategy A: Protected Short Sale (a.k.a. "Synthetic Put")
**Construction**: short 100 shares + long 1 call (same stock), used to cap the theoretically unlimited risk of an uncovered short sale.

**Market outlook**: bearish on the stock, but wanting defined risk instead of open-ended short-sale risk.

**Formula (verbatim)**:
> "Risk = Striking price of purchased call + Call price − Stock price"

Worked example: short XYZ at 40, buy July 40 call at 3 → breakeven 37, max loss $300 (3 points) if stock rises indefinitely; short-seller profit is only slightly reduced vs. an unprotected short.

**Strike selection tradeoff**: buying an OTM call as protection = cheaper insurance but larger max risk (protection doesn't kick in until stock passes the strike); buying an ITM call = minimal risk but severely limits profit potential ("too much protection ... only a small hope of making a profit"). McMillan's general recommendation: "it is best to buy a call that is at-the-money or only slightly out-of-the-money as the protection for the short sale."

**Margin requirement (verbatim rule)**:
> "The margin required is the lower of (1) 10% of the call's striking price plus any out-of-the-money amount, or (2) 30% of the current short stock's market value." A maintenance requirement (≥ the value of the short sale) applies if stock is below the strike.

Worked numeric table given (XYZ at 47, various strike protective calls: margin requirements of $400, $800, or $1,410 depending on strike chosen).

**Portfolio margin note**: qualifying generally requires "account size of at least $100,000 (some brokers require as much as $500,000)" — explicitly **not attainable** for a $100–500 account; standard Reg-T margin applies instead.

**McMillan's caveat**: once the call is in-the-money and profitable, do NOT strip off just the call leg to "bank" that profit while leaving the short exposed — "one is entering into a highly risk-oriented situation by removing his protection when the call is in-the-money."

### Strategy B: Synthetic Straddle (a.k.a. "Reverse Hedge")
**Construction**: short 100 shares + long 2 (or more) calls, same strike, same stock — i.e., buy calls on *more* shares than are shorted. "On stocks for which listed puts are traded, this strategy is outmoded; the same results can be better achieved by buying a straddle."

**Market outlook required**: expects a **large move in either direction** (up or down) — a volatility play, not directional. "This strategy has limited loss potential... and theoretically unlimited profit potential."

**Formulas (verbatim)**:
> "Maximum risk = Striking price + 2 × Call price − Stock price"
> "Upside break-even point = Striking price + Maximum risk"
> "Downside break-even point = Striking price − Maximum risk"

Worked example: short XYZ at 40, buy 2 July 40 calls at 3 each → max risk $600 (occurs exactly at the strike at expiration — "the maximum loss would occur if the stock were exactly at the striking price at expiration"), breakevens at 34 and 46.

**Margin requirement (verbatim)**: "The net margin required for this strategy is 50% of the underlying stock plus the full purchase price of the calls." Worked example: $2,000 (50% of $4,000 stock) + $600 calls = $2,600 total; max risk as % of capital ≈ 23%.

**Ratio variants**: 2:1 is the "standard" ratio; more calls (3:1, 4:1) against 100 shares short = more bullish tilt; more shares short (200) against 3 calls = more bearish tilt. A "synthetic strangle" variant uses two different strikes (short stock + 1 call at the strike above + 1 call at the strike below) to center breakevens when the stock sits between two strikes — worked numeric example given (max loss $350 across the 35–40 range, vs. a larger single-strike max loss).

**Follow-up actions**:
- "Trading against the straddle": take profits on the short-stock leg (or one call leg) once it moves favorably, leaving a smaller residual position; McMillan's caution: "One can never make a large profit if he continually cuts his profits off at a small, limited amount," and cites the case where a full move to 20 nets 14 points if untouched vs. only 2 points if defensively closed early.
- Explicit warning against over-managing: this cuts off the big, rare win that the whole strategy exists to capture.

**Capital/margin size**: Both strategies require **shorting stock**, which needs a margin account and standard Reg-T short-sale margin (50% of stock value) plus the full call premium — this puts both strategies well above a $100–500 account for any normal-priced stock (a $40 stock alone requires ~$2,000+ margin per the worked examples). McMillan gives no low-capital variant.

---

## Chapter 5 — Naked (Uncovered) Call Writing (ch_012.txt)

### Strategy name & construction
Sell 1+ calls **without** owning the stock or any equivalent security (convertible, warrant, or other call). "This strategy has limited profit potential and theoretically unlimited loss."

### Market outlook required
Neutral-to-bearish; writer wants the stock to stay flat or fall, and specifically wants it to **not** rise past the call's strike + premium.

### McMillan's explicit myth-busting (important framing, verbatim-adjacent)
- He opens the chapter directly countering the idea that selling naked calls is easy money from time decay: "Novice option traders often think that selling naked options is the 'best' way to make money, because of time decay... they often assume that market-makers and other professionals sell a lot of naked options. In reality, neither is true." He cites McMillan Analysis Corp. research: "about **65% to 70%** of all options have some value (at least half a point) when they expire" — directly rebutting the popular claim that most options expire worthless.
- Professionals "generally try to hedge them by buying other options or by buying the underlying stock" rather than running naked.

### Numeric rules / formulas
- Worked example: XYZ at 50, sell July 50 naked at 5. Breakeven = 55 (strike + premium). Max profit = premium ($500), occurs anywhere at/below strike at expiration. Loss is theoretically unbounded above breakeven (worked to a $4,500 loss if stock hits 100).
- **Margin requirement (verbatim)**:
> "The margin requirements for writing a naked call are **20% of the stock price plus the call premium, less the amount by which the stock is below the striking price**... a minimum of **10% of the stock price** is required for each call, even if the computation results in a smaller number."
  Worked table (Table 5-2) with four stock prices shows requirements of $1,800 / $1,400 / $720 / $400 depending on how far OTM the written strike is.
- **Collateral, not cash**: "in order to write a naked call, collateral is all that is required. No cash need be 'invested' if one owns securities with sufficient collateral loan value." Marked to market daily; if the stock rises, more collateral is demanded; if it falls, excess collateral is released.
- **McMillan's own risk-management rule**: set aside collateral **as if the stock had already reached the strike price** (or the price at which you intend to cover), even though the formal requirement is smaller: "let the market take you out of a position, [not a margin call]." For naked equity calls specifically: "allow as collateral **20% of the highest naked strike price**."
- **Annualized-return-on-collateral formula (verbatim)**:
> "Annualized current return = (call price) / (0.2 × strike × time [in years])"
  Worked example gives 6% — used as a decision tool for whether to keep holding a nearly-worthless naked short or redeploy capital elsewhere.

### Risk/reward profile
- Max gain = premium received, capped, achieved if stock ≤ strike at expiration.
- Max loss = theoretically unlimited (bounded in practice only by the stock's max possible price move before expiration/before the position is closed).
- Deep OTM naked writing = high probability of a small, capped profit ("this strategy of selling deeply out-of-the-money calls has its apparent attraction in that the writer is assured of a profit unless the underlying stock can rally rather substantially").
- Deep ITM naked writing = closer economically to a short-stock substitute (delta near 1) but with little room before losses begin, and smaller capital requirement (20% vs. 50% margin for an actual short sale).

### Explicit warnings / pitfalls (this is one of the most caveat-heavy sections in these files)
1. **Suitability gate, stated first and foremost**: "The first and foremost question one must address when thinking about selling naked options... is: 'Can I psychologically handle the thought of naked options in my account?'... If one feels that he won't be able to sleep at night, then he should not sell naked options, regardless of any profit projections that might seem attractive."
2. "One or two losses, perhaps... [wipe out] many profits" from the deep-OTM approach — explicitly called "a poor strategy, because one loss may wipe out many profits."
3. **"Rolling for credits" is explicitly condemned as a Martingale strategy**: "This is a strategy that should be avoided." He walks through a worked scenario (Tables 5-3/5-4) where a stock runs from 50→60→70, forcing the writer to roll from 5 contracts → 8 → 15, with collateral ballooning from $5,000 to $21,000 to chase a small original credit. His explicit conclusion: "Martingale strategies should be avoided," and notes real-world limits (OCC position limits, and more commonly, the trader's own collateral) that a casino-style doubling strategy hits and blows up on.
4. Time value premium misnomer repeated a third time in this chapter specifically warning naked writers: "a lot of things can happen between the time an option is sold and its expiration date. The stock can move a great deal, or implied volatility can skyrocket. Both are bad for the option seller."
5. Index options are called out as generally preferable to single stocks for naked writing because "[gaps] are common in stocks, less common in futures, and almost nonexistent in indices" — i.e., single-stock gap risk (news, takeover, etc.) is a real, named danger for naked call writers.

### Capital/margin size
- No cash is strictly required if the trader already holds marginable collateral, but a **brokerage-imposed minimum account equity for naked writing approval ranges "as low as $2,000 to as high as $100,000."** This is explicitly stated and is **directly disqualifying for a $100–500 account** — most brokers will not even approve naked call writing at that equity level, aside from the unlimited-risk problem itself.

---

## Chapter 6 — Ratio Call Writing (ch_012.txt)

### Strategy name & construction
Own a certain number of shares and sell **more** calls than covered by the shares — "a combination of these two types of positions [covered + naked]." Most common form: the **2:1 ratio write** = long 100 shares + short 2 calls (1 covered, 1 naked).

### Market outlook required
> "Generally, when an investor establishes a ratio write, he attempts to be **neutral** in outlook regarding the underlying stock. This means that he writes the calls with striking prices closest to the current stock price." A more bullish stance = wider ratio using OTM calls or fewer calls per round lot (e.g., 3:2); more bearish = more calls per round lot (e.g., 3:1) or ITM calls.

### Numeric formulas (verbatim, 2:1 case)
> "Points of maximum profit = Strike price − Stock price + 2 × Call price"
> "Downside break-even point = Strike price − Points of maximum profit" [= Stock price − 2 × Call price]
> "Upside break-even point = Strike price + Points of maximum profit"

Worked example: buy XYZ at 49, sell 2 October 50 calls at 6 each → max profit 13 points ($1,300) at strike; breakevens at 37 (downside) and 63 (upside); profit anywhere between = the "profit range." Graph described as roof-shaped, peaking at the strike.

**General formulas for any ratio (verbatim)**:
> "Maximum profit = (Striking price − Stock price) × Round lots purchased + Number of calls written × Call price"
> "Downside break-even = Striking price − Maximum profit / Number of round lots purchased"
> "Upside break-even = Striking price + Maximum profit / (Calls written − Round lots purchased)"

**Neutral (delta-based) ratio formula**:
> "The neutral ratio is determined by dividing the delta of the written call into 1" — worked example: delta .60 → neutral ratio = 1/.60 = 5:3 (buy 500 shares, sell 3 calls, roughly).

**Equivalent Stock Position (ESP) formula (verbatim)**:
> "ESP = number of options × delta × shares per option." Worked example: 10 calls with delta .45, 100 shares/contract → ESP = 450 shares equivalent. Used to reduce a whole multi-leg position to a single net directional number; "an ESP of 0 is considered to be a perfectly neutral position."

### Risk/reward profile
- **Max profit**: at the strike price at expiration (roof peak); "the maximum profit occurs at the striking price of the written calls at expiration."
- **Max loss**: theoretically unlimited **upside** (naked-call component) and substantial but limited **downside** (stock can only fall to zero); "the position has both large upside risk above 63 and large downside risk below 37" in the worked example.
- **Selection criterion given explicitly**: the profit range should be wide enough that "the next higher and lower striking prices [are] within the profit range" — this leaves room to roll if the stock approaches either edge. Also stated: "the profit range [should be] wide in relation to the volatility of the underlying stock," and technical support/resistance ideally sit inside the range.
- McMillan directly frames the strategic logic: "in fact, if one were to try to set up the optimum strategy, he would want it to make its most profits in [the] range [of most likely stock prices]" — arguing ratio writing aligns with the empirical shape of stock-price probability distributions better than either pure covered or pure naked writing.

### Variable Ratio Write / "Synthetic Short Strangle" / "Trapezoidal Hedge" (sub-strategy)
When stock sits between two strikes: buy 100 shares + sell 1 ITM call + sell 1 OTM call (instead of 2 of one strike). Creates a flat-topped ("trapezoidal") max-profit zone spanning *between* the two strikes rather than a single peak.

**Formulas (verbatim)**:
> "Points of maximum profit = Total option premiums + Lower striking price − Stock price"
> "Downside break-even point = Lower striking price − Points of maximum profit"
> "Upside break-even point = Upper striking price + Points of maximum profit"

Worked example: XYZ at 65, Oct 60 call at 8 + Oct 70 call at 3 sold against 100 shares → max profit $600 (smaller than a single-strike ratio write's peak profit) but "a vastly greater probability of realizing the maximum profit," with breakevens at 54 and 76.

### Follow-up actions catalogued
1. **Rolling up/down at striking prices** as the stock approaches an edge of the profit range, re-centering the position (worked numeric examples given for both directions).
2. **Adjusting the ratio itself** as the stock trends strongly — decreasing calls-per-share as stock rises (moving toward a plain covered write), increasing calls-per-share as stock falls — "in either case, the ratio of calls outstanding to stock owned is reduced [or increased]." McMillan flags this dynamic-ratio approach as "more oriented to extremely large investors or to firm traders, market-makers" because of the commission cost of frequent rolling — **explicitly not well-suited to a small retail account.**
3. **Delta-based adjustment**, using the formulas above, to keep ESP near zero as deltas shift.
4. **Stop orders on the stock itself** as an automatic, unemotional adjustment mechanism (buy stop above, sell stop below) that converts the ratio write into a plain covered write (if stock rallies through the buy stop) or into a naked write (if stock falls through the sell stop) — worked numeric examples given for both directions, including new post-stop breakevens.
5. **"Telescoping" protective/stop points** closer together as the position accrues unrealized profit approaching expiration, to lock in gains while leaving room for the position to reach full max profit.

### McMillan's caveats / pitfalls
- Common objection countered: "Why bother to buy 100 shares of stock and sell 2 calls? You will be naked one call. Why not just sell one naked call?" McMillan's rebuttal: the two strategies' profit graphs "bear no resemblance" to each other — ratio writing is a genuinely different (roof-shaped, defined profit-range) risk profile, not "sloppy" naked writing.
- Acknowledges the real psychological problem: "When stock prices are rising and everyone who owns stocks is happy and making profits, the ratio writer is in danger of losing money" — an explicit behavioral caveat about why some investors won't tolerate this strategy even though it is mathematically favorable in the "most probable" price range.
- Direct comparison to the reverse hedge/synthetic straddle (Ch. 4): "in stable markets, the ratio writing strategy is generally superior. However, in times of depressed option premiums, the synthetic long straddle gains a distinct advantage" — i.e., which strategy is "correct" depends on whether options are cheap or rich relative to realized volatility, not on a fixed rule.
- Delta-neutral trading is explicitly **not** described as easy money: "Delta-neutral trading is not 'easy': Either (1) one assumes some price risk as soon as the stock begins to move, or (2) one keeps constantly adjusting his deltas to keep them neutral. Method 2 is often not feasible for public traders because of commissions." He also warns that a delta-neutral naked straddle "has naked options on both sides, and therefore has tremendous liability" — neutrality of delta says nothing about tail risk.

### Capital/margin size
- **Margin requirement = sum of the covered-write requirement + the naked-write requirement** (both formulas from Ch. 2 and Ch. 5 combined). Worked example (Table 6-2/6-3): buying 100 XYZ at 49 and selling 2 Oct 50 calls at 6 → total initial requirement **$2,730** (before commissions), but McMillan explicitly recommends reserving capital as if the stock had already risen to the *upside breakeven* (here, **$3,910**) to avoid ever facing a forced margin call: "he should therefore plan to invest $3,910 in this position, not $2,730."
- This — like covered writing and naked writing — requires **several thousand dollars per position** in the worked examples given. No sub-$1,000 or sub-$500 example is provided anywhere in this chapter. Ratio writing inherits both the stock-ownership capital requirement of covered writing *and* the naked-writing collateral/equity-approval requirements, making it (along with naked writing) the **least accessible** of the six strategies covered in these files for a $100–500 account.

---

## Cross-chapter theme: "time value premium is a misnomer"

McMillan repeats this point near-verbatim in **three separate chapters** (Ch. 1, Ch. 3, Ch. 5), each time in the context of a different strategy (basics, call buying, naked writing) — strong enough repetition to flag as one of his central recurring caveats: the non-intrinsic part of an option's price is driven more by **volatility expectations** than by pure time decay, and traders who treat it as "money that just wastes away on a clock" will misjudge both buying and selling decisions.

---

## Note on capital size ($100–500 account)

None of these six files contains a strategy example sized for a $100–500 account. The only strategy in this set that is structurally compatible with that size is **plain long call buying** (Chapter 3) — a single call can cost well under $100 depending on the underlying and strike, requires no margin account, and McMillan gives an explicit position-sizing rule (≤15% of risk capital) that scales down fine to a small account. Every other strategy covered here (covered call writing, protected short sale, synthetic straddle/reverse hedge, naked call writing, ratio call writing) requires either full-price stock ownership, a margin/short-sale account, or broker-imposed minimum equity for uncovered writing ($2,000–$100,000 per McMillan's own figures) — all of which exceed a $100–500 account by a wide margin. This is a direct, stated fact from the text (not an inference dressed up as McMillan's opinion) and should be treated as a hard constraint when deriving actionable strategies from this book for the stated account size.
