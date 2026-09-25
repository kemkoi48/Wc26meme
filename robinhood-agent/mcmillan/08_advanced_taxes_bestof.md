# McMillan Notes — Advanced Concepts, Volatility Derivatives, Taxes, and "The Best Strategy?"

Source: *Options as a Strategic Investment*, 5th ed., Lawrence McMillan. Extracted directly from the epub-to-text conversion of Chapters 40–43 (files ch_043.txt through ch_048.txt). All numeric rules below are quoted or closely paraphrased from the actual text — nothing here is filled in from general options-trading knowledge.

---

## Chapter 40: Advanced Concepts

This chapter is **not** about exotic strategies — it is McMillan's treatment of the option "Greeks" (risk measurements) and how to use them to build, evaluate, and adjust neutral positions. Contents, in the order presented:

### Neutrality
The chapter opens by re-explaining *why* neutral positions matter: "Neutrality, as it applies to option positions, means that one is noncommittal with respect to at least one of the factors that influence an option's price... one can design an option position in which he can profit, no matter which way the underlying security moves." Neutral strategies "always require at least two options in the position—a spread, straddle, or some other combination."

### The Greeks — six risk measures described
The chapter states there are **six** components, though "only four are heavily used": **Delta, Gamma, Vega (Tau), Theta, Rho**, and (for advanced use only) the **"gamma of the gamma."**

- **Delta**: "a number that ranges between 0.0 and 1.0 for calls, and between -1.0 and 0.0 for puts." Also described as roughly the market's implied probability of finishing in-the-money: "if XYZ is 50 and the January 55 call has a delta of 0.40, then there is a 40% probability that XYZ will be over 55 at January expiration." Delta of a longer-term at-the-money option is larger than a shorter-term one, and shrinks faster as expiration nears. **Position delta** = "Option's delta × Shares per option × Option quantity" (this is the "equivalent stock position," ESP, or for futures, EFP).

- **Gamma**: "how fast the delta changes with respect to changes in the underlying stock price." Maximum near the strike, approaches zero deep ITM/OTM. Example: with an at-the-money option and only a day or two left, "the delta of the option would jump to nearly 1.00... Thus, the gamma would be roughly 0.25." Table 40-4 shows the ATM gamma exploding as expiration nears: "With only one week remaining, the gamma is over 0.28." Gamma of the underlying itself is always zero.

- **Vega (Tau)**: "the amount by which the option price changes when the volatility changes... always expressed as a positive number." Example: "the vega of the option is 0.25... If the volatility increases by one percentage point... the option will increase in value by 0.25." Vega is greatest for at-the-money, longer-term options.

- **Theta**: "measures the time decay of a position... generally expressed as a negative number... if an option has a theta of -0.12, that means the option will lose 12 cents... per day." Decay is not linear — "an option will lose a greater percent of its daily value near the end of its life."

- **Rho**: price sensitivity to interest-rate changes. "Rho is expressed as a positive number for calls and a negative one for puts... larger for longer-term options and is nearly zero for very short-term options." McMillan notes rho "is the least used" of the risk measures, "important as a consideration when one is trading LEAPS or warrants."

- **Gamma of the gamma**: "the amount by which the gamma will change when the stock price changes" — a sixth-order measure McMillan says is "most important for strategists involved in positions on highly volatile stocks... its use is limited to only the most sophisticated traders."

### Summary table of strategy exposures (Table 40-8)
McMillan provides a general risk-exposure table (Delta/Gamma/Theta/Vega/Rho signs) for: buy stock, sell stock short, call buy, put buy, straddle buy, covered write, naked call sale, naked put sale, ratio write (straddle sale), calendar spread, bull spread, bear spread, ratio call spread, ratio put spread.

Key takeaway he draws from it: **covered writing and naked put selling have "all the same risk factors" as naked straddle selling, but are *worse* because they aren't even delta neutral** — "if one felt that straddle selling is not a particularly attractive strategy after he had observed these examples, he then should feel even less inclined to do covered writing."

