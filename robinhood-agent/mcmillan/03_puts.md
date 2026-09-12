# McMillan — "Options as a Strategic Investment" (5th ed.)
## Notes: Put Strategies (Chapters 15–21)
Source files: ch_019.txt (Ch.15–17), ch_020.txt (Ch.18–19), ch_021.txt (Ch.20), ch_022.txt (Ch.21)

All quotes are taken directly from the OCR'd chapter text. Minor OCR artifacts in the source (missing/doubled spaces, stray characters like "})ulv" for "July") are left as-is inside quoted passages only where necessary for exactness; paraphrased summaries clean this up.

---

## Chapter 15 — Put Option Basics

### Put mechanics / definitions (background, not a "strategy" per se)
**Construction:** A put option gives the holder "the right to sell the underlying security at the striking price at any time until the expiration date." Not a position per se, but the foundational mechanics every put strategy below depends on.

**Market outlook:** N/A — this is definitional material.

**Real numeric rules/formulas he gives:**
- In-the-money put time value premium formula (verbatim):
  `Time value premium = Put option + Stock price − Striking price` (in-the-money put)
  Contrast with calls: `Time value premium = Call option + Striking price − Stock price` (in-the-money call)
- "A put is considered to be in-the-money when the underlying stock is below the striking price of the put option; it is out-of-the-money when the stock is above the striking price" — the reverse of calls.
- "A put option will generally sell for less than a call option when the underlying stock is exactly at the striking price, unless the stock pays a large dividend." Table 15-1 example: XYZ at 50, July 50 call = 5, July 50 put = 4.
- "An in-the-money put (stock is below strike) loses time value premium more quickly than an in-the-money call does." Example given: with XYZ at 43, a 7-point in-the-money put has lost all time premium, while a 7-point in-the-money call (XYZ at 57) still retains 2 points of time premium.
- Dividend effect: "On the day before a stock goes ex-dividend, the time value premium of an in-the-money put should be at least as large as the impending cash dividend payment." Example: XYZ at 40 about to pay a $.50 dividend — an XYZ January 50 put "should sell for at least 10.50."
- Put writer assignment-anticipation rule: if "the time value premium of an in-the-money put is less [than the dividend]," early assignment is likely — and this tends to happen "on the day after the ex-dividend date," not on it (unlike calls).
- Delta: "The delta of a put ranges between 0 and minus 1." Approximation given: call delta minus put delta ≈ 1 (i.e., put delta ≈ call delta − 1), though McMillan cautions "this formula" is not exact when the put is deeply in-the-money.
- Position limits: "The actual limits are 13,500, 22,500, 31,500, 60,000, or 75,000 contracts," and one cannot exceed the limit on one side of the market (bullish = long calls + short puts; bearish = short calls + long puts) — but could be at the limit on *both* sides simultaneously (e.g., long 75,000 calls AND long 75,000 puts is not a violation).
- Conversion arbitrage (no-risk, defines the put/call price relationship): buy 100 shares, buy 1 put, sell 1 call at the same strike — riskless. The opposite (short stock, sell put, buy call) is a "reversal." These arbitrage mechanics are why puts and calls stay priced in a fixed relationship to each other.

**Risk/reward profile:** N/A (background).

**Caveats/pitfalls:** None strategy-specific; this is foundational material on pricing/mechanics.

**Capital/margin:** N/A.

---

## Chapter 16 — Put Option Buying

### Put Buying (outright speculative long put)
**Construction:** Buy 1 put option, no stock position. "The purchase of a put option provides leverage in the case of a downward move by the underlying stock" — an alternative to shorting stock.

**Market outlook required:** Bearish — expects the underlying to decline "substantially" (for OTM puts) or even moderately (for ITM puts) within the option's life.

**Real numeric rules/formulas:**
- "One should not place more than 15% of his risk capital in the strategy" when put buying is approached as a speculative strategy — stated explicitly by McMillan.
- Comparison example (XYZ at 50, July 50 put at 5): if the stock falls to 20, the put buyer profits $2,500 (+500%) vs. a short-seller's $3,000 (+120%) — the put buyer achieves far higher percentage returns on far less capital at risk, at the cost of capped downside participation.
- ITM vs. OTM put selection: "In a substantial downward move, the out-of-the-money put purchase provides higher reward potential [percentagewise]." But example: XYZ at 49, July 45 put at 1, July 50 put at 3 — if XYZ falls only to 45, the July 45 (OTM) put expires worthless (100% loss) while the July 50 (ITM) put still shows a 2-point profit. McMillan's conclusion: "when purchasing put options for speculation, it is generally best to concentrate on in-the-money puts unless a very substantial decline in the price of the underlying stock is anticipated."
- Ranking method for prospective put purchases (mirrors his call-ranking method from Ch. 3): (1) estimate stock decrease over a fixed holding period (30/60/90 days) based on volatility; (2) estimate resulting put prices; (3) rank by highest reward for aggressive lists; (4) also estimate the loss if the stock instead rose, to rank by best risk/reward for a conservative list.

**Risk/reward profile:** Max loss = 100% of premium paid (defined risk). Max gain = large but not literally unlimited — capped only by the stock going to zero (put buyer "has limited profit potential, since a stock can never drop in price below zero dollars per share"), but percentage gains "can be huge." Compared to short selling, the short seller has theoretically unlimited risk and must pay dividends; the put buyer's risk is capped at premium paid and the put buyer owes no dividends.

