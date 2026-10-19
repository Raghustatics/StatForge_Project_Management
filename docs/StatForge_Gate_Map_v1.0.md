# StatForge — Release 1 Gate Map v1.0 (approved 19 Oct 2026)

- **Date:** 19 Oct 2026 · Owner: Raghu Sinha
- **Baseline:** Development Guidelines v1.1 (approved 19 Oct 2026)
- **Shape:** 30 gates in 8 stages; each gate is one small, testable slice
- **Rule:** a gate starts only after the previous gate is recorded **PASS** in the Gate Log (§4)

---

## 1. How every gate works

### 1.1 Gate lifecycle

1. **Kick-off:** Claude Code restates the scope, lists the files to change and the risks, and confirms the test cases below. It waits for your "go".
2. **Build:** implements only the gate's scope.
3. **Self-test:** runs every test case and check, then posts the exact commands and results.
4. **Evidence pack:** test report, screenshots or a short screen recording, and any validation table.
5. **Owner validation (mandatory, every gate):** you run the validation script hands-on.
   - It always covers scenarios S1–S6: happy path, messy/edge input, failure and recovery, second user/permissions, guided vs expert, regression spot-check (AGENTS.md §4.0). N/A only with a reason.
   - The "Owner validation" line under each gate below lists the gate-specific focus on top of S1–S6.
   - The script takes ≤ 45 minutes.
6. **Decision:** PASS → next gate · FAIL → rework list, re-test the whole gate · A scope change needs a logged decision.

### 1.2 Standard checks (apply to every gate; numbered SC-1 … SC-11)

- **SC-1** CI is green: ruff, mypy `--strict`, pytest, ESLint, `tsc`, Vitest, build.
- **SC-2** **No regression:** every earlier gate's test suite passes.
- **SC-3** New Python/TS code has ≥ 85% line coverage. Statistical functions have 100% branch coverage on validation paths.
- **SC-4** Security: no secrets in code or logs; inputs validated at the API boundary; workspace authorisation enforced on every new endpoint.
- **SC-5** Accessibility: new screens are keyboard-operable, pass axe with no serious or critical issues, and show visible focus.
- **SC-6** Error, empty, loading and failure states are handled with plain-language messages.
- **SC-7** Docs are updated: README, the relevant spec page, decision log and changelog.
- **SC-8** Licence check: no AGPL/SSPL/GPL runtime dependency added.
- **SC-9** `docker compose up` on a clean machine still works.
- **SC-10** The evidence pack is attached to the Gate Log entry.
- **SC-11** TDD proof: RED evidence exists for every TC; `tc_trace` passes; no existing assertion was weakened (AGENTS.md §4.1).

### 1.3 Size legend

- **S** is a small slice, **M** is medium, **L** is large and may be split into a and b gates during kick-off if needed.

---

## 2. Gate overview

| Stage | Gates | Outcome |
|---|---|---|
| 0 · Foundation | G01–G03 | Repo, database, accounts, entitlements, secure base |
| 1 · IDE shell | G04–G06 | Working IDE shell, plugins framework (UI), projects and explorer |
| 2 · Data foundation | G07–G09 | Upload, profiling, data quality, versions |
| 3 · Statistical engine | G10–G17 | Validated stats, graphs, tests, regression/ANOVA, SPC, capability, calculators |
| 4 · Methodology & templates | G18–G21 | 88 templates, methodology engine, linked analyses, drafted methodologies |
| 5 · PM & guidance | G22–G25 | Kanban, Gantt/CPM, registers, KPIs/OKRs, deterministic guidance, journeys A/B/C |
| 6 · Reports | G26 | Saved runs, storyboard, exports |
| 7 · AI & integrations | G27–G29 | BYO AI, confirm-first mentor, Outlook plugin |
| 8 · Pilot readiness | G30 | Hardening, performance, staging in India region, pilot pack |

---

## 3. Gates

### Stage 0 — Foundation

