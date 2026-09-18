# McMillan — Index Options, Futures, and Structured Products
### Extracted from *Options as a Strategic Investment* (5th ed.), Chapters 29–35

**Account context used throughout:** a retail equity account with roughly $100–500 in spendable capital, standard (non-portfolio-margin) equity options approval, and **no futures account**. Every section below ends with an honest read on whether the material is usable at that size — most of it is not, and this file says so directly rather than forcing relevance.

---

## Chapter 29–30: Introduction to Index Option Products and Futures / Stock Index Hedging Strategies

*Source: ch_032.txt, plus the closing pages of Chapter 30 carried into ch_033.txt (lines 1–92)*

### 1. Cash-based index option buying and selling (mechanics, not a directional strategy per se)

**Construction / how it works:** Cash-based options (SPX, OEX/S&P 100, NDX, DJX, NYSE Index, subindex options) have no physical underlying. Exercise/assignment settles for cash only: "the owner receives cash equal to the difference between the index's closing price and the strike price of the option. The option writer who is assigned must pay out an equal amount." Example given: a ZYX Sep 160 call exercised with the index at 175.24 pays $100 × (175.24 − 160.00) = $1,524, using a $100-per-point multiplier (same as stock options).

**Market outlook required:** Same as any long call/put — bullish for calls, bearish for puts — but McMillan frames the appeal as being able to "trade the market" without picking individual stocks: "If one is right on the market, his index option strategies will be profitable. This is superior to stock-oriented buying whereby one might be right on the market, but not make any money because calls were bought on stocks that didn't follow the market."

**Real rules given:**
- European vs. American exercise: "European exercise means that an option may be exercised only on its expiration day." SPX and DJX cash options are European; OEX remains American.
- "In-the-money European put options will be cheaper than their American counterparts... deeply in-the-money European puts will trade at a discount; the higher short-term interest rates are, the deeper the discount will be." This can leave a long-term protective European put worth less than expected at the exact moment (a crash) it's needed most.
- Cash-based exercise notices are accepted "only until 5 minutes after the options close trading on that exchange on any given trading day."
- Commission on exercise is charged "as if he had sold his long calls at" the in-the-money differential, not more.

**McMillan's own caveats:**
- Volatility skewing can make index puts overpriced relative to a package of equivalent equity puts, especially after a crash: "it may actually be more profitable for a trader who is bearish on the market to buy a package of equity puts instead of buying index puts." He notes this is discussed further in the advanced-concepts chapter, not fully detailed here.
- On selling naked index options being "safer" than naked stock options because indices rarely gap on single-company news: "one cannot assume that an index can never gap open widely... The worst case of such a gap... was the stock market crash in 1987... Therefore, one cannot assume that naked option writing of index options is a low-risk strategy."

**Capital/account reality check:** SPX/OEX/NDX/DJX are broad-based, large-multiplier, cash-settled index options — the very "expensive" contracts McMillan himself later contrasts with ETF options (see Chapter 32 notes below, SMH vs. SOX example). A single at-the-money SPX call at even a modest few points of premium runs into the thousands of dollars ($100/point multiplier). **Not usable directly at $100–500.** The one piece of transferable insight is conceptual: prefer a broad, liquid, low-priced underlying (an ETF) over the "expensive index" when your goal is diversified market exposure with a small option premium outlay — see the ETF section below.

### 2. Naked option writing on broad-based index options

**Construction:** Sell an uncovered index call or put (or straddle) against the index itself, collecting premium.

**Market outlook:** Neutral-to-directional income strategy; profits if the index stays away from the strike.

**Real numeric rules (verbatim close):**
"The requirement for writing a broad-based index option naked is 15% of the index, plus the option premium, minus the amount, if any, that the option is out-of-the-money." Worked example: ZYX at 168.00, Dec 170 call at 6 → naked call requirement = 15% of index ($2,520) + call premium ($600) − OTM amount ($200) = $2,920. Both call and put naked requirements in the book's example are "above the minimum of 10% of the index." Narrow-based (sector) index options use the same margin math as stock options: 20% of the index plus premium less OTM amount, with a 15% minimum.

**Risk/reward:** Same unlimited-loss profile as any naked write; McMillan's stated advantage is lower gap risk than single stocks (see caveat above about the 1987 crash exception).