### Delta-neutral positions are not fully neutral
Central worked example: XYZ at 88, sell 100 July 90 straddles for 10 points. Initial position: delta = **-100 shares** (looks like almost nothing), but **gamma = -600 shares**. McMillan shows that a mere 2-point stock move produces an unrealized loss of **$800**, computed via: "Total loss for 2 points of stock movement = 2 × position delta + position gamma." He also shows position theta (+$600/day, favorable) and position vega (**-$3,600** for a 1-point vol increase, "the greatest risk in this short straddle position"). His conclusion: "it is imperative that the straddle seller engage in the strategy only when there is a reasonable expectation that volatilities are high and can be expected to decrease."

### Creating multifaceted neutrality (gamma-neutral, vega-neutral, etc.)
Method: "neutralize gamma first, for delta can always be neutralized by taking an offsetting position in the underlying security." Worked examples show solving 2 simultaneous equations (gamma and vega) for two unknowns (quantities of two options), then neutralizing the resulting delta with stock. He notes a full 3-equation (delta/gamma/vega) solve is possible with three options and no stock needed, and this is best done by computer.

### Evaluating positions using projected price paths
Method: project stock prices at future dates using standard-deviation multiples (formula: `Future Price = Current Price × e^(a·σ√t)`), then recompute P&L, delta, gamma, theta, vega at each projected price/time. Example table shows a gamma/delta-neutral ratio spread that is profitable if the stock stays flat or falls, but develops serious upside risk after the position drifts because gamma decays away from neutral.

### Trading gamma from the long side
Discusses positions constructed to be long gamma (e.g., reverse calendar spreads: buy near-term, sell longer-term) while staying delta- and vega-neutral. Key finding: being long gamma with vega neutral still costs heavily on theta (example position loses "$625 per day from time decay"). He walks through three variant constructions (gamma-long/vega-neutral; gamma-long/vega-long; vega-long/gamma-neutral) and concludes the third — long volatility only, not long gamma — was "probably the best of the three," since being both long gamma and long volatility "involved too much risk of time decay."

### Advanced mathematical concepts
Gives shortcut numerical-approximation recipes for computing each Greek (bump-and-reprice method), and closes with a technique for **"measuring the difference of implied volatilities"** across an option chain: compute the standard deviation of individual implied vols ("implied deviation"), divide by the average implied to get "percent deviation." His threshold: **"This 'percent deviation' number is usually significant if it is larger than 15%."** He notes that on a scan across the market, "the list is usually quite short—perhaps 20 stocks and 10 futures contracts will qualify."

---

## Chapter 41: Volatility Derivatives

### What's covered
VIX history and calculation, VIX futures, variance futures, VIX options, other volatility indices/ETFs/ETNs (VXX, VXZ, XIV, TVIX, etc.), directional/trading strategies using VIX data, portfolio-protection strategies using VIX derivatives, and hedged/spread strategies specific to VIX options.

### VIX calculation basics
- Original VIX released 1993 (backdated to 1986), based on OEX options; renamed **VXO** after the 2003 revamp.
- "New" VIX (2003–present) is based on SPX options, "based on the 'strips' of" nearly all strikes with live bid/offer in the first two expiration months.
- "Both the old and new VIX are **30-day volatility measures**." This is repeatedly emphasized as the reason near-term futures track VIX far better than longer-dated ones.
- VIX-like calculations also exist for other entities: gold (GVZ off GLD), oil (OVX off USO), Euro (EVZ off FXE), Emerging Markets (VXEEM), Silver (VXSLV), China (VXFXI), Gold Miners (VXGDX), Energy (VXXLE), and individual names at time of writing — Apple, Amazon, Goldman Sachs, Google, IBM. Of the whole list, "the only one that has tradeable products at this time is GLD" (CFE futures under GV, options under GVZ).

