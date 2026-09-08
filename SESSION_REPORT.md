## Session 1: Skill Scaffold
**Date:** 2026-09-05
**Goal:** Stand up the repo structure, skill definition shell, README, and mock-data test harness for the Margin Health Copilot.

**Files added/changed:**
- SKILL.md — skill definition Claude Code/Desktop will load; logic marked not-yet-implemented
- scripts/margin_health.py — calculation engine interface stub (raises NotImplementedError by design)
- fixtures/mock_account.json — sample Agentic sub-account position data (2 positions)
- fixtures/mock_market.json — sample market data (mark price, funding rate) for both symbols
- tests/test_margin_health.py — validates fixtures load correctly and the stub raises as expected
- README.md — project overview and setup
- .gitignore

**Current full file tree:**
```
margin-health-copilot/
├── .gitignore
├── BUILD_ROADMAP.md
├── README.md
├── RESEARCH_BRIEF.md
├── SESSION_REPORT.md
├── SKILL.md
├── fixtures/
│   ├── mock_account.json
│   └── mock_market.json
├── scripts/
│   └── margin_health.py
└── tests/
    └── test_margin_health.py
```

**Dependencies installed:**
- None. Switched from a planned pytest dependency to Python's built-in
  `unittest` — this sandbox has no network access to actually verify a
  pytest install, and the ruleset (Section 6, #9) says a new dependency
  gets verified before it's trusted, not assumed. Standard library only
  means this also runs with zero setup for you or for judges.

**Supabase schema state:**
- N/A — Agent-skill pattern, no database (Section 2).

**Env vars required:**
- None yet, and Session 3 likely won't need any either — the Binance MCP
  connection is a manual, human, browser-based OAuth-style consent step,
  not an API key (see Research Brief).

**Agent OS mode:** N/A this session — no live connection made; all work
verified against mock fixtures only.

**Sub-account scope & limits:** Planned scopes: Market data (read) +
Account (read) only. No Trade, no Transfer requested. No spend/position
limits needed — this skill never writes, so Section 9.4 doesn't apply.

**Decision log (this session, if any live/testnet actions were taken):**
- None — no live or testnet actions taken this session.

**API endpoints live:**
- None — Agent-skill pattern, no apps/api (Section 2).

**Known stubs/mocks/TODOs:**
- `analyze_position()` in scripts/margin_health.py deliberately raises
  `NotImplementedError` — real math lands in Session 2.
- SKILL.md's "Data contract" section and the `Position`/`MarketSnapshot`
  TypedDicts in margin_health.py are a best-effort guess from Binance's
  public product docs, unconfirmed against a live tool call.

**Assumptions carried into next session:**
- Mock fixture shapes (mock_account.json / mock_market.json) approximate
  what the real Binance MCP account/position and market-data tools return,
  but this is NOT confirmed. Session 3 must verify actual field names
  before Session 2's math is trusted against real data (ruleset Section
  9.8 — new MCP tool behavior is confirmed, never assumed).
- Whether the account/position tool returns liquidation price directly is
  still open. Session 2's engine should be designed to handle either case
  (see fallback plan in RESEARCH_BRIEF.md) rather than assuming one.
- Deadline: September 8, 2026, 23:59 UTC — 3 sessions plus a demo recording
  remain after this one.

**Style history (only present on UI-touching sessions):**
- N/A — no UI-touching work this session.
