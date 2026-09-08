---
name: margin-health-copilot
description: Use this skill when the user is connected to the Binance Agent OS MCP server and asks about their position risk, margin health, liquidation distance, or "how exposed am I" on a specific symbol. Read-only — this skill never places, modifies, or cancels an order; it only reads account/position and market data and narrates risk.
---

# Margin Health Copilot

**Status:** Session 1 scaffold — calculation logic not yet implemented.
See `BUILD_ROADMAP.md`, Session 2.

## What this skill does

Turns a live Binance Agentic sub-account position into a plain-English
early-warning read on liquidation risk — how far the current price is from
a margin call, and what a given price move would do to that distance.

## What this skill never does

- Never places, modifies, or cancels an order.
- Never requests the Trade or Transfer scopes — Market Data and Account
  (read-only) are the only scopes this skill needs.
- Never invents a liquidation price if the account tool doesn't return one
  directly — see "Data contract" below.

## How to use it

1. Confirm the Binance MCP server is connected (`/mcp` in Claude Code) and
   at minimum the **Market data** and **Account** scopes are granted.
2. Ask something like: "How exposed am I on my BTCUSDT position?" or
   "What happens to my margin if BTC drops 10%?"
3. The skill calls the Binance MCP account/position tool and the market
   data tool, passes the results to `scripts/margin_health.py`, and
   narrates the output in plain English.

## Data contract

See the docstring in `scripts/margin_health.py` for the exact shape this
skill expects. **Do not assume the raw MCP tool output matches this shape
until Session 3 has verified it against a live connection** (ruleset
Section 9.8 — new MCP tool behavior is confirmed, never assumed from the
tool name). The field names here are a best-effort guess from Binance's
public product docs, not a confirmed schema.

## Known open item

Whether the account/position tool returns liquidation price directly, or
only raw position fields (entry price, size, leverage) that this skill
must derive liquidation distance from itself using Binance's published
maintenance-margin tier tables. Either path is handled in Session 2's
design — see the Research Brief for the fallback plan.