**Capital/account reality check:** Naked writing on a broad-based index requires margin collateral in the multiple thousands of dollars per contract (15–20% of an index value that is itself hundreds or thousands of points, times a $100 multiplier). **Completely out of reach for a $100–500 account**, and in any case naked index option writing typically requires the highest options-approval tier, which a small standard account will not have.

### 3. Cash-based bearish call spread — early assignment risk example

**Construction:** Buy ZYX Nov 160 call at 1, sell ZYX Nov 155 call at 3 (net credit $200), a nominally "limited-risk" bear call spread.

**Real numeric rules (verbatim close):** If the short 155 call is assigned early with the index at 175.24, the writer is charged a debit of $100 × (175.24 − 155.00) = $2,024 to cover the assignment overnight. If the market gaps down the next day to 172 and he sells his long 160 calls at parity ($1,200), his net debit is $824 — "larger than his initial, theoretically 'limited' maximum debit of $500," a $624 loss versus the nominal $300 max.

**McMillan's own caveat:** "a spread in cash-based options acquires more risk than the difference in the strikes (the maximum risk in stock options) if the short option in the spread becomes a deeply in-the-money option, ripe for assignment." This is specific to American-exercise cash index options (mainly OEX-style products); most modern SPX-style products are European and don't have this problem, but narrow-based/legacy American cash options do.

**Capital/account reality check:** Even setting aside the early-assignment risk, this is again SPX/OEX-scale premium and multiplier — not sized for $100–500.

### 4. Selling index futures against a stock portfolio (institutional-scale hedge)

**Construction:** A fund holding stocks sells S&P 500 futures to remove market exposure without liquidating the underlying shares.

**Real numeric rules:** "The 'big' S&P 500 futures contract is worth $250 per point of movement," while the e-mini is $50/point. Example margin: initial margin ~$30,000 controls $351,250 worth of index exposure at 1405 × $250 — "leveraged almost 12-to-1."

**McMillan's own caveat:** Futures are marked to market daily; a loss must be covered in cash or by liquidating T-bill collateral, and "the trader must add more cash to his account to cover the loss" if margin is insufficient.

**Capital/account reality check:** Requires a futures trading account (explicitly not available here) and margin in the tens of thousands of dollars per contract. **Entirely inapplicable.**

### 5. Hedging a stock portfolio with index puts or calls

**Construction — Method 1, "disaster insurance":** Buy enough out-of-the-money index puts, sized by the striking price value, to cover the portfolio's "adjusted capitalization" (dollar value of each holding scaled by that stock's volatility relative to the index — Beta-approximation formula given: "Beta approximation = [stock volatility] / [market volatility]").

**Real numeric rules (verbatim close), 4-step formula for number of futures/options to buy/sell to hedge a diverse portfolio:**
1. "If you don't know the Beta, divide each stock's volatility by the market's (S&P 500) volatility. This is the stock's adjusted volatility."
2. "Multiply the quantity of each stock owned by its price and then multiply by the adjusted volatility from step 1. This gives the adjusted capitalization of the stock in the portfolio."
3. "Add the results from step 2 together for each stock to get the total adjusted capitalization of the portfolio."
4. "Divide the sum from step 3 by the index price of the futures to be used and the unit of trading for the futures ($250 per point for the S&P 500 futures) to determine how many futures to sell."

Worked numeric example: a 3-stock portfolio (GOGO, UTIL, OIL) yields total adjusted capitalization of $720,000; hedged with UVX puts ($100/point, index at 178.00) using the "disaster insurance" method 1: "Puts to buy = $720,000/$17,000 = 42.3" (17,000 = value of the 170 strike). Method 2 ("hedge against current market movements," using at-the-money puts and dividing further by the absolute delta): "Puts to buy = $720,00/(100 X 180)/0.60 = 67," costing $30,150.

**Market outlook:** Bearish-to-neutral; buying puts (vs. selling futures or calls) explicitly preserves upside: "he still has profit potential if the market rallies," unlike a futures hedge which "locks in his profit, but does not leave any room for further profits."