**McMillan's caveats/pitfalls:**
- Do not exceed 15% of risk capital in outright put speculation.
- Holding-to-expiration analysis is "generally an erroneous form of analysis, because the buyer generally tends to liquidate his option purchase in advance of expiration" — and near-the-money puts do NOT gain value as fast as one would hope on a modest stock decline, because time premium erodes as it goes ITM (example: XYZ falls 5 points to 44, but the July 45 put "has increased in value only to 2 or 2¼ points" — "somewhat disappointing").
- Exercising to liquidate is "rarely to the option buyer's benefit" — commissions make it a "prohibitive move"; sell the option instead.
- On follow-up: after a run-up in the put's value, McMillan lays out 5 tactics (liquidate / do nothing / "roll down" / spread / combine with a call) and notes the spread tactic "never turns out to be the worst tactic" though it's not always best; for puts (unlike calls) "the premium received for the out-of-the-money put is not as large, and therefore the spread strategy loses some of its attractiveness" versus the call-buyer's equivalent.
- On losses: the "rolling-up" strategy (sell 2 of the losing puts, buy 1 put at the next higher strike, for near-zero net debit) raises the breakeven but caps the max profit — "should be used only if the spread can [be done for a small or zero debit]," and it "would require a margin account, just as calls do."
- The calendar-spread loss-recovery tactic is explicitly called inferior: "This type of spread strategy is not as attractive as the 'rolling-up' strategy" because if the stock falls back to the strike before near-term expiration, "little or no profit will be made — in fact, a loss is quite possible."

**Capital/margin size:** This is the single most small-account-friendly strategy in these chapters. Buying one out-of-the-money put on a low-priced stock can cost well under $100–$500 per contract (e.g., puts trading at fractions of a point to a few points in his examples). **Usable at $100–500** provided the underlying/strike is chosen so the premium fits the budget — but note McMillan's own preference for in-the-money puts (which cost more) for straight speculation, which may not fit a very small account; a true micro-account would be forced into cheaper OTM puts, which McMillan flags as the more speculative, lower-probability choice.

---

## Chapter 17 — Put Buying in Conjunction with Common Stock Ownership

### Protective Put (Married Put / Synthetic Long Call)
**Construction:** Own 100 shares of stock + buy 1 put on that stock. McMillan: "This position is also called a synthetic long call, because the profit graph is the same shape as a long call's."

**Market outlook required:** Fundamentally bullish or at least long-term-holding on the stock, but wanting insurance against a near-term decline — "provides the stock owner with protection, eliminating the possibility of any devastating loss on the stock holding during the life of the put."

**Real numeric rules/formulas:**
- Example: stock at 52, buy October 50 put for 2 → "the most that the stockholder can lose on his stock is 2 points. Since he pays 2 points for the put protection, his maximum potential loss until October expiration is 4 points" (stock decline to the strike + premium paid).
- Strike selection guidance (deep OTM vs. deep ITM vs. slightly OTM):
  - Deep OTM put (example: stock 40, Oct 35 put at .50): "the purchase of this put... would not reduce upside potential much at all, only by .50," but max loss is 5.50 (5 pts down to strike + .50 premium) — "disaster insurance," minimal protection until stock reaches the strike.
  - Deep ITM put (example: stock 40, Oct 45 put at 5.50): max risk is only .50 (5-pt stock gain via exercise offsets a 5.50 cost), but "he would have difficulty making any profit during the life of the put" since stock must rise more than 5.50 to profit at all. McMillan: "The deep in-the-money put purchase is overly conservative and is usually not a good strategy."
  - His explicit recommendation: "Generally, one should purchase a slightly out-of-the-money put as protection. This helps to achieve a balance between the positive feature of protection... and the negative feature of limiting profits."
- Equivalence: protective put + stock has the exact same profit-graph shape as an outright long call purchase — "the call purchase and the long put/long stock strategies are equivalent" (similar P&L, not identical cost/mechanics).

**Risk/reward profile:** Max loss = defined and capped (distance from purchase price down to put strike, plus put premium paid) for the life of the put. Max gain = theoretically unlimited to the upside, reduced by the cost of the put. Risk is DEFINED here — unlike naked put writing.

**McMillan's caveats/pitfalls:**
- Tax warning (explicit): if you are currently a *short-term* holder of the stock when you buy the put, "he eliminates any accrued holding period on his common stock. Moreover, the holding period for that stock does not begin again until the put is sold." Worked example: 5 months of holding + 6 months holding stock+put simultaneously = holding period considered ZERO for tax purposes. "One should consult a tax advisor."
- If the stock owner already holds long-term, or identifies the position as a hedge at time of purchase, there's no such tax effect.

**Capital/margin size:** Requires owning 100 shares outright (or a partial/odd lot) PLUS the put premium. At $100–500 this is only feasible on very low-priced stocks (e.g., sub-$5 shares) or by scaling to fewer than 100 shares if the broker allows fractional options exposure — otherwise this strategy is **not realistically usable** at this account size for anything but penny stocks.

### The Collar / Protective Collar ("Hedge Wrapper")
**Construction:** Own stock + buy a protective put + sell a covered call (typically OTM) to help finance the put. "This strategy is known as a protective collar or, more simply, a 'collar.'"

**Market outlook required:** Own the stock, mildly bullish-to-neutral but risk-averse; willing to cap upside in exchange for downside protection.

