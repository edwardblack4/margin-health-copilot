# Margin Health Copilot

A read-only Claude Skill built for the Binance Agent OS Mini Hackathon (Track A).

It reads a connected Binance account through the Binance Agent OS MCP server
(`https://agent.binance.com/mcp/agentic`) and narrates margin/liquidation
risk in plain English. It never places a trade.

## Status

Session 3 of 4 — pivoted from Futures to Cross Margin after confirming
Futures API access is blocked on the connected account (three endpoint
variants tried, identical permissions error each time). Cross Margin
health is now calibrated against a real live account call. See
`SESSION_REPORT.md` for the full diagnostic trail and `RESEARCH_BRIEF.md`
for the reasoning behind the original build shape.

## Structure

```
margin-health-copilot/
├── SKILL.md                             — skill definition loaded by Claude Code/Desktop/claude.ai
├── scripts/
│   ├── cross_margin_health.py           — LIVE-VERIFIED engine (Session 3, primary path)
│   └── margin_health.py                 — Futures engine (Session 2, unverified — access blocked)
├── fixtures/
│   ├── live_cross_margin_snapshot.json  — real captured live response
│   ├── mock_cross_margin_at_risk.json   — illustrative at-risk scenario (labeled, not live)
│   ├── mock_account.json                — Futures mock data (Session 1/2)
│   └── mock_market.json                 — Futures mock data (Session 1/2)
└── tests/
    ├── test_cross_margin_health.py      — 7 tests, including against the real snapshot
    └── test_margin_health.py            — 7 tests, all against mock data
```

## Setup

1. Add the Binance Agent OS MCP server as a custom connector (Settings →
   Connectors in claude.ai/Claude Desktop, or `/mcp` in Claude Code) —
   URL: `https://agent.binance.com/mcp/agentic`.
2. Grant **Account (read-only)** and **Market data** scopes only — this
   skill never needs Trade or Transfer, and withdrawal is never available
   on Binance's side regardless.
3. Run the test harness locally (no install required — standard library
   only):
   ```
   python3 -m unittest discover -s tests -v
   ```

## Safety

Read-only by design, on top of Binance's own guardrails (no withdrawal
scope ever, every write confirmed by the user first). This skill goes
further and simply never requests write scopes at all.