**Risk/reward:** Put-hedge cost is the premium paid; if the market stabilizes, "the time value decay will cause a loss on the puts." Ratio-writing calls instead (hedging with index calls) is "the opposite... more equivalent to being short a straddle" and McMillan states plainly: "hedging the portfolio with short index calls does not present as attractive a position as hedging with long index puts," citing early-assignment risk, unlimited upside call risk, and the extra work of dynamic adjustment.

**McMillan's own caveat:** Both put and call hedges require re-adjustment as option deltas change — behaving "akin to being long a straddle" (for puts) or "short a straddle" (for calls), and the manager must roll strikes as the market moves.

**Capital/account reality check:** The worked examples involve portfolios worth $465,000–$720,000 and put purchases costing $4,200–$30,150. **Structurally an institutional/large-individual-portfolio technique.** A $100–500 account has no diversified stock portfolio of this scale to hedge in the first place, so the strategy doesn't map onto this account size at all — not even in miniature, since you'd need actual stock holdings to hedge.

### 6. Put-call ratio (contrarian sentiment indicator, not itself a tradeable position)

**Real numeric rules:** "The put-call ratio is simply the number of puts traded divided by the number of calls traded." Weighted version: dollars spent on puts ÷ dollars spent on calls. "An average day will generally produce a [equity] ratio of around 0.50," while index options "produce much larger ratios... An average day might produce readings of 2.00 for some indices." High ratio → contrarian bullish signal; low ratio → contrarian bearish signal, but McMillan cautions: "it is better to look for the ratios to make a high or a low before calling a buy or sell signal" rather than using fixed absolute thresholds, and to discount the signal entirely if the ratio is rising while the market is also rising (a sign of hedging demand, not sentiment).

**Capital/account reality check:** This is a free, data-only indicator — no capital required to observe it. It is the **one genuinely accessible idea in this section** for a small account: it costs nothing to track and could inform timing of small option trades the account can actually afford, though McMillan gives it as a standalone technical tool, not a strategy with its own construction/margin.

---

## Chapter 31: Index Spreading

*Source: ch_033.txt, lines ~1093–1394*

### 7. Inter-index futures spread, one-to-one or ratio-weighted

**Construction:** Buy futures on one index, sell futures on a related index, betting on the *relationship* between them rather than market direction. "If he buys the index that is comprised of smaller stocks and sells the S&P 500 Index, he will make money if his analysis is right, regardless of whether the stock market goes up or down."

**Real numeric rules (verbatim close):** One-to-one example: buying ZYX futures and selling ABX futures, both $500/point, spread widening from 45.00 to 50.00 points nets exactly $2,500 "no matter which way the market goes" (up, flat, or down — table given). But a naive one-to-one spread on mismatched price levels "is not much of a hedge" — his UVX (100) vs. ZYX (200) example shows a 1-for-1 spread producing large losses purely from ZYX's larger point value, not the intended relationship trade.

Ratio formula (verbatim):
"Ratio = (V₁/V₂) × (P₂/P₁) × (U₂/U₁)" where V = volatility of each index, P = price of each index, U = unit of trading (dollar value per point). Worked example: ZYX (15% vol, 175.00, $250/pt) vs. ABX (25% vol, 225.00, $500/pt) → Ratio = 4.286, "one would probably trade four ZYX futures against one ABX future."

**McMillan's own caveat:** "The margin requirements for these spreads are often reduced because margin rules recognize that futures on one index can be hedged by futures on another index" — but this reduction applies to *futures* margin, which this account doesn't have access to.

**Capital/account reality check:** Requires a futures account trading multiple contracts simultaneously. **Not usable.**

### 8. Using in-the-money options as a futures-spread substitute (long put + long call across two indices)

**Construction:** Instead of buying one index's futures and selling another's, buy a deep in-the-money put on the expensive-looking index and a deep in-the-money call on the cheap-looking one — a "long combination" across two underlyings.

**Real numeric rules / worked example:** ZYX at 175.00, UVX at 150.00 (25-point spread). Buy ZYX Dec 185 put (10½) and buy UVX Dec 140 call (11) — combined cost 2¼ points of time premium over intrinsic. If both indices then rally hard (ZYX to 200, UVX to 170 — spread actually *widens* to 30, the "wrong" direction for the original spread thesis) the position still profits because the long call keeps gaining while the worthless put's loss is capped: "the option position still made money" even though the cash spread moved unfavorably. This mirrors "owning a long [straddle-like combination]" — profit potential from big moves in *either* direction, not just the spread narrowing as originally intended.

