# Part VI: Measuring and Trading Volatility — Notes from McMillan, *Options as a Strategic Investment* (5th ed.)

Source files read in full:
- ch_038.txt = Chapter 36, "The Basics of Volatility Trading"
- ch_039.txt = Chapter 37, "How Volatility Affects Popular Strategies"
- ch_040.txt = Chapter 38, "The Distribution of Stock Prices"
- ch_041.txt = Chapter 39, "Volatility Trading Techniques" (file ends mid-sentence at the "poor movement" histogram discussion — everything up to that point was read; nothing was invented to fill the cutoff)

Note on source quality: files are OCR/epub-converted with minor spacing artifacts ("profitability's," "com mon," etc.); quotes below are transcribed as literally as possible, artifacts included in a few spots but not distractingly.

---

## 1. Core concepts — how McMillan defines/measures volatility, and how to judge if current IV is high or low

### Two kinds of volatility (Ch 36)
- **Historical volatility**: "a measure of how fast the underlying instrument has been changing in price." It is the standard-deviation formula from elementary statistics, computed on actual past price changes. "It is an exact calculation, and there is little debate over how to compute historical volatility." By itself the number (e.g., "20%") is fairly meaningless except for comparison purposes — comparing one stock/instrument to another, or comparing time periods.
- **Implied volatility (IV)**: "the option market's prediction of the volatility of the underlying over the life of the option." It's derived, not directly observed: given stock price, strike, time to expiration, interest rate, and dividends, IV is whatever volatility input makes the pricing model (Black-Scholes) output the option's actual market price. "The actual process of determining implied volatility is an iterative one. There is no formula, per se."
- Historical volatility is "usually in the range of 15% to 20%" for the broad market; "a very volatile stock might have an historical volatility in excess of 100%."
- Historical volatility should be computed over multiple lookback windows (10-day, 20-day, 50-day, 100-day) since a stock's recent vs. longer-term behavior can diverge sharply — McMillan gives a worked example where 10-day HV = 20% while 20-day = 23% (a "slowing down" stock), versus another regime where 10-day HV = 80% while 100-day HV = 55% (an "accelerating" stock). "The 20-day historical is commonly the most popular measure."

### Is IV a good predictor of future (actual) volatility? — No.
McMillan is explicit and reviews several real charts (OEX, and two individual stocks) comparing 20-day-moving-average implied volatility against the 20-day historical volatility realized 20 days later:
> "The important thing to note from these figures is that they clearly show that implied volatility is really not a very good predictor of the actual volatility that is to follow. If it were, the difference line would hover near zero most of the time. Instead, it swings back and forth wildly, with implied volatility over- or underestimating actual volatility by quite wide levels."
- OEX options in particular are "almost always" overpriced (implied > subsequent actual) — this is called out as a specific, structural, near-permanent skew for that index.
- One striking example: a stock's IV was near its lowest levels in Feb/March 1999 just before the stock *tripled* in a month — "implied volatility was a poor predictor of forthcoming actual volatility in this case."
- One general finding: "implied volatility seems to fluctuate less than actual volatility" — option-pricing traders tend toward "middle of the road" predictions that get overtaken by real market moves.

### How to judge whether current IV is "cheap" or "expensive" — the percentile concept
This is the central mechanism the book gives for a live IV filter (elaborated further, with numeric criteria, in Ch 39 — see Section 3 below), but it's introduced conceptually in Ch 36:
> "It is often conventional to talk about the percentile of implied volatility. That is a way to rank the current implied volatility reading with past readings for the same underlying instrument."

Critical caveat (quoted in full because it is easy to get wrong): a percentile alone is not sufficient — you also need to know how **wide** the historical range is:
> "One can't really tell if 'cheap' options are cheap as a practical matter. That's because one doesn't know how tightly packed together the past implied volatility readings are... if the first percentile of XYZ options were at an implied volatility reading of 39% and the 100th percentile were at 45%, then a reading of 40% is really quite mundane. There just wouldn't be much room for implied volatility to increase on an absolute basis... However, if the distribution of past implied volatility is wide, then one can truly say the options are cheap if they are currently in a low percentile."

