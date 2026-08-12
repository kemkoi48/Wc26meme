# Research sources

A durable log of news/data sources evaluated for market research, so a future
session doesn't have to re-test them from scratch. Each entry: what it is,
whether it's directly fetchable, and how to actually use it.

Format: `## <name>` — `status`, then notes. Status is one of:
- **Live, fetchable** — WebFetch pulls real current content directly.
- **Educational, not a feed** — useful for framework/method, no live data.
- **Blocked** — direct fetch fails; may still surface via web search.

---

## Investing.com Economic Calendar
`https://www.investing.com/economic-calendar/`
**Status: Live, fetchable.**

Tested 2026-08-06 — returned real, current-dated events with forecast/previous
values and impact level (high/medium/low), e.g. that day's US Initial/
Continuing Jobless Claims (high impact), German Factory Orders, Eurozone
Retail Sales, etc. This is the primary macro-check source: ask for "today's
high-impact events" or "this week's calendar" before acting on a signal.

## Reuters Markets
`https://www.reuters.com/markets/`
**Status: Blocked (confirmed).**

Direct WebFetch fails outright ("unable to fetch from reuters.com") — tested
2026-08-06 across four variants (`www.reuters.com/markets/`,
`reuters.com/markets/` without www, `www.reuters.com/markets/us/`, and a
retry of the original URL): all four failed identically. This is a
domain-wide block on Reuters' side, not a one-off glitch or a paywall
message. High reputational quality as a source, but not usable as a direct-
check tool. Don't keep retrying variants — this is settled.

Workaround: Reuters-sourced content sometimes still surfaces through a
general web search (which indexes the page rather than fetching it live). If
you have a specific Reuters article you want analyzed, paste its text
directly and I can work with that.

## Investing.com Academy — "Stay Updated on the Stock Market"
`https://www.investing.com/academy/trading/stay-updated-on-the-stock-market/`
**Status: Educational, not a feed.**

Recommends a "Signal vs. Noise" framework: earnings reports and scheduled
economic data = signal; sensational headlines and minor price swings = noise.
Recommends a three-layer routine (macro calendar check, portfolio alerts,
curated analysis) and names WSJ, Financial Times, Reuters, and Investing.com
itself as sources. **Caveat: WSJ and FT are paywalled** — full article text
generally isn't fetchable unless pasted in directly.

## stockmarketterminology.com — "Stock Market News: What It Means"
`https://stockmarketterminology.com/stock-market-news-what-it-means/`
**Status: Educational, not a feed.**

Defines what counts as market-moving news (earnings, Fed actions,
geopolitical events, mergers) and stresses that markets are forward-looking
— news often confirms an already-priced-in expectation rather than surprising
the market. Useful lens for weighing a headline's actual price impact, not a
source of current headlines itself.

---

## Stocktwits (connector)
**Status: Live, connected, verified.**

Tested 2026-08-06: `whoami` confirms an authenticated session (real user
account); `get_trending_symbols` returns real live top-movers with price, %
change, intraday sparkline, watcher count, and extended-hours pricing (e.g.
SOUN, SNDK, IONQ, RDW, DKNG at test time). `get_symbol_pulse` and
`get_sentiment` return real aggregate sentiment for a symbol (bull/bear %, a
0-100 score, a label like "EXTREMELY_BULLISH") plus message-volume metrics
across multiple timeframes (now/15m/1D/1W/1M/3M/6M/1Y/ALL). Tested against
AAPL: price $313.07, sentiment 82/100 "EXTREMELY_BULLISH", 987,224 watchers.

Other available tools (not yet tested): `get_symbol_messages`,
`get_message_volume`(+`_history`), `get_sentiment_history`,
`get_following_feed`, `get_watchlist_feed`, `get_user_messages`,
`get_symbol`.

**Caveat — read before surfacing raw posts to a user:** the "top posts" in
`get_symbol_pulse` is unmoderated, real user-generated content. In testing,
AAPL's feed included off-topic, low-quality, and offensive material mixed in
with genuine stock chatter. **The aggregate metrics (sentiment score, message
volume, watcher count) are the reliable signal — don't relay raw post text
without screening it first.**

