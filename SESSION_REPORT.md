## Session 3: Live Connect & Calibrate (revised in-session — pivoted to Cross Margin)
**Date:** 2026-09-06
**Goal (as planned):** Connect the real Binance Agent OS MCP server, confirm what the account/position tool actually returns, calibrate Session 2's Futures engine to match.
**Goal (as executed):** Same intent, different product — Futures access was blocked, so the live-calibration work happened against Cross Margin instead.

**Diagnostic trail (in order):**
1. Connector confirmed live and authenticated: `spot.exchangeInfo` (public, no auth) returned real data immediately.
2. `futures_usds.positionInformationV2` → `{"code":-2015,"msg":"Invalid API-key, IP, or permissions for action"}`.
3. `futures_usds.futuresAccountBalanceV3` → same error.
4. `futures_usds.accountInformationV3` → same error.
5. `futures_coin.accountInformation` → same error. Four Futures-specific endpoints, identical permissions error each time — ruled out a single-endpoint fluke.
6. `spot.getAccount` → succeeded, real account data (real `uid`, real commission rates, `canTrade: true`).
7. `margin.queryCrossMarginAccountDetails` → succeeded, real data (`marginLevel: "999"`, all zero balances, `created: false`).
8. `wallet.accountStatus` → succeeded (`"Normal"`).
9. User confirmed no funds available to deposit, and confirmed Futures activation was attempted on Binance's side — re-tested all three Futures variants again post-activation; identical error persisted. Root cause not confirmed (possible: propagation delay, sub-account-specific Futures enablement separate from the main account, or the connector authorization predating the Futures activation and needing to be redone) — not pursued further given the deadline.

**Decision:** Pivot the live/primary path from Futures isolated-margin (Session 2) to Binance Cross Margin, which is authorized and returns real data right now. This is a genuine scope revision, not a routing-around of the blocker — logged here per the ruleset rather than silently changed.

**Files added/changed:**
- scripts/cross_margin_health.py — new engine, real field names copied verbatim from a live call (not guessed): `marginLevel`, `totalAssetOfBtc`, `totalLiabilityOfBtc`, `totalNetAssetOfBtc`, `tradeEnabled`, `transferEnabled`, `userAssets[]`
- fixtures/live_cross_margin_snapshot.json — the actual captured live response (userAssets trimmed from ~360 real entries to BTC/ETH/USDT; every field verbatim)
- fixtures/mock_cross_margin_at_risk.json — illustrative at-risk scenario, explicitly labeled non-live, built to exercise the margin-call branch the real (debt-free) account can't demonstrate
- tests/test_cross_margin_health.py — 7 tests: real snapshot, illustrative scenario, and constructed boundary values for all four status thresholds
- SKILL.md — rewritten: Cross Margin is now the primary, live-verified capability; Futures marked explicitly as built-but-unverified
- README.md, BUILD_ROADMAP.md — updated to reflect the pivot

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
│   ├── live_cross_margin_snapshot.json
│   ├── mock_account.json
│   ├── mock_cross_margin_at_risk.json
│   └── mock_market.json
├── scripts/
│   ├── cross_margin_health.py
│   └── margin_health.py
└── tests/
    ├── test_cross_margin_health.py
    └── test_margin_health.py
```

**Dependencies installed:** None (standard library only, unchanged).

**Supabase schema state:** N/A — Agent-skill pattern, no database.

**Env vars required:** None — connector auth is browser-based OAuth-style consent, confirmed in practice this session (no API key ever touched this conversation).

**Agent OS mode:** LIVE. Real tool calls made this session: `spot.exchangeInfo`, `spot.getAccount`, `margin.queryCrossMarginAccountDetails` (x2), `wallet.accountStatus`, plus 4 failed Futures calls (documented above). All calls were read-only (USER_DATA/public endpoints) — nothing was written, no trade or transfer attempted.

**Sub-account scope & limits:** Confirmed in practice: Account (read-only) access works for Spot and Margin; Futures blocked. No Trade/Transfer used or needed.

**Decision log:**
- Pivoted primary product from Futures to Cross Margin (reasoning above). Session 2's Futures engine is kept in the repo, not deleted — it's real, tested work, just unverified against live data given the access blocker.

**API endpoints live:** None — Agent-skill pattern, no apps/api. (Binance MCP tool calls are not "our" API, they're the live external verification target.)

**Known stubs/mocks/TODOs:**
- `mock_cross_margin_at_risk.json` is explicitly illustrative — no real at-risk state exists on the connected account (zero debt everywhere). Session 4's demo needs to present this honestly as a constructed scenario, not imply it's live.
- Margin call (1.3x) / liquidation (1.1x) thresholds are well-known public Binance levels, not re-confirmed against a live non-zero margin level.
- Futures access root cause is unconfirmed — noted as an open item, not chased further given the deadline.

**Assumptions carried into next session:**
- Session 4's demo should show the real live "no debt" call first (proves genuine connectivity and correct handling of Binance's sentinel value), then walk through the illustrative at-risk scenario clearly labeled as such, rather than presenting one as if it were the other.
- Deadline: September 8, 2026, 23:59 UTC — 1 session (demo + submission) remains.

**Style history:** N/A — no UI-touching work this session.