So the practical rule is two conditions, not one:
1. Current IV is in a low (or high) percentile of its own trailing history, AND
2. The trailing range (1st-to-100th percentile spread, or similar) is wide enough that moving back toward the middle would produce a meaningful price change.

### LEAPS / longer-dated options behave differently
Using a scatter diagram of OEX regular vs. LEAPS option IVs over several years: near-term option IV ranged roughly 14%–40%, while options with 24+ months to expiration ranged only about 17%–32%. Conclusion:
> "LEAPS option implied volatilities just don't change nearly as much as those of short-term options... LEAPS options will rarely appear 'cheap' when one looks at their percentile of implied volatility, including all the short-term options, too."
He warns against comparing a LEAPS IV percentile against a percentile computed using all expirations (including short-term) — the ranges aren't comparable. He also warns against the reverse fallacy: restricting the percentile calc to only long-term options and assuming that's now a clean read, because (a) if you hold the LEAPS a long time the volatility range will widen and IV could still drop a lot, and (b) even a "cheap" percentile within the narrow long-term range might not translate to much dollar gain if it moves to the top of that narrow range.

### Composite IV computation
The "implied volatility" number for an underlying (as opposed to for one specific option) is a **composite**: individual option IVs weighted by (a) distance in- or out-of-the-money (at-the-money gets more weight) and (b) trading volume, combined into one daily reading. This composite reading, smoothed with a 20-day (or 20-to-30-day exponential) moving average, is what's tracked historically for percentile calculations. This composite is explicitly different from VIX, which "uses only the options closest to the money."

### Other volatility-forecasting approaches mentioned (Ch 36)
- **GARCH** (Generalized Autoregressive Conditional Heteroskedasticity): incorporates both historical and implied volatility plus a "fudge factor" constant; requires the user to choose weightings, so "it can be just as vague" as simpler approaches. "It might not even be superior, from a strategist's viewpoint, to using the simple minimum/maximum techniques." Best suited to short-term forecasts (favored by currency-option dealers); "for longer-term volatility projections, which is what a position trader of volatility is interested in, GARCH may not be all that useful."
- **Moving averages**: a smoothed (often exponential) moving average of the daily composite IV, or of recent historical volatility, over 20–30 days.

---

## 2. How IV should change strategy choice — verbatim rules for buying vs. selling options

This is the most load-bearing section for the project. Quoting closely as instructed.

### The master rule (Ch 39, stated plainly)
> "...we do know that volatility tends to trade in a range in the long run. Therefore, the approach that traders agree upon is this: If implied volatility is 'low,' buy it. If it's 'high,' sell it with caution. So simple: Buy low, sell high (not necessarily in that order)."

### Ch 37's version of the same rule, applied to specific strategy types
On straddle/strangle buying and selling:
> "Since owning a straddle involves owning both a put and a call with the same terms, it is fairly evident that an increase in implied volatility will be very beneficial for a straddle buyer... Thus, if a straddle buyer is careful to buy straddles in situations in which implied volatility is 'low,' he can make money in one of two ways. Either (1) the underlying price makes a move great enough in magnitude to exceed the initial cost of the straddle, or (2) implied volatility increases quickly enough to overcome the deleterious effects of time decay."

And the mirror-image warning for sellers:
> "...it is very important when selling options — and this applies to covered options as well as to naked ones — to sell only when implied volatility is 'high.'" [context: a seller who sells when IV is low is exposed to losses that outrun time decay if IV then rises]

On outright option purchase timing relative to time decay (Ch 37):
> "If you are buying options, and you buy them when implied volatility is 'low,' you stand to benefit if implied volatility merely returns to 'normal' levels while you hold the position... Conversely, an option seller should be keenly aware of implied volatility when the option is initially sold — perhaps even more so than the buyer of an option... If implied volatility is 'too low' when the option writing position is established, then an increase (or worse, an explosion) in implied volatility will be very detrimental to the position, completely overcoming the effects of time decay. Hence, an option writer should not just sell options because he thinks he is collecting time decay each day that passes."
> "In a similar manner, a decrease in implied volatility can be just as important. Thus, if the call buyer purchases options that are 'too costly,' ones in which implied volatility is 'too high,' then he could lose money even if the underlying makes a modest move in his favor."

### Debit spreads (bull/bear vertical spreads) behave *opposite* to outright long options — a key, counterintuitive, quotable finding
This directly matters since the repo's draft strategy is long calls/long puts and might later consider spreads.