#### G01 · Repository, governance and dev environment (S)
- **Goal:** a clean, reproducible project base that Claude Code works inside safely.
- **In scope:**
  - new repo `statforge`
  - `CLAUDE.md` (aligned to the v1.1 guidelines)
  - `docs/`: guidelines, gate map, decision log, Gate Log
  - monorepo layout (`apps/web`, `apps/api`, `packages/engine`)
  - Docker Compose: web, api, db (PostgreSQL 18), s3 (SeaweedFS)
  - health endpoints, CI workflow, `.env.example`, pre-commit
  - **TDD enforcement (AGENTS.md §4.1):**
    - `scripts/tc_trace.py` (TC-to-test traceability)
    - `scripts/verify.ps1` (lint, types, tests, trace)
    - `.claude/settings.json` hooks (Stop → verify; PreToolUse on `git commit` → test-first guard)
    - pre-commit and CI rules (coverage gate, unmapped-TC gate, earlier-gate regression gate)
- **Out of scope:** any product feature.
- **Test cases:**
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
- **Owner validation:**
  - Clone and run on your laptop using the README only.
  - Open the app.
  - Open the CI run page.

#### G02 · Core data model and authorisation scoping (M)
- **Goal:** a team-ready schema with strict workspace isolation from day one.
- **In scope:** organization, user, workspace, membership (roles), project, audit_event; Alembic migrations; a repository layer that enforces workspace scoping.
- **Test cases:**
  - TC-02.1 Migrations upgrade from empty and downgrade cleanly.
  - TC-02.2 User A cannot read, update or delete any of User B's workspace or projects (API returns 404, not 403 leakage).
  - TC-02.3 Every write creates an audit_event with actor, action, entity and timestamp.
  - TC-02.4 Deleting a workspace soft-deletes it; hard delete after retention removes the rows (test with clock control).
  - TC-02.5 A property test runs 200 random cross-workspace requests and gets 0 leaks.
- **Owner validation:** review the entity diagram and the audit log sample.

#### G03 · Accounts, sessions and entitlements (M)
- **Goal:** individual sign-up and login, plus an entitlement layer with no billing.
- **In scope:**
  - email + password sign-up with verification (dev mail catcher), login, logout, password reset
  - session security
  - OIDC-ready token interface
  - entitlement service: plan = Free; feature flags checked server-side
  - account and data deletion
- **Test cases:**
  - TC-03.1 Sign-up → verify → login → logout works end to end in a browser test.
  - TC-03.2 Wrong password ×5 triggers a rate limit; there is no user enumeration in error messages.
  - TC-03.3 An expired or forged session token is rejected.
  - TC-03.4 A feature disabled by entitlement is hidden in the UI **and** refused by the API.
  - TC-03.5 "Delete my account" removes the user's data and files (verified in db and s3).
- **Owner validation:** create two accounts and confirm neither can see the other's workspace.

### Stage 1 — IDE shell

#### G04 · IDE shell layout (M)
- **Goal:** the full Cursor/Antigravity-style frame, with empty states.
- **In scope:**
  - title bar with the top menu tree
  - activity rail, primary sidebar, workbench (dockview tabs, splits)
  - bottom panel (Output, Problems, Runs, Audit), insights pane, AI pane (placeholder), status bar
  - resize, collapse, layout persistence, responsive rules
- **Test cases:**
  - TC-04.1 Every region renders and can collapse and restore; sizes persist after reload.
  - TC-04.2 Tabs open, close, split, reorder and move between groups.
  - TC-04.3 The layout follows the agreed rules at 1600, 1280, 1024 and 390 px.
  - TC-04.4 Each region has a defined empty state.
  - TC-04.5 F6 / Shift+F6 cycles focus through the regions.
- **Owner validation:** compare against the 18 Oct prototype; list visual deviations.

#### G05 · Commands, palette, keyboard, themes and fonts (M)
- **Goal:** one command registry behind menus, the palette, shortcuts and (later) AI; appearance plugins.
- **In scope:** command registry with `when` context; command palette; remappable shortcuts; frontend plugin manifest registry; theme plugins (Dark, Light, High Contrast Dark/Light); font plugins (UI and mono, size, density).
- **Test cases:**
  - TC-05.1 Every menu item is a registered command and appears in the palette.
  - TC-05.2 `when` clauses enable and disable items correctly (unit table of 20 contexts).
  - TC-05.3 Switching theme updates every token, including chart colours; HC themes meet contrast ≥ 7:1 for text.
  - TC-05.4 A remapped shortcut works and persists; conflicts are warned.
  - TC-05.5 A disabled theme or font plugin disappears from the choices.