**Real numeric rules/formulas:**
- Worked numeric example: XYZ at 39, Oct 40 call at 3, Oct 35 put at .50. Plain covered write: max profit 4 pts above 40, breakeven 36. Adding the put: max profit reduced to 3.50, breakeven raised to 36.50, but max loss capped at 1.50 if XYZ is below 35 at expiration.
- **No-cost collar:** buy an OTM put whose cost is exactly offset by selling an OTM call — "he has established a protective collar at no cost — at least no debit. His 'cost' is the fact that he has forsaken the upside profit potential... above the striking price of the written call."
- Table 17-3 (his own numbers, LEAPS/2.5-yr example) — "Highest Call Strike That Pays for an At-the-Money Put," by volatility of underlying:
  - 30% vol → call struck ~30% out of the money
  - 40% vol → ~35% OTM
  - 50% vol → ~40% OTM
  - 70% vol → ~50% OTM
  - 100% vol → ~70% OTM
- Real-world example cited: 1999 Cisco (CSCO) 3-year no-cost collar — "a three-year put struck at 130 sells for about the same price as a three-year call struck at 200!" (stock at 130, ~50% volatility) — full downside hedge, still >50% upside room.
- Partial-cover variant: buy puts on the full share count but sell calls on only a fraction of it to leave some shares with uncapped upside. Example: own 1,000 shares, buy 10 Apr 55 puts at 1 (cost $1,000), sell only 5 Apr 65 calls at 2 (proceeds $1,000) — protection funded at zero cost, and 500 of the 1,000 shares retain unlimited upside.

**Risk/reward profile:** Max loss defined and capped by the put strike. Max gain capped by the call strike (unless using the partial-cover variant, in which part of the position keeps open upside). Fully defined risk.

**McMillan's caveats/pitfalls:**
- Adjustment dilemma: "there is no convenient exit strategy from a collar on the upside" — if the stock rallies hard, unwinding requires paying a large debit to buy back the written calls.
- Explicit warning: "if one sells options against stock that he has no intention of selling, he is actually writing naked calls in his own mind" — i.e., if you can't actually let the stock be called away (tax reasons, family stock, etc.), don't sell calls against it, because a big rally forces you to either take the tax hit or effectively behave as a naked call writer emotionally/financially.

**Capital/margin size:** Same underlying-stock capital requirement as the protective put above — requires 100-share lots typically. **Not realistically usable** at $100–500 except on penny stocks.

---

## Chapter 18 — Buying Puts in Conjunction with Call Purchases

### Locking in Call Profits with a Put Purchase (follow-up tactic)
**Construction:** Already holding a profitable long call; buy an OTM put to lock in gains while preserving upside. Not an initial strategy — "such a position can never be created as an initial position."

**Market outlook:** Was bullish (hence the call), now wants to protect built-up gains while staying open to further movement in either direction.

**Numeric example given:** Bought Oct 50 call at 3 when stock was 48; stock rises to 58, call now worth ~9; buy Oct 60 put at 4. Resulting "strangle" position cost 7 total (3+4) but "is always worth at least 10 points" at expiration if stock is between 50–60, and worth more outside that range — locking in a minimum 3-point profit with continued upside/downside potential.

**Risk/reward:** No further risk once locked in this way (worst case is the pre-computed minimum gain, per the specific numeric window). Reward: unlimited further gain if stock moves far in either direction beyond the strikes.

**Caveats:** None beyond noting it's a follow-up, not entry, tactic.

**Capital:** Only relevant to someone already holding a profitable call — moot for entry-level small-account use.

### Straddle Buying
**Construction:** Buy 1 call + 1 put, same strike, same expiration, same underlying.

**Market outlook required:** Expects a large move in the underlying but is directionally agnostic — needs volatility/movement, not a specific direction.

**Real numeric rules/formulas:**
- Worked example: XYZ 50, July 50 call at 3, July 50 put at 2 → straddle cost 5, breakevens at 45 and 55 (strike ± total premium).
- "One would normally purchase a straddle on a relatively volatile stock that has the potential to move far enough... This strategy is particularly attractive when option premiums are low, since low premiums will mean a cheaper straddle cost."
- "There is actually only a minute probability of losing one's entire investment" even though losses occur in "a relatively large percentage of cases" held to expiration — because there is usually some residual value to sell on the last trading day.
- Selection/ranking method: estimate % chance of the stock being above/below certain levels in a fixed period (e.g., 25% chance above 54 and 25% chance below 46 in 90 days), estimate resulting straddle values in each scenario, average them, and compare to current straddle price to estimate expected % return; rank candidates by this.
- Follow-up ("rolling"): if stock rises to next strike, roll the put UP (sell old put, buy put at higher strike); if stock falls, roll the call DOWN. Worked example: straddle bought for 6 at strike 40, stock rises to 45; sell Jan 40 put (worth 1), buy Jan 45 put (cost 3), net cost of adjustment = 2, leaving a combination costing 8 total that is worth at least 5 at any expiration price — "the most that the new position can lose at expiration is 3 points." Explicit rule: "reduces his risk exposure without limiting his profit potential — exactly the type of follow-up result the straddle buyer should be aiming for."
- Explicit caution against "taking small profits": "By taking small profits, the straddle buyer is immediately cutting off his chances for a substantial gain; that is why it is a poor strategy to limit the profits."

**Risk/reward profile:** Max loss = 100% of total premium paid, occurring only if the stock is exactly at the strike at expiration (a narrow/unlikely outcome). Max gain = theoretically unlimited on the call side, very large on the put side (capped only by stock going to zero). Risk is fully DEFINED (paid-in-full premium), even though the position looks aggressive.

