# Quickstart — no programming knowledge needed

You don't need to know Python. You'll paste a few commands into a terminal and
edit two small text files. That's it.

**What's a terminal?** A window where you type commands.
- **Mac:** press `Cmd+Space`, type `Terminal`, press Enter.
- **Windows:** install "Git Bash" (comes with https://git-scm.com/download/win),
  then open **Git Bash** from the Start menu. Use Git Bash for every step here.

## Step 1 — Install two free programs (one time)

1. **Python** — https://www.python.org/downloads/ → big yellow button.
   **Windows: tick the box "Add python.exe to PATH"** during install.
2. **Node.js** — https://nodejs.org → the LTS version.

## Step 2 — Get the code and set it up (one time)

Open a terminal and paste these lines one at a time (press Enter after each):

```
git clone https://github.com/kemkoi48/Wc26meme.git
cd Wc26meme/robinhood-agent
bash setup.sh
```

The setup script checks everything, installs what's needed, and creates a
settings file called `.env`. If it prints an error, it tells you exactly what to
install and you just run `bash setup.sh` again.

## Step 3 — Fill in your settings (one time)

Two files to edit. Open them with any text editor (Notepad / TextEdit works —
on Mac, TextEdit must be in plain-text mode: Format → Make Plain Text).

**File 1: `.env`** (it's inside the `robinhood-agent` folder; it may be hidden —
in the terminal you can open it with `open -e .env` on Mac or `notepad .env` on
Windows). Fill in the three lines:

```
ROBINHOOD_ACCESS_TOKEN=paste-your-token-here
ROBINHOOD_ACCOUNT_NUMBER=432805174
ANTHROPIC_API_KEY=paste-your-anthropic-key-here
```

- The **Robinhood token** comes from the Robinhood app: enable Agentic Trading
  and authorize an agent (Robinhood's setup shows the token).
- The **account number** is your "Agentic" account (the one agents may trade).
- The **Anthropic key** comes from https://platform.claude.com (API keys).

**File 2: `config.json`** — find the line

```
"symbol_allowlist": [],
```

and put the stock symbols you allow between the brackets, in quotes:

```
"symbol_allowlist": ["AAPL", "VOO"],
```

(Leave it empty and the bot refuses every trade — that's a safety feature.)

## Step 4 — Test it (safe — cannot place real orders)

```
bash start.sh
```

This runs ONE cycle in **dry run**: the agent looks at the market and says what
it *would* do, but every real order is blocked. Read what it prints. A file
called `audit.jsonl` appears, listing every action it attempted and whether the
safety guard allowed it.

Do this a few days in a row. Only continue when what it proposes looks sane.

## Step 5 — Going live (real money — read this twice)

```
bash start.sh live
```

It asks you to type `YES` first. "Live" means real orders, real money, within
the limits in `config.json` (per-order dollar cap, orders per day, allowlist).
Start tiny. You can stop a running loop any time with `Ctrl+C`.

To keep it running on a schedule (`bash start.sh loop` / `bash start.sh live loop`)
the computer must stay on. See `deploy/` and the README's Deploying section when
you're ready for that.

## If something goes wrong

- **"command not found: git"** → install Git: https://git-scm.com/downloads
- **"Python is not installed"** → Step 1, then `bash setup.sh` again.
- **The agent reports auth problems / needs-auth** → your Robinhood token
  expired. Get a fresh one in the Robinhood app and update `.env`.
- **It refuses every trade** → that's usually the allowlist being empty
  (Step 3, File 2) or dry-run doing its job.
- Ask Claude — paste the error message and the contents of `audit.jsonl`.