**Second variant — option ratio with delta**, formula (verbatim close):
"Option Ratio = (V₁/V₂) × (P₂/P₁) × (U₂/U₁) × (d₂/d₁)" where dᵢ is the option's delta. Worked example: ZYX 175 put (delta −0.45, $500/pt) vs. UVX 150 call (delta 0.52, $100/pt) → ratio ≈ 6.731, "buy nearly 7 UVX calls for every ZYX put purchased."

**McMillan's own caveat:** "Volatility Differential" and "Striking Price Differential" sub-strategies require that the options on the two indices already be individually fair-valued, with the edge coming purely from a volatility or strike-equivalence mismatch between the two indices — a fairly advanced, data-intensive setup ("Normally, one would want the differential in implied volatilities to be at least 2% apart before establishing the spread").

**Capital/account reality check:** Still built on SPX/OEX/DJX-scale option premiums per the book's own dollar figures (index options at $100–500/point multipliers). **Not usable at $100–500**, though the underlying *concept* — using an ITM call as a cheaper futures proxy — is one of the few ideas here that, if translated to small, low-priced ETF options, could in principle scale down (McMillan doesn't do that scaling in this chapter, though; he does it explicitly with SMH vs. SOX in Chapter 32, discussed below).

---

## Chapter 32–33: Structured Products / Mathematical Considerations for Index Products

*Source: tail of ch_033.txt (Chapter 32 opening) + ch_034.txt + opening of ch_035.txt (lines 1–58, end of Chapter 33)*

### 9. "Riskless" principal-protected structured notes (embedded call + zero-coupon bond)

**Construction:** An issuer (bank/brokerage) combines zero-coupon government bonds with index call options and sells the package as a listed note. "Would you like to own an index fund that had no risk?... This is akin to owning the stock or the index and having protected it by buying a put option." Mechanically: "the bank could take $600,000 and buy [zero-coupon] bonds... The other $400,000 is spent to buy call options on the S&P 500 index." Cash value formula (verbatim, general form): "Cash Surrender Value = Guarantee + Guarantee × Participation Rate × (Final Index Value/Striking Price − 1)."

**Market outlook:** Buy-and-hold bullish with full principal protection — investor wants upside participation but cannot tolerate downside.

**Real numeric rules:** Cost of the embedded option = lost interest vs. a bank account, computed via continuous compounding: "Money in the bank = Guarantee Price × e^(rt)." Worked SIS example (real product, S&P Midcap 400-linked, 1993–2000): 115% participation, imbedded call cost calculated at "40.87% of the guarantee price," implying volatility "just over 26%" versus listed options trading near 14% at the time — i.e., the embedded option is priced expensively; "this was an expensive call in terms of its initial cost." SIS itself tripled (issued ~$10, matured >$30) because the underlying index rallied hard over the period — an actual favorable outcome, not just theory.

**McMillan's own caveats:**
1. **Credit risk:** "the risk of the structured product is that the underwriter might not be able to pay the... obligation at maturity... structured products are really forms of debt (senior debt) of the brokerage firm that underwrote them."
2. **Phantom interest / tax drag:** "the IRS...requires you to pay taxes annually on a proportionate amount of that OID [Original Issue Discount]... structured products should be bought in a tax-free retirement account."
3. **Adjustment factor** (in later-issued products): a compounding annual haircut applied to the *index value itself* before computing payout. Worked example: an 8.75% total adjustment factor over 7 years means "if the index doubles, then the structured product 'should' be worth double the initial price, or 20. But instead, it's worth 91.25% of 20, or 18.25" — and the underlying "must increase in value by more than 9.5%" just to break even. McMillan calls this "an onerous burden for the investor" and shows the effect compounds worse as gains grow (only 82.5% captured on a double, ~74% captured on a triple).
4. **Discount to theoretical value in the secondary market:** products "generally trade at a slight discount to their theoretical cash surrender value," similar to closed-end funds.
5. **Bull-spread ("callable") variants** cap upside via an implicit written call and "will not trade near its maximum price... until time shrinks to nearly the maturity date."