**Caveats/pitfalls:** Volatile whipsaw price action can produce a straddle that "seems" to become profitable on one side, reverses, and ends up a net loser at expiration if held passively without follow-up. Old-style "trading against the straddle" (shorting/buying stock against it) is explicitly discouraged in the modern listed-put market as commission-inefficient and generally inferior to the roll-up/roll-down technique above.

**Capital/margin size:** Cost = combined put + call premium, no margin/collateral required beyond the debit paid (long options only). This **can be usable at $100–500** on lower-priced, higher-volatility underlyings, though the combined cost of ATM put+call on many stocks may exceed $500 depending on price/IV — needs to be sized to cheap underlyings.

### Reverse Hedge (Synthetic Long Straddle) with Puts
**Construction:** Buy 100 shares of stock + buy 2 puts (at the money) on that stock. Equivalent in payoff shape to a straddle purchase.

**Market outlook required:** Expects a large move in either direction (same as straddle buying), but through a stock-plus-puts structure rather than a pure options straddle.

**Real numeric rules/formulas:** None quantified beyond the general description; "the cost of two put options would normally be a relatively small percentage of the total cost of buying the stock," which limits risk percentagewise.

**Risk/reward profile:** Max loss occurs "if the stock were exactly at the striking price of the puts at their expiration date" (worst case is capped/limited). Gains accrue on either side: rising stock offsets the fixed put-purchase loss; falling stock generates put profits exceeding the stock loss.

**Caveats:** McMillan states plainly: "the straddle purchase is superior to the reverse hedge with calls" and "where listed puts exist on a stock, the reverse hedge strategy with calls becomes obsolete" — implying the pure straddle purchase (not this stock+2-puts version either) is generally preferred, since it avoids dividend obligations to no one (irrelevant here since long stock actually collects dividends) and has smaller commission costs than the multi-leg reverse hedge.

**Capital/margin size:** Requires buying 100 shares outright plus 2 puts — **not usable** at $100–500 except on penny stocks.

### Strangle Buying
**Construction:** Buy 1 put + 1 call, same expiration, DIFFERENT strikes (typically both out-of-the-money).

**Market outlook required:** Same as straddle — expects a large move, direction-agnostic — but strangle buying is a cheaper, wider-breakeven variant.

**Real numeric rules/formulas:**
- OTM example: Jan 45 put + Jan 50 call, stock at 47, total cost $400. Breakevens: below 41 or above 54 (i.e., strike ± premium on each side). "This investment... is generally smaller than that required to buy a straddle."
- "The maximum loss is possible over a much wider range than that of a straddle" — anywhere between the two strikes, vs. only exactly at the single strike for a straddle. Loss amount per instance is smaller for the strangle, "a compensating factor."
- ITM strangle variant: buy Jan 45 call (4) + Jan 50 put (4), stock at 47, total cost 8; but value is "always at least 5 points" (the width between strikes) → max loss capped at 3 points, versus 3 points max loss on the wider $400-cost OTM version above (same $ risk in this example but on a smaller base % for the cheaper OTM strangle — McMillan says the ITM version has *lower percentage risk* since it "can never lose all his investment").
- Explicit conservatism ranking: "the in-the-money strangle purchase certainly involves less percentage risk... Therefore, the strangle created by the two — an in-the-money call and an in-the-money put — should be more conservative than the out-of-the-money strangle."

**Risk/reward profile:** Max loss = 100% of premium paid (OTM version) or premium paid minus the guaranteed intrinsic floor (ITM version) — DEFINED risk either way. Max gain = large/unlimited on either side if stock moves far enough beyond either strike.

**McMillan's caveats/pitfalls:** Explicit warning on cheap OTM strangles: "the out-of-the-money strangles may appear deceptively cheap... However, the probability of realizing the maximum loss equal to one's initial investment is fairly large with strangles. This is distinctly different from straddle purchases, whereby the probability of losing the entire investment is small. The aggressive speculator should not place a large portion of his funds in out-of-the-money strangle purchases."

**Capital/margin size:** The cheapest of the long-volatility strategies in these chapters — OTM strangles can often be bought for well under $500 total premium on many underlyings. **Usable at $100–500**, with the caveat above about high probability of total loss on cheap OTM strangles specifically.

---

## Chapter 19 — The Sale of a Put

### Uncovered (Naked) Put Sale
**Construction:** Sell 1 put without any offsetting stock or option position. "The uncovered sale of a put is a more common strategy than the covered sale of a put." A bullish/neutral income strategy.

**Market outlook required:** "One needs to be somewhat bullish, or at least neutral, on the underlying stock." Two variants: writing OTM puts (less aggressive, higher probability of max profit) or writing ITM puts (more aggressive, more premium collected, faster losses if wrong).

