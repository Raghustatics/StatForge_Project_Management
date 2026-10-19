# Decision Log

Format: ID · Date · Decision · Reason · Approved by. Scope moves between gates **must** be logged here before they happen.

| ID | Date | Decision | Approved by |
|---|---|---|---|
| D-001 | 2026-10-19 | StatForge is a new clean product; the PMO app stays internal | Owner |
| D-002 | 2026-10-19 | Owner states personal ownership of the PMO app code; reuse allowed (keep written confirmation) | Owner |
| D-003 | 2026-10-19 | Positioning: guided problem-solving; learning by doing; human-centred assistance for real-world official work | Owner |
| D-004 | 2026-10-19 | BYO AI (API key or Ollama), free first, entitlements only, no billing | Owner |
| D-005 | 2026-10-19 | R1 analysis: profiling/EDA/graphs, tests, regression/ANOVA, SPC, capability, template calculators | Owner |
| D-006 | 2026-10-19 | R1 project: methodology engine, Kanban/to-do/next steps, KPIs/OKRs, Gantt/CPM/registers | Owner |
| D-007 | 2026-10-19 | Gates soft by default, hard optional; a skipped step is never done | Owner |
| D-008 | 2026-10-19 | Outlook Copilot Gateway: optional opt-in plugin in R1, with conditions | Owner |
| D-009 | 2026-10-19 | Reuse: port Python engines; new React IDE shell; PostgreSQL | Owner |
| D-010 | 2026-10-19 | Methodologies: Lean, Discovery, DMAIC (source) + drafted DMADV/DFSS, PDCA, 8D, A3, Kaizen, MoM, Action Plan, generic stage-gate (owner-approved) | Owner |
| D-011 | 2026-10-19 | Individual accounts, team-ready model; India region first | Owner |
| D-012 | 2026-10-19 | AI mentor in R1, confirm-first | Owner |
| D-013 | 2026-10-19 | Template calculations become validated Python functions | Owner |
| D-014 | 2026-10-19 | Minitab datasets are internal test fixtures only (git-ignored) | Owner |
| D-015 | 2026-10-19 | Full IDE shell and reports/export in R1 | Owner |
| D-016 | 2026-10-19 | Stage-wise delivery through 30 gates; all checks must pass before the next gate | Owner |
| D-017 | 2026-10-19 | Repository root = `C:\Users\60073\Python\New_Stat_Forge_v2`; inputs move to `sources/` in G01 | Owner |
| D-018 | 2026-10-19 | AGENTS.md is the rules file; CLAUDE.md imports it; project skills and subagents live in `.claude/` | Owner |
| D-019 | 2026-10-19 | TDD is enforced, not just advised: RED evidence first, TC-to-test traceability (`tc_trace`), Claude Code Stop/commit hooks, pre-commit and CI gates; added to G01 (TC-01.6–01.10) and as standard check SC-11 | Owner |
| D-020 | 2026-10-19 | Owner approval is mandatory at every gate, after testing and evidence, through a hands-on validation script covering scenarios S1–S6 (≤ 45 min) | Owner |
| D-021 | 2026-10-19 | Gate-specific skills are created just in time at kick-off (`docs/SKILLS_MAP.md`); owner approves each with the gate brief | Owner |
| D-022 | 2026-10-19 | Product: questionnaire engine and rule-based question chips in G25; versioned prompt library with eval suite in G28. Owner: `docs/OWNER_PROMPTS.md` + standard kick-off questionnaires by gate type | Owner |
| D-023 | 2026-10-19 | GitHub remote: private repo `Raghustatics/StatForge_Project_Management`; `main` and gate branches pushed only after owner PASS, via `/gate-close` (merge --no-ff, tag `gate-Gxx-pass`, push, verify CI) | Owner |
| D-024 | 2026-10-19 | Exception: temporary `ci-check/*` branches may be pushed before PASS only to prove CI test cases; deleted after evidence is captured | Owner |
| D-025 | 2026-10-19 | `sources/88_Templates/Project Phase Template v0.1.xlsx` is committed (owner's own material, private repo); Minitab datasets stay git-ignored | Owner |
| D-026 | 2026-10-19 | Node 24 LTS (installed, current LTS) replaces Node 22; Python via `uv python install 3.14`; pnpm via corepack; pre-commit and gitleaks as uv/standalone tools | Owner |
| D-027 | 2026-10-19 | Session logs per working session in `docs/sessions/`, plus `docs/TROUBLESHOOTING.md`; committed with each gate | Owner |
| D-028 | 2026-10-20 | psycopg 3 (LGPL-3.0) accepted as the PostgreSQL driver: used unmodified as a library, so SC-8 (no AGPL/SSPL/GPL runtime dependency) is met | Owner |
| D-029 | 2026-10-20 | G01 kick-off answers: G01 stays one gate (no a/b split); TC-01.1 "clean machine" = fresh clone with the project's images, volumes and build cache removed; no scope change (no worker service); validation time 30–45 min | Owner |
| D-030 | 2026-10-20 | pnpm shims installed per user (`corepack enable pnpm --install-directory %USERPROFILE%\.local\bin`) because the default target `C:\Program Files\nodejs` needs admin; documented in README | Agent (reversible; flagged to owner) |
| D-031 | 2026-10-20 | GitHub stays on the Free plan: no server-side branch protection on the private repo. Merge enforcement relies on red CI plus `/gate-close` refusing to merge (it re-runs `scripts/verify.ps1 -Mode Full` itself and stops on any failure) | Owner |
| D-032 | 2026-10-20 | G01 plan approved with conditions: (a) throwaway `ci-check/G01-*` demo branches may be pushed before gate close (D-024); run URLs and screenshots go into `docs/evidence/G01/` before deletion; `main` is never pushed before PASS (AGENTS.md §14); (b) the gitleaks planted secret is generated at runtime in a temp repo and never committed; (c) TC-01.1 is tested in the "clean pull" condition (no project images, base images, volumes or build cache); (d) pnpm pinned via `packageManager`; (e) `/gate-close` re-runs `verify.ps1` independently, even after a Stop-hook "NOT done" release; (f) all governance docs are committed; only the Minitab datasets, `.env`, local Claude settings, hook state and build/cache output are git-ignored | Owner |
