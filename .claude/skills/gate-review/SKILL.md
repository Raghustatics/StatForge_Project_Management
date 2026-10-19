---
name: gate-review
description: Close out a StatForge gate — run every test case and standard check, get independent agent reviews, and build the evidence pack and owner validation script. Use when implementation of the active gate is complete or the owner asks for a gate report.
---

# Gate review and evidence pack

## Steps

1. **Verify before claiming** (`superpowers:verification-before-completion`): run every command fresh. Never reuse old output.
2. **Standard checks:** run SC-1…SC-11 from the gate map and record the exact command and summarised result for each.
   - Python: `uv run ruff check`, `uv run mypy --strict`, `uv run pytest --cov`
   - Web: `pnpm lint`, `pnpm tsc --noEmit`, `pnpm test`, `pnpm build`, `pnpm e2e`
   - Stack: `docker compose up -d` then health check
   - Regression: full test suites of all earlier gates
   - TDD proof (SC-11):
     - `uv run python scripts/tc_trace.py --gate Gxx`: every TC is mapped to a non-skipped test
     - RED evidence in `docs/evidence/Gxx/red/` for every TC, timestamped before its GREEN commit (check with `git log`)
     - no existing assertion was weakened (check the diff of the test files)
3. **Gate test cases:** a table with TC id, how it was tested, result (PASS/FAIL) and evidence (test name, screenshot, log).
4. **Statistical gates:** attach the `/stats-validate` table (case, source, expected, actual, difference, tolerance, pass).
5. **Independent reviews**, run as subagents that did not write the code:
   - `gate-reviewer` (always)
   - `security-reviewer` (any API, auth, upload, AI or integration change)
   - `ux-a11y-reviewer` (any UI change)
   - `statistician` (any statistical or calculator change)

   Fix confirmed defects, then re-run steps 2–4.
6. **Evidence pack:** save it to `docs/evidence/Gxx/`: `report.md`, test outputs, screenshots or a short recording, validation tables.
7. **Owner validation script (mandatory, AGENTS.md §4.0):**
   - Cover scenarios S1–S6: happy path, messy/edge input, failure and recovery, second user/permissions, guided vs expert, regression spot-check. N/A only with a one-line reason.
   - Give each scenario numbered click-by-click steps, the expected result, and a ✓/✗ + comment box.
   - Add the gate-specific focus from the gate map's "Owner validation" line.
   - Keep the whole script under 45 minutes.
8. **Handover message** (bullets):
   - files changed
   - results
   - limitations
   - risks
   - decisions needed
   - the link to the evidence pack
9. Update the `docs/GATE_LOG.md` row: Self-test = date + "all pass" or the failing list. **Never** fill in Result. The owner records PASS.

## Rules

- Any FAIL means the gate isn't ready. Report it honestly; don't soften it.
- Don't mark a check "not applicable" without a one-line reason.