**Real numeric rules/formulas (verbatim/close):**
- Collateral requirement: "The collateral requirement for writing naked puts is the same as that for writing naked calls. The requirement is equal to 20% of the current stock price plus the put premium minus any out-of-the-money amount."
- "The minimum requirement is 10% of the put's striking price, plus the put premium, even if the computation above yields a smaller result."
- Full worked example (Table 19-2): XYZ 50, Jan 50 put at 4, writer plans to hold until stock falls to 43. Collateral at stock=43: 20% of 43 = $860, plus 7 points ITM ($700) = $1,560 per put. For 5 puts: $7,800 gross requirement, less $1,925 net premium received (5 × $400 gross − $75 commission) = **$5,875 net collateral** for a **32.8% potential return** (computed as premium ÷ net collateral).
- Break-even formula: strike − premium per contract (example: $50.00 − $3.85 = $46.15).
- Screening rules he suggests for building a candidate list: reject puts offering less than 5% downside protection (or return-if-unchanged below 5%) on the "highest return" list; require a minimum annualized return, e.g. "at least 12% on an annualized basis," for the "most downside protection" list.
- The naked put write's collateral requirement is smaller than covered call writing: "one is only collateralizing 20% of the stock price plus the put premium, as opposed to 50% for the covered call write on margin."

**Risk/reward profile:** Max gain = premium received, capped, achieved if stock is above the strike at expiration (or unchanged with an OTM put). Max loss = very large — "limited only by the fact that a stock cannot go below zero" — this is a large, technically bounded-but-substantial, UNDEFINED-feeling risk relative to the small premium collected. Table 19-1 example: stock falling from 50 to 30 turns a max $400 gain into a $1,600 loss.

**McMillan's caveats/pitfalls (explicit, strongly worded):**
- "Despite the seemingly benign nature of naked put writing, it can be a highly dangerous strategy for two reasons: (1) Large losses are possible if the underlying stock takes a nasty fall, and (2) collateral requirements are small, so it is possible to utilize a great deal of leverage."
- "It may seem like a good idea to write out-of-the-money puts on 'quality' stocks that you 'wouldn't mind owning.' However, any stock is subject to a crushing decline." Cites real examples: "IBM in 1991, Procter and Gamble in 1999, and Xerox in 1999."
- Direct instruction: "do not leverage your account heavily in the naked put strategy, regardless of the 'quality' of the underlying stock."
- On rolling: unlike covered call writing (where rolling down/forward is advantageous to avoid stock commissions), "rolling down is not as advantageous for the naked put writer" — since there are no stock commissions to save, it's often better to simply close out and look for a fresh opportunity in a different stock.
- Buy-stock-below-market application: writing a naked put as a proxy for a "buy limit order" (e.g., write a 3-month put at 5 instead of a limit order at 55 when stock is 60) — nets the same effective purchase price of 55, with the bonus of keeping the premium if never assigned. McMillan presents this favorably but it's still subject to the same large-loss caveat above if the stock crashes.

**Capital/margin size:** Requires real cash/margin collateral (the 20%-of-stock-price-plus-premium formula, with a floor of 10% of strike + premium) — his own numeric example ties up $5,875–$7,800 for just 5 puts on a $50 stock. **Not usable** at $100–500 except on extremely low-priced stocks (e.g., sub-$5–$10 shares), and even then the position ties up essentially all of a micro account's capital in a single undiversified bet with large tail risk — flagged as high-risk regardless of size per McMillan's own explicit warning above.

### The Covered Put Sale
**Construction:** Sell 1 put while simultaneously short the underlying stock (margined as the stock short; "there is none required for the short put").

**Market outlook:** Neutral-to-bearish (limited profit if stock stays below the strike).

**Numeric rules:** None given beyond the general description of the payoff.

**Risk/reward:** "Limited profit potential... obtained if the underlying stock is anywhere below the striking price of the put at expiration. There is unlimited upside risk" (from the short stock leg).

**McMillan's caveat — this strategy is explicitly dismissed:** "This is really a position equivalent to a naked call write, except that the covered put writer must pay out the dividend on the underlying stock... The naked sale of a call also has an advantage over this strategy in that commission costs are considerably smaller... The covered put sale is a little-used strategy that appears to be inferior to naked call writing. As a result, the strategy is not described more fully." He explicitly does not recommend it.

**Capital/margin:** Requires margin for a short stock position — not usable at $100–500.

### Ratio Put Writing
**Construction:** Short the underlying stock + sell 2 puts for each 100 shares shorted. Payoff shape identical to ratio call writing.

**Numeric rules:** None quantified.

**Risk/reward:** Same shape as ratio call write (limited/moderate gain zone with escalating risk on both sides, given the short stock leg).

**McMillan's caveat — also explicitly dismissed:** "The ratio call write is a highly superior strategy... The ratio call writer receives dividends while the ratio put writer would have to pay them out. In addition, the ratio call writer will generally be taking in larger amounts of time value premium, because calls have more time premium than puts do. Therefore, the ratio put writing strategy is not a viable one." Not usable/not recommended by the author at all.

**Capital/margin:** Requires shorting stock — not usable at $100–500 and not recommended regardless.

---

## Chapter 20 — The Sale of a Straddle

### Covered Straddle Write
**Construction:** Own 100 shares of stock + sell 1 call and 1 put (same strike). McMillan clarifies the naming: "this position is not totally covered — only the sale of the call is covered by the ownership of the stock. The sale of the put is uncovered." Equivalent to "a 200-share covered call write" or to selling 2 uncovered puts.

**Market outlook required:** Same as covered call writing — neutral to mildly bullish; "does not change the price parameters of his position" versus a plain covered write on the same stock/strike.

**Real numeric rules/formulas (verbatim):**
- Max profit formula: `Maximum profit = Straddle premium + Striking price − Initial stock price`
- Breakeven formula: `Break-even price = Stock price + Strike price − Straddle premium`
- Worked example: stock 51, Jan 50 call at 5, Jan 50 put at 4 → max profit $800, breakeven 46.