### VIX futures
- "A VIX futures contract is worth **$1,000** for every one point move it makes."
- "At this time, the exchange minimum margin for trading one VIX futures contract is **$4,000**." (spread margin discussed separately, see below)
- Expiration: "The expiration of VIX futures in any given month is **30 days prior to the SPX option expiration in the next month**. This is always a Wednesday." Settlement price symbol: **VRO**.
- Futures at a higher price than VIX = trading "at a premium"; lower = "at a discount." Term structure = the collective pattern of premiums across the curve.
- Positive-sloping term structure "usually exists during bullish markets and/or if VIX is quite low-priced." Negative slope (inverted) "usually exists during the throes of an ongoing bear market."
- Repeated historical examples (Feb 2007 China margin-rate shock, July–Aug 2007 subprime onset, Sept–Oct 2008 Lehman crisis) all make the same structural point: **"the near-term contracts are the only ones that approximate what VIX is doing, even when VIX explodes in a financial crisis."** In the Sept 3 – Oct 10, 2008 window VIX rose **+226%**, the September/October blended futures rose **+186%**, but the March '09 contract only rose **24%**.
- Trading signal McMillan states explicitly: **"a spike peak in VIX— especially when all of the futures are trading at a discount to VIX—is a buy signal for the broad stock market."**

### Variance futures
Settle at 90-day historical volatility of SPX, quarterly (Mar/Jun/Sep/Dec), one point worth **$50**. Margin: **"If all of the futures contracts listed are trading at prices of 400 or less, then margin is $5,500 per contract"** scaling up to **"$230,000"** per contract at the high end. McMillan is blunt: **"these variance contracts have been a great disappointment... the open interest was only a few hundred contracts."**

### VIX options — the critical mechanical point for a small trader
**VIX options are priced off the VIX *futures*, not off VIX itself.** This is stated repeatedly and is the single most important mechanical fact in the chapter: "the price of VIX is an irrelevant piece of information! ... VIX options are priced off of the futures contracts!" He gives a real example from the Oct 10, 2008 crisis where VIX was 69.96 but the Oct 25 call, Nov 25 call, and Dec 25 call all traded at wildly different, seemingly nonsensical levels relative to VIX — but were priced correctly relative to their respective futures months (Oct fut 56.71, Nov fut 38.30, Dec fut 33.78).

**Concrete danger flagged: VIX option calendar spreads.** He walks through an actual case (Sept 8, 2008: buy Nov 25 call/sell Oct 25 call for a 0.40 debit) that by Oct 10, 2008 was trading at **-17.90**, for a total loss of **"$1,830 plus commissions"** on what looked like a normal, low-risk calendar spread — because the two legs have *different underlyings* (different futures months). He notes the industry response: **"most experienced brokerage firms are asking for naked margin for any short options in a VIX calendar spread or diagonal spread; only vertical spreads receive the usual reduced margin requirement."**

### Volatility of volatility
"the historical volatility of VIX remains amazingly constant, averaging about **90%**" (100-day HV), ranging roughly 60%–150%; 20-day HV ranged 40%–270%. This underlies why VIX options carry very high implied vols and wide skews.

