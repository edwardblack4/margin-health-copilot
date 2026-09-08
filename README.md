# Margin Health Copilot

A read-only Claude Skill built for the Binance Agent OS Mini Hackathon (Track A).

It turns a live Binance Agentic sub-account position into a plain-English
early-warning system for liquidation risk. It never places a trade — it only
reads account and market data through the Binance Agent OS MCP server
(`https://agent.binance.com/mcp/agentic`) and narrates what it sees.

## Status

Session 1 of 4 — scaffold only, no live connection yet. See
`BUILD_ROADMAP.md` for what's next and `RESEARCH_BRIEF.md` for the
reasoning behind the build (including why the hackathon's 3-day window
ruled out a full backend/database build in favor of this skill-only shape).

## Structure

```
margin-health-copilot/
├── SKILL.md              — the skill definition Claude Code/Desktop loads
├── scripts/
│   └── margin_health.py  — calculation engine (interface stub — Session 2)
├── fixtures/
│   ├── mock_account.json — sample Agentic sub-account position data
│   └── mock_market.json  — sample market data (ticker, funding rate)
└── tests/
    └── test_margin_health.py — validates fixtures + engine contract
```

## Setup

1. Connect the Binance Agent OS MCP server in Claude Code, Claude Desktop,
   or another supported client (search Binance's developer docs for
   "Binance MCP Server" for the current setup steps).
2. Grant **Market data** and **Account** scopes only — this skill never
   needs Trade or Transfer, and withdrawal is never available on Binance's
   side regardless.
3. Run the test harness locally (no install required — standard library
   only):
   ```
   python3 -m unittest discover -s tests -v
   ```

## Safety

Read-only by design, on top of Binance's own guardrails (no withdrawal
scope ever, every write confirmed by the user first). This skill goes
further and simply never requests write scopes at all.