**Risk/reward profile:** Max gain = capped (per the formula above), realized anywhere above the strike at expiration. Max loss = large — "the covered straddle writer loses money twice as fast on the downside, since his position is similar to a 200-share covered write." Risk is technically bounded only by the stock going to zero, same character as naked put writing (because of the uncovered put leg).

**McMillan's caveats/pitfalls:**
- Margin note: "the covered call writer who is writing on margin and is fully utilizing his borrowing power for call writing will have to add additional collateral in order to write covered straddles," since the put leg is uncovered — though a cash-account stockholder can "switch to the covered straddle writing strategy without putting up additional funds" by moving to a margin account and using the stock's collateral value.
- Variant: selling the put at a lower (OTM) strike than the call increases upside profit potential and creates a "both expire worthless" zone, at the cost of more downside dollar risk if the stock falls below that lower put strike.

**Capital/margin size:** Requires owning 100 shares plus uncovered-put collateral on top — **not usable** at $100–500 except on penny stocks; effectively combines the capital demands of covered call writing AND naked put writing.

### Uncovered (Naked) Straddle Write
**Construction:** Sell 1 call + 1 put, same strike, same expiration, no stock position. Equivalent in payoff shape to ratio call writing (100 shares long + 2 calls short).

**Market outlook required:** Strongly neutral — expects the stock to stay near the strike through expiration. "A neutral strategy with limited profit potential and large risk potential. However, the probability of making a profit is generally quite large."

**Real numeric rules/formulas:**
- Worked example: stock 45, straddle sold for 7 → profitable zone (before follow-up) is 38 to 52 (strike ± total premium collected), per Table 20-2.
- Margin requirement: "The investment required for a naked straddle is the greater of the requirement on the call or the put. In general, this means that the margin requirement is equal to the requirement for the in-the-money option in a simple naked write. This requirement is 20% of the stock price plus the in-the-money option premium."
- Selection index formula (his own, explicitly labeled a "somewhat subjective measurement"):
  `Index = Straddle time value premium / (Stock price × Volatility)`
  with suggested screens: exclude candidates where either leg trades under ½–1 point, or where in-the-money time premium is small; also suggests requiring the straddle premium be worth at least 10% of the stock price, and excluding straddles with less than 30 days of remaining life.
- Neutral-ratio delta rule (mirrors ratio call writing): "the difference between a call's delta and a put's delta is approximately one." Worked example: call delta .60, put delta −.40 → neutral ratio is 1.5:1 (puts:calls), i.e., sell 3 puts for every 2 calls — noted as equivalent to the classic "sell 5 calls, buy 300 shares" ratio-write neutral ratio.

**Risk/reward profile:** Max gain = total premium collected, capped, achieved only if stock is exactly at the strike at expiration (Figure 20-2 profile: "shape like a roof"). Max loss = large in EITHER direction if the stock moves far from the strike — genuinely large, UNDEFINED-feeling risk without follow-up action (the call side is theoretically unlimited upward; the put side is bounded only by the stock reaching zero).

**McMillan's caveats/pitfalls (extensive follow-up discussion, most detailed risk-management section in these chapters):**
- "The risks involved in straddle writing can be quite large... in an extremely volatile market, especially a bullish one, losses can occur rapidly and follow-up action must be taken."
- Buying back at the breakeven point is flawed as a rule of thumb: "it is a misconception to believe that one can always buy the straddle back at the break-even point and hold his losses to mere fractions of a point... This type of buy-back strategy works best when there is little time remaining in the straddle."
- Two follow-up actions explicitly discouraged: (1) doing nothing at all ("should be used only by the most diversified and well-heeled investors"), and (2) "legging out" by covering the profitable side and hoping for a reversal on the other — "This is a trader's sort of action, not that of a disciplined strategist, and it should be avoided."
- Recommended follow-up: buy an option at the next strike beyond the threatened side (e.g., stock rallying → buy a call at a higher strike) to cap the loss while preserving some remaining profit zone; this converts the naked side into a defined-risk spread and typically reduces the margin requirement.
- Explicit warning against selling deeply OTM, short-dated, "fractionally priced" straddles/strangles purely for the high win-probability: "This can be an extremely aggressive strategy at times, for if the underlying stock should move quickly in either direction through a striking price, there is little the strangle writer can do... Selling fractionally priced combinations is a poor strategy and should be avoided."
- Explicit advice to avoid excess trading/anticipation: "the strategist should not attempt to anticipate movement in an underlying stock... he should resist the temptation to trade, and should operate his strategy according to his original plan."

**Capital/margin size:** Naked options on both sides — margin equal to the greater of the put or call naked-write requirement (effectively similar magnitude to the naked put example in Ch. 19, i.e., thousands of dollars for a single normal-priced underlying). **Not usable** at $100–500.

### Strangle (Combination) Writing
**Construction:** Sell 1 OTM call + 1 OTM put, same expiration, different (wider) strikes than a straddle. Equivalent in payoff shape to "variable ratio writing."

**Market outlook required:** Neutral, with a wider expected trading range than straddle writing accommodates — "the strangle writer can remain neutral on the outlook for the underlying stock, even when the stock is not near a striking price."

**Real numeric rules/formulas:**
- Worked example: stock 65, Jan 70 call at 4, Jan 60 put at 3 → total credit 7, profitable zone 53–77 at expiration (Table 20-3).
- Margin rule: "the true collateral requirement for any write involving both puts and calls — straddle write or strangle write — is the greater of the requirement on the put or the call plus the amount by which the other option is in-the-money." When both legs are OTM, the smaller of the two out-of-the-money amounts can be deducted from the requirement.