- **Owner validation:** five minutes of keyboard-only use; switch all themes.

#### G06 · Projects, explorer and search (M)
- **Goal:** create and organise work.
- **In scope:** create, open, rename, archive and delete projects; folders and notes; explorer drill-down with segments (All, Data, Analyses, Templates, Tasks, Reports); context menus; basic search.
- **Test cases:**
  - TC-06.1 The full CRUD cycle works; deletes go to Trash with restore.
  - TC-06.2 Segment filters keep the hierarchy and show the correct items.
  - TC-06.3 Explorer keyboard navigation works (arrows, Enter, F2, Delete).
  - TC-06.4 Search finds projects, notes and folders by name and content; there are no cross-workspace results.
  - TC-06.5 1,000 items render without lag (virtualised; under 100 ms interaction).
- **Owner validation:** build a folder structure that mirrors one real project (no company data).

### Stage 2 — Data foundation

#### G07 · Upload and immutable storage (M)
- **Goal:** safe ingestion of CSV/XLSX.
- **In scope:** upload up to 10 MB; extension, magic-byte and size checks server-side; original bytes stored content-addressed (sha256); safe preview (first N rows, read as text); XLSX sheet picker.
- **Test cases:**
  - TC-07.1 A 10 MB file is accepted and a 10 MB + 1 byte file is rejected with a clear message.
  - TC-07.2 A renamed `.exe` posing as `.csv` is rejected.
  - TC-07.3 Encodings are handled: UTF-8, UTF-8 BOM, UTF-16, Windows-1252.
  - TC-07.4 Delimiters are handled: comma, semicolon, tab, pipe; quoted newlines.
  - TC-07.5 Empty file, header-only file and duplicate headers each give a defined behaviour.
  - TC-07.6 The original hash is unchanged after any number of later operations.
  - TC-07.7 Formula cells such as `=cmd` stay inert in preview and export.
- **Owner validation:** upload 5 of the Minitab fixture sheets (exported) and 2 messy files you create.

#### G08 · Profiling and data-quality detection (M)
- **Goal:** evidence-based quality review.
- **In scope:** profile (rows, columns, types, missing, unique, min/max, distributions) computed in DuckDB/pandas; detectors for ambiguous dates, numeric-as-text, mixed types, missing markers (blank, NA, −999), duplicates, identifiers, category codes and outliers (flag only); Problems view.
- **Test cases:**
  - TC-08.1 A fixture suite of 15 messy CSVs, each with expected profile JSON, all match.
  - TC-08.2 `03/04/2026` is flagged ambiguous; `25/04/2026` is resolved as DMY with its evidence shown.
  - TC-08.3 `"1,200"` and `"N/A"` give a numeric-as-text flag with parse success/fail counts.
  - TC-08.4 Codes `1/2/3` in a low-cardinality column give a category-code flag.
  - TC-08.5 Outliers are flagged and **never** removed (row count unchanged).
  - TC-08.6 Profiling of a 10 MB file finishes in under 10 s (p95).
- **Owner validation:** judge whether the flags on 3 datasets match your expert view.

#### G09 · Type confirmation, transformations and versions (M)
- **Goal:** user-approved changes with full provenance.
- **In scope:** confirm types and roles; transformation types (set type, date format, missing-code mapping, recode, filter, compute column); before/after diff; dataset versions (Parquet); version compare and rollback.
- **Test cases:**
  - TC-09.1 No transformation is applied without explicit confirmation.
  - TC-09.2 Each transformation is recorded with params, rows affected, user and time.
  - TC-09.3 Replaying the recorded transformations on the original reproduces the version byte-for-byte (hash match).
  - TC-09.4 Rollback to an earlier version leaves later versions intact.
  - TC-09.5 The diff shows rows affected and the effect on summary statistics.
- **Owner validation:** fix a messy file end to end; confirm the audit trail reads correctly.

