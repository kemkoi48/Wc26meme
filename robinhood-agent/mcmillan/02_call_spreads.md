# McMillan Notes — Call Spread Strategies (Chapters 7–14)

Source: *Options as a Strategic Investment*, 5th ed., Lawrence McMillan. Extracted verbatim/close-paraphrase from OCR text files `ch_013.txt` through `ch_017.txt`. All quotes below are from the actual text as read; no outside/training-data knowledge was used to fill gaps.

---

## Chapter 7: Bull Spreads Using Call Options

### General spread mechanics (applies to all spreads in these chapters)
- **Vertical spread**: same expiration, different strikes. **Horizontal (calendar) spread**: same strike, different expirations. **Diagonal spread**: different strikes AND different expirations.
- "The short call in a spread is considered covered, for margin purposes, only if the long call has an expiration date equal to or longer than the short call."
- All-opening spread transactions must be done in a margin account, "normally $2,000" minimum equity. A spread can be done in a cash account only if one leg is a closing transaction (e.g., rolling a covered write).
- Spread execution price is NOT the difference between last-sale prices — you must use bid/ask. McMillan's own example: Oct 30 call bid 3.90/ask 4.10 (last 4.00); Oct 35 call bid 1.95/ask 2.00 (last 2.00) — spread appears to be a 2-point debit on last sale but actually costs 2.15 at market (pay the ask on the long, receive the bid on the short).
- "It is generally advisable to spread at least 5 options at a time" to reduce the percentage impact of commissions.
- Legging into or out of spreads is generally discouraged as "a poor idea" given modern market liquidity — enter/exit as a single spread order.

### Strategy: Bull Spread (Call Vertical)
**1. Construction**: Buy a call at a lower strike, sell a call at a higher strike, same expiration date, same number of contracts (1:1). Always a **debit** transaction with calls (lower-strike call always costs more than higher-strike call at same expiration).

Example used throughout: XYZ at 32; buy Oct 30 call at 3, sell Oct 35 call at 1 → net debit 2.

**2. Market outlook required**: Bullish but "not overly so" — moderately bullish. McMillan: "the strategist establishing the bull spread is bullish, but not overly so." If "rampantly bullish," he says the investor should just buy the call outright instead.

**3. Formulas (quoted near-verbatim)**:
- Break-even point = Lower striking price + Net debit of spread
- Maximum profit potential = Higher striking price − Lower striking price − Net debit of spread
- In the example: break-even = 30 + 2 = 32; max profit = 35 − 30 − 2 = 3 points.
- Table 7-2 rule of thumb across time/movement: for a stock that declines or stays flat, the bull spread wins in all timeframes (1 week, 1 month, at expiration). For a moderate advance, the bull spread wins at expiration but the outright call purchase wins over 1 week/1 month. For a substantial advance, the outright purchase wins in all timeframes.

**4. Risk/reward — DEFINED risk**:
- Max loss = the net debit paid, realized if stock is anywhere below the lower strike at expiration.
- Max gain = difference between strikes minus net debit, realized if stock is anywhere above the higher strike at expiration.
- Risk can never exceed net investment. "A bull spread requires a smaller dollar investment and therefore has a smaller maximum dollar loss potential than does an outright call purchase of a similar call."

**5. Caveats/pitfalls McMillan states explicitly**:
- The spread "will not widen out to its maximum profit potential right away" — it needs time to work even if the stock moves favorably. "For this reason, bull spreads are not for [short-term] traders unless the options involved are very short term in nature." On a 1-day or 1-month quick rally, an outright call purchase beats the bull spread.
- Three "degrees of aggressiveness":
  - **Aggressive** (most common): stock well below the higher strike at entry — low cost, high % return potential.
  - **Extremely aggressive** (out-of-the-money spread, both strikes above stock): "usually quite deceptive in nature... the spreader could realize a 100% loss of his investment even if the underlying stock advances moderately." McMillan: "It is not recommended that such a strategy be pursued with more than a very small percentage of one's speculative funds."
  - **Least aggressive** (in-the-money spread, both strikes below stock): smaller max profit but large probability of achieving it; larger commission drag since options are more expensive — "should therefore be figured into one's profit calculations."
- Ranking bull spreads by raw max-profit-percentage is a trap: "Such a ranking will always give the most weight to deeply out-of-the-money spreads, which can rarely achieve their maximum profit potential."
- Watch time value premium on the short call as stock rises — close if premium disappears (assignment risk); satisfy assignment by exercising the long leg if needed, but liquidating is cheaper than exercising due to stock commissions.
- Net max profit point is technically exactly at the higher strike (not above it) because commissions to liquidate rise with higher call prices.
- Do NOT "leg out" of a profitable long side hoping for a decline to also profit the short side — "The risk is too great."
- Only true way to lock in gains mid-life without giving up more upside is to buy the accompanying put bear spread (covered in a different chapter, Ch. 23, not in these files).

**6. Capital/margin size**: Requires a margin account with the firm's minimum equity (McMillan cites "normally $2,000" account minimum, separate from the spread's own debit cost). The spread's own capital requirement is just the net debit × number of contracts (e.g., $200/spread in his example, ×10 spreads = $2,000 debit before commissions). **This is a defined-risk, debit-paid-in-full strategy — no undefined/naked risk.** For a $100–500 account: a single low-cost aggressive or extremely-aggressive bull spread (e.g., a $0.50–$2 debit per contract) could fit, but the broker's overall margin-account minimum equity (McMillan says "normally $2,000") may itself be an obstacle at very small account sizes — this is a real constraint the text flags, not one this summary invents.