> "Ask yourself this simple question: If the stock remains unchanged at 100, and implied volatility increases dramatically, will the price of the 90-110 call bull spread grow or shrink? ... The truth is that, if implied volatility increases, the price of the spread will shrink. I would suspect that this comes as something of a surprise to a good number of readers."

He shows the position vega of an at-the-money call bull spread is *negative* — the position loses value as IV rises, gains as IV falls — the reverse of an outright long call. And critically, this hurts a bullish trader who chose a spread specifically because the calls looked expensive:

> "High or increasing implied volatility is not a friend of the bull spread, while it is a friendly ally of the outright call purchase... So, be careful when using bull spreads. If you really think a call option is too expensive and want to reduce its cost, try this strategy: Buy the call and simultaneously sell a credit put spread (bull spread) using slightly out-of-the-money puts."

Symmetric findings for the other spread types:
- **Put credit (bull) spreads**: "makes money when implied volatility decreases" — same direction as call bull spreads (loses when IV rises), plus added early-assignment risk if IV falls and the stock falls together.
- **Put bear spreads (debit)**: benefit from an IV increase ("the spread will widen out slightly") — opposite of call bull spreads. But like all verticals, "the spread doesn't widen out much if the underlying makes a favorable move" — the structural problem with verticals under high IV is general, not just directional.
- **Calendar spreads**: "a calendar spread is a 'long volatility' play (and a reverse calendar spread is just the opposite)." An increase in IV widens a calendar spread (both options gain value, but the longer-dated leg gains more, since it has higher vega) — this is the *opposite* dynamic to vertical debit spreads. Concrete numeric table (5-month vs. 2-month ATM calls on a $100 stock): spread value at 20% IV = 2.58, at 40% IV = 4.46, at 100% IV = 12.92 (one week after establishment, stock unchanged) — "implied volatility levels have a huge effect on the value of a calendar spread. The actual initial contribution of time decay is rather small in comparison." Explicit trap warned against: buying a calendar when IV is already very high (e.g., 80%) because the position "seems...very attractive," but if IV later normalizes back toward the stock's typical level (e.g., 40%), the anticipated long-dated option value at the short expiration will be much lower than expected, turning an apparently profitable calendar into a breakeven or loser even at the ideal (pin-the-strike) outcome.
- **Ratio spreads / backspreads**: A call ratio spread = a call bull spread + extra naked short calls, so it inherits *both* problems: hurt by rising IV (bull-spread-vega effect) *and* hurt by rising IV (naked short call vega effect) simultaneously — "both components are harmed by an increase in implied volatility." A backspread is the mirror image and benefits from rising IV in both components.

### Practical selection rule at position-construction time (Ch 37 Summary)
> "In general, one can always determine the exposure of his position to volatility by computing the vega of this position... Once one has a feeling for his exposure to volatility, he can then assess whether an adverse volatility movement is likely. For example, if an increase in implied volatility would be harmful, and the strategist sees that current levels of implied volatility are quite low in comparison to historical norms, then perhaps he should remove or adjust the position."

### Underlying-instrument suitability by strategy type (Ch 39, on selling volatility)
> "Index options are by far the best choices for naked option selling. Futures are next, and stocks are last. This is because of the ways those various instruments behave; stocks have by far the greatest capability of making huge gap moves that are the bane of naked option selling."

Choice between naked writing and credit spreads:
> "The problem with a credit spread is that one is both selling expensive options and also buying expensive options as protection... if volatility decreases, the profits to be realized by a credit spreader are quite small (perhaps not even enough to overcome the commission expense of removing the position), whereas a naked option seller would benefit to a greater and more obvious extent."

