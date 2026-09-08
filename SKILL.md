---
name: margin-health-copilot
description: Use this skill when the user is connected to the Binance Agent OS MCP server and asks about their margin/position risk, margin level, liquidation distance, or "how exposed am I". Read-only — this skill never places, modifies, or cancels an order; it only reads account and market data and narrates risk.
---

# Margin Health Copilot

**Status:** Session 3 complete. Primary capability is Cross Margin health,
calibrated against a real live account call. Futures isolated-margin
support exists (Session 2) but is unverified — Futures API access was
confirmed blocked on the connected account.

## What this skill does

**Cross Margin (primary, live-verified):** reads the connected account's
real margin level via Binance's Account (read-only) scope and narrates how
close it is to a margin call (~1.3x) or forced liquidation (~1.1x), in
plain English.

**Futures isolated-margin (Session 2, unverified):** given a position's
entry price, size, and leverage, derives an estimated liquidation price
and runs adverse-scenario stress tests. Built and unit-tested against mock
data only — this account's Futures API access returned a permissions
error on every endpoint tried, so this path has never been exercised
against real data. Documented honestly as unverified rather than presented
as working.

## What this skill never does

- Never places, modifies, or cancels an order.
- Never requests the Trade or Transfer scopes — Account (read-only) and
  Market Data are all it needs.
- Never invents a margin level or liquidation price — if the account
  carries no debt, it says so plainly rather than fabricating a ratio.

## How to use it

1. Confirm the Binance Agent OS connector is enabled (Settings →
   Connectors in claude.ai, or `/mcp` in Claude Code) with at least
   **Account (read-only)** access granted.
2. Ask something like: "How's my margin account looking?" or "Am I close
   to a margin call?"
3. The skill calls the account tool, passes the result to
   `scripts/cross_margin_health.py`, and narrates the output.

## Data contract (confirmed live, not guessed)

`margin.queryCrossMarginAccountDetails` returns: `marginLevel`,
`totalAssetOfBtc`, `totalLiabilityOfBtc`, `totalNetAssetOfBtc`,
`tradeEnabled`, `transferEnabled`, `userAssets[]` (`asset`, `free`,
`locked`, `borrowed`, `interest`, `netAsset`). Captured directly from a
live call during Session 3 — see `fixtures/live_cross_margin_snapshot.json`.

## Known open items

- Margin call (1.3x) and liquidation (1.1x) thresholds are Binance's
  long-standing public levels, not re-verified against a live non-zero
  account state (the connected account currently carries no debt).
- Futures access remains blocked on this account; if it's ever enabled,
  Session 2's engine is ready to be calibrated the same way Session 3
  calibrated this one.