**Risk/reward profile:** Wider max-profit zone than a straddle (profit if stock stays *between* the two strikes, not just exactly at one strike), but same character of large/open-ended risk beyond either breakeven if unmanaged.

**McMillan's caveats/pitfalls:** "If the stock begins to rise quickly or to drop dramatically, the strangle writer often has little recourse but to buy back the in-the-money option in order to limit his losses. This can... entail a purchase price involving excess amounts of time value premium, thereby generating a significant loss" — i.e., the wider breakevens look safer at entry but don't eliminate the follow-up problem. Same explicit warning against selling cheap, short-dated, deeply OTM strangles as under the naked-straddle section above.

**Capital/margin size:** Same order of magnitude as naked straddle writing — **not usable** at $100–500.

---

## Chapter 21 — Synthetic Stock Positions Created by Puts and Calls

### Synthetic Long Stock
**Construction:** Buy 1 call + sell 1 (naked) put, same strike, same expiration — no stock position. "Sets up a position that is equivalent to owning the stock."

**Market outlook required:** Bullish — same outlook as an outright stock purchase.

**Real numeric rules/formulas:**
- Worked example: XYZ 50, Jan 50 call at 5, Jan 50 put at 4 → net debit of 1 point. At every expiration price, the synthetic position's result is "exactly $100 less than the stock results," attributable to the net time premium paid (call's 5 pts time premium out vs. put's 4 pts time premium in).
- Margin comparison: buying 100 shares of a $50 stock needs "$5,000 in a cash account or $2,500 in a margin account (if the margin rate is 50%)." The synthetic version needs only "a $100 debit plus a collateral requirement — 20% of the stock price, plus the put premium, minus the difference between the striking price and the stock price," worked out to **$1,500 total** in his example (vs. $2,500 or $5,000 for actual stock).
- Leverage example: stock rallies to 60 → stock-position return is 40% ($1,000/$2,500 margin); synthetic-position return is 60% ($900/$1,500 collateral) — "leverage works to the downside as well, so that the percent risk is also greater in the option strategy."

**Risk/reward profile:** Essentially matches long stock — large/unlimited upside, large downside (bounded only by stock going to zero via the naked put leg) — but on materially less capital, meaning PERCENTAGE risk is amplified relative to owning stock outright.

**McMillan's caveats/pitfalls:** Trade-offs vs. real stock ownership: the option strategist "does not collect dividends, whereas the stock owner does" (though he earns interest on the unspent balance instead). Presented as a capital-efficient substitute for stock ownership in certain strategies, not a distinct standalone recommendation with special caveats beyond the leverage/risk tradeoff.

**Capital/margin size:** Still requires naked-put-style collateral (20% of stock price + put premium, adjusted), which the chapter's own numbers put at $1,500 for a single $50-stock synthetic position — **not usable** at $100–500 except on very low-priced underlyings, and even then it carries the same large-tail-risk character as naked put writing (undefined/large downside via the short put leg).

### Synthetic Short Sale
**Construction:** Sell 1 call + buy 1 put, same strike, same expiration — no stock position. Equivalent to shorting the stock.

**Market outlook required:** Bearish — same outlook as shorting stock outright.

**Real numeric rules/formulas:**
- Margin comparison: shorting stock needs "$2,500 to collateralize this position" (50% margin, $50 stock); the synthetic version needs "20% of the stock price, plus the call price, less the credit received, for a $1,400 requirement."
- Same underlying example (XYZ 50, call 5, put 4) shows the option strategy outperforming a straight short sale at every expiration price by $100, again due to the net time-premium capture (selling the higher-time-premium call, buying the lower-time-premium put).

**Risk/reward profile:** Matches short stock's shape — large gains on a decline, theoretically unlimited losses on a rally (via the naked short call leg) — again on materially less capital than an actual margined short sale.

**McMillan's caveats/pitfalls:**
- Practical advantages over actual short selling: no need to borrow shares, no uptick-rule constraint (relevant to the era this was written), can be executed "even though the underlying stock might be trading on a minus tick."
- Explicit caveat: "If one sells calls on a stock that cannot be borrowed, then he must be sure to avoid assignment. For if one is assigned a call, then he too will be short the stock. If the stock cannot be borrowed, the broker will buy him in." Recommendation: use a strike where the call is initially OTM to reduce (not eliminate) early-assignment risk in hard-to-borrow names.