### Strategy picked once "cheap" or "expensive" has been identified (Ch 39)
- **If IV is too low**: buy a straddle (if underlying is near an available strike) or a strangle (if between strikes); position traders should use "several months of life remaining, in order to improve his chances of making a profit." Construct the straddle/strangle **delta-neutral** using option deltas to set the put:call ratio (a worked example shows a 2-calls-to-3-puts neutral ratio at 40% IV — note from Ch 37 that this neutral ratio itself shifts with IV level, e.g. becomes 2-to-1 at IV=110% instead of 3-to-2 at IV=40%, so "a trader wishing to remain delta-neutral must monitor not only changes in stock price, but changes in implied volatility as well"). A calendar spread is a secondary, less-preferred, low-IV strategy (positive vega, but limited profit potential is "too much of a burden" for most traders).
- **If IV is too high**: sell an out-of-the-money strangle (naked put + naked call) if suitable for the trader's risk tolerance, or a credit spread if naked selling isn't appropriate. Strike selection is a probability-and-premium tradeoff (see Section 3).

### Caution flags before selling volatility even when it looks "expensive" (Ch 36)
This is one of the most operationally important warnings in the whole section — it explains *why* a naive "sell when IV percentile is high" filter is dangerous:
> "The seller of volatility can watch for two things as warning signs that perhaps the options are 'predicting' a corporate event (and hence should be avoided as a 'volatility sale'). Those two things are a dramatic increase in option volume or a sudden jump in implied volatility of the options."
And:
> "...a major market-maker once said he believed that most increases in implied volatility were eventually justified — that is, some corporate news item was released that made the stock jump. Hence, a volatility seller should avoid situations such as these. Any sudden increase in implied volatility should probably be viewed as a potential news story in the making."

Distinguishing signal of "informed" (avoid selling) vs. "benign" (okay to sell) expensive options:
> "...if the options are active and expensive, and if the stock is rising too, you probably have a reasonably good indication that 'someone knows something.' However, if the options are expensive but none of the other factors are present, especially if the stock is declining in price — then one might feel more comfortable with a strategy of selling volatility in this case."

Also flagged as an acceptable-to-sell case: broad market/bear-market volatility spikes with a known cause (crash, sharp selloff) — "In these situations, the volatility seller knows why implied volatility is high... The time when the volatility seller must be careful is when the options are expensive and no one seems to know why."

Asymmetric risk of being wrong:
> "Buyers of volatility really have little to fear if they miscalculate and thus buy an option that appears inexpensive but turns out not to be... Sellers of volatility, however, have to be a lot more careful. One mistake could be the last one."

---

## 3. Specific numeric techniques for measuring "cheap" vs. "expensive"

Chapter 39 ("Volatility Trading Techniques") lays out five distinct methods traders use, ranked by the author's own preference, plus concrete numeric thresholds. This is the section to mine hardest for a literal filter.

### Five methods for determining if IV is "out of line" (verbatim list from the text)
> "So the approaches are:
> 1. Compare implied volatility to its own past levels (percentile approach).
> 2. Compare implied volatility to historical volatility.
> 3. Interpret the chart of volatility.
> In addition, we will examine two lesser-used methods: comparing current levels of historical volatility to past measures of historical volatility, and finally, using only a probability calculator and trading the situation that has the best probabilities of success."

### Method 1 — The Percentile Approach (author's preferred method)
> "In this author's opinion, there is much merit in the percentile approach."

Concrete numeric rules given:
- Lookback window: "about 255 trading days in a year." A two-year history = 510 daily readings. **"This author typically uses 600 days of implied volatility history for the purpose of determining percentiles, but a case could be made for other lengths of time."**
- Threshold for actionable cheapness/expensiveness: **"Those with readings in the 10th percentile or less, say, would be considered 'cheap'; those in the 90th percentile or higher would be considered expensive."**
- Range-width sanity check (rule of thumb): **"If the option rises from the current (low) percentile reading to the 50th percentile in a month, will the increase in implied volatility be equal to or greater than the time decay over that period? Alternatively stated, with all other things being equal, will the option be trading at the same or a greater price in a month, if implied volatility rises to the 50th percentile at the end of that time? If so, then the width of the range of implied volatilities is great enough to produce the desired results."**
- The percentile distribution is dynamic, not static — during a broad market selloff many names simultaneously show 90th-percentile+ IV; during calm periods (he cites 1993 and summer 2001) many simultaneously sit at 10th-percentile-or-lower.
- Asymmetric confidence: buying volatility at extreme-low percentiles is more reliably valid than selling at extreme-high percentiles, because the public being "wrong" at turning points supports fading depressed IV, but expensive IV may reflect real (if non-public) information: **"The converse may not necessarily be true: that we would want to be short volatility when everyone else has pushed it up to extremely high levels. The caveat in that case is that someone may have inside information that justifies expensive options."**

