# Margin Health Copilot

**A read-only AI skill for Binance Agent OS that turns a live margin account into a plain-English early-warning system for liquidation risk. It watches and explains — it never trades.**

Built for the Binance Agent OS Mini Hackathon (Track A).

📺 **Demo video:** _[add link here after recording]_
🔗 **Live connector:** `https://agent.binance.com/mcp/agentic`

---

## What it does

Margin Health Copilot connects to a real Binance account through the Binance Agent OS MCP server and, on request, reads the account's actual margin level and explains — in plain English — how close it is to a margin call (~1.3x) or forced liquidation (~1.1x), including what a given adverse price move would do to that distance.

```
> How's my margin account looking?

Margin level is 1.25x (in margin call territory). Margin call sits
around 1.3x (-3.8% away), and forced liquidation around 1.1x
(+13.6% away).
```

It only ever reads. It never places, modifies, or cancels an order, and it never requests the Trade or Transfer scopes — Account (read-only) and Market Data are all it asks for. Withdrawal access isn't available to it regardless, by Binance's own design.

## Engineering notes (the honest version)

This project was originally scoped around Binance Futures isolated-margin positions, with a liquidation-price calculator derived from first principles (`scripts/margin_health.py`). Partway through the build, Futures API access turned out to be blocked on the demo account — confirmed across four different endpoint variants, all returning the same permissions error, ruling out a single-endpoint fluke.

Rather than fake a workaround, the live path pivoted to Binance's Cross Margin product (`scripts/cross_margin_health.py`), which authorized successfully. That engine is calibrated against a **real captured response** from a live account call — the field names in the code aren't a guess from the docs, they're copied from what Binance actually returned (see `fixtures/live_cross_margin_snapshot.json`).

The Futures engine remains in the repo, built and unit-tested against mock data, ready to be calibrated the same way if Futures access ever becomes available. It's marked as unverified rather than presented as working.

Full diagnostic trail, decision log, and session-by-session build history: `SESSION_REPORT.md`, `BUILD_ROADMAP.md`, `RESEARCH_BRIEF.md`.

## Replicate it

1. **Get the code** — clone this repo.
2. **Verify it offline first** (no live account needed):
   ```
   python3 -m unittest discover -s tests -v
   ```
   14 tests, standard library only, zero install — runs against the real captured snapshot and a clearly labeled illustrative at-risk scenario.
3. **Connect Binance Agent OS** — in claude.ai or Claude Desktop: Settings → Connectors → Add custom connector → `https://agent.binance.com/mcp/agentic`. In Claude Code: `/mcp`.
4. **Authorize on Binance** — grant only **Account (read-only)** and **Market data**.
5. **Load the skill** — Claude Code: copy `SKILL.md` and `scripts/` into `.claude/skills/margin-health-copilot/`. claude.ai: upload as a custom Skill (Settings → Features, needs a paid plan with code execution) or simply attach/paste `SKILL.md` into the conversation.
6. **Ask it** — "How's my margin account looking?"

## Structure

```
margin-health-copilot/
├── SKILL.md                             — skill definition loaded by Claude Code/Desktop/claude.ai
├── scripts/
│   ├── cross_margin_health.py           — live-verified engine (primary path)
│   └── margin_health.py                 — Futures engine (built, unit-tested, access-blocked)
├── fixtures/
│   ├── live_cross_margin_snapshot.json  — real captured live response
│   ├── mock_cross_margin_at_risk.json   — illustrative at-risk scenario (labeled, not live)
│   ├── mock_account.json                — Futures mock data
│   └── mock_market.json                 — Futures mock data
├── tests/
│   ├── test_cross_margin_health.py      — 7 tests, including against the real snapshot
│   └── test_margin_health.py            — 7 tests, all against mock data
├── DEMO_SCRIPT.md                       — video walkthrough script
├── RESEARCH_BRIEF.md                    — Session 0 research and scoping
├── BUILD_ROADMAP.md                     — the fixed session plan
└── SESSION_REPORT.md                    — latest build session's full report
```

## Safety

Read-only by design, on top of Binance's own guardrails (no withdrawal scope ever, every write confirmed by the user first). This skill goes further and simply never requests write scopes at all — there's nothing here that can touch funds.