### Stage 3 — Statistical engine

#### G10 · Engine, plugin contract, run records and descriptive statistics (M)
- **Goal:** the execution pipeline every analysis uses, proven on one plugin.
- **In scope:**
  - Python plugin SDK: manifest, input/output schemas, preconditions
  - run record: inputs, params, versions, warnings, outputs, run id
  - execution limits (CPU, memory, time); configurator form generated from the schema
  - result view
  - **Descriptive Statistics** plugin
- **Test cases:**
  - TC-10.1 NIST StRD univariate cases (e.g., Lew, Lottery, Mavro, Michelso, NumAcc1–4, PiDigits) match certified mean, SD and r1 to the required digits.
  - TC-10.2 Re-running a run gives identical outputs and a new run id linked to the original.
  - TC-10.3 A precondition failure blocks execution with a plain message.
  - TC-10.4 A job past its time limit is stopped cleanly and reported.
  - TC-10.5 The run record contains every field listed in guidelines §7.2.
- **Owner validation:** run descriptives on a Minitab fixture and compare with your expectation.

#### G11 · EDA dashboard and graphs (M)
- **Goal:** a standard EDA view and the chart set.
- **In scope:** histogram, boxplot, scatter, Pareto, run chart, dot plot, probability plot, time series; normality tests (Anderson-Darling, Shapiro-Wilk); auto EDA dashboard; chart text summaries generated from computed values; "view as table".
- **Test cases:**
  - TC-11.1 Chart specs are snapshot-tested for each chart type.
  - TC-11.2 AD and SW statistics and p-values match R `nortest` / `shapiro.test` on 5 reference sets.
  - TC-11.3 Pareto ordering, cumulative % and "Other" grouping match a hand-checked case.
  - TC-11.4 Every number in a text summary equals a computed value (automated check).
  - TC-11.5 Charts follow the active theme and the colour-blind-safe palette.
- **Owner validation:** produce an EDA on 3 datasets and judge whether the defaults are sensible.

#### G12 · Hypothesis tests I: means and variances (M)
- **Goal:** port and validate the continuous tests.
- **In scope:** 1-sample t, 2-sample t (Welch default), paired t, equal-variance tests (F, Levene); CIs; effect sizes; assumptions report; statistical vs practical significance message.
- **Test cases:**
  - TC-12.1 Every test matches R `t.test`, `var.test` and `car::leveneTest` on 10 reference cases (p rel ≤ 1e-4).
  - TC-12.2 The paired test refuses unequal-length or unpaired inputs.
  - TC-12.3 Small n (< 20) raises a fragility warning.
  - TC-12.4 Output never says "probability H₀ is true".
- **Owner validation:** check 3 PMO-app benefit cases give the same verdicts.

#### G13 · Hypothesis tests II: proportions, counts, non-parametric (M)
- **Goal:** discrete and distribution-free tests.
- **In scope:** 1- and 2-proportion (z / Fisher auto-switch), chi-square (independence, goodness of fit), Mann-Whitney, Wilcoxon signed-rank, Kruskal-Wallis.
- **Test cases:**
  - TC-13.1 Results match R `prop.test` / `fisher.test` / `chisq.test` / `wilcox.test` / `kruskal.test` on 10 cases.
  - TC-13.2 Expected counts < 5 switch to Fisher, and the reason is shown.
  - TC-13.3 Ties and zero differences are handled as documented.
- **Owner validation:** run the TelevisionDefects and HospitalComparison fixtures.

#### G14 · Correlation, regression and ANOVA (L)
- **Goal:** model-based analysis with diagnostics.
- **In scope:** Pearson/Spearman correlation; simple and multiple linear regression (coefficients, CI, R², adjusted R², VIF, residual plots, unusual observations); one-way ANOVA with Tukey; identifier-as-predictor warning.
- **Test cases:**
  - TC-14.1 NIST StRD linear regression (Norris, Pontius, NoInt1/2, Filip, Longley, Wampler1–5) matches certified coefficients and SEs.
  - TC-14.2 NIST StRD ANOVA (SiRstv, SmLs01–09, AtmWtAg) matches certified F and MS.
  - TC-14.3 Tukey intervals match R `TukeyHSD` on 3 cases.
  - TC-14.4 High VIF and identifier-predictor warnings fire.