### Method 2 — Comparing Implied to Historical Volatility
Rated inferior to the percentile method by the author but still describes a concrete rule set if used:
- **"One should ensure that implied volatility is significantly different from all of the pertinent historical volatilities. For example, one might require that implied volatility is less than 80% of each of the 10-, 20-, 50-, and 100-day historical volatility calculations."** (i.e., IV < 0.8 × HV across all four lookback windows, for a buy signal)
- Must still be cross-checked against the IV percentile (method 1) — don't buy IV that's cheap-relative-to-HV but still in a high percentile of its own history, and don't sell IV that's expensive-relative-to-HV but still in a low percentile of its own history.
- Convergence-magnitude check: require that if IV converges to (the lowest of) the historicals within a defined horizon (e.g., a month), the position would actually be profitable — because a "wide" *relative* gap (e.g., IV=10%, HV=13%, a 30% relative difference) can still be a trivially small *absolute* gap (3 points) insufficient to produce profit after costs.
- Named weakness: no guarantee of timely convergence ("Historical and implied volatility often remain fairly far apart for weeks at a time"), and convergence doesn't guarantee profit if both revert toward a lower level than either started (his example: IV 40%, HV 60%, but both converge down to 30%).

### Method 3 — Reading the Volatility Chart (trend-reversal confirmation, not absolute level)
Rather than a level-based percentile trigger, this waits for a *directional reversal* in the IV trend before acting:
> "This is a valid approach in the use of many indicators, particularly sentiment indicators, that can go to extreme levels. By waiting for the trend to change, the user is not subjecting himself to buying into the midst of a downtrend in volatility, nor selling into the midst of a steep uptrend in volatility."
- Applies especially to sellers avoiding "stepping into the vortex of massive option buying" (possible informed buying), and to buyers avoiding "foolhardy" purchases into a still-declining IV trend, "just as it is usually foolhardy to buy a stock that is in a severe downtrend."
- Cross-reference given: same logic as the equity-only put/call ratio during the 1990s bull market, where a static "buy when put/call > 50" rule got run over once the regime shifted and ratios reached 70–75; a reversal-based trigger would have adapted.

### Method 4 — Comparing Historical Volatility to Its Own Past (weakest method)
Explicitly downgraded: "generally an inferior method because such a comparison doesn't tell us anything about the option prices." Backward-looking only, no IV input at all, and it assumes mean-reversion in a stock's volatility regime that frequently doesn't hold — illustrated with Rambus (RMBS), whose historical volatility regime shifted permanently upward (from a 50%–110% range to consistently 120%+) after a structural change in the stock's behavior in 2000; naive reversion-based selling would have been "a very expensive mistake." Best used only as a supplementary cross-check, not a primary signal.

