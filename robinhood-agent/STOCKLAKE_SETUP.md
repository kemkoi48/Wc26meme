# Stocklake Pro Setup

You have access to Stocklake Pro API to verify catalysts and detect insider trading signals. This guide explains how to set it up and use it with the manual on/off toggle.

## 1. Get Your API Key

1. Go to https://stocklake.com and log in with your account
2. Navigate to **Settings** → **API** → **Pro Tier**
3. Generate or copy your API key (it starts with `sk_` or similar)
4. Keep this key private — never commit it to git

## 2. Configure Your Environment

Copy the existing `.env.example` to `.env` and add your key:

```bash
cp .env.example .env
```

Edit `.env` and find the line:

```
STOCKLAKE_API_KEY=
```

Paste your key:

```
STOCKLAKE_API_KEY=sk_your_actual_key_here_never_commit_this
```

**Security:** `.env` is in `.gitignore` and will never be committed to the repository.

## 3. Test the Connection

Test cache-only mode (no API calls):

```bash
python3 stocklake_screener.py --symbol AAPL --disable
```

You should see either cached results or a message that the cache is empty.

Test with API enabled (costs 1 quota call):

```bash
python3 stocklake_screener.py --symbol AAPL --enable
```

If successful, you'll see:
- Recent insider transactions (buys/sells/exercises)
- Research verdict (BULLISH / BEARISH / NEUTRAL)
- Latest news catalyst
- Timestamp of when data was fetched

## 4. Using the Manual Toggle

### Recommended workflow:

**Daily check (cache only, no cost):**
```bash
# Check your open positions before market open
python3 stocklake_screener.py --symbols AEYE,HHS --disable
```

**Weekly deep dive (enable refresh):**
```bash
# Update research on all candidates once per week
python3 stocklake_screener.py --symbols AEYE,HHS,SMWB,RSKD --enable
```

**On suspicion (emergency check):**
```bash
# If a position looks about to reverse, check insider flow immediately
python3 stocklake_screener.py --symbol AEYE --enable
```

### Understanding the toggle:

- **`--enable`**: Fetch fresh data from API. Costs 1 quota call per symbol. Use when you want the latest insider activity and news.
- **`--disable`** (or omit, this is the default): Use cache only. Zero quota cost. Works as long as data is <24h old.
- **Quota limit**: Stocklake Pro gives you 5000 API calls per day. At 1 call per symbol, that's enough for ~5000 symbols daily. The toggle prevents accidentally burning your quota like ChatGPT was doing (every 10 minutes).

## 5. Interpreting Results

### Insider Activity

Look for a **trend** field in each transaction:
- `accumulation`: Insiders are buying (bullish signal)
- `distribution`: Insiders are selling (bearish signal, especially in small caps)
- `neutral`: Mixed or ambiguous activity

**Rule:** If you see insider `distribution` (selling) on a small-cap candidate, it's often a halt precursor. Rule 1 (name the news) may catch it, but Stocklake gives you an earlier warning.

### Research Verdict

- `BULLISH`: Tape, insider flow, and sentiment align positively
- `BEARISH`: Red flags (insiders selling, tape rejecting catalyst, negative sentiment)
- `NEUTRAL`: Mixed or no strong signal

**Example (2026-08-13 MLTX):** get_signals said LONG (Phase 3 positive), but research said BEARISH (insiders sold $6.1M, tape down 5% on the headline, -72.5% from 52-week high). Research was right; the headline was a trap.

### Coverage Notes

- **Large caps** (AAPL, MSFT, QQQ, SPY): Full data, all fields populated
- **Small caps** (SMWB, RSKD, AEYE, HHS): Often missing. If you see `error: symbol_not_found`, Stocklake doesn't cover that ticker yet. Fall back to Stocktwits and Robinhood fundamentals for catalyst check.

## 6. Common Issues

**"Daily quota exhausted" after a few calls**

This means someone (maybe the ChatGPT screener, or another tool) burned the 5000/day limit. Wait until tomorrow UTC, or ask the account owner to upgrade to a higher quota tier.

**"Symbol not found"**

Stocklake covers ~3,501 symbols (mostly large/mid caps). Our day-trade picks are often micro-caps outside that universe. This is expected; use Stocktwits + Robinhood for catalyst check instead.

**"API key not set in .env"**

Make sure:
1. `.env` file exists in the `robinhood-agent/` directory
2. The file contains `STOCKLAKE_API_KEY=sk_...` (not blank)
3. You ran `cp .env.example .env` and edited it

**Cache older than expected**

Cache is valid for 24 hours. If you see "Cached: 2 days ago", the data is stale. Run with `--enable` to refresh:

```bash
python3 stocklake_screener.py --symbol AEYE --enable
```

## 7. Integrating with Trade Screening

Before adding a new candidate to your watch list:

```bash
# Check if there's insider distribution or negative research
python3 stocklake_screener.py --symbol NEWCANDIDATE --disable
```

If you see:
- Insider `distribution` trend → Risk/reward shifts. Ask "what do insiders know that I don't?"
- Research `BEARISH` verdict → Usually means tape is rejecting the catalyst, even if news looks good
- Recent halt or trading halt in notes → This is what stops don't prevent; rule 1 (name the news) is your defense

## 8. Next Steps

Once configured:
1. Add daily cache-only checks to your pre-market routine
2. Use `--enable` sparingly (weekly or on suspicion)
3. Log findings in `sources.md` if you discover a pattern (e.g., "insider distribution always precedes X-day halt")
4. Report quota issues so the ChatGPT screener can be fixed (it should not be burning 5000/day)