**Capital/account reality check:** This is the most *literally* feasible construct in these five chapters for a small account — the notes traded at prices like $8.75–$16.50 per "share," i.e., order of $10–30 for a small lot, which a $100–500 account could technically afford a handful of. **However:** (a) these specific listed structured notes (SIS, JEM, MITTS, TARGETS, etc.) were largely 1990s/2000s-era AMEX/NYSE listings that have since matured or been discontinued — McMillan is describing a product landscape that is far thinner today; (b) the tax treatment (phantom interest) makes them impractical outside an IRA, which is a separate account type from what's specified; (c) credit risk is concentrated in whichever bank underwrote the note. This is a "know it exists, don't build a strategy around it at this size" item — flag it, don't recommend it.

### 10. Writing listed options against a held structured product / rolling the embedded strike

**Construction:** If you already hold a structured product (a synthetic long call), sell a listed call against it to create a synthetic bull spread ("collar"), or roll the embedded call up by selling a listed call at the old low strike and buying one at a higher strike.

**Real numeric rules:** Multiplier to convert structured-product shares into "SPX-equivalent shares" = Striking price ÷ Base price (worked example: 700/10 = 70-to-1). Rolling example: buying 2-year SPX LEAPS at 1,200 and selling ones at 700 "would bring in 340 points, two times; or $68,000."

**Capital/account reality check:** Requires already owning thousands of shares of a structured product (15,000 in the example) plus margin capacity to sell naked/covered SPX LEAPS calls. **Not remotely usable at $100–500** — this is written for an investor with a six-figure position already in place.

### 11. Exchange-Traded Funds (SPY, QQQ, DIA, sector SPDRs, iShares, HOLDRS) as cheaper substitutes for expensive index options

**Construction:** ETFs are unit trusts holding a basket of stocks tracking an index (SPY = S&P 500 ÷ 10; QQQ = NASDAQ-100 ÷ 40; DIA = Dow 30). "Exchange-traded funds are attractive to all investors who like to trade or invest in index funds... Options on ETFs can be used as substitutes for many expensive indices. This brings index option trading more into the realm of reasonable cost for the small individual investor."

**Real numeric rules (verbatim close, the direct comparison McMillan gives):** SOX (PHLX Semiconductor index) traded 500–1,300 with ~70% implied/historical volatility; "a three-month at-the-money call... would cost approximately 135 points. That's $13,500 for one call option. For many investors, that's out of the realm of feasibility." By contrast, Semiconductor HOLDRS (SMH), holding the same 20 underlying stocks and carrying the same ~70% implied volatility, traded near $100/share, and "a three-month at-the-money call on the $100 SMH... would cost only 13.50 points ($1,350) — a much more feasible option cost for most investors and traders." He generalizes this to the QQQ/MSH pair as well.

**McMillan's own caveat:** None stated against ETFs specifically beyond what's implicit — he presents this as a genuinely useful substitution, not a strategy with hidden risk, though he notes liquidity varies a lot by product ("sector SPDRs... have proven to be less popular," "OEX... now barely trades one-thirtieth" of its former volume).

**Capital/account reality check:** This is **the single most directly relevant idea in all five chapters for a $100–500 account.** Even $1,350 for one SMH-era call is still too large for this account size, but the *principle* scales further: today's small, liquid, standard-equity-approval-eligible index ETF options (SPY, QQQ, IWM, DIA, and their many cheaper single-digit-to-double-digit-priced sector/thematic cousins) are exactly the kind of "expensive index made cheap" substitute McMillan is describing — just taken one step further than his own SMH example, into ETFs priced low enough that a single contract's premium fits inside a few hundred dollars. This is a legitimate, text-supported bridge from "index options are unaffordable" to "ETF options might not be," even though McMillan's own dollar example (SMH at $1,350/contract) is itself still above this account's stated $100–500 ceiling.

### 12. Mathematical/arbitrage techniques (discounting, conversions/reversals, box spreads on index products)