## Robinhood connector — no dedicated news tool
Confirmed via tool search: none of the Robinhood tools is a `get_news` /
article-feed endpoint. Closest equivalents are `get_earnings_calendar` /
`get_earnings_results` / `get_financials` / `get_equity_fundamentals` —
fundamentals and earnings data, not news articles. For actual news-adjacent
signal, use Stocktwits sentiment/chatter (above) or a general web search.

## Yahoo Finance — not actually connected
User mentioned adding a Yahoo Finance connector alongside Stocktwits, but
only Stocktwits tools appeared in the session (checked via tool search — no
match). If a Yahoo Finance connector gets added later, re-check and log it
here; don't assume it's present just because it was mentioned.

## Stocklake (connector)
**Status: Live, connected, verified — free tier.**

Tested 2026-08-06. 17 tools total; account is on the **free tier** (200
calls/day, 8 non-AI tools). Two tools require **Pro** ($20/mo, 7-day trial,
5000 calls/day) and returned `pro_required` errors when tested:
`get_news_feed` (market-wide AI-flagged news briefing) and `get_signals`
(AI-screened trade signals with conviction/rationale). Both gave a useful
`preview` of a few symbols even on free tier.

**Confirmed working on free tier:**
- `get_market_pulse` — VIX, Fear & Greed, market breadth (RSI distribution),
  SPY/QQQ/IWM + RSI, TLT/GLD. One call, no AI cost. Real live data verified.
- `get_market_movers` — gainers/losers/most-active with price, volume, RSI,
  ATR%, market cap. Real live data verified.
