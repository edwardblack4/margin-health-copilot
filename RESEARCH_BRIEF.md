# Research Brief — Session 0
**Project:** Margin Health Copilot
**Event:** Binance Agent OS Mini Hackathon
**Date compiled:** 2026-09-05

---

## Idea Lock
- **Track:** Track A — build an AI agent with Agent OS; submit a video demo + GitHub repo.
- **Workflow category:** Data Analysis (read-only — no trade execution, no confirm-before-execute flow needed).
- **Pattern (Section 2):** Agent-skill pattern. No `apps/web`, no `apps/api`, no Supabase. The deliverable is a skill/system-prompt package that runs inside an MCP-connected client (Claude Code / Claude Desktop) against the real Binance Agent OS MCP server. Any web page, if built at all, is a thin display layer for the demo video only.

## One-Line Pitch
A read-only Binance Agent OS skill that turns your live Agentic sub-account's positions into a plain-English early-warning system for liquidation risk — using only Binance's own live account and market data, no trades placed, no external feeds.

## Event Rules (from secondary sources — official rules page not located; verify if you have the direct link)
- Prize pool: $60,000 USDC total, split across two tracks.
- Track A: $20,000 pool — video demo + GitHub repo.
- Track B: $40,000 pool — connect an MCP and trade live; no submission beyond following @Binance, reposting, replying with entry + a completed survey.
- **Deadline: September 8, 2026, 23:59 UTC** — roughly 3 days from today. This is the constraint the whole roadmap below is built around.
- Reported as unavailable to entrants in the US, UK, EEA, Hong Kong, Singapore, or other Binance-restricted jurisdictions — confirm your own eligibility against Binance's actual terms.
- **Open item:** exact published judging rubric not found. Proceeding on the general hackathon pattern (innovation, technical execution/feasibility, real-world usefulness, presentation) until a source turns up.

## Agent OS Feasibility Check (verified directly against Binance's developer docs)
- Live endpoint: `https://agent.binance.com/mcp/agentic`. Connects via Claude Code, Claude Desktop, Codex CLI, ChatGPT, VS Code, or Grok Bot.
- No local install, no API keys stored on-device — auth is a manual, human, browser-based OAuth-style consent step on Binance.com. This cannot be automated or substituted by any build session.
- Scopes relevant to this project: **Market data** (tickers, order books, candlesticks, funding rates — public, no auth) and **Account** (Agentic sub-account balance, positions, bills; optional read-only view of main account).
- **No testnet mode for this flow.** Safety comes from a different mechanism than credential-swapping: withdrawal scope is never available, every write action requires explicit confirmation, and the sub-account holds nothing until the user manually funds it from the main Binance UI. Since this project never writes (Data Analysis only, no trades), this is largely moot for us — but it means Section 9.2's testnet/mainnet credential split does not apply to this build in the way the ruleset assumes.
- **Unverified:** whether the Account/position tool returns liquidation price or margin ratio directly, vs. raw fields we compute from ourselves. Treat as unconfirmed until Session 3's live check (Section 9.8). Fallback plan if not returned directly: derive margin health from position size, entry price, mark price, and leverage against Binance's published maintenance-margin tier tables.

## Prior-Art Check
- A competing entrant has already published a production-style MCP server / trading-execution framework (precision decimal handling, signed trade intents, pre-trade risk checks) as an explicit hackathon submission — the "wrap Binance trading in an MCP server" space is taken.
- Generic "portfolio balance/insights across wallets" and "signal-generating trading bot with TA + sentiment + backtesting" are both common, well-trodden patterns in adjacent crypto-agent hackathons.
- This project differs on both counts: it's read-only, protective rather than predictive, and narrows to one specific mechanical question (how close is this position to a margin call) rather than a general dashboard or a buy/sell signal generator.

## Assumptions Carried Into Session 1
- Building against documented MCP scopes only; no custom backend, no database.
- Sessions 1–2 can be built and tested entirely against mock/sample account data, since live data requires the user's own manual Binance browser consent.
- Judging criteria are assumed generic until/unless the official page is found — if you get the link, share it and the pitch/demo emphasis can be adjusted before Session 4.