### Method 5 — Probability calculator as final filter (used regardless of which of the above screens is used)
- Concrete threshold from a worked example: **"an attractive volatility buying situation should have probabilities in excess of 80% of the underlying ever exceeding the break-even point, while an attractive volatility selling situation should have probabilities of less than 25% of ever trading at prices that would cause losses."**
- Elsewhere (Ch 38): "many naked option sellers try to sell options that have only probabilities of 15% or less of potentially becoming troublesome" — a slightly stricter alternate threshold cited for naked selling specifically.
- Use the "ever" probability (probability of touching the breakeven/target at *any point* during the option's life), not the simpler "endpoint" probability (probability of being past that price only *at expiration*). Endpoint-only probability materially understates risk for sellers: worked OEX example shows endpoint P(worry-free) = 81%, but true P(worry-free, i.e., never even dips below the strike intraperiod) = 67%, with the missing 14% being scenarios where the position dipped through the strike and had to be defended/adjusted before recovering by expiration.
- Best practice: use a fat-tail-adjusted Monte Carlo distribution rather than pure lognormal for this calculation (see Section 4).
- Volatility input should be deliberately biased conservative depending on directionality of exposure: **option buyers should use the lowest of the available historical-volatility measures (10/20/50/100-day) as the model input; option sellers (negative-vega positions) should use the highest.** ("Since one is buying options in this strategy he should use the lowest of the above [readings]... he can feel fairly certain that he has not overstated the possibilities of success... Similarly, if one is considering the sale of options or is taking a position with a negative vega... he should use the highest historical volatility when making his probability projections.")
- When a stock's recent behavior has been erratic/unrepresentative for a long stretch, compute historicals (20/50/100-day) over a long lookback (he suggests ~1,000 trading days, "although... something like 600 trading days would be better" is also floated) and take the **median** of the resulting distribution of historical-volatility readings as the "true" long-run volatility estimate, rather than trusting the current/recent reading. Worked example: current 100-day HV = 80% (a "very high reading"), but the median 100-day HV computed across ~901 rolling 100-day windows over the last 1,000 days was 48% — a large, decision-relevant gap.

### Check the fundamentals before trading either extreme
Regardless of method used to flag a mispricing, always check news before acting:
> "Once these mispriced options have been found, it is always imperative to check the news to see if there is some fundamental reason behind it. For example, if the options are extremely cheap and one then checks the news stories and finds that the underlying stock has been the beneficiary of an all-cash tender offer, he would not buy those options... Similarly, if the options appear to be very expensive, and one checks the news and finds that the underlying has a product up for review before a governmental agency (FDA, for example), then the options should not be sold..."

### Stock-price-history / histogram cross-check (before finalizing a straddle/strangle buy)
Even after IV and probability screens pass, McMillan adds a final empirical sanity check: has the underlying's *actual price history* shown it capable of the required percentage move over the relevant time window?
> "Has this stock been able to make moves of [X%] over [N] months, in the past?"
He recommends building a **histogram** of the stock's historical N-month percentage moves and checking: (a) does the stock's move distribution reliably clear the required breakeven distance (not just barely, and not only through one non-repeatable historical outlier like a single earnings gap or a mania-era spike), and (b) is there reasonable continuity of outcomes across the distribution rather than one dominant cluster right at the breakeven line (a distribution clustered tightly around ±1× the required move, with little beyond it, predicts a low win rate even though the "50%+ of the time it clears the level" number might look superficially fine).

---

## 4. Distribution-of-prices content (Ch 38) — practical trading conclusions

### Central finding: stock prices are NOT lognormally/normally distributed the way most models assume
> "Statistics are used to estimate stock price movement... in many areas of financial analysis... Unfortunately, almost all of these applications are wrong! Perhaps wrong is too strong a word, but almost all estimates of stock price movement are overly conservative."

Baseline math for a normal/lognormal model: stocks stay within 3 standard deviations 99.74% of the time; probability of a 3-sigma move is only 0.13% (so out of 2,500 optionable stocks, only ~3 would be expected to move 3 sigma on a given day); probability of an 8-sigma move under lognormal assumptions is so tiny it should occur roughly once in the history of the universe.

Reality, demonstrated with multiple actual studies:
- **April 5, 1999** (a "somewhat volatile" day, Dow +174): individual stock moves up to **31.2 standard deviations** (Aspect Development), with several other names moving 8+ sigma same day.
- **July 25, 1993** (the single lowest-volatility day on record at the time by VIX): still had **12 stocks** move more than 4 standard deviations, including large, well-known names (Adaptec, Bethlehem Steel, US Steel, Chiquita, Novell).
- **October 8, 1998** (market-bottom day after the Russian-debt-crisis selloff): 33 stocks moved 4+ sigma; Utility Index fell ~5.5 sigma; American Power Conversion rose over 5 sigma.
- **30-day rolling study, Oct 22–Dec 7, 1999**, across 2,888 optionable stocks (a period that itself started at a "middle of the range" VIX ≈ 23, not an extreme regime): **648 stocks (22%) had a move of 3+ standard deviations at some point in the 30 days**, including 65 that moved more than 6 sigma.
- Repeated over a calmer window (June 1–July 18, 1999): still ~250/2,500 stocks (10%) exceeded 3 sigma.
- Repeated over the least volatile month in the whole database (July 1993): still ~10% of the (smaller) sample exceeded 3 sigma.
- Big-picture aggregate study (Sept 1993–Apr 2000, ~2.5 million stock-trading-day observations, 30-day windows): actual distribution shows **"fat tails"** — more than 12× the lognormal-predicted frequency of ≥4-sigma down moves (~2,500 actual occurrences vs. ~200 predicted), and a comparable excess on the upside (~2,000 actual ≥4-sigma up moves vs. far fewer predicted).
- Index-level extremes cited: the Dow's >550-point drop in October 1997 was about a 7-standard-deviation move; the Crash of '87 was roughly a **16-standard-deviation move** — which a cited Berkeley professor characterized as something that "should occur about once in ten times the life of our current universe" under lognormal math.

### Why this matters mechanically, not just as trivia
Crucially, McMillan notes this fat-tail finding is **not** an artifact of using stale/understated volatility inputs — the standard-deviation count in each study used the *current* (contemporary) 20-day historical volatility on each measurement day, so already-elevated-volatility periods required proportionally larger dollar moves to register as "large" sigma events, and the excess still showed up. He also flags the inflection-point detail: the normal distribution over-predicts frequency between roughly -2.5 and +0.5 standard deviations (a bullish-period-skewed dataset) — real-world center-of-distribution behavior can drift with regime, even while tail-fatness is persistent.

### Practical strategy conclusions McMillan draws directly from this (his own words / clearly stated implications)
1. **"Volatility buyer's rule"**: stocks move farther and faster (with gap risk) than conventional models suggest, so any option-selling strategy — including ones marketed as "conservative" like covered call writing or naked put selling — carries more real tail risk than lognormal-based probability tools indicate. "You should certainly think twice about selling stock options in a potentially volatile market (or any market, for that matter, since these large moves are not by any means limited to the volatile market periods)."
2. Covered call writing specifically: because of these large-move statistics, covered writers frequently either "give up large upside profits" (stock runs past the call strike) or "suffer large downside losses" (stock crashes through) — the strategy's real risk/reward is worse than its "conservative" reputation implies.
3. Vertical (limited-profit) spreads similarly can't capture the frequent large moves: "a vertical spread limits profits so that one can't participate in these relatively frequent large stock moves when they occur."
4. If selling options anyway, an option seller should (a) size/model with materially larger assumed moves than lognormal implies, (b) sell only when options are actually expensive in IV terms (so a subsequent IV decline works in the seller's favor as a cushion), and (c) **prefer index options (or select futures) over individual stocks** for any short-volatility strategy, "because they are statistically much less volatile than stocks." ("Hard as it is to believe, futures are less volatile than stocks, although the leverage available in futures can make them a riskier investment overall.")
5. Directly stated expected-return conclusions from fat-tail-adjusted Monte Carlo studies (bulleted verbatim from text):
   - "A bull spread is an inferior strategy when the options are fairly priced, no matter which distribution is assumed."
   - "While covered writing might seem superior to stock ownership under the lognormal distribution, the two are about equal under a fat tail distribution."
   - "Most startling, though, is the fact that option buying strategies fare much, much better under a fat tail distribution than a lognormal one... A limited-risk investment with unlimited profit potential can be expected to perform very well if the fat tails are allowed for."
   - Direct rebuttal of conventional broker advice: "Using the lognormal distribution more or less represents the conventional wisdom regarding option strategies — the one that many brokers promote: 'Don't buy options, don't mess with spreads, either buy stocks or do covered call writes.' The fat tail distribution column stands much of that advice on its head. In real life..., strategies with limited profit potential and unlimited or large risk potential are inferior strategies."
6. For setting realistic profit targets/stops with probability tools: use the "ever" (path-dependent, any-time-during-life) probability rather than the simpler endpoint (expiration-only) probability, and where possible use a fat-tail-adjusted Monte Carlo simulation rather than pure lognormal, since it more realistically prices in the frequency of big continuation or reversal moves that a stop/target design needs to account for. Also — a subtlety relevant to sizing stops — out-of-the-money options, especially in commodities/futures showing volatility skew, are "probably underpriced" by lognormal-based models relative to true tail risk, though "often not enough to make any real difference" in practice.

---

## 5. Caveats — what McMillan says is commonly misunderstood about volatility

1. **"Time value premium" is a misnomer.** The excess-value portion of an option's price is driven far more by stock price movement (delta) and volatility (vega) than by the passage of time (theta), at least outside the very final days before expiration. Worked example: a call trading with 6 points of "time value" has theta of only $0.06/day (delta 0.60, vega 0.13) — the everyday drivers of that 6 points are stock movement and IV changes, not decay, until expiration is truly close. "Many (perhaps novice) option traders seem to think of time as the main antagonist to an option buyer" — this is presented as a misconception. Only once very little time remains does theta dominate (his 1-week-to-expiry example shows theta jumping to -0.51/day while vega collapses to 0.044).
2. **IV is not a reliable predictor of subsequent realized volatility**, despite feeling intuitively like it should converge with historical volatility — see Section 1 above. Convergence isn't guaranteed in a useful timeframe, and even when IV and HV do converge, there's no guarantee of profitability (they could converge downward, hurting a long-volatility position).
3. **Vega is surprisingly flat/constant across a wide range of IV levels** for a given option, and it "begins to decline only if implied volatility gets exceedingly high" — traders don't need to worry about a meaningful "vega of vega" effect except at IV extremes.
4. **At very high IV, an option's delta stops behaving like the trader expects** — the price/stock curve becomes nearly a straight line, so delta barely changes across a huge range of stock prices, and an out-of-the-money option with extremely high IV can carry a delta of 0.70+ "and can be expected to mirror stock price movements more closely than one might think." This also means a *drop* in IV, even with the stock rising, can leave a long-option position with a net loss (his example: stock rises 9 points, option holder makes nothing, because IV fell from 170% to 140% simultaneously).
5. **Delta-neutral ratios are not fixed — they shift with IV**, so intuition/estimation ("everybody knows ATM call delta is a bit higher than ATM put delta, so 3 puts to 2 calls is neutral") can be badly wrong at different volatility regimes; his worked example shows the correct neutral ratio moving from 3-to-2 (at IV 40%) to 2-to-1 (at IV 110%) for otherwise identical strikes/expirations. "One can't necessarily rely on his intuition; it is always best to check with a model."
6. **Debit vertical spreads (bull call spreads, bear put spreads) do NOT behave like simplified versions of outright long options with respect to volatility** — this is called out explicitly as commonly misunderstood, with the vega sign flipping relative to the outright purchase (Section 2 above has the full quote/example). This is flagged as a trap specifically for traders who choose a spread believing options are "too expensive," not realizing the spread strategy itself is now *hurt* by further IV expansion.
7. **Calendar spreads move opposite to verticals** with respect to IV (long-vega, not short-vega) — a trader unaware of this can misjudge a "cheap-looking" calendar established during an unusually high-IV period (e.g., ahead of an anticipated event), not realizing the position's apparent value depends on IV *staying* elevated, not just on price pinning the strike.
8. **A sudden spike in option volume or IV is frequently informationally meaningful, not just noise** — it is explicitly framed as a common trap for volatility sellers who see "expensive" options purely as a statistical mispricing to fade, without checking whether informed/insider-driven buying (ahead of a takeover, earnings surprise, FDA decision, etc.) might explain and justify the price. The chapter gives specific behavioral tells (near-term/ATM volume concentration, market-makers buying stock to hedge negative delta, illiquid options where IV explodes without much printed volume because market-makers keep raising offers rather than selling size) to help distinguish informed-driven expensive options from benign/statistical mispricings.
9. **Endpoint probability materially understates real risk for a position held to expiration but subject to interim adjustment decisions** — using only "probability of being past the strike at expiration" ignores the very real, and separately quantifiable, chance of touching/breaching the strike mid-life and needing a defensive adjustment (a 14-percentage-point gap in his OEX example between endpoint and "ever" probabilities).
10. **Comparing historical volatility only to its own past (Method 4, Section 3) tacitly assumes a stock's volatility "regime" is stable/mean-reverting, which is often false** — the RMBS case study shows a stock whose historical-volatility range permanently shifted upward following a structural change in its trading behavior; naive reversion-based volatility-selling in that situation would have been "a very expensive mistake."
11. **Probability-calculator results (and "expected return" figures generally) should not be trusted as gospel** — they are highly sensitive to the volatility estimate fed in (itself unknowable in advance) and to the assumed constancy of that volatility and the assumed distribution shape (lognormal vs. fat-tailed). "Many investors accept these 'returns' on blind faith, figuring that if they're generated by a computer, they must be correct. In reality, they may not be representative, even for comparisons."