- `get_stock_news` — per-symbol news (docs say "1 article" on free tier;
  observed 5 articles per call in testing — better than documented, but
  don't rely on the discrepancy holding).
- `get_screener` — most filters (RSI/SMA/MACD/performance/volume/market cap/
  analyst rating) work on free tier; `min_flag_score` and the `high_conviction`
  preset are Pro-only (silently ignored on free tier per its own docs).
- `get_stock` — price/fundamentals/raw indicators on free tier; the four
  *interpreted* blocks (rating, signals, stance_signals, ai overview) are Pro.

**Not yet tested:** `get_earnings_calendar`, `get_earnings_intelligence`,
`get_indicator_history`, `get_insider_activity`, `get_market_assessment`,
`get_sector_intelligence`, `get_stock_history`, `get_stock_research`,
`get_stocks`, `get_watchlist`.

**Real finding worth remembering:** cross-referencing Stocklake's mover list
against Stocktwits trending caught a data-quality issue. Two names on
Stocklake's gainers list (CLBK +126.6%, VSCO +69.6%) had no same-day news
that explained a move that size, AND neither appeared on Stocktwits
trending at all. A third name, IOVA (+38.99% on Stocklake, +38.36% on
Stocktwits independently), had same-day news (8-K filing + a same-morning
article) and showed up on both platforms — that agreement is what makes it
trustworthy. **Lesson: an extreme single-source % move with no matching
same-day news and no cross-platform attention is a reason for suspicion, not
excitement — verify large movers against a second source before treating
them as real.**

## Robinhood native scanner (`get_scans` / `run_scan`) — covers names Stocklake misses
**Status: Live, verified — and catches a real gap.**

Tested 2026-08-06: the account has saved scans including "Daily gainers"
(294 matches, all Robinhood-tradable stocks, sorted % change desc).
`run_scan` on it surfaced **WYHG at +540%** (a $10.2M market-cap ADS) —
a move that **never appeared in Stocklake's `get_market_movers` gainers
list** (top Stocklake gainer at the same moment was CLBK at 126.6%, not
close). WYHG had zero news (`get_stock_news` returned empty) and classic
retail-hype-driven chatter with no informational catalyst — textbook thin/
low-float momentum spike, not a real opportunity, but the point stands
regardless of that stock's quality: **Stocklake's ~3,300-name tracked
universe does not cover everything Robinhood's own scanner does.**

**Process lesson: check both `get_market_movers` (Stocklake) AND
`run_scan` on Robinhood's "Daily gainers" (or equivalent) when looking for
"what's moving today" — they cover different universes and can each miss
names the other catches.** `run_scan` results can be large (200+ rows) and
overflow the tool-result limit; save to file and extract with
`python3`/`jq` rather than reading inline.

## Robinhood consumer app — "Short interest" / "Trading Trends" panels
**Status: Blocked — app-only, no MCP tool exposes it.**

Confirmed 2026-08-07: the Robinhood mobile app's stock-detail screen has a
"Short interest" chart (short interest in shares + short float %, ~2 months
trailing) and a "Trading Trends" chart (net buy/sell % by Robinhood retail /
Hedge funds / Insiders, weekly). Checked the full `Robinhood` MCP tool list
(`get_equity_fundamentals`, `get_financials`, `get_equity_technical_indicators`,
etc.) — none of them return short interest, short float, or ownership-flow
data. This is because the connected server is the narrower **Agentic Trading
API** (`agent.robinhood.com/mcp/trading`), not the full consumer-app backend;
`get_equity_fundamentals` gives float/shares outstanding but stops there.

**Workaround: read the values directly off a user-provided screenshot of the
app screen** — no live fetch is possible, but a pasted image can be
transcribed manually. Example (TSLA, screenshot dated through Aug 6 2026):
short interest ran ~75–79M shares (2.8–3.0% of float) from early June through
mid/late July, then dropped sharply ~Jul 25–28 to ~67–70M shares (2.4–2.6%
float) and held there — a short-covering signal, not something any connected
tool surfaced independently. Robinhood retail net-buy/sell trend for the same
symbol was net-positive overall Jul 8–Aug 3 with two sharp sell days.

If a dedicated short-interest data connector (e.g. Ortex, S3 Partners, or a
FINRA short-interest feed) gets added later, re-check and replace this entry.

## Warrior Trading — "Small Account Challenge" momentum strategy (YouTube + PDFs)
**Status: Educational, not a feed. Incompatible with this repo's cash account for live use.**

Reviewed 2026-08-08: a Ross Cameron / Warrior Trading YouTube class plus three
companion PDFs (strategy guide, sample trading-plan worksheet, blank trade-log
worksheet). This is promotional content for a paid course (PDF upsells, "check
out my class" links) — the $600→$20M / $2K→$65K-in-30-days figures are the
marketing hook; treat as a strategy description, not a performance claim.

**The strategy — 5 steps:**
1. **Stock selection** (scanner-driven): relative volume ≥5x (ideally ≥20x)
   50-day average, high total volume, gapping/up ≥10% intraday, price in a
   narrow band (video: $2–20; the trading-plan worksheet narrows this to
   **$5–10** as the small-account "sweet spot"), float **<20M shares in a hot
   market / <10M in a cold market** (lower = better). News preferred, not
   required if other criteria are strong.
2. **Entry — "first pullback" pattern**: buy the first candle to make a new
   high after a pullback that (a) retraces ≤50% of the prior move, (b) shows
   heavier volume on green than red candles, (c) holds above VWAP, (d) holds
   above the 9 EMA. Stop-loss = low of the pullback.
3. **Level 2 / tape** for entry timing and confirmation around psychological
   price levels (half-dollar/whole-dollar).
4. **Exit on indicators, not fixed targets**: a large resting sell wall, a
   suspected iceberg/hidden seller, a burst of red tape, a topping-tail /
   "jackknife rejection" candle, MACD crossing its signal line, or buying
   visibly slowing.
5. **Journal every trade** and mine the log for leaks (e.g. time-of-day
   win-rate) — the log template tracks P/L, accuracy, float, relative volume,
   news, hold time, and candlestick pattern per trade.

**Concrete risk rules from the worksheets** (not stated in the video):
7:00–11:00am ET trading window; risk ~5% of account per trade, profit target
~10% (2:1 reward:risk); daily max loss 10% of account; **3 consecutive losers
= stop for the day**; accuracy/P&L progression benchmarks from 40–50%
accuracy / 0.5–1.0 P/L ratio (novice) up to 70%+ / 1.0+ P/L ratio sustained
over 5+ weeks (pro).

**Why this doesn't map onto this repo:**
- It requires multiple same-day round trips (buy and sell the same low-float
  stock within minutes) on a **cash account** — this causes good-faith
  settlement violations regardless of the 2024 T+1 settlement change (T+1
  speeds up when capital becomes available again, it does not permit same-day
  round trips). Same restriction already documented for Pattern Scalp in the
  README — this strategy has the identical conflict, more so (it's designed
  around several round trips per session, not one).
- Exit logic depends on reading Level 2 order flow and tape **in real time,
  continuously** (spotting an iceberg seller, a burst of red tape). The
  Robinhood connector's `get_equity_price_book` returns a real Level 2
  snapshot, but only on-demand — a polling/interval-based bot cannot watch
  continuous tick-by-tick order flow the way this strategy requires.
- The target stock profile (float <20M, extreme relative volume, sometimes no
  news) is exactly the profile already flagged as suspicious in the WYHG
  entry above (extreme single-source move, no news, no cross-platform
  confirmation = reason for caution, not excitement in that entry). This
  strategy treats that same profile as the *goal* — the two takeaways only
  don't contradict each other because Warrior Trading's edge depends on
  discretionary skill/speed to tell a real squeeze from a pump, which isn't
  something this bot's tools or architecture can replicate safely.

## Warrior Trading — warriortrading.com/momentum-day-trading-strategy
`https://www.warriortrading.com/momentum-day-trading-strategy/`
**Status: Live via the AMP URL. Canonical URL is blocked (truncates).**

**Use `https://www.warriortrading.com/amp/momentum-day-trading-strategy/`.**
The canonical URL was tested twice on 2026-08-10 with different extraction
prompts and both times returned only the page title followed by "[Content
truncated due to length...]" — the body sits past nav/ad markup that eats the
fetch window. The AMP copy strips that markup and returned the **complete,
untruncated article** on the first try. Generalize this: for any content site
that truncates, try `/amp/` before declaring it blocked.

**Correction — an earlier WebSearch summary of this page got several numbers
wrong.** Before the AMP read, a search-engine summary was logged claiming
$1–10 price / <10M float / ≥5% change / 5x rel. volume. The actual article
says none of those things except approximately the float ideal. Lesson: a
search summary of a page is *not* a read of the page — label it as such and
replace it once the real text is obtained. Do not cite those figures.

**What the article actually says (read directly, 2026-08-10):**

*Selection:* float **under 100M shares**, with **under 20M ideal**; relative
volume **at least 2x** average; stocks moving **20–30%+** on the day; on the
daily chart, price above its moving averages with **no nearby resistance**; a
fundamental catalyst — PR, earnings, FDA news, activist investor, breaking
news.

*Entry patterns (named):* **Bull Flag** — buy the first candle to make a new
high after the breakout — and **Flat Top Breakout**, where resistance forms
across several candles before an explosive move.

*Exits:* sell **half** the position at the first profit target; **the first
candle to close red is an exit indicator**; exit into extension bars (spikes
of $200–400+).

*Risk:* **2:1 profit/loss ratio** required. Max stop distance **20 cents** —
if the technical stop is further away, stop out at −20¢ anyway. Position size
falls out of that: `shares = max_risk ÷ stop_distance` (their example: $500
risk ÷ $0.20 = 2,500 shares).

**The finding that matters most here: a hard time window of 9:30–11:30am ET,
with the first hour called optimal, and 5-minute charts only after 11:30am.**

This reframes a result from live testing the same day. Two scanner runs at
**12:43pm and 1:07pm ET** — both more than an hour past this strategy's own
cutoff — found that every "building" name from the earlier run had flipped to
fading 24 minutes later, none breaking to a new high (WFF 20.9x→0.16x, VERU
3.4x→0.26x, GLBS 1.9x→0.34x, HKIT 2.5x→0.34x). That was recorded as a
weakness of the acceleration signal. Per this article it is at least partly
the expected behavior of the *market* in that window, not only a defect in the
metric: the strategy does not claim to work at 1pm. **Any future test of an
intraday momentum signal should run inside 9:30–11:30am ET before its decay is
attributed to the signal itself.**

*Not from this page:* a "switch from Top Gainer to a High of Day Momentum
Scanner as the day progresses" workflow appeared in search results, but the
article text does not mention it — it belongs to Warrior's separate scanner
pages (`/day-trading-scanners/`, `/how-to-use-stock-scanners/`), unread as of
this entry. Worth reading before building a high-of-day strategy on it.

**Where this conflicts with config.json** (which encodes the YouTube-class
numbers — $2–20 price, <20M float, ≥10% change, ≥5x rel. volume): this page is
looser on relative volume (2x vs 5x) and float (<100M vs <20M), and much
tighter on the move size (20–30% vs 10%). It states no price band at all.
These are two different write-ups of the same house strategy and they do not
agree; treat neither as authoritative and keep config.json's numbers unless
there's a reason to change them.

## daytrading.com — Strategies overview
`https://www.daytrading.com/strategies`
**Status: Live, fetchable.**

Tested 2026-08-11 — full page fetched cleanly, no truncation. A survey
article naming six strategies plus a general risk-management section.
Shallower than the Warrior Trading source (a few sentences per strategy, not
a full walkthrough), but two pieces are concretely new and worth carrying
forward.

**The six strategies, briefly:**
1. **Breakout** — close above resistance = long bias, close below support =
   short bias; price target from the average size of recent swings. No
   numeric thresholds given.
2. **Scalping** — sell the instant a trade is profitable; needs a broker that
   explicitly permits it (worth checking on the Robinhood Agentic account
   before ever building toward this).
3. **Momentum** — "there is always at least one stock that moves 20-30% each
   day"; enter on news + high volume, exit on reversal signs or volume
   drying up. This is the same shape as momentum_scanner.py's Strategy 1,
   just without numeric filters — doesn't add anything config.json doesn't
   already have more precisely.
4. **Reversal / mean reversion** — trade pullbacks against the trend;
   flagged in the article itself as needing more experience than the others.
5. **Pivot points** — classic floor-trader formula: `P = (H+L+C)/3`,
   `R1 = 2P-L`, `S1 = 2P-H`, `R2 = P+(R1-S1)`, `S2 = P-(R1-S1)`. Session
   range often runs between P and the first support/resistance. More a
   forex/futures tool per the article; untested against any of this repo's
   equity candidates so far.
6. **Moving average crossover** — three SMAs (20/60/100 period); buy when
   the 20 crosses above the 60, sell on the cross below; the 100-period line
   sets trend bias (price above it = uptrend context, below = downtrend).
   **This is a direct, more specific version of the trend rule already coded
   into `run.py`'s strategy prompt** (20-day above 50-day = uptrend) — same
   idea, different period pair and an added third line for regime context.
   Worth testing 20/60/100 against the existing 20/50 pair before assuming
   either is better.

**The two genuinely new things, not present anywhere else in this repo:**

- **Position sizing formula, stated generally (1% risk convention, not
  specific to any one strategy):** `position_size = max_risk ÷ (entry_price
  − stop_price)`, with max_risk itself capped at ~1% of account equity per
  trade (their example: £27,500 account → £275 max risk). This is a
  *relative* (% of equity) sizing rule. config.json's
  `risk.max_order_notional_usd` is a flat dollar cap (currently $5) —
  fundamentally different logic (fixed dollar ceiling vs. stop-distance-based
  sizing that shrinks or grows the share count with volatility). Not
  contradictory, just a different risk model; worth deciding deliberately
  which one this repo wants rather than defaulting to the flat-dollar one by
  omission.
- **Two-tier stop-loss:** a mental stop at the point the entry thesis breaks
  (exit criteria, not a price), plus a hard physical stop at the maximum
  tolerable dollar loss. Nothing in this repo currently encodes an exit rule
  tied to *thesis invalidation* rather than price — every stop discussed so
  far (Warrior Trading's 20¢, the momentum scan's pass/fail) is price- or
  filter-based only.

**Not tested against this session's actual data** (WXM, PLAG, GRI, etc.) —
this was a read of the source, not yet an application of pivot points or the
MA crossover to today's candidates. If asked to re-evaluate today's names
against this framework, that's a separate step.

## Michael Sincere — *Start Day Trading Now* (Adams Media, 2011)
Uploaded as EPUB 2026-08-11 (ISBN 1440511861). ~281K chars, read in full.
**Status: Educational, not a feed. The most directly relevant book-length
source logged so far — and it contradicts this repo's current setup in two
places that matter.**

### ~~THE BLOCKER: Pattern Day Trader rule~~ — OBSOLETE, see correction

The book's PDT chapter (>4 day trades in 5 business days ⇒ $25,000 minimum
equity, 90-day freeze as penalty) **is no longer current law.** Verified by
web search 2026-08-11:

- **2026-04-14** — SEC approved FINRA's amendments to Rule 4210.
- **2026-06-04** — rule took effect. The **$25,000 minimum equity requirement
  and the "pattern day trader" designation itself are both eliminated**; day
  trades are no longer counted.
- Replaced by **proportional margin requirements** — equity must be
  proportional to actual intraday market exposure during the session, rather
  than a flat account-size gate.
- **Brokerages have until 2026-10-20 (18 months) to implement.** So whether
  the new framework is live *at Robinhood specifically* is a separate
  question from whether it is law. Worth confirming before relying on it.

**Two corrections to my own earlier analysis, not just the book's:**

1. Sincere's book is 2011. Its regulatory content is 15 years stale and
   should not be treated as current on *any* rule — check anything
   regulatory against a live source before acting on it. (I initially logged
   the PDT constraint as a live blocker; that was wrong.)
2. More fundamentally: **PDT applied to margin accounts. This is documented
   as a cash account.** So PDT was likely never the operative constraint here
   even before the repeal — I conflated it with the real one.

**The constraint that does still apply, and is unaffected by this change:**
cash-account settlement. Same-day round trips on unsettled funds cause
good-faith violations regardless of PDT — that limit comes from Reg T
settlement mechanics, not Rule 4210, and is already documented in the
Warrior Trading entry above. The 2024 move to T+1 speeds up when capital
frees up; it does not permit same-day round trips.