**Other uses McMillan describes**: rolling down into a bull spread to lower a stock owner's breakeven (detailed example: stock bought at 48, now at 42, buying 1 Oct 40 call + selling 2 Oct 45 calls for even money lowers breakeven from 48 to 44); using a deeply in-the-money call with little/no time premium as a "substitute for stock" purchase, making the bull spread a lower-capital substitute for covered writing (same profit/breakeven, smaller max loss, plus interest income on the freed-up cash).

---

## Chapter 8: Bear Spreads Using Call Options

### Strategy: Bear Spread (Call Vertical)
**1. Construction**: Buy a call at a higher strike, sell a call at a lower strike, same expiration, 1:1 ratio. Always a **credit** transaction with calls. "It should be pointed out that most bearish strategies that can be established with call options may be more advantageously constructed using put options."

Example: XYZ at 32; buy Oct 35 call at 1, sell Oct 30 call at 3 → net credit 2.

**2. Market outlook required**: Bearish — "the strategist is hoping that the stock will drop in price and that both options will expire worthless."

**3. Formulas (quoted near-verbatim)**:
- Maximum profit potential = Net credit received.
- Break-even point = Lower striking price + Amount of credit.
- Maximum risk = (Difference in striking prices − Credit received) + Commissions; this equals the collateral/investment required.
- Example: credit = 2; breakeven = 30 + 2 = 32; max risk = (5 − 2) = 3 points plus commissions.

**4. Risk/reward — DEFINED risk (but margined as a credit spread, not a cash outlay)**:
- Max profit = net credit, realized if stock is anywhere below the lower strike at expiration (both calls expire worthless).
- Max loss = difference in strikes minus credit, realized if stock is anywhere above the higher strike at expiration.
- "Since this spread involves a call that is not 'covered' by a long call with a striking price equal to or lower than that of the short call, some brokerage firms may require a higher maintenance requirement per spread than would be required for a bull spread."
- It's a credit spread: "the investor does not really 'spend' any dollars to establish the spread. The investment is really a reduction in the buying power of the customer's margin account" — still requires margin account minimum equity.

**5. Caveats/pitfalls**:
- Large-credit bear spreads (stock well above the lower strike at entry) are the *aggressive* version — need a big downward move, low probability of hitting max profit, AND are dangerous for early assignment because "the time value premium in the call will be small to begin with." McMillan states this is generally suboptimal: "selling a call that has mostly intrinsic value and little time value premium... and buying a call that is nearly all time value. This is just the opposite of what the option strategist should be attempting to do... the large credit bear spread is not an optimum strategy."
- Small-credit bear spreads (stock already below the lower strike at entry) are less aggressive, realize max profit even if stock stays flat or rises slightly (as long as it stays below the lower strike), and are the philosophically preferred setup ("sell time and buy intrinsic value").
- Bear spreads don't collapse to max profit immediately even on a quick down move, similar to bull spread lag.
- Follow-up: must watch for early assignment on the short (in-the-money) call — close the spread if the short leg loses its time premium, regardless of time to expiration, to avoid stock-assignment commission costs.
- Explicit editorial note: "The bear spread using calls may not be the optimum type of bearish spread that is available; a bear spread using put options may be."

**6. Capital/margin size**: Requires a margin account (credit spread — reduces buying power rather than requiring cash outlay), plus the account's minimum equity requirement. Max dollar risk is defined and modest per spread (e.g., $300 in the worked example for a 5-point-wide spread). Fits a small account on a per-spread-risk basis but needs a margin account approved for spreads.

---

## Chapter 9: Calendar Spreads

### Strategy: Neutral Calendar Spread (Time/Horizontal Spread)
**1. Construction**: Sell a near-term call, buy a longer-term call, same strike price. Established at (or near) the current stock price (at-the-money) for the *neutral* version. Always a debit (the longer-dated option costs more).

Example: XYZ at 50; sell April 50 call (5), buy July 50 call (8) → debit 3.

**2. Market outlook required**: Neutral. "The neutral philosophy for using calendar spreads is that time will erode the value of the near-term option at a faster rate than it will the far-term option." The strategist "is interested in selling time and not in predicting the direction of the underlying stock." Ideally close the whole spread by near-term expiration.

**3. Formulas / numeric detail given**:
- No closed-form breakeven formula is given (unlike vertical spreads) because the long leg still carries time value at near-term expiration — McMillan instead illustrates with a full table (Table 9-1) and says the profit range in his example is roughly 46 to 55 stock price at near-term expiration, versus a 50 strike, on a 3-point net debit.
- "When a call has less than 8 weeks of life, the rate of decay of its time value premium increases substantially with respect to the longer-term options on the same stock" — this is why the position is put on/managed close to near-term expiration.
- Effect of volatility: "As volatility increases, the spread widens; as volatility contracts, the spread shrinks... buying a calendar spread is an antivolatility strategy." Caveat: a spread that "looks especially attractive" on a volatile stock can be misleading two ways — greater chance of moving out of the profit zone, and if the stock does stabilize, "the spread will lose value because of the decrease in volatility. That loss may be greater than the gain from time decay!"

