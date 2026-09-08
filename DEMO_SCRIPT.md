# Demo Script & Submission Notes — Margin Health Copilot

Note: I couldn't find Binance's official time limit or format spec for
the Track A video demo (see the open item in RESEARCH_BRIEF.md). ~2-3
minutes is a safe default for hackathon demos generally — trim to fit if
you find an actual limit before submitting.

## Script

**[0:00–0:15] Hook**
Say something like: "Binance's Agent OS gives an agent live access to
your account, but only read scopes are actually safe to hand an AI by
default. This is Margin Health Copilot — it reads your margin account
and tells you, in plain English, how close you are to a margin call.
It never places a trade."

**[0:15–0:45] Show the live connection**
Screen-record asking the skill something like "How's my margin account
looking?" in a client with the Binance Agent OS connector enabled. Let
the real tool call happen on screen. Say while it loads: "This is a live
call to my actual Binance account right now — nothing mocked."

**[0:45–1:15] Narrate the real result honestly**
When it comes back "no debt outstanding," say so plainly: "My account
currently has no borrowed funds, so there's no liquidation risk — and the
skill says exactly that instead of making up a number." This honesty is
itself worth showing — it demonstrates the skill doesn't fabricate risk
where none exists.

**[1:15–2:00] Show the at-risk case**
Say: "To show what it looks like when there IS risk, here's a
constructed example" — then run the illustrative fixture
(`fixtures/mock_cross_margin_at_risk.json`) through
`scripts/cross_margin_health.py` on screen (a simple terminal command
works fine, e.g. the snippet the Session 3 build used to print output).
Be explicit on camera that this is a labeled hypothetical, not a real
position — that transparency is part of the pitch, not a weakness to
hide.

**[2:00–2:30] Prove it's tested**
Run `python3 -m unittest discover -s tests -v` on screen — 14 tests
passing, zero external dependencies. Mention briefly: built against a
Futures engine too (Session 2), parked because Futures API access wasn't
available on this account — shows the pivot was a real engineering
decision, not a missed feature.

**[2:30–2:45] Close**
"Read-only, no trade scope, works today against Binance's real Agent OS
MCP server." End on the GitHub repo URL or your name/handle.

## Suggested repo name & description

- **Repo name:** `margin-health-copilot`
- **One-line description:** "Read-only Binance Agent OS skill that turns your live margin account into a plain-English liquidation early-warning system — no trades, ever."

## Suggested submission blurb

> Margin Health Copilot is a read-only Claude Skill for Binance Agent OS.
> It reads your Cross Margin account's real margin level and narrates how
> close you are to a margin call (~1.3x) or forced liquidation (~1.1x) in
> plain English — no trading, no external data feeds, just Binance's own
> live account data. Built and calibrated against a real live account
> call during development; a Futures isolated-margin engine also ships
> in the repo, built and unit-tested, pending Futures API access on the
> demo account.

## Pre-submission checklist

- [ ] Record and upload the video demo
- [ ] Push the repo to GitHub (public, so judges can access it)
- [ ] Re-read RESEARCH_BRIEF.md's eligibility note and confirm against Binance's actual terms before submitting
- [ ] Confirm the exact submission mechanism (video demo + GitHub repo link) hasn't changed — the official rules page was never located during this build; a last check is worth the two minutes it costs
- [ ] Submit before September 8, 2026, 23:59 UTC