- **Owner validation:** run regression on the LoanApplicant fixture; review the diagnostics wording.

#### G15 · SPC: variables charts (M)
- **Goal:** validated control charts for continuous data.
- **In scope:** constants table (n = 2–25); I-MR, Xbar-R, Xbar-S; configurable run rules (Nelson 1–8; Western Electric preset; 8 vs 9 documented); staged charts (before/after); historical limits.
- **Test cases:**
  - TC-15.1 The constants table matches published values for all n.
  - TC-15.2 Limits match R `qcc` on 10 fixtures (e.g., Cable wire diameter, Camshaft, Can weight).
  - TC-15.3 Each run rule is detected exactly on synthetic sequences built to trigger it.
  - TC-15.4 σ for I-MR uses MR̄/d2 (a regression test guards against overall SD).
  - TC-15.5 Staged limits are recomputed per stage.
- **Owner validation:** compare 3 charts with the PMO app output and your expectation.

#### G16 · SPC attribute charts and capability (M)
- **Goal:** attribute charts plus baseline capability.
- **In scope:** p, np, c, u (variable sample size); Cp, Cpk, Pp, Ppk (one- and two-sided), PPM, Z-bench, DPMO↔sigma (with and without 1.5 shift, labelled); stability and normality preconditions.
- **Test cases:**
  - TC-16.1 Attribute limits match `qcc` on 8 fixtures (e.g., Defective records, Unanswered calls, Wallpaper defects, Transcription errors).
  - TC-16.2 Capability matches R `qcc::process.capability` / hand calculations on 6 cases, including one-sided specs.
  - TC-16.3 Capability on an unstable process carries the "provisional" warning.
  - TC-16.4 DPMO↔sigma table round-trips within 0.01.
- **Owner validation:** reproduce M07.A/M07.B workbook examples and compare.

#### G17 · Template calculators (M)
- **Goal:** workbook formulas as validated functions.
- **In scope:** OEE, Kanban card count, line balancing, takt time, FMEA RPN, financial savings, prioritiser, effort-impact, attribute agreement (GRR-discrete, kappa).
- **Test cases:**
  - TC-17.1 Each calculator matches its workbook sheet (L05, L07, L08, I03, 02, 03, 04, M02) on the sheet's own example plus 2 edge cases.
  - TC-17.2 Kappa and % agreement match R `irr` on the Attribute gage fixture.
  - TC-17.3 Invalid inputs (negative time, zero demand) give clear errors.
- **Owner validation:** spot-check 3 calculators against your Excel.

### Stage 4 — Methodology and templates

#### G18 · Template engine and importer (L)
- **Goal:** 88 templates as versioned data.
- **In scope:** template schema (7 types); importer from `Project Phase Template v0.1.xlsx`; cleanup applied (A02 IDs, typos, bloat); form, table, checklist and narrative renderers; template versioning; fill, save and export a template instance.
- **Test cases:**
  - TC-18.1 The importer produces exactly 88 templates with IDs and groups matching the index.
  - TC-18.2 Every template has a type, fields, help text and an applicability flag (0 unclassified).
  - TC-18.3 A re-import of the same file creates no duplicates; a changed file creates a new version.
  - TC-18.4 A filled instance survives save → reload → export to Excel.
  - TC-18.5 Placeholder sheets (D09, I12, A07, 10, C10) are marked "content pending".
- **Owner validation:** open 10 templates of your choice and compare them with Excel.

#### G19 · Methodology engine and workflow states (L)
- **Goal:** methodology definitions vs project instances.
- **In scope:**
  - definitions for Lean, Discovery, DMAIC Green Belt and Black Belt from the source
  - applicability rules: required, conditional, choose-one, optional
  - project workflow instance and step states
  - skip, defer and N/A with a reason
  - soft by default, hard gates optional; tollgate checklists; workflow events
