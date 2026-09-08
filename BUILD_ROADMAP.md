# Build Roadmap — Margin Health Copilot
**Track:** Binance Agent OS Mini Hackathon, Track A
**Pattern:** Agent-skill (Section 2) — no monorepo, no Supabase, no custom backend
**Deadline:** September 8, 2026, 23:59 UTC

Session 1 — Skill Scaffold — repo structure, skill/system-prompt shell, README, and a mock-data test harness standing in for live Binance data.
Session 2 — Margin Health Engine — liquidation-distance and margin-ratio calculation plus the plain-English scenario narration, built and tested entirely against Session 1's mock data.
Session 3 — Live Connect & Calibrate — **revised in-session**: Futures API access was confirmed blocked on the connected account (three endpoint variants, same permissions error). Pivoted to Binance's Cross Margin product, which authorized successfully; built and calibrated a new engine against a real captured live response. Session 2's Futures engine remains in the repo, unit-tested but unverified.
Session 4 — Demo & Submission — record the video demo, finalize the README, clean the repo, submit for Track A.

## Open Items Carried From Session 0
- [ ] Official judging rubric unconfirmed — proceeding on general criteria (innovation, technical execution, real-world usefulness, presentation).
- [ ] Eligibility/restricted-jurisdiction wording unconfirmed against Binance's own terms.
- [x] Whether the Account tool returns liquidation price/margin ratio directly — resolved for Cross Margin (returns `marginLevel` directly; confirmed live). Remains unconfirmed for Futures since that path is blocked.

## New Open Items From Session 3
- [ ] Futures API access is blocked on this account (permissions error, not a connection error) — root cause unconfirmed (propagation delay / sub-account-specific enablement / stale authorization). Not pursued further given the deadline.
- [ ] Margin call (1.3x) / liquidation (1.1x) thresholds are Binance's well-known public levels, not re-verified against a live non-zero account state.
- [ ] No funded position exists to demo a real at-risk state — Session 4's demo will need to lean on the illustrative fixture for that part, clearly labeled as such.