**Capital/margin size:** Requires naked-call-style collateral ($1,400 in his own example) — **not usable** at $100–500 except on very low-priced underlyings, and carries theoretically unlimited-upside risk on the short call leg (arguably the single riskiest risk-profile shape covered in these chapters, since a stock's upside is unbounded while its downside is capped at zero).

### Split-Strike Conversion (Bullish) — "Buy an OTM Call for Free"
**Construction:** Sell 1 OTM put (naked) + buy 1 OTM call, different (split) strikes, generally for a net credit. "This position is sometimes called a split-strike conversion, even though it doesn't contain a position in the underlying stock."

**Market outlook required:** Bullish, with a specific target zone in mind — profits if the stock is unchanged, moderately up, or way up; loses only if the stock declines significantly.

**Real numeric rules/formulas:**
- Worked example: stock 53, Jan 50 put sold at 2, Jan 60 call bought at 1 → net credit 1 point. If stock finishes between 50 and 60 at expiration, both legs expire worthless and profit = the 1-point credit. Above 60: unlimited profit via the long call. Below 50: large losses via the naked put (Table 21-3).

**Risk/reward profile:** Small, capped gain in the "sideways-to-moderately bullish" and "large rally" zones; large, essentially open-ended loss if the stock falls significantly (naked put leg) — an asymmetric profile: small defined-ish upside credit vs. large downside tail risk.

**McMillan's caveats/pitfalls:** Frames it as "attempting to buy an out-of-the-money call for free," useful "often useful when options are overpriced" (rich premium on both legs makes the free-call financing more attractive). Requires "a definite opinion about the future price movement of the underlying stock" and the investor "must have... sufficient collateral" (naked put) to support it.

**Capital/margin size:** Requires naked-put collateral for the short put leg — **not usable** at $100–500 except on very cheap underlyings, and shares naked-put-writing's large-tail-risk character.

### Split-Strike Reversal (Bearish)
**Construction:** Buy 1 OTM put + sell 1 OTM call (naked), different strikes, generally for a net credit — the bearish mirror image of the above. "Also called a split-strike reversal."

**Market outlook required:** Bearish, with the same tolerant middle zone — profits if the stock declines, stays flat, or falls moderately; loses if the stock rallies significantly.

**Real numeric rules/formulas:**
- Worked example: stock 65, Feb 60 put bought at 2, Feb 70 call sold at 3 → net credit 1 point. Between 60–70 at expiration, both legs expire worthless and profit = 1-point credit. Below 60: large profits via the long put. Above 70: "unlimited losses are possible because there is a naked call at 70" (Table 21-4).

**Risk/reward profile:** Small capped gain in the "sideways-to-moderately bearish"/"large decline" zones; large, essentially unlimited loss if the stock rallies significantly past the naked call strike — mirror-image asymmetry to the bullish version above.

**McMillan's caveats/pitfalls:** Notes this exact structure "is used very frequently in conjunction with the ownership of common stock" — i.e., it's the mechanical basis of the protective collar covered in Chapter 17 (buy an OTM put, sell an OTM call to finance it) when applied against an existing stock position instead of standalone. Standalone (no stock), the naked call leg carries the same unlimited-upside-risk warning as the synthetic short sale above.

**Capital/margin size:** Requires naked-call collateral for the short call leg — **not usable** at $100–500, and carries the theoretically-unlimited-loss profile of a naked call write if the stock rallies hard.

---

## Summary Table — Usable at $100–500 spendable capital?

| Strategy | Defined risk? | Usable at $100–500? |
|---|---|---|
| Put buying (speculative) | Yes — premium paid | **Yes**, size to cheap/OTM puts; McMillan's own preference for ITM puts may exceed budget |
| Protective put (put + stock) | Yes | No — needs 100-share stock position, unless a penny stock |
| Collar / no-cost collar | Yes | No — same stock-ownership requirement |
| Straddle buying | Yes — premium paid | Yes on cheap/volatile underlyings; combined premium can exceed budget on higher-priced names |
| Reverse hedge / synthetic straddle (stock + 2 puts) | Bounded but stock-heavy | No — requires 100 shares |
| Strangle buying | Yes — premium paid | **Yes**, generally the cheapest defined-risk long-volatility play; McMillan warns cheap OTM strangles have high probability of total loss |
| Uncovered put sale | No — large tail risk, real collateral required | No — his own example ties up $5,875+ for 5 contracts; McMillan explicitly warns against overleveraging even quality names |
| Covered put sale | No | No, and McMillan says don't use it at all (inferior to naked call writing) |
| Ratio put writing | No | No, and McMillan says don't use it at all (inferior to ratio call writing) |
| Covered straddle write | No | No — needs stock + naked put collateral |
| Uncovered straddle write | No — large risk both directions | No — real naked-option margin required |
| Strangle (combination) write | No | No — same margin character as naked straddle write |
| Synthetic long stock (call + short put) | No — naked put leg | No — his own example needs $1,500 collateral |
| Synthetic short sale (short call + long put) | No — naked call leg, unlimited risk | No — his own example needs $1,400 collateral |
| Split-strike conversion (bullish) | No — naked put leg | No |
| Split-strike reversal (bearish) | No — naked call leg, unlimited risk | No |

Bottom line from these five chapters: for a genuinely small (~$100–500) account, McMillan's own numbers point almost exclusively toward the pure long-premium strategies — **outright put buying** and **long straddles/strangles** — since every strategy involving a naked written option or 100-share stock ownership carries collateral requirements he himself quantifies in the thousands of dollars.

---

## Notes on source completeness

- ch_019.txt, ch_020.txt, ch_021.txt, and ch_022.txt were all read in full (all lines).
- ch_020.txt (Ch. 19, "The Sale of a Put") ends abruptly mid-sentence at "...to incorporate the volatility of the underlying stock should rightfully be employed. As men-tioned previously, that technique is presented in Chapter 28 on mathematical applications." — this is the natural chapter-end sentence, so content is NOT thin/missing here; the covered-put-sale and ratio-put-writing sections that logically follow appear instead at the *top* of ch_021.txt, confirming the chapter boundary was simply split across the two files as expected.
- No chapter in this set was unexpectedly thin — all four files contained substantial, detailed strategy discussion with worked numeric examples, consistent with the rest of the book's style.