### The cheap/illiquid question — separate the regulation from the mechanics

The PDT correction above does **not** transfer to the book's penny-stock
advice, because the two are different kinds of claim. PDT was a *rule*, and
rules get repealed. Bid/ask spread and halt risk are *market mechanics* —
they don't have an effective date.

That said, the book's "under $3" line is a 2011 heuristic and shouldn't be
treated as a threshold either. The defensible version is the mechanism, and
this session produced direct evidence for it rather than needing the book:

- **WXM halted 9:44am and PLAG halted ~11:25am on 2026-08-11** — both were
  full scanner passes, both sub-$10, neither had any confirmed news.
- **TISI quoted $21.55 bid / $22.55 ask** — a ~4.5% spread on a $22 stock.
  On a $28 account that spread is a larger cost than most realistic edges.

So the actionable takeaway is not "avoid stocks under $3" — it's **measure
spread and halt exposure directly instead of proxying them with a price
floor.** A max-spread-percent filter does that honestly; `min_price: 2.0`
only does it by accident, and (per the PLAG entry) also silently excluded a
name that ran while it was below the floor.

One open question raised by the new margin framework: it ties requirements
to **intraday exposure** rather than account size, which in principle could
make volatile, wide-spread names *more* expensive to hold than they were
under the flat-$25K regime. Unverified — worth checking against Robinhood's
actual implementation before assuming either direction.

