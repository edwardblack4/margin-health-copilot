# Build Roadmap — Margin Health Copilot
**Track:** Binance Agent OS Mini Hackathon, Track A
**Pattern:** Agent-skill (Section 2) — no monorepo, no Supabase, no custom backend
**Deadline:** September 8, 2026, 23:59 UTC

Session 1 — Skill Scaffold — repo structure, skill/system-prompt shell, README, and a mock-data test harness standing in for live Binance data.
Session 2 — Margin Health Engine — liquidation-distance and margin-ratio calculation plus the plain-English scenario narration, built and tested entirely against Session 1's mock data.
Session 3 — Live Connect & Calibrate — human connects the real Binance Agent OS MCP server, we confirm what the account/position tool actually returns (Section 9.8), and calibrate Session 2's logic to match reality.
Session 4 — Demo & Submission — record the video demo, finalize the README, clean the repo, submit for Track A.

## Open Items Carried From Session 0
- [ ] Official judging rubric unconfirmed — proceeding on general criteria (innovation, technical execution, real-world usefulness, presentation).
- [ ] Eligibility/restricted-jurisdiction wording unconfirmed against Binance's own terms.
- [ ] Whether the Account/position MCP tool returns liquidation price/margin ratio directly — verify at Session 3, don't assume; fallback calculation plan exists (see Research Brief).