- **Test cases:**
  - TC-19.1 GB and BB tracks list exactly the templates ticked in the index.
  - TC-19.2 A choose-one group (A01/A02) is satisfied by either option.
  - TC-19.3 A skipped step is never shown as complete and is flagged in the tollgate.
  - TC-19.4 Under hard-gate mode a phase cannot sign off with a required item open; in soft mode it can, with a recorded reason.
  - TC-19.5 Editing a project instance never changes the methodology definition (checksum).
- **Owner validation:** run a mock GB project through Define and Measure.

#### G20 · Analysis-linked and diagram templates, standalone use (L)
- **Goal:** templates connected to the engine; Journey C.
- **In scope:** M06, M07.A/B, I09, I10, I11, C08, M02/C06 linked to plugin runs; fishbone (A02), process map (D09/I12) and VSM (L06) diagram editors; any template usable standalone.
- **Test cases:**
  - TC-20.1 Values in linked templates come only from run outputs, and every value links to its run id.
  - TC-20.2 Re-running the source analysis updates the template, with history.
  - TC-20.3 The fishbone supports 6M categories and causes, and export.
  - TC-20.4 A standalone template (e.g., a fishbone only) works without a methodology.
- **Owner validation:** complete M06 → M07.B on a fixture; build a fishbone.

#### G21 · Drafted methodologies and the Yellow Belt track (L, owner-heavy)
- **Goal:** the content not in the source, owner-approved.
- **In scope:** draft DMADV/DFSS, PDCA, 8D, A3, Kaizen, MoM, Action Plan and the generic stage-gate; Yellow Belt subset; "Draft" status flag and approval workflow; version history.
- **Test cases:**
  - TC-21.1 Each draft shows the "Draft" badge until approved; approval is recorded with date and version.
  - TC-21.2 An unapproved draft cannot be set as an organisation default.
  - TC-21.3 Each methodology passes the same engine tests as G19.