**Construction & rules:**
- **Discounting** (buying deep ITM American-style options at a discount to intrinsic value near the close, to capture the discount by exercising same day): "OEX is trading at 673.53 and an arbitrageur can buy the June 690 puts for 16. That is a discount of 0.47." McMillan notes one OEX point ≈ 30 Dow points, so "this is not a lot of cushion" and the strategy is only viable "if there are just a few minutes of trading left."
- **Conversions/reversals with futures options:** "most futures conversions and reversals trade very nearly at a net price equal to the strike," with a small carrying-cost adjustment computed via simple interest over the days to expiration.
- **Box spreads on cash-based options:** "It is often the case with cash-based options that the box sells for more than the difference in the strikes... because of the possibility of early assignment." McMillan's verdict: "box strategies are not particularly attractive... this is not normally a retail strategy" (four commissions involved).

**Capital/account reality check:** All three are **explicitly floor-trader/arbitrageur strategies** requiring speed, real-time bid/offer visibility, and — per McMillan's own words — are "not normally a retail strategy." **Not usable regardless of account size**, let alone at $100–500.

### 13. Modeling adjustments for index and futures options (background math, not a strategy)

**Real formulas given:**
- Cash-based index option present-value-of-dividend adjustment to Black-Scholes: subtract the present worth of the index's aggregate dividend stream from the index price before running the model.
- **Implied dividend** back-solving method (iterative: assume $0 dividend, solve implied vol from the call, check if the resulting theoretical put matches the market put price, adjust dividend assumption by $0.10 increments and repeat) — useful for a retail trader without a dividend data feed.
- **Black model for futures options:** "Call value = e^(−rt) × [Black-Scholes call value using r = 0%]," and the call/put parity relation "Call = Put + e^(−rt)(f − s)."

**Capital/account reality check:** Pure valuation math, not a position/strategy — no capital requirement to understand it, but no direct trading action attaches to it either. Background knowledge only.

---

## Chapter 34: Futures and Futures Options