**4. Risk/reward — DEFINED risk**:
- Max loss = the initial net debit plus commissions (bounded — "the spread between two calls at the same strike cannot shrink to less than zero").
- Profit is realized within a range around the strike at near-term expiration; loss (but not full max loss) occurs well outside that range even at near-term expiration, since the long call retains some time value.
- No formula is given for max profit at near-term expiration in this section (it's model/curve-dependent, illustrated via Table 9-1, not formulaic like the vertical spreads).

**5. Caveats/pitfalls**:
- "'Legging' out of a spread is highly risky and is not recommended" — close as a single order.
- Must close before the near-term short call trades at parity, to avoid assignment.
- Three downside defensive choices identified if stock breaks down: (a) do nothing, hold long call hoping for recovery (McMillan's preferred, "easiest and most conservative"); (b) sell the long call to lock in some recovery value; (c) sell more short calls against the long ("naked call") — McMillan explicitly warns this "requires that one have enough collateral... often an amount substantially in excess of the original debit" and "if the underlying stock should reverse... the short side of the spread is naked and could produce substantial losses. The risk assumed by such a follow-up violates the initial neutral premise of the spread, and should therefore be avoided."
- On an early upside breakout, "doing nothing is often the best course of action" rather than rushing to close (paying two commissions on relatively expensive options). A described aggressive upside hedge (covering, i.e. adding short calls) is called "extremely aggressive and illogical for the neutral strategist."
- Suggests using mental stop-out points as expiration nears and profits have accrued, narrowing action points as time passes (paralleling ratio-write management).

### Strategy: Bullish Calendar Spread
**1. Construction**: Same as neutral calendar (sell near-term call, buy longer-term call, same strike) but established **out-of-the-money** — stock some distance *below* the strike.

Example: XYZ at 45; sell April 50 call at 1, buy July 50 call at 1.50 → debit 0.50.

**2. Market outlook required**: Two-stage bullish bet — first, the near-term call should expire worthless (stock stays below strike through near-term expiration); second, the stock must then rally above the strike before the long-dated call expires. "This strategy offers a small probability of making a large profit."

**3. Numeric rules McMillan gives explicitly** (his 3 stated criteria):
1. "Select underlying stocks that are volatile enough to move above the striking price within the allotted time." He warns that cheap-looking spreads on nonvolatile stocks needing a 20% move in a few months are "not worthwhile."
2. "Do not use options more than one striking price above the current market." Example: if XYZ is 26, use the 30 strike, not the 35.
3. "Do not invest a large percentage of available trading capital in bullish calendar spreads."

**4. Risk/reward — DEFINED risk**:
- Max loss = initial (small) debit, "100% of the initial investment" if the stock stays depressed and both calls end worthless — but the dollar amount is small (his example: 50 cents/spread).
- Upside profit potential is large and effectively open (the long call, once acquired "for free" or near-free, can appreciate substantially) but is not literally unlimited within the position's remaining life since the long call has an expiration date.
- "One large profit can easily offset several losses, because the losses are small, dollarwise."

**5. Caveats/pitfalls**:
- "The bullish calendar spreader must never consider 'legging' out of the spread, or consider covering the short call at a loss and attempting to ride the long call. Either action could turn the initial small, limited loss into a disastrous loss."
- Only sanctioned pre-expiration follow-up: close the whole spread early if it has become profitable due to the stock moving up toward the strike and/or a rise in implied volatility.

### Using All Three Expiration Series (variant note, not a distinct named strategy)
- Selling near-term, buying long-term (e.g., sell April, buy October) leaves the option, once the near-term expires worthless, to sell an intermediate-term call (e.g., July) against the same long call — potentially making the *sum* of the two credits exceed the original debit, "a guaranteed profit" (cannot lose, provided no legging). Tradeoff: larger initial debit, more dollars initially at risk.
- Buying the longest-term call and selling only the intermediate-term against it is called out as "generally an inferior approach" — smallest debit but little profit potential until the intermediate expiration nears, leaving lots of time for the stock to wander.

**6. Capital/margin size (both calendar variants)**: Requires a margin account for spreads (multi-expiration debit spread). Capital needed = the net debit only (no naked options in the neutral/bullish calendar spread as described in this chapter — those come later, in Ch. 12's *ratio* calendar spread). Debits here are described as very small (McMillan's example: $50–$300 per spread), so this is one of the more plausible strategies for a $100–500 account, PROVIDED the broker allows multi-month debit spreads in a small margin account and the "several positions" diversification McMillan recommends is feasible at that size (may not be, with only $100–500 total).

---

## Chapter 10: The Butterfly Spread

### Strategy: Butterfly Spread (Call)
**1. Construction**: Three strikes, same expiration. Buy 1 call at the lowest strike, sell 2 calls at the middle strike, buy 1 call at the highest strike (strikes evenly spaced in the standard version). "A combination of both a bull spread and a bear spread."

Example: buy July 50 call (12), sell 2 July 60 calls (6 each = 12), buy July 70 call (3) → net debit $300 (i.e., $3/contract-equivalent).

**2. Market outlook required**: Neutral — "for the neutral strategist, one who thinks the underlying stock will not experience much of a net rise or decline by expiration."

**3. Formulas (quoted, valid for same-month expiration + evenly spaced strikes)**:
- Net investment = Net debit of the spread.
- Maximum profit = Distance between strikes − Net debit.
- Downside break-even = Lowest strike + Net debit.
- Upside break-even = Highest strike − Net debit.
- Worked: distance = 10, debit = 3 → Net investment $300; Max profit = 10 − 3 = $700; downside BE = 50+3 = 53; upside BE = 70−3 = 67.
- "Maximum amount of profit is realized at the striking price of the written calls" (the middle strike) — general rule McMillan flags as broadly useful across written-option spread types.
- In percentage terms his example returns: "loss limited to about 100% of capital invested and could make profits of nearly 133%."

**4. Risk/reward — fully DEFINED risk, both sides**:
- Max loss = net debit (both upside and downside), i.e., 100% of what's invested, capped.
- Max gain = distance between strikes − debit, realized only right at the middle strike at expiration.
- "In accordance with more lenient margin requirements passed in 2000, the investment required for a butterfly spread is equal to the net debit expended, which is the risk in the spread." (No margin beyond the debit paid — genuinely capital-light and capped-risk.)

**5. Caveats/pitfalls McMillan states explicitly**:
- Commission cost is a major, explicitly flagged drag: "it is costly in terms of commissions" — up to 4 commissions to open, "eight commissions might have to be paid to establish and liquidate the spread" round-trip.
- Trade-off between debit size and stock position at entry: the lowest-debit butterflies require the stock to already be off the middle strike, which forces the trader into an implicit bullish or bearish bias to hit max profit; staying neutral (stock near the middle strike at entry) means paying a somewhat larger debit.
- "The best butterfly spreads are generally found on the more expensive and/or more volatile stocks that have striking prices spaced 10 or 20 points apart." With 5-point-wide strikes on lower-priced stocks, "he is normally putting himself at a disadvantage unless the debit is extremely small" (an exception exists for higher-priced stocks with 5-point strikes).
- With uneven strike spacing (e.g., 45/50/60), the standard 1-2-1 butterfly becomes lopsided/non-neutral; to rebalance, McMillan shows constructing it as **2 bull spreads + 1 bear spread** in the ratio matching the strike gaps (his example: buy 2 of the near strike, sell 3 of the middle, buy 1 of the far strike) — note this raises the *margin requirement* substantially versus the risk actually taken: "the margin requirement would be $1,100, even though the risk is only $100," because the bear-spread leg still requires collateral for the strike-price difference even though excess equity, not new cash, can satisfy most of it.
- Assignment risk is on the short middle-strike calls; if that call goes to parity (e.g., pending ex-dividend), close rather than accept assignment — accepting assignment doesn't change butterfly's own defined risk but changes margin requirement (creates "a synthetic put — long calls, short stock") and adds stock commissions.
- "Legging" adjustment described as legitimate follow-up only in one specific case: if the stock has moved sharply to one side so that either the bull-spread portion or the bear-spread portion has nearly reached its own max profit, that portion can be closed near its max, converting the butterfly into a plain bull or bear spread — at a small, explicitly quantified increase in risk (his examples: 50 cents added risk in each direction) in exchange for a much wider profit zone if the stock reverses.

**6. Capital/margin size**: Very capital-light and clean for a small account — net debit only, capped downside at 100% of that debit, no naked legs in the standard 1-2-1 same-strike construction. McMillan's own numeric example is a $300 debit for 1 spread (i.e., $3/contract on 10-point-wide strikes) — that alone could eat 60–300% of a $100–500 account for just ONE spread, and commissions ("up to eight") would materially erode the edge at this size. The modified uneven-strike version explicitly requires MORE margin ($1,100 in his example) than the risk taken ($100) — a genuine trap for a small account that has to post collateral it doesn't have relative to actual risk.

---

## Chapter 11: Ratio Call Spreads

### Strategy: Ratio Call Spread (2:1 and other ratios)
**1. Construction**: Buy calls at a lower strike, sell a larger number of calls at a higher strike, same expiration. Most common is 2:1 (buy 1, sell 2), but 3:2, 3:1, etc. are discussed. Contains a naked (uncovered) written-call component beyond the covered bull-spread portion.

Example: XYZ at 44; buy 1 April 40 call (5), sell 2 April 45 calls (3 each = 6) → net credit 1.

**2. Market outlook required**: Neutral — max profit occurs with stock exactly at the written (higher) strike at expiration. "A ratio call spread is a neutral strategy."

**3. Formulas (quoted near-verbatim, 2:1 case)**:
- Points of maximum profit = Initial credit + Difference between strikes (or = Difference between strikes − Initial debit if established at a debit).
- Upside break-even point = Higher strike price + Points of maximum profit.
- Worked: credit 1 + 5 = 6 → max profit $600; upside BE = 45+6 = 51.

**General-ratio formulas (quoted)**:
- Points of maximum profit = Net credit + (Number of long calls × Difference in striking prices) [or = (Number of long calls × Difference in strikes) − Net debit].
- Upside break-even point = [Points of maximum profit ÷ Number of naked calls] + Higher striking price.

**Margin/collateral formula given explicitly**: "The requirement for the naked call is 20% of the stock price plus the call premium, less the out-of-the-money amount." Worked example: 20% of 44 = $880, + $300 call premium, − $100 (1 pt OTM) = $1,080 naked-call requirement; minus the $100 credit received = **$980 net requirement** for just ONE 2:1 spread contract-unit in his example. McMillan explicitly recommends: "it is recommended that the ratio spreader allow at least enough collateral to reach the upside break-even point" (i.e., size for a mark-to-market at the breakeven stock price, not just current prices).

- Ratio guidance: "It is not common to write in a ratio of greater than 4:1 because of the large increase in upside risk at such high ratios." Higher ratio → bigger credit / bigger downside profit if stock collapses, but pushes the upside breakeven closer in (more risk). Lower ratio → higher (safer) upside breakeven.

**4. Risk/reward — UNDEFINED (unlimited) risk on the upside**:
- Downside: "relatively small, limited downside risk... if the spread is established at an initial credit, there is no downside risk at all." Below the lower strike, profit/loss is flat/constant (both legs worthless) — his example nets a small profit ($100) even with stock collapsed, since it was a credit spread.
- Upside: "the greatest risk in a ratio call spread lies to the upside, where the loss may theoretically be unlimited" — this IS a margin/naked-option strategy with open-ended risk, explicitly flagged by McMillan.
- Compared to a ratio write (Table 11-2): ratio spread's downside risk is much smaller than a ratio write's (1 point vs. 40 points, in his comparative example) since you own a call rather than the stock, but upside risk is "unlimited" for both.

### Sub-strategy: "Delta Spread"
**3. Formula**: Neutral ratio = delta of long call ÷ delta of short call. Example: deltas .80 (April 40) / .50 (April 45) → ratio 1.6:1, expressed as buy 10 April 40 / sell 16 April 45 (or 5:8).
- **Screening rules McMillan states explicitly**: cap the ratio at "an absolute limit, such as 4:1"; eliminate short-side candidates priced under $0.50 (this naturally caps the ratio too); reject if the delta-neutral ratio computes to less than 1.2:1 (6:5); optionally cap total debit outlay, e.g., "not paying a debit of more than 1 point per long option."

**5. Caveats/pitfalls**:
- Reducing the ratio is the standard *upside* defense (buy more long calls to move toward 1:1/bull-spread), NOT rolling up as in ratio writing. McMillan gives an explicit break-even-cost formula for the added long calls: [Number of short calls × strike difference − total debit-to-date] ÷ number of naked calls remaining = price ceiling to pay for the next tranche of long calls to keep the position at breakeven-or-better if stock is above the higher strike at expiration. Worked example yields 11, then (in a partial-adjustment scenario) 13.
- Delta-neutral re-adjustment is available but explicitly cautioned: "should be careful not to overadjust, because the commission costs would become prohibitive."
- Downside follow-up (if entry debit was large): roll the whole spread down to lower strikes, similar to ratio-write rolling.
- Take profits early if stock nears the max-profit (higher) strike with time still left, or if a stock decline has made the short calls "nearly worthless" and the long call's remaining value is at risk of being wiped out by a further decline.

**6. Capital/margin size**: Requires margin for NAKED calls — his own worked example needed roughly $980–$1,080 of collateral for a single one-naked-call unit of a 2:1 spread, and recommends sizing collateral to the (potentially much higher) upside breakeven mark-to-market level. **This is explicitly flagged as impractical for a $100–500 account** — the naked-call margin alone on a single spread unit exceeds the entire stated account size in McMillan's own numbers, and "upside risk may theoretically be unlimited," meaning further adverse moves increase the requirement further. Not a fit for a very small account without deep discounting of size (e.g., cheap, low-priced underlyings), and even then the undefined-risk nature is a structural mismatch for limited capital.

---

## Chapter 12: Combining Calendar and Ratio Spreads

### Strategy: Ratio Calendar Spread (out-of-the-money / naked-call version)
**1. Construction**: Sell MORE near-term calls than the number of longer-term calls bought, same strike, out-of-the-money at entry (extends the bullish calendar spread by unbalancing the ratio). Example: buy 1 July 50 (1.50), sell 2 April 50 (1 each = 2) → net credit 0.50.

**2. Market outlook required**: Same two-stage bullish thesis as the bullish calendar spread — stock stays below the strike until near-term expiration (letting short calls expire worthless), then rallies before the long call expires. Because it's typically set up for a credit, "if the underlying stock never rallies above the strike, the strategist will still make money."

**3. Numeric rules given**:
- "Always set up the spread for a credit, commissions included. This will assure that a profit will be made even if the stock goes nowhere."
- "If the credit has to be generated by using an extremely large ratio — greater than 3 short calls to every long one — one should probably reject that choice, since the potential losses in an immediate rally would be large."
- Collateral requirement formula (explicit, matches the naked-call formula from Ch. 11): 20% of stock price + call premium − credit taken in, sized to the trader's chosen defensive/breakeven stock price, not the current price. Worked example: at hypothetical stock price 53, 20% of 53 = $1,060 + $350 call premium − $50 initial credit = **$1,360 collateral** for this single-unit example.
- The upside breakeven is explicitly "dynamic" (changes with time remaining) because the two legs expire at different dates — McMillan provides a worked table (Table 12-1) showing breakeven stock price rising from 45 (at 90 days out) to 53 (at near-term expiration) as time passes, using a pricing model.
- Rule-of-thumb follow-up trigger: "close the spread if the stock breaks out above technical resistance or if it breaks above the eventual break-even point at expiration" — in his example, close if XYZ rises above 53 at any point before April expiration.

**4. Risk/reward — UNDEFINED (naked) risk on the immediate-rally scenario**:
- If stock stays below the strike through near-term expiration: guaranteed small profit (the credit).
- If stock rallies AFTER the near-term calls expire worthless: "large profits will accrue" — effectively open-ended upside for the strategist (he now just owns long calls).
- If stock rallies BEFORE near-term expiration: "the ratio calendar spread is in danger of losing a large amount of money because of the naked calls, and defensive action must be taken" — this is explicitly an undefined-risk exposure requiring active monitoring, unlike the plain calendar spread.
- Table 12-2 (his own probability characterization, described as "not mathematically definitive" but illustrative): stock never rallies above strike → small profit, large probability; stock rallies above strike quickly → small loss IF defensive action taken, small probability; stock rallies after near-term expiry → large potential profit, small probability. Net characterized as having "a positive expected return."

**5. Caveats/pitfalls**: Same volatility/strike-selection criteria as the bullish calendar spread (Ch. 9) apply. Explicitly: "since naked calls are involved, the collateral requirements for participating in this strategy may be large." Described as "a viable strategy for the advanced investor" — McMillan's own characterization, not this summary's.

### Strategy: Delta-Neutral (In-the-Money) Ratio Calendar Spread
**1. Construction**: Same idea, but calls are IN-the-money and the neutral delta ratio comes out to LESS than 1:1 sold-to-bought — i.e., you end up buying MORE long-dated calls than near-term calls sold (e.g., his example: buy 8 April [longer]/sell 7 July... actually per text: buy the longer-dated in-the-money call in greater quantity, sell fewer near-term). Formula: neutral ratio = delta of short (near-term) call ÷ delta of long call. Worked: .7/.8 = .875:1 → sell 7, buy 8.

**4. Risk/reward — this variant is fully DEFINED risk, unlike the OTM/naked version**: "There is no risk to the upside as there is with the out-of-the-money calendar; the in-the-money calendar would make money [on a big upside gap]... There are no naked calls to margin with this strategy, making it attractive to many smaller investors. In the above example, one would need to pay for the entire debit of the position, but there would be no further requirements." Downside: "loss is limited to the amount of the initial debit of the spread." This is explicitly the small-investor-friendly variant per McMillan's own words.

**5. Caveats**: Follow-up to maintain strict delta-neutrality (shifting between the OTM/naked structure and the ITM/extra-long structure as the stock moves) is called out as often impractical for small positions: "if one had originally sold 5 and bought 3, he would be better to adhere to the follow-up strategy outlined earlier... The spread is not large enough to dictate adjusting via the delta-neutral ratios." Only large traders (his example: 500 sold/300 bought) have "enough profitability... to make several adjustments."

**6. Capital/margin size (Chapter 12 overall)**: The OTM/naked ratio calendar spread requires substantial naked-call collateral (explicitly "may be large," with a $1,360 single-unit example given) — **not suitable for a $100–500 account**, same as the Ch. 11 ratio spread. The ITM extra-long-calls variant is explicitly flagged by McMillan as needing only the net debit with "no further requirements" and being attractive to "smaller investors" — this is the one variant in this chapter that could plausibly fit a very small account, though the underlying ITM calls needed are more expensive (larger absolute debit) than OTM equivalents, so real dollar cost per spread must be checked against the $100–500 ceiling.

---

## Chapter 13: Reverse Spreads

### Strategy: Reverse Calendar Spread
**1. Construction**: Sell a LONGER-term call, buy a SHORTER-term call, same strike — the opposite of the normal calendar spread. Established for a credit.

Example: XYZ at 80; sell Dec 80 call (12), buy July 80 call (7) → net credit 5.

**2. Market outlook required**: Either the stock moves far away from the strike in either direction by near-term expiration, OR implied volatility shrinks. "Best to establish it when implied volatility is high and the underlying has a tendency to be volatile."

**3. Numeric detail given**: No closed-form breakeven formula stated; example only — a fall from 80 to 50 shrinks the spread from 5 to about 1 (4-point profit); a volatility decline alone (stock flat) can shrink it from 5 to about 4 (1-point profit). Graph description: profit occurs "if XYZ were to rise above 98 or fall below 70" at near-term expiration in his example (unchanged-volatility case); a bigger profit zone if IV also falls.

**4. Risk/reward**: 
- Max profit = the initial credit (achieved if both calls go to worthless / near-worthless on a big move away from the strike, or if IV craters).
- Risk: the text does not give an explicit max-loss dollar figure or formula for this strategy in the chapter (the risk sits in the SHORT longer-term call vs. the LONG shorter-term call — loss would occur if the stock sits near the strike and near-term option decays away while the longer-dated short retains value / IV rises). This is NOT spelled out with a formula in the source text — flagged here as a gap rather than invented.
- **Margin/undefined risk explicitly flagged by McMillan**: "The problem with this spread, for stock and index option traders, is that the call that is sold is considered to be naked. This is preposterous, of course, since the short-term call is a perfectly valid hedge until it expires. Yet the margin requirements remain onerous." He notes futures options traders get better margin treatment; stock/index traders do not.

**5. Caveats/pitfalls**: Explicitly called "an infrequently used strategy, at least for public customers trading stock or index options, because of the margin requirements."

**6. Capital/margin size**: Explicitly flagged by McMillan himself as margin-heavy/impractical for the ordinary public customer due to "onerous," naked-style margin treatment on the short long-dated call — **not suitable for a $100–500 account** per the text's own characterization.

### Strategy: Reverse Ratio Spread (Backspread)
**1. Construction**: Sell 1 call at a LOWER strike, buy MORE calls (his example 2, i.e., 2:1) at a HIGHER strike, same expiration — opposite of the ratio call spread in Ch. 11. "These spreads are generally established for credits. In fact, if the spread cannot be initiated at a credit, it is usually not attractive."

Example: buy 2 July 45 calls (1 each = 2), sell 1 July 40 call (4) → net credit 2.

**2. Market outlook required**: Wants a big move, doesn't much care which direction, but has an asymmetric payoff favoring a big UP move (unlimited upside, limited/defined downside). "The investor is bullish and is buying out-of-the-money calls but is simultaneously hedging himself by selling another call."

**3. Formulas / numeric rules**:
- Max downside profit = the initial credit received (if stock < lower strike at expiration, all calls worthless).
- Max loss occurs at expiration AT the strike of the purchased (higher) calls — a general rule McMillan restates: "With most spreads, the maximum loss is attained at expiration at the striking price of the purchased call. This is a true statement for backspreads." Worked: stock at exactly 45 → loss of $300 (his example).
- Upside break-even is computed by example (48 in his case) rather than a stated closed formula in this passage.
- Delta-neutral ratio formula (same method as Ch. 11): neutral ratio = delta of short (lower-strike) call ÷ delta of long (higher-strike) call. Worked: .80/.35 = 2.29:1 → sell 5, buy 11 (or sell 10, buy 23).

**4. Risk/reward — DEFINED risk (this is the key distinguishing feature vs. the ratio spread)**:
- Max loss is capped and occurs at the strike of the long calls at expiration (his example: $300).
- Upside profit potential is unlimited (more long calls than short).
- Downside profit is capped at the initial credit.
- Margin: "the spread portion is long the July 45 and short the July 40. This requires a $500 collateral requirement, because there are 5 points difference in the striking prices. The credit of $200 received for the entire spread can be applied against the initial requirement, so that the total requirement would be $300 plus commissions. There is no increase or decrease in this requirement, since there are no naked calls." — McMillan explicitly notes NO naked calls are involved (unlike the forward ratio spread), because there are more longs than shorts.

**5. Caveats/pitfalls**:
- Must watch for early exercise on the short (in-the-money) call.
- "The strategist would seek out volatile stocks for implementation of this strategy, because he would want as much potential movement as possible by the time the calls expire."
- Otherwise "there is little in the way of defensive follow-up action that needs to be implemented, since the risk is limited by the nature of the position."

**6. Capital/margin size**: DEFINED, bounded risk with a stated, modest collateral requirement in his worked example ($300 plus commissions for a $500-wide, 2:1 spread) — and explicitly NO naked-option component. This is one of the more plausible strategies in these chapters for a small account, capital-wise, though real-world strike widths and option prices would need to be checked against the $100–500 ceiling; McMillan's own numeric example ($300) alone would consume 60%+ of the top of that range for a single spread unit.

---

## Chapter 14: Diagonalizing a Spread

### General principle
"When one uses both different striking prices and different expiration dates in a spread, it is a diagonal spread... the long side must have a maturity equal to or longer than the maturity of the short side... any of these spreads can be diagonalized; one can replace the long call in any spread with one expiring at a later date." "In general, diagonalizing a spread in this manner makes it slightly more bearish at near-term [expiration]" in the sense that it trades away some upside profit for downside protection, because the longer-dated long leg retains value if the stock falls.

### Strategy: Diagonal Bull Spread
**1. Construction**: Buy a longer-term call at the lower strike, sell a near-term call at the higher strike (vs. same-month for a normal vertical bull spread).

Example: buy July 30 call (4) or Oct 30, sell April 35 call (1) → 3-point debit (vs. 2-point debit for the plain April/April vertical bull spread using the same strikes).

**3/4. Numeric comparison McMillan gives (Table 14-1)**: Vertical bull spread max profit $300 (3 pts) above 35 at April expiration, max loss $200 (2 pts, the debit) below 30. The diagonal version costs more upfront (3 vs 2 debit) but "lowers the probability of losing 2 points in the position" — its dollar loss between 27 and 32 at April expiration is smaller than the vertical spread's, and even below that range it doesn't go to a full/near-total loss until the stock is well under ~24 (vs. below 30 for the vertical spread). Above 35, the plain vertical spread produces the larger profit ($300 vs. $200-250 range) because the diagonal spread cost more to establish.
- Reinvestment feature: once the near-term short call expires (if stock ended between the two strikes, e.g. still at 32), the position can be converted into a normal vertical bull spread in the next expiration month by selling that month's higher-strike call — in his example this produces a net July bull spread costing only 2 points total (vs. 2.50 if set up as a plain July vertical from scratch on day one) — "the diagonalizing effect can prove beneficial if the writer is able to write against the same long call two times, or three times if he originally purchased the longest-term call."

**5. Caveats**: If the stock drops far enough (his example, to 20), "both spreads will experience nearly a total loss," so diagonalizing does not eliminate large-decline risk, just softens moderate-decline risk and trades away some upside.

### Strategy: Diagonal Bear Spread / "Owning a Call for Free"
**1. Construction**: Sell a near-term call at a LOWER strike, buy a longer-term call at a HIGHER strike (still a bear spread — lower strike sold, higher strike bought — but now diagonalized).

Example: XYZ at 32; sell April 30 call (3), buy July 35 call (1.50) → credit 1.50.

**3. Numeric rule / mechanism explicitly described**: If the near-term short call can be bought back for a profit that "covers the entire cost" of the long call, the trader ends up "owning [the long call] for free." Worked: if XYZ ≤ 31.50 at April expiration, the April 30 can be bought back for ≤1.50 — since it was sold for 3, that's a ≥1.50 profit, exactly covering the 1.50 cost of the July 35 → own the July 35 for free. If the stock later rallies above 35 (before July expiration), unlimited profit potential on the now-free call; if it never rallies, "he would make nothing from the overall trade" (but also lost nothing further).

**4. Risk/reward for the diagonal bear spread itself**: Profits if XYZ falls before near-term expiration (example: fall to 29 → +2 points). Risk is to the upside, "just as in a regular bear spread" — if stock advances a great deal, both options go to parity and the spread widens to the full strike difference (5 points in his example); loss = that width minus the initial credit (5 − 1.50 = 3.50 in his example). Diagonalizing here means "the spread will do slightly better to the downside... but it will do slightly worse to the upside if the underlying stock advances substantially" (paid more for the longer-dated long call than a same-month bear spread would have cost).

### Strategy: Diagonal Backspread
**1. Construction**: Sell 1 near-term call at a lower strike, buy MORE (his example: 2) longer-term calls at a higher strike, for roughly even money. Example: sell April 30 (3), buy 2 July 35 calls at 1.50 each (3 total) → even-money spread.

**4. Risk/reward**: If the near-term short expires worthless (stock below 30), "the spreader would own 2 July 35 calls for free." Even a partial profit on the short leg reduces the cost basis of the long calls. "The worst situation that could result would be for the underlying stock to rise very slightly by near-term expiration. If this happened, it might be possible to lose money on both sides of the spread" — but McMillan characterizes this as "a rather low-probability event" with "still... a limited loss." This is a strategy "favored by some professionals, because the short call reduces the risk of owning the longer-term calls if the underlying stock declines."

### General diagonal-spread rationale (chapter close)
"One would want to sell options with a short life remaining, so that the maximum benefit of the decay could be obtained. Correspondingly, the purchase of a longer-term call would mean that the buyer is not subjecting himself to a substantial loss in time value premium, at least over the first three months of ownership. A diagonal spread encompasses both of these features."

**6. Capital/margin size**: Diagonal bull and diagonal bear spreads are debit/credit-defined-risk vertical-style spreads with an extra time dimension — capital requirement is essentially the net debit (diagonal bull) or the margined credit-spread collateral (diagonal bear), similar in kind to Chapters 7–8's requirements, just somewhat larger due to the longer-dated leg's higher premium. The diagonal backspread, per the text, has more long calls than short and thus (by the same logic as the Ch. 13 backspread) should not require naked-option margin, though the chapter does not give an explicit collateral figure for it the way Ch. 13 did for the same-month backspread. None of the diagonal variations described here are flagged by McMillan as naked/undefined-risk in the way the ratio spread (Ch. 11) and reverse calendar spread (Ch. 13) explicitly were.

---

## Cross-cutting notes relevant to a small ($100–500) account

Strategies with **defined, capped risk** and no naked/margin-intensive component, per the text itself:
- Bull spread (Ch. 7) — debit-only, capped loss = debit paid.
- Bear spread (Ch. 8) — credit spread but capped loss, margin-account credit-spread collateral required.
- Neutral / bullish calendar spread (Ch. 9) — debit-only, no naked legs (McMillan's neutral downside-defense advice explicitly avoids adding naked shorts).
- Butterfly spread (Ch. 10) — debit-only, capped both sides, "investment required... is equal to the net debit expended" — but commission-heavy (up to 8 commissions) and the standard example debit ($300) alone would be large relative to a $100–500 account; uneven-strike butterfly variant needs disproportionate margin ($1,100 collateral for $100 risk in his example).
- Delta-neutral IN-the-money ratio calendar spread (Ch. 12) — explicitly "no naked calls to margin... attractive to many smaller investors," capped loss = debit.
- Reverse ratio spread / backspread (Ch. 13) — capped, defined max loss at the long strike, explicitly "no increase or decrease in [margin] requirement, since there are no naked calls."
- Diagonal bull/bear spreads and diagonal backspread (Ch. 14) — same defined-risk character as their non-diagonal counterparts, per the text.

Strategies explicitly flagged by McMillan himself as **margin-intensive / naked / undefined-risk**, and therefore a poor structural fit for $100–500 of capital:
- Ratio call spread (Ch. 11) — "the greatest risk... may theoretically be unlimited" to the upside; his own worked collateral example (~$980–$1,080) alone exceeds the entire stated account size.
- Ratio calendar spread, out-of-the-money/naked version (Ch. 12) — "collateral requirements... may be large" (his example ~$1,360).
- Reverse calendar spread (Ch. 13) — McMillan calls stock/index margin treatment on it "onerous," a naked-style requirement on the short long-dated call.

---

## Notes on file content completeness

All five files (ch_013 through ch_017) had substantial, complete chapter content with no thin or missing sections — each covered its named strategy or strategies in full, including worked numeric examples, tables, formulas, and explicit follow-up/caveat discussion. The reverse calendar spread section (Ch. 13) is the one place where the text does not give an explicit max-loss formula or dollar figure (unlike every other strategy in these chapters, which all get worked numeric examples of max loss) — this is noted above as a genuine gap in the source rather than filled in.