- **Owner validation:** approve, or return with comments, each methodology (this gate can't pass without your review).

### Stage 5 — Project management and guidance

#### G22 · Kanban and to-do (M)
- **Goal:** task flow linked to the work.
- **In scope:** boards (default columns, WIP limits); cards linked to steps, templates, runs and evidence; drag-drop plus keyboard move; to-do view; Excel import/export (ported).
- **Test cases:**
  - TC-22.1 A card moved by mouse and by keyboard persists the same way.
  - TC-22.2 A WIP limit breach is warned.
  - TC-22.3 A linked run, template or step opens from its card.
  - TC-22.4 An Excel round-trip keeps all fields.
- **Owner validation:** run a sprint of 10 cards.

#### G23 · Gantt, critical path and registers (L)
- **Goal:** schedule and governance.
- **In scope:** Gantt (planned and actual, milestones, zoom); CPM finish-to-start engine (ported); delay monitoring and attention list; registers (risk & dependency, decision & change log, benefits & KPIs, requirements, options appraisal, stakeholders) with CSV templates.
- **Test cases:**
  - TC-23.1 CPM matches hand-solved networks (5 cases, including parallel paths).
  - TC-23.2 A plan shorter than its dependencies allow is warned.
  - TC-23.3 The attention list ranks by the documented priority formula.
  - TC-23.4 Register CSV import/export round-trips cleanly.
- **Owner validation:** compare one schedule against the PMO app's output.

#### G24 · KPIs, OKRs, skill ledger and the insights pane (M)
- **Goal:** live, evidence-based progress.
- **In scope:** KPIs bound to run metrics (baseline, current, target); project OKRs (KR ← KPI); personal learning OKRs (KR ← skill ledger); skill ledger rules; insights cards (phase status, KPIs, chart, to-do, next steps, OKR progress, data health).
- **Test cases:**
  - TC-24.1 A new run updates its KPI and the KR progress automatically.
  - TC-24.2 KR progress follows the documented formula, clamped.
  - TC-24.3 A skill is credited only after a validated run with checked assumptions and a confirmed interpretation.
  - TC-24.4 The insights pane always reflects the active project.
- **Owner validation:** run a baseline → after comparison and watch the KR move.

#### G25 · Deterministic guidance and journeys A, B, C (L)
- **Goal:** guidance that works with AI switched off.
- **In scope:**
  - first conversation (problem, objective, data) as a guided form
  - rule-based recommendations: methodology fit, missing information, next action, overdue items, stakeholder prompts
  - Journey B data-collection plan generator
  - labels for fact, hypothesis, recommendation and decision
  - accept, reject, defer or edit each recommendation
  - guided vs expert mode
  - **questionnaire engine:** versioned question sets in `content/questionnaires/`:
    - intake (problem, objective, data)
    - each methodology step (e.g., VOC → CTQ, charter, data-collection plan, root-cause validation)
    - Journey B (no data → data-collection plan)
    - question types: single/multi choice, number with unit, date, short text, table; skip logic; "I don't know" always allowed
  - **suggested-question chips:** rule-based, context-aware (e.g., "Why this test?", "What does this Cpk mean for my target?", "What should I do next?", "What if I skip this step?")
- **Test cases:**
  - TC-25.1 Journeys A, B and C complete end to end in E2E tests with AI off.
  - TC-25.2 Recommendation rules fire correctly on a 30-scenario table.
  - TC-25.3 The guidance layer never states that an action happened without evidence.
  - TC-25.4 Expert mode reaches any tool in ≤ 2 actions with no interview.
  - TC-25.5 Every questionnaire validates against its schema; skip logic is tested on all branches; "I don't know" never blocks progress.
  - TC-25.6 Answers save to the project record and pre-fill the matching template fields, with each field showing its source question.
  - TC-25.7 The suggested chips shown match the expected set for 20 context scenarios (step, data state, run results).
  - TC-25.8 Questionnaire content is versioned; changing a question set keeps old projects' answers readable.
- **Owner validation:** ask a non-expert colleague (outside Altius data) to try Journey B.

### Stage 6 — Reports

#### G26 · Saved analyses, storyboard report and exports (M)
- **Goal:** shareable, reproducible outputs.
- **In scope:** saved runs (reopen, re-run); storyboard report (charter → baseline → analysis → improvement → control → learnings / executive summary); export to PDF, Excel, CSV, PNG and SVG; injection-safe CSV.
- **Test cases:**
  - TC-26.1 Every number in a report equals its source run value (automated).
  - TC-26.2 A report reopened later matches the stored version (hash).
  - TC-26.3 Cells starting with `=`, `+`, `-` or `@` are escaped in CSV and Excel exports.
  - TC-26.4 The PDF renders the charts and tables correctly (visual snapshot).
  - TC-26.5 Sponsor-ready: an exported tollgate pack needs no manual reformatting before it is presented (owner judges this on 2 real-shaped projects).
- **Owner validation:** produce a tollgate pack you would show a sponsor.

### Stage 7 — AI and integrations

#### G27 · AI connector: bring your own key and Ollama (M)
- **Goal:** a safe, optional AI connection.
- **In scope:** provider abstraction (Anthropic, OpenAI, Gemini, Ollama); key entry with envelope encryption; consent screen naming the provider and data sent; minimal-context builder; disconnect and delete key; AI-off fallback.
- **Test cases:**
  - TC-27.1 Keys never appear in the browser, logs, exports or plugin contexts (automated scan).
  - TC-27.2 No data is sent before consent; consent is recorded.
  - TC-27.3 By default, raw rows are absent from the payload (payload snapshot).
  - TC-27.4 With the provider down or the key invalid, the user sees a clear message and the core still works.
  - TC-27.5 The Ollama local model works with no internet access.
- **Owner validation:** connect your own key, then disconnect it and confirm deletion.

#### G28 · AI mentor and agent, confirm-first (L)
- **Goal:** helpful AI that never decides and never invents numbers.
- **In scope:**
  - Ask, Plan and Agent modes
  - proposals → review step (port the PMO pattern)
  - tool calls limited to registered commands
  - grounding check on numbers
  - AI-drafted template content as proposals
  - mentor evals ported
  - **prompt library** in `content/prompts/`:
    - system prompt with guardrails
    - mode prompts
    - an "explain this result" prompt for each plugin (fed only structured outputs)
    - a "draft this template" prompt for each template
    - a "clarify the problem" prompt that uses the G25 questionnaires
    - each prompt has an id, version, variables, a target token budget and an owner-approval status
  - **prompt evaluation suite**: golden scenarios per prompt, run in CI on every prompt change, across Claude, OpenAI, Gemini and Ollama
  - AI-assisted suggested questions layered on the G25 rule-based chips
- **Test cases:**
  - TC-28.1 Every AI action produces a pending proposal; nothing applies without approval.
  - TC-28.2 The grounding check blocks every number not traceable to a run (eval set of 50 replies: 0 violations).
  - TC-28.3 Data transformations can never be auto-approved.
  - TC-28.4 Method recommendations agree ≥ 95% with your expert answers on the 50-scenario set.
  - TC-28.5 Prompt-injection text inside an uploaded file does not trigger tools.
  - TC-28.6 Every prompt in the library has ≥ 5 evaluation cases; the suite passes on each supported provider (documented thresholds; Ollama may have a lower, stated threshold).
  - TC-28.7 Changing a prompt without updating its version and evals fails CI.
  - TC-28.8 An unapproved (draft) prompt can't be used in production mode.
  - TC-28.9 Variables are filled only from allow-listed context (no raw rows without consent); payload snapshots are verified.
- **Owner validation:** complete one DMAIC phase using the mentor and rate every reply.

#### G29 · Outlook Copilot Gateway plugin (M)
- **Goal:** the PMO bridge as a safe, opt-in plugin.
- **In scope:** port the bridge and question builder; extension targets the StatForge domain; per-user opt-in with a policy notice; review step showing confidence, basis and source; manual-paste fallback; admin kill switch; security review.
- **Test cases:**
  - TC-29.1 The extension's ported Node tests pass; the bridge only acts on the StatForge origin.
  - TC-29.2 It never types into an email editor or clicks Send (ported safety tests).
  - TC-29.3 With the plugin off (default), no extension messages are accepted.
  - TC-29.4 Every answer lands unticked or ticked by confidence, and nothing auto-applies.
  - TC-29.5 The kill switch disables it for all users immediately.
- **Owner validation:** run "Fill from mail" on a non-confidential test mailbox.

### Stage 8 — Pilot readiness

#### G30 · Hardening, performance, staging and pilot pack (L)
- **Goal:** ready for real users.
- **In scope:** security review (OWASP ASVS L1 checklist); dependency and licence scan; load and large-file tests; full accessibility audit; backup and restore drill; staging deployment in an India region; privacy notice and AI governance page; metric instrumentation (activation, completion, return, guidance usefulness, trust); pilot guide.
- **Test cases:**
  - TC-30.1 ASVS L1 items are complete; high/critical findings = 0.
  - TC-30.2 Backup → restore drill completes in under 1 h with verified data.
  - TC-30.3 Fixtures up to the 10 MB limit profile within budget; the Semiconductor / Debt / Diamonds sets are handled per limit policy.
  - TC-30.4 Full axe and keyboard audit of the main screens passes.
  - TC-30.5 Metrics events are recorded without dataset contents.
- **Owner validation:** go / no-go for a pilot with 5–10 guided users and 3–5 experts.

---

## 4. Gate log (fill in as gates pass)

| Gate | Started | Self-test | Owner validation | Result | Evidence link | Notes |
|---|---|---|---|---|---|---|
| G01 | | | | | | |
| G02 | | | | | | |
| … | | | | | | |
| G30 | | | | | | |

Result values: **PASS** · **PASS WITH CONDITIONS** (each condition gets a due gate) · **FAIL** (rework list).

---

## 5. Before G01 can start (owner)

- Where the repository will live: GitHub (connect it to Claude) and/or a local folder.
- The laptop has Docker Desktop, Git, Python 3.14 and Node 22 LTS (G01 kick-off verifies these).
- Approve this gate map, or return it with changes (gate order, sizes, test cases).

## 6. Notes

- Gate order follows the guidelines: the deterministic core comes before AI.
- **Owner-heavy gates:** G21 (drafted methodologies) and G25 (guidance validation). Plan your time for them.
- **L gates** may split into "a/b" at kick-off; the total stays within 20–30 gates' worth of scope, and any split is logged.