### THE CONFLICT: the book says avoid exactly what our scanner surfaces

> "When looking for stocks to buy, avoid the cheap or illiquid stocks."
> "If you see a wide spread, you're either in the after-hours market or
> you're looking at a **penny stock trading for under $3**. As a day trader,
> you need liquid stocks, which is why you want to **avoid most penny
> stocks**."

config.json's `momentum_scan.min_price` is **$2.00**. Every full pass the
scanner produced on 2026-08-11 sat in or near the band this book tells you
to avoid — PLAG $2.57, GRI $2.13, WXM $8.01 (thin 577K float), and the
near-misses WAFU $1.74 / AIHS $1.79 were rejected *only* for being too
cheap. Two of those (WXM, PLAG) halted the same session.

The book also gives the diagnostic that would have flagged this
independently: **a wide bid/ask spread is the tell for illiquidity.** Live
example from the same session — TISI quoted **$21.55 bid / $22.55 ask, a
$1.00 spread on a $22 stock (~4.5%)**. Nothing in momentum_scanner.py looks
at spread at all; `get_equity_quotes` returns bid/ask and it is currently
ignored. **Cheapest available improvement to the scanner: add a
max-spread-percent filter.** It is a better liquidity proxy than either the
price floor or the volume minimum, and it is one field away.

