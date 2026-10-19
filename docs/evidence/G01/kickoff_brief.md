# G01 kick-off brief (approved: owner "Go for G01", 2026-10-20)

- **Source of scope:** `docs/StatForge_Gate_Map_v1.0.md` §3 G01; AGENTS.md §4.1, §8, §14, §15; DECISIONS D-017, D-019 to D-030.
- **Owner answers:** one gate, no split · clean machine = fresh clone with the project's images, volumes and build cache removed · no scope change · validation 30–45 min · psycopg (LGPL-3.0) accepted (D-028).
- **Document conflicts (reported):** gate map "new repo `statforge`" vs D-023 (existing private repo `Raghustatics/StatForge_Project_Management`) → D-023 followed. Gate map §5 Node 22 vs D-026 Node 24 → D-026 followed. 03_ARCHITECTURE lists a `worker` service → out of scope (AGENTS.md §8: no queue until a gate proves the need).

## Goal
- A clean, reproducible project base that Claude Code works inside safely, with test-first development enforced by tooling.

## In scope
- Move `88_Templates/` and `Business_Cases_Examples/` into `sources/` (move only); `.gitignore` excludes `sources/Business_Cases_Examples/` before the first commit.
- Monorepo: `apps/web` (Vite 8 + React 19.3 + TS 6 placeholder), `apps/api` (FastAPI: `/health`, `/api/v1/version`), `packages/engine` (empty typed package).
- `docker-compose.yml`: web, api, db (PostgreSQL 18), s3 (SeaweedFS), with healthchecks; `.env.example`; uv and pnpm workspaces.
- pre-commit (ruff, mypy, ESLint, gitleaks, tc_trace, commit guard); GitHub Actions CI (lint, types, tests, coverage gate, tc_trace, gitleaks, compose integration).
- `scripts/tc_trace.py`, `scripts/verify.ps1`, `.claude/settings.json` hooks (Stop → verify; PreToolUse on `git commit` → test-first guard), `scripts/red_green_check.py`.
- `origin` = existing private repo; only `ci-check/G01-*` branches pushed before PASS.

## Out of scope
- Product features, DB schema/Alembic (G02), auth (G03), IDE shell (G04), worker/queue.

## Test cases (verbatim from the gate map)
- TC-01.1 `docker compose up` brings all services healthy in under 3 min on a clean machine.
- TC-01.2 `GET /health` reports db and s3 status; it returns 503 when db is down.
- TC-01.3 The web app loads a placeholder page served by the api version endpoint.
- TC-01.4 CI fails on a deliberate lint error and a deliberate failing test (checked on a branch).
- TC-01.5 A secret scan on the repo finds 0 secrets.
- TC-01.6 `tc_trace.py` fails when a G01 TC has no matching test, and passes when every G01 TC is mapped (both cases demonstrated).
- TC-01.7 The Stop hook blocks "done" when a test fails (demonstrated with a deliberate failing test on a scratch branch).
- TC-01.8 The commit guard blocks a product-code commit with no tests; a tests-first commit followed by a code commit is allowed.
- TC-01.9 CI blocks a PR that drops coverage below threshold or leaves a TC unmapped.
- TC-01.10 The G01 evidence pack contains RED runs timestamped before the matching GREEN commits.

## Proposed edge cases
- TC-01.2: `/health` returns 503 when s3 is down; the body names the failing component and contains no connection strings.
- TC-01.5: a planted fake secret on a scratch repo is caught.
- TC-01.6: `tc_trace` fails when a mapped test is skip or xfail.
- TC-01.10: `scripts/red_green_check.py` verifies RED-before-GREEN automatically.
- Guard rail: no file under `sources/Business_Cases_Examples/` is ever tracked (R-07).

## Owner validation outline (S1–S6)
- S1: clone into a new folder using the README only → `docker compose up` → open the app, see the api version → open the CI run page.
- S2: cold start with images and volumes removed, timed (< 3 min); start once without `.env` → clear error.
- S3: stop `db` → `/health` 503 and a plain message on the page → restart → recovery.
- S4: N/A (no accounts or data in G01); stand-in: confirm the GitHub repo is private and contains no Minitab files.
- S5: N/A (no product UI until G04); stand-in: README has a newcomer path and an expert path.
- S6: N/A (first gate); stand-in: owner runs `scripts/verify.ps1` and sees it green.