### VIX skew structure
Two skews: (1) horizontal — near-month VIX options always trade at higher IV than far months, because "the range of volatilities of each futures month" (i.e., realized vol of the front-month future) is genuinely higher; this is *not* automatically a trading opportunity the way a stock skew would be. (2) Vertical — "for VIX, higher strikes should have higher implied volatilities than lower strikes" (the mirror image of SPX's put skew), which he says favors call ratio spreads (buying lower/cheaper-IV strikes, selling higher/richer-IV strikes) and put backspreads.

### VXX / ETN mechanics and the roll-cost problem
VXX = "iPath S&P 500 VIX Short-term Futures Exchange Traded Note," launched Jan 31, 2009, uses front two VIX futures months. Companion mid-term note VXZ uses months 4–7. Because the term structure is usually upward-sloping (contango) in bull/calm markets, the daily roll from front-month to next-month **costs money every day** — "VXX outperforms when the term structure slopes downward (which only happens in bearish times or when VIX is at very high levels), while VXX underperforms when the term structure slopes upward (which is common during bullish times)." Inverse product: **XIV** (VelocityShares); "double speed" leveraged products: **TVIX/TVIZ**. His verdict: **"If you just want to speculate on volatility, the VIX futures appear to be superior to VXX."**

### Directional/predictive use of VIX
- "VIX moves opposite to the market about **75%** or **80%** of the time" on a daily basis.
- Spike peaks in VIX (especially when futures are at deep discounts to VIX) = market-bottom buy signals; extreme lows in VIX (below 10) historically preceded sharp market declines — his study (Table 41-10) of dates when VXO closed below 10 and VIX below 10.30 found SPX declines of roughly 0.7%–3.3% typically arriving within 1–8 trading days.
- **"When VIX is higher-priced, and the front-month futures trade at a large premium, that is usually a sign that 'smart money' is expecting a sharp increase in volatility."** He gives the Dec 2007 example: a **4.63-point** front-month futures premium over VIX preceded a 230-point SPX drop within a month. He also cautions this signal loses effectiveness in an ongoing bull market (2009–2011 example), where large premiums are simply normal.
- He explicitly says he is **not** a fan of applying stock-style technical indicators to VIX itself: "Using Bollinger Bands, MACD, or even put-call ratios on VIX and its options does not produce steady or significant results."
- A backtested "perpetual VIX call buy" strategy — buying VIX calls 3 strikes OTM monthly and rolling — is shown (Figure 41-11) to have produced roughly **"a total profit to date of about $2,000"** (before commissions) over the ~5-plus years since VIX options began trading, with a max drawdown around **"$1,300"** by mid-2008 before the crisis paid off.

### Using VIX derivatives to protect a stock portfolio — the chapter's main practical payoff
McMillan lists six "macro" hedging approaches (broad-based index puts, put spreads [he explicitly disfavors], selling calls, collars, futures, and volatility derivatives) and argues volatility derivatives, specifically VIX calls, are **structurally superior to SPX puts** as portfolio insurance:

> "VIX CALLS ARE A BETTER PORTFOLIO HEDGE THAN SPX PUTS... VIX calls... provide dynamic protection, whereas SPX puts do not." Example: SPX puts bought 8% OTM become "300 points out of the money" and nearly worthless as protection after a summer rally, while VIX calls stay useful because "if the market drops sharply from 1700, VIX will shoot up into the 30s and the VIX long calls will provide protection even though the stock market is much higher than it originally was."

Sizing guidance (explicitly sourced to a pre-2004 Merrill Lynch study, later studies revised upward):
> "shortly before the volatility futures were listed in 2004, an analysis performed by Merrill Lynch showed that a **10%** volatility hedge was sufficient to protect a broad-based stock portfolio... In later years, other studies have shown that a **20%** hedge is more appropriate."

Concrete formula given: **"Quantity = 10% × NAV/(100 × Strike price)"** for VIX call quantity, and a rule of thumb: **"Calls to buy per $100,000 of volatility-adjusted value = percentage × 0.35"** where percentage is 10–20 (his stated opinion: **"percentage should be 20, or perhaps even higher"**).

Cost data for the SPX-put alternative (13-year backtest, 1997–2010, buying 3-month 10%-OTM SPX puts quarterly): **"the cumulative cost of the protection over the 13+ years was 18% of the SPX value... On average, that's a less than 2% annual cost."** At the worst point (late summer 2008) cumulative cost reached **"about minus 32 percent"** (~3%/year average to that point).

### VIX/SPY hedged strategy
A market-neutral(ish) strategy exploiting large VIX-futures premiums/discounts: buy calls on both VIX and SPY (when futures are at a discount to VIX) or puts on both (when at a premium). Sizing formula given (uses relative volatility, price, and deltas of the two legs): rule of thumb stated as **"this formula generally tells one to buy about twice as many VIX options as SPY options"** (a ~2-to-1 ratio), though he stresses "the formula should be applied each time... Do not merely rely on the 2-to-1 ratio."

### VIX ratio spreads/backspreads
Because of the forward (positive) vertical skew in VIX options, **call ratio spreads** (buy lower-strike, sell more higher-strike calls) have "a theoretical advantage," while **put ratio spreads** work against the trader's edge ("Certain institutional traders seem to like VIX put spreads, even though there is a theoretical disadvantage"). **Put backspreads** are favored for downside-volatility speculation because they exploit the same skew in the trader's favor.

### Access/account-requirement notes flagged explicitly in the text
- VIX futures require a **futures account** (margin currently $4,000/contract minimum per the text; calendar-spread margin in the first three months was raised from an original $100 to **$625**).
- Variance futures require far larger margin ($5,500 up to $230,000/contract) and are described as illiquid ("a great disappointment").
- VIX options settle for **cash** based on the special AM VRO settlement, not the usual close-of-market process — mechanically different from equity/index options a retail trader may be used to.
- The chapter repeatedly stresses that **VXX/VXZ and the various ETNs (XIV, TVIX, VIIX, VIIZ, ZIV, etc.) are the accessible route for traders who cannot or do not want a futures account** ("a way for entities that cannot trade futures and options to trade volatility"), since these trade as ordinary equities/ETNs in a standard brokerage account and have listed options with normal expiration. The text does not otherwise state any special account-approval requirement for VIX index options themselves beyond the standard options-approval tiers used elsewhere in the book (index/cash-settled option approval), but does flag that "most brokerage option platforms... do not calculate VIX option Greeks and implied volatility correctly" — a practical, not regulatory, caution.

---

## Chapter 42: Taxes

**Disclaimer stated by the author up front:** "tax laws change, and therefore should consult tax counsel before actually implementing any tax-oriented strategy." (Repeated multiple times in the chapter — treat everything below as historical text, not current law.)

### Basic holding-period / character rules
- "An option is a capital asset and any gains or losses are capital gains or losses."
- "The holding period for option transactions to qualify as long-term is always the same as for stocks (currently, its one year)."
- "**Gains from the sale of options are short-term capital gains**" — i.e., a written option that is bought back or expires can never itself produce a long-term gain, regardless of how long it's held short. ("A written call cannot produce a long-term gain, regardless of the holding period.")
- Table 42-1 mapping (option premium treatment on exercise/assignment):
  - "Call buyer exercises → Add call premium to stock cost"
  - "Put buyer exercises → Subtract put premium from stock sale price"
  - "Call writer assigned → Add call premium to stock sale price"
  - "Put writer assigned → Subtract put premium from stock cost"
- "For tax purposes, an option that expires worthless is considered to have been sold at zero dollars on the expiration date."

### The 60/40 rule (Section 1256 contracts)
Applies to **nonequity options** (index options such as OEX/SPX, and futures/futures options) — they "must be marked to market at the end of the tax year and taxes paid on both the unrealized and realized gains and losses." Rate treatment: **"Regardless of the actual holding period of the positions, one treats 60% of his tax liability as long-term and 40% as short-term."** This applies "even [to] gains made from extremely short-term activity such as day-trading." Reported on **"Section 1256"** form. He flags an asymmetric downside: **"if one loses money in nonequity options, he actually has a tax disadvantage in comparison to equity options, because he must take some of his loss as a long-term loss, while the equity option trader can take all of his loss as short-term."**

### Qualified covered call rules (the deeply-in-the-money covered-write trap)
If you write a call against stock **not yet held long-term**, and the call is "too deeply in-the-money," it can **wipe out the stock's accrued holding period entirely**; if it's in-the-money but not too deep (a "qualified covered call"), the holding period is merely **suspended** while the call is outstanding (it resumes counting once the call is gone). Out-of-the-money calls never affect the stock's holding period at all.

The "qualified" test, quoted directly (from Appendix E rules as summarized in the chapter — flagged by McMillan as subject to change, consult a tax advisor):
1. "the option has more than **30 days** of life remaining when it is written, and"
2. Benchmark strike test based on "applicable stock price" (ASP, usually prior day's close, or the opening print if the stock gaps up more than 10%):
   - "If the ASP is less than $25, then the benchmark strike is **85% of ASP**."
   - "If the ASP is between 25.01 and 50, then the benchmark is the **next lowest strike**."
   - "If the ASP is greater than 50 and not higher than 150, and the call has more than **90 days** of life remaining, the benchmark is **two strikes below the ASP**" (with the added condition that "the benchmark cannot be more than 10 points lower than the ASP").
   - "If the ASP is greater than 150 and the call has more than 90 days of life remaining, the benchmark is two strikes below the ASP" (no 10-point cap stated at this tier).

If the stock is **already long-term** when the call is written, none of this matters — it stays long-term when called away regardless of strike depth. But: "if one sells an in-the-money call on stock already held long-term, and then subsequently buys that call back at a loss, the loss on the call must be taken as a long-term loss because the stock was long-term."

### Wash sale rule — explicitly discussed for options
> "the wash sale rule denies a tax deduction for a security sold at a loss if a substantially identical security, or an option to acquire that security, is purchased within **30 days before or 30 days after** the original sale." (i.e., a 61-day window.) "A call option is certainly an option to acquire the security. It would thus invoke the wash sale rule for an investor to sell XYZ stock to take a loss and also purchase any XYZ call within 30 days before or after the stock sale."

Two useful clarifications given:
- "Various series of call options are not generally considered to be substantially identical securities" — selling one call series at a loss and buying a *different* call series/strike/expiration on the same stock does not itself trigger a wash sale on the option-to-option trade (though it's unclear whether repurchasing the *identical* series would).
- **Selling a put is generally held NOT to be "acquisition of an option to buy stock"** — so a specific workaround strategy is given: sell your stock at a loss (to realize the loss), and simultaneously sell an in-the-money put on the same stock (long-dated, to minimize early-assignment risk) to retain economic exposure without triggering the wash sale rule. Must be done in a margin account since the put is naked. Caveat: if the stock is put back to you before the 30 days elapse, "the wash sale rule would be invoked" after all.

### Short-sale rule / "married put" — the put-buyer's holding-period trap
Buying a **protective put** against stock that is **not yet long-term** is treated under the short-sale rules and **wipes out the entire accrued holding period of the stock** — the clock resets and doesn't start again until the put is disposed of. Two exceptions:
1. Stock already long-term when the put is bought → no effect.
2. **"Married" put and stock**: bought at the same time, with a stated intent to exercise that specific put against that specific stock — normal holding-period rules then apply. But: "the investor must actually go through with the exercise of the put in order for the 'married' status to remain valid" — if the put instead expires worthless, its cost simply adds to stock basis instead of being a separate loss; and once an original married put is disposed of, "no other put may be considered to be 'married' to the stock" (you can't roll married status forward).

This mechanic can be used deliberately: buying a put on a long-term-gain position defers realization of that gain to a later tax year without giving up the position; or buying a put on an unrealized loss position that is close to going long-term "avoids having to take a long-term loss" by resetting to short-term status.

### Deferring short-term gains into the next tax year
For a profitable long call about to expire in the following tax year, three named tactics to lock in the gain while deferring realization: (1) buy an in-the-money put (a "combination"/collar-like lock), (2) sell an in-the-money call against it to create a spread (risk: early assignment), (3) short the stock against the long call. Analogous tactics given for a profitable long put (buy a call, sell a put to spread, or buy the stock). McMillan flags that **deferring gains on a naked short option position this way essentially doesn't work** — none of the "opposite" actions actually lock in the writer's profit without introducing new open-ended risk, so "there is no relatively safe way for an uncovered call writer to attempt to 'lock in' an unrealized gain for the purpose of deferring it to the following tax year."

### Unequal tax treatment on spreads (LEAPS example)
A vertical spread held >1 year, with one leg long-term and one leg short-term, can generate a real quoted result: **long-term gain on the long leg, short-term loss on the short leg, even though the spread as a whole made money.** Worked example (buy Jan 70 LEAPS call at 13, sell Jan 80 LEAPS call at 7, close 14 months later): "$700 long-term gain" on the long leg vs. "$400 short-term loss" on the short leg — net favorable tax character despite the spread having widened from a 6-point debit to a 9-point credit. Same logic applies, he notes, to spreads pairing nonequity (1256/60-40) instruments against equity options — though he cautions "there is no riskless way to do this" and "one should be cautious about establishing spreads merely for tax purposes."

### Author's closing caution (verbatim spirit)
> "the options strategist should be careful not to confuse tax strategies with his profit-oriented strategies... one should not attempt to stay in a position too long or to close it out at an illogical time just to take advantage of a tax break. The tax consequences of options should never be considered to be more important than sound strategy management."

---

## Chapter 43: The Best Strategy? (McMillan's own closing synthesis — read carefully)

This is a short chapter (roughly 5 pages of text) and is explicitly framed as McMillan's final word across the whole book. Below are his conclusions closely following the actual language.

### There is no single best strategy — his opening thesis, verbatim
> "There is no one best strategy. Although this statement may appear to be unfair and disappointing to some, it is nevertheless the truth. Its validity lies in the fact that there are many types of investors, and no one strategy can be best for all of them. **Knowledge and suitability are the keys to determining which strategy may be the best one for an individual.**"

### Strategy grouping by market attitude
- **Aggressive / directional**: outright put or call buying, low-debit (high-potential) bull and bear spreads.
- **Conservative**: covered call writing, in-the-money (large-debit) bull or bear spreads — "the possibility of making a reasonable but limited return, coupled with decreased risk exposure."
- **If options are expensive and the market is expected to be range-bound/small-moving**: ratio writing, ratio spreading ("especially 'delta neutral spreads'"), straddle and strangle writing, neutral calendar spreading, and butterfly spreads "should perform well."
- **If options are cheap and the market is expected to be volatile**: straddle and strangle buys, backspreads, and reverse hedges and spreads "would be best."
- Calendar/diagonal spreads are noted as overlap strategies: "initially a neutral position. It only assumes a bullish or bearish bias after the near-term option expires."

### Strategies McMillan explicitly says to avoid
> "some strategies are generally to be avoided by most investors: **high-risk naked option writing (selling options for fractional prices) and covered or ratio put writing.**"

### The strategy shape he prefers in general
> "In essence, the investor will normally do best with a position that has **limited risk and the potential of large profits**. Even if the profit potential is a low-probability event, one or two successful cases may be able to overcome a series of limited losses."

He names two concrete examples of this shape: the diagonal put/call combinations (Chapters 23–24) and, as "the simplest strategy fitting this description," **the T-bill/option purchase program** (Chapter 26) — i.e., keeping the bulk of capital in Treasury bills and risking only a small speculative slice on option purchases.

### Equivalent positions — the same payoff can carry very different practical risk
He stresses that strategies with mathematically identical dollar profit/loss profiles can have very different *percentage* risk and practical characteristics:
- Stock + protective put ≈ long call in dollar-risk/dollar-profit shape, but "the purchase of stock and a put requires substantially more initial investment dollars than does the purchase of a call... The stockholder will receive cash dividends while the call holder will not."
- Straddle purchase ≈ reverse hedge (short stock + long calls) ≈ "buying 100 shares of stock and simultaneously buying two puts" — same dollar payoff shape, "Their percentage risks are substantially different, however."

His conclusion from this section: **an investor must know two things well — the strategy itself, and his own attitude toward risk/reward (suitability)** — and understanding the *mechanics* (e.g., annualized risk on the T-bill piece) is not optional even if the philosophy is understood.

### "What is best for me might not be best for you" — investor-type mapping
- **Conservative investor**: "would certainly not want to be an outright buyer of options... covered call writing might be the best strategy... accomplish his financial aims—moderate profit potential with reduced risk."
- **Aggressive investor**: "would most likely not consider covered call writing to be the best strategy, because he would consider the profit potential too small... Outright option purchases might suit him best." Explicit sizing caution from the author: **"one would hope that he uses only 15 to 20% of his assets for speculative option buying."**
- **Investor "in between"**: spreads may appeal, "especially the low-debit bullish or bearish calendar spreads," with occasional forays into other strategy types; the T-bill/option strategy "might work well for this investor also."
- **Wealthy aggressive investor**: may be attracted to credit strategies like straddle/combination writing or ratio writing — "generally... strategies for the wealthier investor because he needs the 'staying power' to be able to ride out adverse cycles."

His suitability test, stated directly as a question to ask yourself in advance:
> "A good test of suitability is for the investor to ask himself in advance: **'How will I react if the worst case occurs?'** If there will be sleepless nights, pointing of fingers, threats, and so forth, the strategy is unsuitable. If, on the other hand, the investor believes that he would be disappointed... but that he can withstand the risk, the strategy may indeed be suitable."

### Mathematical ranking of strategies by expected return (his own ranking, in order)
This is the closest thing in the chapter to a ranked list, and it's explicitly *not* the same as a suitability ranking:

1. **Highest mathematical expectation**: "strategies that take in large amounts of time value premium... ratio writing, ratio spreading, straddle writing, and naked call writing (but only if the 'rolling for credits' follow-up strategy is adhered to)." Ratio strategies need to be run "according to a delta-neutral ratio" to be mathematically optimum. His caveat: **"these strategies are not for everyone. All involve naked options, and also require that the investor have a substantial amount of money (or collateral) available... naked option writing in any form is not suitable for some investors, regardless of their protests to the contrary."**
2. **Next tier**: limited-risk strategies with occasional large-profit potential — the **T-bill/option strategy** is his named prime example, plus calendar-spread-family strategies that fund longer options by selling near-term ones (calendar combination, calendar straddle, diagonal butterfly spread from Ch. 23; bullish call calendar / bearish put calendar spreads) — with the explicit sizing caution again: **"one should limit his dollar commitment to 15 to 20% of his portfolio."**
3. **Behind those**: strategies offering "limited profits with a reasonable probability of attaining that profit" — **covered call writing, large-debit bull or bear spreads, neutral calendar spreads, and butterfly spreads.** He flags that all of these tend to have "relatively large commission costs" relative to position size.
4. **Lowest mathematical ranking**: "speculative buying and spreading strategies rank the lowest on a mathematical basis." Within pure option buying, in-the-money purchases (including in-the-money combinations) "generally outrank out-of-the-money purchases," because ITM starts with a better chance of retaining some value even if wrong, whereas constant purchase of pure time-value premium "will have a burdensome negative effect" as it wastes away toward expiration.

### His final synthesis (verbatim, the last words of the book's strategy discussion)
> "Mathematical expectations for a strategy do not make it suitable even if the expected returns are good, for the improbable may occur. **Profit potentials also do not determine suitability; risk levels do.** In the final analysis, one must determine the suitability of a strategy by determining if he will be able to withstand the inherent risks if the worst scenario should occur. **For this reason, no one strategy can be designated as the best one, because there are numerous attitudes regarding the degree of risk that is acceptable.**"

---
