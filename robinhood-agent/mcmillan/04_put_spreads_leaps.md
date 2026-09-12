# McMillan, *Options as a Strategic Investment* (5th ed.) — Notes
## Chapters 22–25: Basic Put Spreads, Combined Spreads, Ratio Put Spreads, LEAPS

Source files (OCR'd from epub, minor spacing artifacts left intact where quoted):
- `ch_023.txt` = Chapter 22, "Basic Put Spreads"
- `ch_024.txt` = Chapter 23, "Spreads Combining Calls and Puts"
- `ch_025.txt` = Chapter 24 (start), "Ratio Spreads Using Puts"
- `ch_026.txt` = Chapter 24 (continued) + Chapter 25 (start), "Long-Term Option Strategies" — **this file cuts off mid-sentence** partway into the "Advantages of Buying Cheap" section of Chapter 25; everything after that point (rest of Ch. 25) was not in the supplied text and is NOT covered below.

---

## Chapter 22: Basic Put Spreads

Opening framing from the text: "Put spreading strategies do not differ substantially in theory from their accompanying call spread strategies... However, because puts are more oriented toward downward stock movement than calls are, some bearish put spread strategies are superior to their equivalent bearish call spread strategies." The three simplest spread forms covered are the bull spread, the bear spread, and the calendar spread — all constructed with puts here.

### Bear Spread (Put Bear Spread)

**Construction:** Sell a put at a lower strike, buy a put at a higher strike (same expiration). Example given: Buy XYZ Jan 60 put, Sell XYZ Jan 50 put. "The put bear spread is a debit spread" — because a higher-strike put costs more than a lower-strike put.

**Market outlook:** Bearish — same profit shape as a call bear spread (bearish on the stock).

**Numeric example:** XYZ common 55; Jan 50 put = 2; Jan 60 put = 7. Buying the 60 put and selling the 50 put costs a 5-point debit.

**Formulas (quoted verbatim):**
- "Maximum risk = Initial debit"
- "Maximum profit = Difference between strikes - Initial debit"
- "Break-even price = Higher striking price — Initial debit"

In the example: max risk = 5, max profit = 10 − 5 = 5, breakeven = 60 − 5 = 55.

**Risk/reward:** Defined risk and defined reward. Max profit realized "anywhere below 50 at expiration"; max risk realized "anywhere above 60 at expiration." "The maximum risk is always equal to the initial debit required to establish the spread plus commissions."

**McMillan's stated advantages of the put bear spread over the call bear spread (his own reasoning, not paraphrase-diluted):**
1. Early-exercise risk: with a put bear spread you are selling an out-of-the-money option initially. "For the written put to be in-the-money, and thus in danger of being exercised, the spread would have to be [in-the-money]" — i.e., less early-assignment risk than the written ITM call typically involved in a call bear spread's set-up region.
2. Faster widening on a quick decline: "if the underlying stock drops quickly... the spread will normally widen quickly as well... put options tend to lose [time value premium quickly]." He contrasts this with call bear spreads: "Call bear spreads often do not produce a similar result on a short-term downward movement... this call may actually pick up time value premium as the stock falls close to the lower strike."

**Caveat on the credit-spread objection:** Some investors prefer the call bear spread because it's established for a credit (no cash outlay). McMillan calls this "a rather weak reason to avoid the superior put spread and should not be an overriding consideration." He notes the call bear spread's margin requirement reduces buying power by "an amount approximately equal to the debit required for a similar put bear spread" — i.e., there's no real capital-efficiency edge to the credit version except for accounts "near the minimum equity requirement to begin with."

**Capital/margin note:** "For most brokerage firms, the minimum equity requirement for spreads is $2,000." The put bear spread must be paid for in full (net debit) — no additional margin is described.

### Bull Spread (Put Bull Spread)

**Construction:** Buy a put at a lower strike, sell a put at a higher strike (same expiration) — a credit spread. Example: Buy Jan 50 put (2), Sell Jan 60 put (7), for a 5-point credit, XYZ at 55.

**Market outlook:** Bullish — "The strategist wants the underlying stock to rise in price."

**Formulas (quoted verbatim):**
- "Maximum potential risk = Initial collateral requirement = Difference in striking prices - Net credit received"
- "Maximum potential profit — Net credit"
- "Break-even price = Higher striking price — Net credit"

In the example: collateral/max risk = $1,000 − $500 = $500; max profit = $500; breakeven = 60 − 5 = 55.

**Risk/reward:** Defined risk, defined reward. Max profit if stock is above the higher strike at expiration (both puts expire worthless, spreader keeps the full credit). Max loss if stock is below the lower strike at expiration ("the maximum possible loss is always equal to the collateral requirement in a bullish put spread").

**Capital/margin:** "The investment required for a bullish put spread is actually a collateral requirement, since the spread is a credit spread. The amount of collateral required is equal to the difference between the striking prices less the net credit received for the spread." In the example, $500 collateral (not the full $1,000 strike-width) is needed — this is capital-efficient relative to a debit spread of the same width, but it is still a margin (collateral) requirement, not a cash outlay you fully control the size of — it's fixed by the strike differential minus the credit.

### Calendar Spread (Put Calendar Spread)

**Construction:** Sell a near-term put, buy a longer-term put, same strike. Two philosophies described, both explicitly carried over from the call-calendar discussion in Ch. 9:

**1. Neutral calendar spread (put version):**
- Example: XYZ at 50; Jan 50 put sells for 2, Apr 50 put sells for 3 → established for a 1-point debit (sell Jan 50 put, buy Apr 50 put).
- Market outlook: Neutral — "the spreader is merely attempting to capitalize on the fact that the time value premium disappears more rapidly from a near-term option than it does from a longer-term one." Maximum profit is realized "if the stock is exactly at the striking price at expiration" (of the near-term leg).
- If XYZ is exactly at 50 at January expiration: Jan put expires worthless, Apr put worth ~2 → 1-point profit before commissions on a 1-point original debit.
- **Explicit rule of thumb on commissions/sizing:** "Since commission costs can cut into available profits substantially, spreads should be established in a large enough quantity to minimize the percentage cost of commissions. This means that at least 10 spreads should be set up initially." (This is a hard number he states directly — and it is a major capital-size flag for a small account; see Capital section below.)
- Risk: limited to the net debit. Max loss scenario: underlying moves far from the strike in either direction before near-term expiration, both puts converge toward the same (low or high) price, spread shrinks toward zero.
- **Explicit strategy comparison:** "Neutral call calendar spreads are generally superior to neutral put calendar spreads. Since the amount of time value premium is usually greater in a call option (unless the underlying stock pays a large dividend), the spreader who is interested in selling time value would be better off utilizing call options." — i.e., McMillan directly tells the reader to prefer the call version for the neutral strategy.

**2. Aggressive (bearish) calendar spread with puts:**
- Set up with out-of-the-money puts. Example: XYZ at 55; sell Jan 50 put for 1, buy Apr 50 put (net cost reduced to 50 cents after the credit from the short leg).
- Market outlook: The strategist wants (a) the near-term put to expire worthless, then (b) "the underlying stock must drop... substantially before April expiration" to generate large profits on the long put.
- Risk/reward: "the initial debit for a bearish calendar spread is small... Thus, the losses will be small and the potential profits could be very large if things work out right." This is explicitly a small-defined-loss / occasionally-large-gain strategy — "one profitable situation can more than make up for several losing ones."
- **Explicit caveat:** "The aggressive spreader must be careful not to 'leg out' of his spread, since he could generate a large loss by doing so." Also: "if the underlying stock should fall to the striking price before the near-term put expires, the spread will normally have widened enough to produce a small profit; that profit should be taken by closing the spread at that time."

---

## Chapter 23: Spreads Combining Calls and Puts

### Butterfly Spread (four constructions, incl. put/call mix)

**Construction:** Three strikes; a bull spread between the lower two strikes and a bear spread between the higher two strikes. Because a bull or bear spread can each be built with either calls or puts, there are four ways to build a butterfly: all-calls, all-puts, calls-bull/puts-bear, or puts-bull/calls-bear (the last is described as "a short straddle protected by buying the out-of-the-money put and call").

**Numeric example (XYZ at 60; strikes 50/60/70; calls 12/6/2; puts 1/5/11):**

| Bull spread (buy@50, sell@60) | Bear spread (buy@70, sell@60) | Total money |
|---|---|---|
| Calls (6 debit) | Calls (4 credit) | 2 debit |
| Calls (6 debit) | Puts (6 debit) | 12 debit |
| Puts (4 credit) | Calls (4 credit) | 8 credit |
| Puts (4 credit) | Puts (6 debit) | 2 debit |

**Risk/reward (identical across all four constructions at expiration, per the text):** "In each of the four spreads, the maximum potential profit at expiration is 8 points if the underlying stock is exactly at 60 at that time. The maximum possible loss in any of the four spreads is 2 points, if the stock is at or above 70 at expiration or is at or below 50 at expiration." The equivalence across constructions is attributed to arbitrage forcing put/call prices into line ("the arbitrageur... this particular form of arbitrage, known as the box spread").

**McMillan's stated preference:** "The best way to set up the butterfly spread is to use calls for the bull spread and puts for the bear spread" (the largest-debit version, second row above) "because all the other combinations involve selling an in-the-money put or call at the outset, a situation that could lead to early exercise." Many investors avoid this version because of its larger debit, but he flags that as the tradeoff for avoiding early-exercise risk.

**Overall verdict (his own words):** "A butterfly spread is not an overly attractive strategy although it may be useful from time to time. The strategy should not be considered unless one has low commission costs." Rule of thumb given: "If the potential profit is at least three times the maximum risk and preferably four times, and the underlying stock appears to be in a trading range, the strategy [may be worth considering]" (sentence truncated by page break in source but the ratio figures — 3x, preferably 4x — are explicit).

### Condor and Iron Condor Spreads

**Construction:** Like a butterfly but with two different (separated) strikes in the center instead of one. Condor = all-calls or all-puts; Iron Condor = mix of calls and puts, all four legs out-of-the-money, established for a credit. "In actual practice, most traders use the iron condor strategy."

**Numeric example:** XYZ at 120.
- Buy 1 Dec 135 call: .50
- Sell 1 Dec 130 call: 1.00
- Sell 1 Dec 110 put: 1.00
- Buy 1 Dec 105 put: .50
- Net Credit: 1.00

**Construction rule stated:** "In its basic form, the difference in the call strikes and the put strikes should be the same (5 points in this example)."

**Formula (quoted):** "Maximum loss = Difference In High Strikes − Initial Credit = 135 − 130 − 1.00 = 4.00." Also noted: "The maximum loss is also the difference in the low strikes minus the initial credit, when the put spread and the call spread have the same differential in their strikes. If the differential in the lower strikes is greater than that for the upper strikes, the maximum loss would be the difference between the two low strikes minus the initial credit."

**Max profit:** the initial credit ($100 in the example) if the stock closes between the two middle (short) strikes at expiration.

**Margin/capital:** "The margin required for this spread is the maximum risk. Therefore one can lose as much as 100% of his investment in this position, if the underlying is above the higher strike or below the lower strike at expiration. As a result, this strategy has great risk."

**Strike-placement guidance:** "It is common to attempt to set the short strikes at one or more standard deviations from the current stock price" (standard-deviation calc detailed in his Ch. 28 on math applications, not in these files).

**Explicit volatility caveat:** "An increase in volatility will harm this strategy in two ways: (1) the stock will have a greater probability of moving outside the short strikes than one had initially estimated, and (2) the options will all become more expensive, which will cause a mark-to-market loss in the spread."

**Follow-up/money-management rule (explicit, quoted):** "Allocate a certain portion of your entire capital to this strategy. In addition, only establish condors with one-third to one-half of the capital that one is allocating to the strategy. In that manner, if the maximum loss occurs, there is still capital left to trade with, and the same percentage limits apply to allocation of that capital."

**Overall verdict:** "There is a large chance of making a small profit... There is also a small chance of ruin, so the trade cannot be established with a significant portion of one's capital. Overall, there are far more attractive strategies in general, especially when the stock market is volatile."

### Combining an Option Purchase and a Spread (Call Buy + Put Credit Spread / Put Buy + Call Credit Spread)

**Bullish version — call buy + put credit spread:**
- Rationale: used "when one has a quite bullish opinion regarding the underlying security, yet the call one wishes to purchase is 'overpriced.'"
- Example: XYZ at 100; buy Dec 100 call for 10 (deemed overpriced); simultaneously sell a put credit spread: Sell Dec 90 put (6), Buy Dec 80 put (3) → 3-point credit. Net cost of the whole position: 7 points (10 − 3).
- **Explicit risk/margin figure:** "if the stock were to fall dramatically, the put spread could lose 7 points (the width of the strikes in the spread, 10 points, less the initial credit received, 3 points). This, added to the call's cost of 10 points, means that the entire risk here is 17 points. In fact, that is the margin required for this spread as well." So max loss = margin = 17 points in the example — larger than the plain call purchase's 10-point risk.
- Behavior: at expiration it outperforms an outright call purchase "as long as the stock is higher than 87 at expiration" in the example; near-term (halfway to expiration) its P&L curve resembles a plain long call.
- Caveat: "it does increase risk and require a larger collateral deposit than the outright purchase of the at-the-money call would." Variant noted: buy an OTM call and sell enough put credit spread to fully finance it, producing a "free" call with no risk above the higher put strike.

**Bearish version — put buy + call credit spread:**
- Example: XYZ at 80; Buy Dec 80 put (8 debit); Sell Dec 90 call (4 credit); Buy Dec 100 call (2 debit) → total cost 6 debit ($600).
- **Explicit risk/margin figure:** "The introduction of the call credit spread has increased the risk to $1,600 if the stock should rally to 100 or higher by expiration... The margin required would be this maximum risk, or $1,600."
- Caveat: "it does require a larger margin investment and has theoretically larger risk" than an outright put purchase, though it can be more attractive when options are expensive.

### Follow-Up: Using Puts/Calls to Verify or Lock In Bull/Bear Spread Profits

Not a standalone position but a described technique: use the complementary put (or call) spread to (a) check whether an existing call bull spread is priced "in line" (put spread value + call spread value should sum to the strike width), or (b) lock in profits on a deep ITM spread when market-maker bid/ask on the ITM options is too wide to exit efficiently, by buying a cheap OTM put (or call, for a bear spread) as insurance/lock-in instead of trying to sell the wide ITM spread directly. Example shown yields a better net exit (9.60 credit) than trying to sell the wide call spread outright (9.30 credit), plus optionality if the stock craters through the lower strike. Caveat: commission costs and early-assignment risk should be weighed by the public customer before using this technique.

### Three Advanced Combination (Calendar) Strategies

All three combine puts and calls **and** combine near-term (sold) with longer-term (bought) options. McMillan: "Although all of these are somewhat complex and are for the most advanced strategist, they do provide attractive risk/reward opportunities... they are not designed strictly for professionals."

#### 1. Dual Calendar Spread ("Calendar Combination")

**Construction:** Simultaneously run an OTM bullish call calendar spread (sell near-term OTM call, buy longer-term OTM call at same strike) AND an OTM bearish put calendar spread (sell near-term OTM put, buy longer-term OTM put at same strike), with the stock roughly midway between the two strikes.

**Numeric example (3 months before Jan expiration):** XYZ 65; Jan 70 call 3 / Apr 70 call 5 (call side = 2 debit); Jan 60 put 2 / Apr 60 put 3 (put side = 1 debit). Total = 3-point debit, no additional collateral required beyond the debit.

**Market outlook:** Direction-agnostic — "the spreader does not care which direction the stock moves after the near options expire worthless; he only hopes that the stock becomes volatile and moves a large distance in either direction." Explicitly suited to anticipated volatility events: "earnings announcement, or an FDA hearing for a biotech company, or a potentially volatile lawsuit." Suggests sizing legs using the near-term straddle price as a gap estimate, and balancing the two peaks with unequal ratios (e.g., "3 call calendars and 4 put calendars").

**Risk/reward:** Risk limited to the initial debit (3 points here) if the stock gaps hard before near-term expiration (both spreads collapse toward zero — "the least desirable result," though in practice a small residual differential usually remains). If both near-term options expire worthless (stock still near 65), position can be closed at a profit (example: Apr options worth ~5 total vs. 3-point cost). If the strategist holds and the stock later makes a big move, the April 70 call or April 60 put alone can be sold for large gains (example: stock to 100 → Apr 70 call sells for 30; stock to 30 → Apr 60 put sells for 30) against the original 3-point investment.

**Explicit caveats:**
- "One should be willing to hold the combination, even if this means that he lets a small profit decay into a loss... He will probably sustain a number of small losses by doing this, but by giving himself the opportunity for large profits..."
- Take small profits when one side goes slightly ITM near near-term expiration rather than risk assignment: "At no time does the strategist want to risk being assigned on an option that he is short, so he must always close the portion of the position that is in-the-money at near-term expiration."
- Position-sizing caveat: "The strategist must be careful not to place a large portion of his trading capital in the strategy... even though the losses are limited, they still represent his entire net investment."

**Selection criteria (explicit, quoted list):**
1. Relatively volatile stock.
2. Stock price nearly midway between two strikes.
3. Strikes at least 10 points apart (and stock relatively volatile).
4. Two or three months remaining until near-term expiration.
5. "Price of near-term combination greater than one-half the price of the longer-term combination."

#### 2. Calendar Straddle

**Construction:** Sell a near-term straddle, buy a longer-term straddle, both at the same (single) strike, with stock at/near that strike. Example: XYZ 40; Jan 40 straddle = 5, Apr 40 straddle = 7 → 2-point debit.

**Market outlook:** Neutral — profits from faster time decay of the near-term straddle relative to the longer-term one; ideally closed at near-term expiration with stock still near the strike.

**Risk:** "The risk is limited to the amount of this debit up until the time the near-term straddle expires" (2 points here) — but if the strategist buys back the near-term straddle and holds the longer-term one, risk increases by the buy-back cost. Example: stock at 43 at Jan expiration, near straddle bought back for 3 → total invested 5 (2 original debit + 3 buy-back) → if stock is exactly 40 at April expiration, could lose the full 5.

**McMillan's verdict:** "This strategy is inferior to the [calendar combination]... this strategy should be used only in cases when the near-term straddle appears to be extremely overpriced." He explicitly ranks it as "the least attractive of the three strategies, primarily because one is forced to increase his risk after near-term expiration, if he wants to continue to hold the longer-term options."

**Selection criteria (explicit, quoted list):**
1. Stock near striking price initially.
2. Two to four months remaining until near-term expiration.
3. "Near-term straddle price at least two-thirds of longer-term straddle price."

#### 3. Diagonal Butterfly Spread ("Owning a Free Combination")

**Construction:** Sell a near-term straddle; simultaneously buy a longer-term OTM put and a longer-term OTM call (different, wider strikes than the straddle). Differs from the "protected straddle write" (=synthetic butterfly, all same expiration) in that here the long options have a later expiration than the short straddle.

**Numeric example:** XYZ 40; sell Jan 40 straddle for 7; buy Apr 35 put for 1.50 and Apr 45 call for 2.50 (4-point debit on the long combo) → net credit 3. Collateral required = strike differential (5 pts calls + 5 pts puts = 10) less net credit (3) = **$700** plus commissions.

**Risk (explicit formula/logic):** "The risk can always be quickly computed as being equal to the difference between two contiguous striking prices (two strikes next to each other), less the net credit received." In the example, worst case ≈ 5 − 3 = 2 points.

**Objective:** buy back the near-term straddle for less than the original credit (3 points), leaving the long strangle/combination "owned for free." Example: straddle bought back at 2 → 1-point locked-in credit remains, plus the free long options for further upside if the stock later makes a big move.

**Explicit exception to his "don't leg out" rule:** "It has repeatedly been stated that one should not attempt to leg out of a spread, but this is an exception to that rule, since one owns a long combination and therefore is protected."

**Selection criteria (explicit, quoted list):**
1. Stock near middle striking price initially.
2. Volatile underlying (helps meet the pricing criterion below).
3. "Near-term straddle price should be at least one and one-half times that of the longer-term, out-of-the-money combination." (Example satisfies this: 7 vs. 4.)
4. Three to four months to near-term expiration.
5. "The risk should always be less than the credit taken in" — he gives a rejected counter-example (20-point-wide strikes, 4-point straddle sale, 1-point long combo cost) where risk (17) would swamp the credit (4× cost coverage) despite meeting the 1.5x price criterion — showing the 1.5x rule alone is insufficient.

**Cross-strategy summary from the chapter's own text:** the "calendar combination" [dual calendar] has "the largest probability of capturing the entire near-term premium" but also "the largest probability of losing the entire debit eventually" (since both long legs are OTM to start); the "calendar straddle" offers "the largest potential profits at near-term expiration" but is "the least attractive... because one is forced to increase his risk"; the "diagonal butterfly" is "the only one of the three... whereby the strategist has a possibility of owning free options" but is "the most difficult... to locate."

**Capital allocation guidance (explicit, quoted) — directly relevant to a small account:** "Since they are attractive strategies with little or no margin collateral requirements, the strategist should constantly be looking for these types of positions. A certain amount of cash or collateral should be reserved for the specific purpose of utilizing it for these types of positions—perhaps 15 to 20% of one's dollars." He also flags a practical drag for small accounts across all three: "Since there are four options involved, the commission cost will be large. Again, establishing the spreads in quantity can reduce the percentage cost of commissions" — sizing up to fight commission drag runs directly against a $100–500 account.

---

## Chapter 24: Ratio Spreads Using Puts

Opening framing: "The put option spreader may want to sell more puts than he owns. This creates a ratio spread... two types of put ratio spreads may prove to be attractive: the standard ratio put spread and the ratio calendar spread using puts. Both strategies are designed for the more aggressive investor."

### Ratio Put Spread

**Construction:** Buy puts at a higher strike, sell a greater number of puts at a lower strike (same expiration). "This position involves naked puts, since one is short more puts than he is long."

**Market outlook:** "Neutral to slightly bearish." Max profit if the stock is exactly at the strike of the written (lower-strike, short) puts at expiration.

**Numeric example:** XYZ 50; buy 1 Jan 50 put (4), sell 2 Jan 45 puts (2 each). Profit table shows a profit range of 40–50; max loss below 40 is theoretically bounded only by the stock going to zero.

**Formulas (quoted verbatim):**
- "Maximum upside risk = Net debit of spread (no upside risk if done for a credit)"
- "Maximum profit = Striking price differential × Number of long puts − Net debit (or plus net credit)"
- "Downside break-even price = Lower strike price − Maximum profit potential ÷ Number of naked puts" (from ch_026.txt continuation)

**Risk/reward:** No upside risk (if stock rallies past the higher/long strike, all puts expire worthless, worst case is loss of any net debit paid, or a small commission loss if done for a credit). Downside risk is large/theoretically bounded only by stock going to zero — "these losses could become very large."

**Margin/collateral (explicit):** "The investment required for the put ratio spread consists of the collateral requirement necessary for a naked put, plus or minus the credit or debit of the entire position. Since the collateral requirement for a naked option is 20% of the stock price, plus the premium, minus the amount by which the option is out-of-the-money..." In the example: 20% of $5,000 + $200 premium − $500 OTM amount = **$700** actual dollar requirement. He further advises over-collateralizing for an anticipated adverse move: e.g., to tolerate a decline to 39, allow $1,380 (20% of $3,900 + $600 ITM amount).

**Placement guidance:** "The ratio put spread is generally most attractive when the underlying stock is initially between the two striking prices." If the stock starts below the lower strike, it's "not as attractive, since the stock is already too close to the downside risk point." Larger ratios (4:1, 5:1) can eliminate the debit but "have extraordinarily large downside risk and are therefore very aggressive."

**Follow-up:** "Follow-up action is rather simple... There is very little that one need do, except for closing the position if the stock breaks below the downside break-even point." Buying in additional long puts as a hedge is possible but "not as advantageous in the put spread because of the time value premium shrinkage."

**Psychological note (his own words):** "This strategy may prove psychologically pleasing to the less experienced investor because he will not lose money on an upward move... they may often prefer ratio put spreads to ratio call spreads because of the small upside risk."

### Ratio Put Spread Using Three Strikes (variant)

**Construction:** Buy 1 put at the highest of three strikes, sell 1 put at the middle strike, sell 1 put at the lowest strike (a 1:1:1 three-strike combination, net short 2 puts vs. 1 long).

**Numeric example:** XYZ 127; Dec 125 put 3.00 (buy), Dec 121 put 2.00 (sell), Dec 116 put 1.25 (sell) → net credit 0.25.

**Formulas (quoted verbatim):**
- "Downside break-even = Lower Strike − (Difference in two Higher Strikes) − Net credit" = 116 − (125−121) − 0.25 = **111.75**
- "Maximum Profit Potential = (Difference in two Higher Strikes) + Net credit" = (125−121) + 0.25 = **4.25**, and this max profit is attainable anywhere between the two lower strikes (116–121), not just at a single point.

**Margin:** "One must margin the 116 put as a naked put. The other two puts constitute a bear spread, and thus don't require any collateral. It is generally wise to margin the put as if the stock were at the lower strike, in order to allow some excess collateral."

**Follow-up:** monitor as underlying falls through the max-profit zone (116–121) — may want to take partial/full profits early; if the underlying is just above the upper strike near expiration, the whole spread may be closeable for a credit due to time decay differentials. Overall: "if the spreader monitors that and exits when the downside break-even point is breached... the net effects of this strategy over time are quite favorable" — but downside risk remains the key hazard.

### Using Deltas (Neutral Ratio Put Spreads)

**Rule stated:** "The neutral ratio is determined by dividing the delta of the put at the higher strike by the delta of the put at the lower strike." Example: Jan 45 put delta −.30, Jan 50 put delta −.50 → neutral ratio = 1.67 (i.e., sell 1.67 puts per put bought; e.g., sell 5 Jan 45 puts, buy 3 Jan 50 puts). As the stock moves, the ratio can be rebalanced by selling more or buying more of the respective strike to stay neutral.

### Ratio Put Calendar Spread

**Construction:** Buy a longer-term put, sell a larger quantity of shorter-term puts, all at the same (single) strike, generally OTM (stock above the strike), established for a net credit.

**Numeric example:** XYZ 55; buy 1 Apr 50 put (2), sell 2 Jan 50 puts (1.50 each) → net credit 1 point ($100). If XYZ stays above 50 through Jan expiration, the short puts expire worthless and the long Apr put is "owned for free"; even if the Apr put then also expires worthless, "the strategist will make a small profit... in the amount of his original credit — $100 — less commissions."

**Risk (explicit):** Large if the stock drops well below the strike before near-term expiration. Example: stock to 30 before Jan expiration → pay $4,000 to buy back 2 Jan 50 puts, receive only $2,000 from selling the 1 long Apr 50 put — "a rather large loss."

**Explicit rule-of-thumb stop:** "Normally, one would close the position if the stock fell more than 8 to 10% below the striking price before the near-term puts expire."

**Margin (explicit numbers):** Initial requirement in the example = $750 (20% of $5,500 + $150 Jan premium − $500 ITM amount of the naked Jan 50 put). If planning to hold to a stock price of 46, allow $1,320 collateral (20% of $4,600 + $400 ITM amount). The initial $100 credit can be applied against these requirements.

**Suitability caveat:** "This strategy is a sensible one for the investor who is willing to accept the risk of writing a naked put... One should take care... to limit his losses before near-term expiration, since the eventual large profits will be able to overcome a series of small losses, but could not overcome a preponderance of large losses."

### Ratio Put Calendars Using Deltas (OTM vs. ITM variants)

**Neutral ratio rule:** "the delta of the put to be purchased is divided by the delta of the put to be sold."

**OTM example:** XYZ 59; Jan 50 put delta 0.10 (sic — magnitude used), Apr 50 put delta −0.17 → neutral ratio 1.7:1 (sell 17 for every 10 bought). This variant has naked puts and "large risk if the underlying stock declines too far," but follow-up action can limit it if the decline is orderly.

**ITM example:** XYZ 59; Jan 60 put delta −0.45, Apr 60 put delta −0.40 → neutral ratio 0.889:1, i.e., "sell 8 and buy 9" — **more longs than shorts, no naked puts**, so max loss is capped at the initial debit if the stock rallies away; optimum result is stock at the strike at expiration. Caveat: "Another risk of the in-the-money put spread is that one might be assigned rather quickly if the stock should drop... one must be careful not to establish the spread with puts that are too deeply in-the-money" — early assignment increases commission/margin cost via forced stock purchase, though it doesn't necessarily hurt overall profitability.

### Ratio Calendar Combination (put + call combined ratio calendar)

**Construction:** Sell a larger number of near-term OTM put+call combinations, buy a smaller number of longer-term OTM put+call combinations, for a net credit.

**Numeric example:** XYZ 55; sell 2 near-term Jan combos (Jan 50 put 1.50 + Jan 60 call 3.50 = 5 pts each, ×2 = 10 pts in) ; buy 1 longer-term Apr combo (Apr 50 put 2 + Apr 60 call 5 = 7 pts) → **net credit 3 points**.

**Best case:** near-term combo expires worthless → guaranteed 3-point profit even if the long combo later also expires worthless; if the stock then moves big in either direction, large additional profit on the "free" long combo.

**Follow-up thresholds (explicit method, worked example):** compute the stock price at which closing the in-the-money side of the near-term combo would just cost the 3-point credit (breakeven), e.g., upside breakeven ≈ 65, downside breakeven ≈ 46 in the example — "the strategist has two parameters to work with in attempting to limit losses... In practice, if the stock should reach these levels before, rather than at, January expiration, the strategist would incur a small loss by closing the in-the-money side... This action should still be taken, however."

**Near-expiration decision rule:** if the near-term combo can be bought back for less than the original credit, there's already an unrealized total gain; "the general philosophy should be to hold on to the [longer-term] combination" since "a profit is already guaranteed at this time."

**Overall verdict:** "This strategy is very attractive and should be utilized by strategists who have the expertise to trade in positions with naked options. As long as risk management principles of taking small losses are adhered to, there will be a large probability of [success — sentence continues past a page break]."

**Chapter close (Put Option Summary, explicit):** "This concludes the section on put option strategies... The combination strategies... The four combination strategies that involve selling short-term options and simultaneously buying longer-term options are complex, but are most attractive in that they have the desirable features of limited risk and large potential profits."

---

## Chapter 25: Long-Term Option Strategies (LEAPS)

**Note on source completeness:** `ch_026.txt` cuts off mid-sentence inside the "Advantages of Buying 'Cheap'" section — "Suppose that one buys a 2-year LEAPS call at-the-money when the following situation exists:" is the last line in the supplied file. Everything below reflects only what is present up through that cutoff. Sections that would likely follow in the full book (e.g., specific LEAPS spread strategies, LEAPS-selling strategies in low-rate/low-vol environments beyond the general rule quoted, and any further worked "buying cheap" example) are **not present in these files** and are not reported here.

### Background / Definitions

"Listed long-term options are actually a slightly different class of options called LEAPS. While that term still exists, it is somewhat outmoded... long-term options are just referred to by their month and year." LEAPS were "first introduced by the CBOE in October 1990... on a handful of blue-chip stocks." Prior to the 2010 Options Symbol Initiative they used distinct symbols; post-OSI "the term LEAPS was no longer mandatory."

"Long-term options are generally listed about 2.5 years before they expire" (previously up to 2.75 years before a 2008 change shortened the listing period). "For long-term stock options, the only expiration month is January. However, for some index options, long-term options expire in December instead." (He flags these mechanics could change.)

### Pricing LEAPS

Same six pricing factors as any option (stock price, strike, time remaining, volatility, risk-free rate, dividend rate), but "the relative influence of these factors may be a little more pronounced for LEAPS than it is for shorter-term equity options" — so a LEAPS may look mispriced "by inspection" when it is not; a model should be used.

**Time decay non-linearity, quoted finding:** "the 2-year LEAPS, which has eight times the amount of time remaining as compared to the 3-month call, only sells for about four times as much." Warning: "Do not be deluded into thinking that a LEAPS looks cheap merely by comparing its price to a nearer-term option; use a model to evaluate it."

**Interest rate sensitivity (explicit, large effect on LEAPS specifically):** Using a 2-year, 100-strike call at 3%/6%/9% risk-free rates: "A shift of 3% in rates causes a larger price difference of over 2 points in the at-the-money, 2-year LEAPS... the in-the-money LEAPS are changed in price by over 4 points when rates change by 3%. That is a monstrous differential." "The difference in LEAPS prices increases as the LEAPS becomes in-the-money."

**Dividend sensitivity (explicit):** For 2-year calls, "the increase in dividends manifests itself by decreasing the LEAPS call price... For the in-the-money call, a $1 increase in [annual] dividends over two years can cause the LEAPS to be worth about 1¼ points less in value." Effect is smaller than the interest-rate effect. "Dividend increases have the opposite effect on puts... an increase in the dividend payout of the underlying common will cause a put to increase in price... even larger" for long-term puts.

**Comparison table (Table 25-1, quoted values) — price change per unit of variable change, 3-month vs. 2-year option:**

| Variable | Increment | 20% OTM: 3-mo / 2-yr | ATM: 3-mo / 2-yr | 20% ITM: 3-mo / 2-yr |
|---|---|---|---|---|
| Stock Price | +1 pt | .03 / .41 | .54 / .70 | .97 / .89 |
| Volatility | +1% | .03 / .43 | .21 / .48 | .04 / .33 |
| Interest Rate | +½% | .01 / .27 | .08 / .55 | .14 / .72 |

He notes only three of the nine comparisons are "not large" (the stock-price-change deltas, and ATM volatility change is "only" a 2:1 factor) — LEAPS traders will "gain or suffer substantially and immediately" from small rate/dividend/volatility moves that short-term traders would ignore.

**General positioning rule (quoted):** "As a general rule, one would want to be a buyer of LEAPS when interest rates were low and when the volatilities being implied in the marketplace are low. If the opposite were true (high rates and high volatilities), he would lean toward strategies in which the sale of LEAPS is used."

### LEAPS as Stock Substitute — Substitution for Stock Currently Held Long

**Concept:** Sell owned stock, reinvest a small portion in an ITM LEAPS call (upside exposure retained), put the rest in interest-bearing cash (substitutes for lost dividend), with capped downside equal to the option cost.

**Full worked example (numbers exactly as given):**
- XYZ at 50; 1-year LEAPS, strike 40, price $12 (2 points time value: 40+12−50=2); dividend $0.50/yr; rates 5%.
- Sale of 100 XYZ stock: $5,000 − $25 commission = $4,975 credit.
- Cost of 1 LEAPS call: $1,200 + $15 commission = $1,215 debit.
- **Total credit balance generated: $3,760.**
- Costs of switching: time value premium −$200; loss of dividend −$50; stock commission −$25; option commission −$15 = **−$290 total**.
- Fixed benefit: interest on $3,760 credit balance at 5% for 1 year = +$188.
- **Net cost of switching: −$102.**
- Downside protection level ≈ **39¼** (per the text, "equivalent to limiting his risk to about 39¼ on the original 100 shares" once accounting for the ~$3,948 that would sit in the bank account).

**Caveats (explicit, quoted/paraphrased tightly):**
- If the investor "were planning to sell the stock before it fell to 39½ in any case, he might not feel the need to pay for this protection" — though he could replicate the effect anytime by selling the LEAPS call.
- A stock commission (or two option commissions to roll) will be owed again after a year if the position needs to be re-established.
- Risk that "the underlying common might declare an increased dividend or, even worse, a special cash dividend" — the LEAPS call owner does not participate in that increase (stock dividends are fine, the call owner is entitled to those).
- Tax considerations: selling appreciated stock triggers a taxable gain; if the stock is at a loss, buying the call creates a wash sale, disallowing the loss.
- "Be very [careful]... trading for exchange members and paying no commission — would take advantage of such a situation before the general public could" — i.e., if the arithmetic looks like free money, professionals have likely already arbitraged it away.

### Buying LEAPS Instead of Buying Common Stock (Initial Purchase)

**Full worked example (same prices: XYZ 50, 1-yr 40-strike LEAPS at $12, dividend $0.50, rates 5%):**
- Stock cost: $5,000 + $25 = $5,025. LEAPS cost: $1,200 + $15 = $1,215. **Net difference (investable): $3,810.**
- Costs: time value premium −$200; loss of dividend −$50.
- Savings: interest on $3,810 at 5% = +$190.
- **Net "cost" of buying the LEAPS instead of stock: $60**, for which "he has all the upside appreciation (except $60 worth), but has risk only down to 40 (he will have $4,000 in his bank account at the end of one year even if the LEAPS expire worthless)."
- Caveat/catch-22 he flags directly: this strategy "might seem it would be especially attractive if interest rates for the differential were high. Unfortunately, those high rates would present something of a catch-22 because... higher rates will cause the LEAPS to be more expensive."
- Same downside caveat as above re: not participating in dividend increases/specials.

**Using Margin variant (explicit numbers):**
- Cost of buying stock on margin: $5,025 total, borrow 50% ($2,512), equity required = $2,513.
- Cost of buying LEAPS outright: $1,215.
- Difference available to bank = $1,298.
- Costs: time value premium −$200; dividend loss −$50.
- Savings: interest on $1,298 at 5% = +$65; margin interest saved on the $2,512 debit balance at 8% for a year = +$201.
- **Net savings from buying LEAPS instead of margined stock: +$16** (a real, if small, edge in this example).
- Note: "current margin rules allow one to purchase a LEAPS option on margin" too — that would change these numbers (reduce required investment, increase margin charges on the debit balance).

### Protecting Existing Stock Holdings with LEAPS Puts

**Concept:** Instead of selling stock and substituting a call (previous strategy), simply buy a LEAPS put against stock you keep — protects downside, keeps upside, and crucially keeps you entitled to dividend increases/specials, at the cost of only one commission (on a cheap OTM put) rather than the two-sided stock-sale-plus-call-purchase transaction.

**Direct comparison math (using the earlier example's own numbers):** the call-substitution strategy cost $102 and protected at ~39¼ — "he is effectively paying $152 for a LEAPS put with a strike of 40" ($102 cost + the 40 − 39¼ gap). So: "if an XYZ 1-year LEAPS put with strike 40 were available at [less than 1½]... he could accomplish everything he had initially wanted merely by buying the put," and would additionally save commissions and keep dividend upside — "these additional benefits should make the put worth even more to the stockholder." Bottom line guidance: compute both costs and choose whichever (call substitution vs. put protection) is cheaper/more favorable for the specific situation and tax picture.

### LEAPS Instead of Short Stock

In-the-money LEAPS puts can substitute for shorting stock. Advantages stated explicitly: "limited risk (whereas the short seller of stock has theoretically unlimited risk)"; "he does not have to pay out any dividends on the underlying stock as the short seller would"; and put commissions are typically smaller than stock-short commissions. Rule of thumb: "If the time value premium spent is small in comparison with the dividend payout that is saved, then the put is probably the better choice."

### Speculative Option Buying with LEAPS

Standard speculative buying, but with a longer runway. "The risk, of course, can be 100% of the investment, and time decay works against the option owner as well." Key advantage: "Purchasing LEAPS options instead of the shorter-term equity options generally exposes the buyer to less risk of time decay on a daily basis... time decay increases more rapidly as expiration approaches."

**Daily percent time-value decay table (Table 25-2, quoted values):**

| Months remaining | At-the-money | 20% OTM |
|---|---|---|
| 24 | .12% | .18% |
| 18 | .14% | .27% |
| 12 | .19% | .55% |
| 9 | .22% | .76% |
| 6 | .27% | 1.18% |
| 3 | .60% | 3.57% |
| 2 | .73% | 4.43% |
| 1 | 1.27% | — |
| 2 wks | 3.33% | — |

Explicit callout: "The out-of-the-money 2-month option loses over 4% of its value daily!" vs. "Most LEAPS, even the out-of-the-money ones, lose less than ¼ of one percent of their value daily."

**But — explicit warning against thinking LEAPS barely decay at all:** "Do not be deluded into believing that LEAPS don't decay at all. Although the rate of decay is slow... an option that is losing 0.15% of its value daily will still lose about 25% of its value in six months." Worked example: XYZ at 60, 18-month LEAPS call at strike 60 for $8; barely moves week to week, but "if the option is held for six months and nothing else happens, the LEAPS call will be selling for about 6" — a 25% loss in six months with the stock unchanged. Compare: "those familiar with holding equity calls and puts are more accustomed to seeing an option lose 25% of its value in possibly as little as four or five weeks' time" — so LEAPS decay much slower, but not negligibly, over a 6-month horizon.

**Rolling guidance (explicit, tied to the decay-curve inflection points):**
- For an at-the-money option, the decay curve "begins to bend dramatically upward soon after the 6-month time barrier is passed" → "one would sell his long at-the-money call when it has about 6 months of life left and simultaneously buy a 2-year LEAPS call" to minimize decay exposure.
- For an out-of-the-money option, the inflection is earlier — "just before it reaches one year until expiration" → "sell his option held long when it has about one year to go and reestablish his position by buying a 2-year LEAPS option at the same time."

**Psychological/timing advantage (explicit):** "The LEAPS option buyer who feels strongly that the stock will move in the desired direction has the luxury of being able to wait calmly for the anticipated move to take place. If it does not, even in perhaps as long as 6 months' time, he may still be able to recoup a reasonable portion of his initial purchase price because of the slow percentage rate of decay."

### Advantages of Buying "Cheap" (section incomplete in source)

The section opens by restating that rising interest rates or rising volatility make LEAPS calls more expensive (echoing the earlier pricing-factor discussion), implying the converse — low-rate, low-volatility regimes are more favorable for LEAPS buyers, consistent with the "general rule" quoted above. The text then begins a new worked example ("Suppose that one buys a 2-year LEAPS call at-the-money when the following situation exists:") and **the supplied file ends there** — the specific numbers and conclusion of that example, and any further content in Chapter 25, are not available in these files.

---

## Notes for a small ($100–500) account — drawn only from explicit statements above, not outside inference

- **Spread minimum equity:** McMillan states "For most brokerage firms, the minimum equity requirement for spreads is $2,000" (Ch. 22) — this is stated as a general brokerage rule, not specific to any one spread type, and would be a hard constraint for a $100–500 account attempting most of the debit/credit spreads above.
- **Commission-driven quantity requirement:** For calendar spreads he explicitly says "at least 10 spreads should be set up initially" to control commission drag (Ch. 22) — not feasible at $100–500 capital for anything but the cheapest underlyings.
- **Iron condor money management rule:** "Only establish condors with one-third to one-half of the capital that one is allocating to the strategy" (Ch. 23) — implies condors need a capital base large enough to survive a full max-loss and still trade on, which is hard to reconcile with $100–500 total.
- **Combination-calendar allocation:** he suggests reserving "perhaps 15 to 20% of one's dollars" for the three advanced combination strategies (Ch. 23) — again framed for a portfolio with meaningfully more than $100–500, and those strategies involve 3–4 option legs each, multiplying commissions.
- **Ratio put spreads require naked-put margin** — explicit 20%-of-stock-price-plus-premium collateral formulas (Ch. 24) — naked short options generally require broker approval levels and margin capacity a very small account is unlikely to have.
- **LEAPS as stock/margin substitute is the one strategy in these chapters explicitly framed around capital efficiency.** The book's own worked numbers show buying an ITM LEAPS call instead of buying stock outright frees up thousands of dollars of capital (e.g., $3,810 freed in the initial-purchase example) for a "net cost" of leverage as small as $60–102 in the given examples, while capping downside risk at the strike price. However, note two caveats explicit in the text that bear directly on very small accounts: (1) all of McMillan's LEAPS-substitution examples are built around a 100-share-equivalent, several-thousand-dollar stock/LEAPS position (e.g., $1,200 LEAPS contract, $5,000 stock) — the underlying arithmetic (commission drag as a fraction of position size, dividend/interest offsets) does not by itself validate scaling down to a $100–500 single-contract LEAPS purchase; (2) the text nowhere discusses buying a single LEAPS contract with no stock/short-stock position to compare against and no bank/CD reinvestment — that "plain speculative LEAPS purchase" is covered only in the general "Speculative Option Buying with LEAPS" section, where the operative facts are simply: max loss is 100% of premium, and decay is much slower than short-term options (well under ¼%/day for most LEAPS) but still real over 6 months (~25% at a 0.15%/day rate in his example).