*Source: ch_035.txt (this file's coverage of Chapter 34 is partial — it runs from the chapter opening through the middle of the SPAN margin discussion and cuts off mid-example at line 773; the file supplied ends there, so any strategy content appearing later in Chapter 34 is not covered here and should not be assumed.*

### 14. Currency/commodity hedging with futures (background — not an index-option strategy)

**Construction:** A business with future foreign-currency receivables sells currency futures to lock in today's exchange rate. Example: a U.S. exporter due Swiss francs in 6 months sells Swiss franc futures to lock in the dollar value of the contract regardless of which way the franc moves.

**McMillan's framing:** "Think of futures as stock with an expiration date... futures contracts can rise dramatically in price and can fall all the way to nearly zero (theoretically)... there is great potential for risk," unlike bounded-risk long options.

**Capital/account reality check:** Requires a futures account. **Not applicable.**

### 15. Futures speculation (leverage mechanics, not a strategy per se)

**Real numeric rules:** Cotton future: 50,000 lbs/contract, $30,000 notional at 60¢/lb, exchange minimum margin $1,500 → "one can trade cotton on 5% margin." A 1¢ move = $500; "a 3-cent move to the upside would generate a profit of $1,500, a 100% profit" — and equally, a 3¢ adverse move wipes out the entire margin deposit.

**McMillan's own caveat:** Daily mark-to-market ("maintenance margin") can force cash calls at any time; "he must add $400 to his account, or sell out $400 worth of T-bills" in his worked example.

**Capital/account reality check:** **Explicitly excluded by the account's constraints** (no futures account) — and the leverage/margin-call mechanics described are precisely the kind of open-ended cash-call risk that would be dangerous to a $100–500 account even if access existed.

### 16. SPAN margin mechanics and the covered-write example

**Construction/rules:** SPAN (Standard Portfolio ANalysis of Risk) computes a "risk array" of 16 potential gain/loss scenarios per contract (7 futures price levels × 2 volatility states, plus 2 "extreme move" scenarios) and sets margin equal to the single worst-case loss in the array. Worked example: long S&P future, worst case "futures down three-thirds" = −$10,000, so that becomes the futures margin. For a long Dec 1400 call, worst case (futures down, volatility down) = −$3,990, so that becomes the option's SPAN margin. Combining a long future + short call (a covered write) nets the two arrays together scenario-by-scenario, generally producing a smaller combined requirement than either leg alone.

**McMillan's own caveat:** "Not all futures clearing firms automatically put their customers on SPAN margin. Some use the older customer margin system... As a strategist, it would be beneficial to be under SPAN margin."

**Capital/account reality check:** SPAN is a futures-account margin methodology. **Not applicable without a futures account**, and the dollar figures in the example ($10,000–$14,000+ margin per contract) are wildly beyond a $100–500 account regardless.

---

## Chapter 35: Futures Option Strategies for Futures Spreads

*Source: ch_037.txt, complete*

### 17. Intramarket futures spread (calendar-style, same commodity, two expirations)

**Construction:** Buy one expiration month's futures, sell another month's futures on the *same* commodity, betting on the price differential rather than absolute direction. Worked example: buy July soybeans at 600, sell September at 606 (6¢ differential); later the spread inverts (July 650, September 630) for a 26¢/$1,300 profit "whether soybeans are in a severe bear market, in a rousing bull market, or even somewhat unchanged" — a full table is given showing the same $1,300 profit across seven wildly different absolute price levels, as long as the *differential* moves the same way.

**Real numeric rule:** Spread margin is reduced vs. outright: "the speculative initial margin requirement is $1,700. Then, the spread margin requirement might be $500" — roughly a 3.4x reduction, "considerably less than one would have to put up... if each side of the spread had to be margined separately."

**McMillan's own caveat:** "it cannot be considered conservative; it's just less risky than outright futures speculation" — a $500 margin position with $5,000 worth of potential swing "is certainly high leverage."

**Capital/account reality check:** Futures-account-only. **Not applicable.**

### 18. Intermarket futures spread (cross-currency, TED spread, crack spread)

**Construction & real numeric rules:**
- **Cross-currency spread** (e.g., long yen futures, short Euro futures): worked example shows a 17.00-point initial differential with profit/loss scaling at "$1,250" per point of differential change.
- **TED spread** (long T-bill futures, short Eurodollar futures, trading the credit-risk yield gap): "the margin for the TED spread, however, is only $400" versus $800 outright — a 4x reduction. McMillan notes it "has carrying cost... the spread will shrink as time passes" (~0.05 points per quarter at low rates).
- **Crack spread** (oil refining margin: long 2 crude oil futures, short 1 heating oil + 1 unleaded gasoline future), with formula (verbatim): "Crack = [(Unleaded gasoline + Heating oil) × 42 − 2 × Crude] / 2."

**Capital/account reality check:** All are futures-account-only strategies, several requiring multiple simultaneous contracts (the crack spread alone needs 4 contracts, 3 different commodities). **Not applicable.**

### 19. Futures option calendar spread (structurally different from a stock/index calendar spread)

**Construction:** Buy a longer-dated futures option, sell a shorter-dated futures option at the same strike — but McMillan stresses this is fundamentally unlike an equity calendar spread because "a calendar spread using futures options involves two separate underlying instruments" (e.g., the May soybean futures contract vs. the March soybean futures contract), not one stock. "If one buys the May soybean 600 call and sells the March soybean 600 call, he is buying a call on the May soybean futures contract and selling a call on the March soybean futures contract."

**Real numeric rules / worked example:** May/March 600 call calendar established for a 7-point debit; McMillan builds a full sensitivity table (Table 35-4) crossing March futures price level against the March/May futures spread level, showing the position can *lose more than its initial debit* if March futures rally and the futures spread simultaneously narrows — "This would never happen with stock options." His conclusion: "one must approach the problem" two-dimensionally (plot profit against both the near-term future's price *and* the futures spread), and check whether the calendar spread actually outperforms a plain intramarket futures spread before using it (in his example it usually does, given the specific mispricing assumed).

**McMillan's own caveat:** "calendar spreading with futures options is a less popular strategy than its stock option counterpart" because of this added dimension of risk.

**Capital/account reality check:** Futures-account-only. **Not applicable.**

### 20. Long combinations (in-the-money options substituting for both legs of a futures spread) — the chapter's central, most fully worked strategy

**Construction:** Instead of buying futures for one leg and selling futures for the other leg of an intramarket/intermarket spread, buy an in-the-money call on the "long" side and buy an in-the-money put on the "short" side — never *sell* naked options as substitutes.

**McMillan's explicit rule (verbatim close):** "Do not substitute at- or out-of-the-money options for the futures in intramarket or intermarket spreads" — because time decay on OTM/ATM legs erodes profits even if the spread thesis plays out (worked wheat example: futures spread converges fully for a 20-point gain, but the ATM-option version only captures 10 points because of decayed time premium). Selling options instead of using futures outright is even worse — it can *increase* risk asymmetrically (worked live-cattle example: futures spread narrows favorably by 2.00 points, but the short-put/short-call substitute loses 4.80 points net because the short put's loss on a big move swamps the short call's capped gain).

**The recommended construction, in his words:** "If one buys in-the-money calls instead of buying futures, and buys in-the-money puts instead of selling futures, he can often create a position that has an advantage over the intramarket or intermarket futures spread... There is no increase of risk, since the options are being bought, not sold... the amount of money spent on time value premium is small, since both options are in-the-money."

**Real numeric worked example (TED spread via options):** June T-bill 9450 call at 0.32 (0.25 ITM, so 0.07 time premium) + June Eurodollar 9450 put at 0.40 (0.35 ITM, 0.05 time premium) = $1,800 total cost for one of each, versus $400 futures-spread margin. When rates fell and both futures rallied, "the TED spread has shrunk from 0.60 to only 0.40" — a futures-only spreader would have *lost* $500 — but the combined option position gained $725, because the deep ITM call kept appreciating while the now-worthless put's loss was capped. McMillan's honest caveat: "if the futures prices had remained relatively unchanged, the 0.12 points of time value premium ($300) could have been lost."

**Follow-up mechanics:** Track the position's equivalent futures position (EFP) using each option's delta (worked table: long 5 calls at delta 0.99 = +4.95 EFP; long 5 puts at delta −0.40 = −2.00 EFP), and rebalance toward neutral if the position drifts from a spread into an effectively outright directional bet as one leg goes deep ITM and the other goes OTM.

**Risk/reward summary in McMillan's words:** Bounded risk (both legs are long options, premium paid in full up front), asymmetric upside if the underlying futures are volatile enough in either direction to outrun the combined time-premium cost, but a real chance of losing the full time-premium outlay if the futures stay range-bound.

**Capital/account reality check:** This is conceptually the most "portable" idea in Chapter 35 — bounded-risk long options instead of margined futures — but it is still explicitly built on *futures options* (T-bill futures options, live cattle futures options, heating oil/RBOB futures options), which require a futures account this profile doesn't have. **Not directly usable**, though the underlying logic (prefer bounded-risk long ITM options over margined short/naked positions when substituting for a two-legged spread) is a transferable risk-management principle, not a specific trade this account can place.

---

## Overall summary of Part V's applicability to a $100–500 standard equity-options account

Chapters 29 through 35 cover index options, index futures, structured notes, and futures/futures-option spreading — nearly all of it explicitly institutional or floor-trader material by McMillan's own description ("not normally a retail strategy," "for many investors, that's out of the realm of feasibility," multi-thousand-dollar margin requirements, six-figure hedge examples). Cash-settled broad index options (SPX/OEX/NDX/DJX) carry $100+ multipliers that price single contracts in the thousands of dollars; naked index writing needs 15–20% margin on index-sized notional; portfolio and market-basket hedges assume the investor already owns a diversified stock portfolio worth hundreds of thousands of dollars; and every futures and futures-option strategy (index futures, TED spread, crack spread, futures calendar spreads, SPAN margin) is categorically closed off by the account's lack of a futures account. Structured notes are the one product priced low enough per "share" ($10–30) to theoretically fit a small account, but they carry issuer credit risk, awkward tax treatment (phantom interest), and are a largely faded product category today. The single genuinely actionable, text-supported idea for this account is McMillan's own point in Chapter 32 that liquid ETF options (SPY, QQQ, DIA and similar) substitute for "expensive" index options at a small fraction of the cost — his own example still lands at $1,350/contract, above this account's ceiling, but the same logic extended to today's lower-priced, more liquid ETF options is the one bridge from this material to a $100–500 account. The honest conclusion: most of Part V is not usable at this account's current size or account type, and it functions here mainly as background literacy for reading index/futures markets rather than as a source of trades this account can actually place.