Sincere's own target profile is different from Warrior Trading's: stocks
that move **2-5% intraday** (he names APC, AIG, TTWO, BCSI as examples) —
*not* the 20-30%+ low-float movers. Both books are "momentum day trading";
they disagree about what to point it at.

### Rules worth adopting regardless of the above

*Risk:* minimum **1:2 risk-reward, 1:3 better** — with the honest caveat
"as a day trader this may not always be realistic." Before entry, **the most
important calculation is what to do if you're wrong** (position size follows
from the stop, not the other way round). Never hold a losing stock overnight
hoping it recovers. **Do not carry a hard stop overnight** — gap-down risk
fills it far below the stop.

*Orders:* limit orders, not market orders — a market order in a fast tape can
fill "10, 15, or 20 points lower than you anticipated." Scale in (buy half,
add the rest only if it works). One pro (Kurisko) uses a conditional order
that won't trigger **until the market has been open at least 10 minutes**,
avoiding the opening auction — relevant given the 9:35am scan runs.
Toni Turner: place the protective stop **immediately on entry**, not later.

*Exits:* "When in doubt, get out" — the moment you first think about selling
is the signal. Trailing stop: after a 2-point gain, move the stop to +1 to
lock profit, then raise in ~$0.50 increments. **Cockroach theory** — one bad
piece of news about a position implies more you can't see yet.

*Indicators (defaults he teaches):* RSI 14-period, >70 overbought / <30
oversold, with 9-period and even 2-period as day-trading variants; explicitly
"guidelines, not fixed rules." MACD = 12/26 EMA difference with a 9-period
signal line; buy on cross above signal or above zero. Bollinger Bands default
(20, 2); band squeeze = low volatility, expansion = high; piercing a band is
"pay attention," *not* an actionable trade by itself. MA crossover: 8-day
above 13-day as a buy signal; on intraday charts use *period* not *day*
(20-period, 50-period). Timeframes: 5/15/30/60-minute intraday; one pro
deliberately uses an **8-minute** chart to "get off the fives" where everyone
else is looking.

*Expectations:* **"No more than 5 percent of people who try make a
consistently profitable living as a day trader."** And the Jim Rogers quote
he closes on — do nothing until there is something to do.

### What this does NOT resolve
The book predates (2011) the current market structure and says nothing about
trading halts, which is the single most consequential thing observed in live
testing on 2026-08-11 (WXM and PLAG both halted; PLAG then reopened +71%).
Its "avoid penny stocks" guidance points away from the names that halt, but
it offers no framework for what to do when one is already in play.

## Also available (not from a user-provided link)

- **Robinhood connector** (`get_earnings_calendar`, `get_earnings_results`,
  `get_financials`) — earnings dates/results and fundamentals for specific
  symbols. Already wired into research; see README.
- **General WebSearch** — works for "what's happening with X today" style
  queries; quality varies by query specificity.
