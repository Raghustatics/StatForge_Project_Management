# AGENTS.md — StatForge

> Operating manual for every AI coding agent working in this repository (Claude Code, Cursor, Codex, others).
> Claude Code loads this file through `CLAUDE.md`. Read it fully at the start of every session.

---

## 1. Project identity

- **StatForge** is a browser-based SaaS problem-solving platform: guided methodology + deterministic statistics + project management + optional AI, in a Cursor/Antigravity-style IDE.
- **Positioning:** solve real operational problems with scientific rigour, and learn the method by doing it.
- **Primary objective:** human-centred assistance for real-world official work (outputs fit for a sponsor, auditor or management).
- **Owner and product authority:** Raghu Sinha. Owner decisions override agent preferences.
- **Principle that governs every decision:** **The platform guides. The statistical engine calculates. Optional AI assists. The user decides.**

## 2. Governing documents (precedence order)

1. `docs/StatForge_Development_Guidelines_v1.1.md`: approved scope baseline (signed off 19 Oct 2026)
2. `docs/StatForge_Gate_Map_v1.0.md`: the 30 gates, test cases and standard checks (approved 19 Oct 2026)
3. `docs/GATE_LOG.md`: which gate is active and which have passed
4. `docs/DECISIONS.md`: logged decisions and scope moves
5. `docs/reference/*`: detailed specs (UX, architecture, plugin contract, data model, AI, validation, research). These are subordinate to 1–4; where they conflict, items 1–4 win.

If documents conflict, follow the higher one and report the conflict in your final message.

## 3. Non-negotiable rules

- Deterministic, tested Python is the **only** source of numbers. AI never computes, rounds, invents or alters a statistic.
- Every AI action is a **proposal**. It applies only after the user approves it on a review step.
- Original uploads are **immutable**. Every change is a recorded transformation on a new dataset version.
- Never silently delete outliers, impute values, coerce ambiguous dates, reinterpret category codes or drop rows.
- The whole product works with AI switched off.
- Users never write code. Python libraries power plugins behind the UI.
- Statistical significance is never presented as business significance.
- Never claim an action, meeting or communication happened without evidence.
- Methodology content comes from `sources/` or is marked **Draft** until the owner approves it. Never invent it from memory and present it as authoritative.
- Minitab example datasets are **internal test fixtures only**. Never ship, commit to a public repo, or redistribute them.

## 4. Gate protocol (mandatory)

Work happens only inside the **active gate** listed in `docs/GATE_LOG.md`. Never start work that belongs to a later gate.

| Step | What to do | Skills / agents to use |
|---|---|---|
| 1. Kick-off | Confirm the previous gate is PASS. Restate scope, out-of-scope, test cases, files to change, risks. **Wait for the owner's "go".** | `/gate-kickoff` · `superpowers:brainstorming` (only if scope is unclear) · `superpowers:writing-plans` |
| 2. Design | For UI: follow `docs/reference/02_UX_IDE_SPEC.md`. For architecture choices: write an ADR. | `frontend-design` · `design:design-system` · `engineering:architecture` · `engineering:system-design` |
| 3. Test first (RED) | Write the gate's test cases as failing tests before implementation. Capture the failing run as RED evidence and commit the tests first (§4.1). | `superpowers:test-driven-development` · agent `qa-engineer` · `engineering:testing-strategy` |
| 4. Build | Implement only the agreed scope, in small commits. | `superpowers:executing-plans` · `superpowers:subagent-driven-development` (independent tasks) |
| 5. Statistics | Validate every statistical or calculator function against references. | `/stats-validate` · agent `statistician` · `data:statistical-analysis` · `data:validate-data` |
| 6. Debug | On any failure, find the root cause before changing code. | `superpowers:systematic-debugging` · `engineering:debug` |
| 7. Self-review | Run all standard checks SC-1…SC-11 and the gate's test cases. | `superpowers:verification-before-completion` · `superpowers:requesting-code-review` · `engineering:code-review` |
| 8. Independent review | Fresh-eyes reviews by agents that did not write the code. | agents `gate-reviewer`, `security-reviewer`, `ux-a11y-reviewer` (UI gates), `statistician` (stats gates) |
| 9. Evidence pack | Test report, screenshots or recording, validation tables, owner validation script. | `/gate-review` · `engineering:documentation` |
| 10. Handover | Report to the owner. **Never** mark a gate PASS yourself. Only the owner records PASS in `docs/GATE_LOG.md`. | `superpowers:finishing-a-development-branch` |
| 11. Close | **Only after the owner records PASS:** merge, tag, commit and push to GitHub (§14); write the closing session log (§15). | `/gate-close` |

A failed check means rework and a full re-test of the gate. Scope moves only through a logged entry in `docs/DECISIONS.md`, approved by the owner.

### 4.0 Owner approval is mandatory at every gate

- **No gate passes without the owner's approval,** given after testing and evidence presentation, through hands-on validation of multiple scenarios.
- **The owner validation script for every gate must cover at least these scenarios:**

| # | Scenario | Purpose |
|---|---|---|
| S1 | Happy path | The main user goal works end to end |
| S2 | Messy or edge input | Ambiguous dates, missing codes, empty file, boundary sizes, unusual values (as relevant to the gate) |
| S3 | Failure and recovery | Invalid action, service down, cancelled job; the error message is clear and nothing is corrupted |
| S4 | Second user / permissions | Another account can't see or change the owner's data (any gate with data or API changes) |
| S5 | Guided vs expert path | A novice can find the next action; an expert reaches the tool directly (from G04 onward, where UI exists) |
| S6 | Regression spot-check | 2–3 features from earlier gates still work |

- Mark a scenario N/A only with a one-line reason.
- Each scenario lists its steps, the expected result, and a box for the owner to mark ✓ or ✗ with a comment.
- The script should take **no more than 45 minutes**. If it needs longer, propose splitting the gate at kick-off.
- **Result:** the owner records PASS, PASS WITH CONDITIONS or FAIL in `docs/GATE_LOG.md`. Any ✗ means rework, unless the owner explicitly accepts it as a condition with a due gate.

### 4.1 TDD enforcement (mandatory, from G01 onward)

1. **RED evidence first**
   - Before any product code for a test case, commit its failing tests with the message `test(Gxx): RED for TC-xx.y …`.
   - Save the failing run output to `docs/evidence/Gxx/red/<timestamp>.txt`.
   - The RED commit's timestamp must be earlier than the first `feat`/`fix` commit that makes it pass.
2. **GREEN, then REFACTOR**
   - Implement the minimum code that makes the tests pass (`feat(Gxx): GREEN TC-xx.y …`).
   - Refactor only with all tests green.
3. **Traceability**
   - Every test that covers a gate test case carries the TC id in its name or marker:
     - pytest: `@pytest.mark.tc("TC-07.1")` or the name `test_tc07_1_…`
     - Vitest/Playwright: a `[TC-07.1]` prefix in the test title
   - `scripts/tc_trace.py` lists every TC in the active gate's section of the gate map and fails if any TC has no matching test, or if a mapped test is skipped or xfail.
4. **Claude Code hooks** (in `.claude/settings.json`, created in G01)
   - A **Stop** hook runs `scripts/verify.ps1` (lint, types, tests, `tc_trace`). Claude can't report "done" while it fails.
   - A **PreToolUse** hook on `git commit` blocks a commit that changes product code (`apps/`, `packages/`, `plugins/`) without also changing or already having tests for the same gate.
5. **Pre-commit and CI**
   - pre-commit runs ruff, mypy, ESLint and `tc_trace` on staged changes.
   - CI on every push and pull request runs the full suite, the coverage thresholds (SC-3) and `tc_trace`. A PR into `main` is blocked if coverage drops, any TC is unmapped, or any earlier gate's test fails.
6. **No weakening**
   - Never delete, skip or relax an existing assertion to get to green.
   - If a test is wrong, explain why in the gate report and get the owner's approval first.

## 5. Skill playbook (when to invoke what)

If a named skill isn't installed, follow the **Fallback** column. Never skip the step.

### 5.1 Product, research, brainstorming

| Situation | Skill | Fallback |
|---|---|---|
| Exploring a new idea or ambiguous requirement | `product-management:product-brainstorming` / `superpowers:brainstorming` | Ask the owner 2–4 focused questions, generate at least 3 options with trade-offs, recommend one |
| Turning a capability into a spec | `product-management:write-spec` | Problem, users, goals, non-goals, acceptance criteria, edge cases |
| Market or competitor questions | `product-management:competitive-brief` · `marketing:competitive-brief` · `anthropic-skills:deep-research` | Search the web, cite every claim, date every price |
| Pilot feedback and user research | `design:user-research` · `design:research-synthesis` · `product-management:synthesize-research` | Interview guide → themes → ranked insights |
| Roadmap changes after a gate | `product-management:roadmap-update` | Update the gate map via a DECISIONS entry |
| Pilot metrics (G30+) | `product-management:metrics-review` | Activation, completion, return, guidance usefulness, trust |
| Owner status updates | `product-management:stakeholder-update` · `operations:status-report` | Bullets: done, next, risks, decisions needed |

### 5.2 Design and UX

| Situation | Skill | Fallback |
|---|---|---|
| Any new screen or component | `frontend-design` · `design:design-system` | Use tokens from the theme plugin; no ad-hoc colours or spacing |
| Reviewing a screen | `design:design-critique` | Hierarchy, consistency, states, density, against the 02 spec |
| Accessibility (every UI gate) | `design:accessibility-review` | WCAG 2.2 AA: keyboard, focus, contrast, ARIA, axe clean |
| Buttons, errors, empty states, coach text | `design:ux-copy` | Plain English, action-first, no jargon, no blame |
| Handover of a UI slice | `design:design-handoff` | States, tokens, breakpoints, interactions listed |
| Charts and KPI tiles | `dataviz` · `data:data-visualization` · `data:create-viz` | Colour-blind-safe palette from theme tokens; text summary + table view |

### 5.3 Engineering

| Situation | Skill | Fallback |
|---|---|---|
| Architecture or technology choice | `engineering:architecture` (ADR) · `engineering:system-design` | ADR in `docs/adr/`: context, options, decision, consequences |
| Test design | `engineering:testing-strategy` · `superpowers:test-driven-development` | Unit, integration, E2E, reference validation; failing test first |
| Bugs | `superpowers:systematic-debugging` · `engineering:debug` | Reproduce → isolate → root cause → fix → regression test |
| Code review | `superpowers:requesting-code-review` · `engineering:code-review` | Correctness, security, performance, readability, scope creep |
| Tech debt check (every 5 gates) | `engineering:tech-debt` | List, categorise, prioritise; log in DECISIONS |
| Docs | `engineering:documentation` | README, spec pages, changelog updated in the same gate |
| Deployment (G30) | `engineering:deploy-checklist` · `operations:runbook` | Checklist, rollback, runbook |
| Incidents | `engineering:incident-response` | Triage, communicate, blameless postmortem |
| Parallel independent tasks | `superpowers:dispatching-parallel-agents` · `superpowers:using-git-worktrees` | One worktree per independent task |
| Building StatForge MCP tools (later) | `anthropic-skills:mcp-builder` | Follow the MCP spec; read-only by default |

### 5.4 Data, statistics, documents

| Situation | Skill | Fallback |
|---|---|---|
| Statistical method correctness | `/stats-validate` · agent `statistician` · `data:statistical-analysis` | NIST StRD → R oracle → textbook; tolerances in `docs/reference/07_STATISTICAL_VALIDATION.md` |
| Data-quality rules and fixtures | `data:validate-data` · `data:explore-data` | Messy-CSV fixtures with expected profile JSON |
| Reading or writing the Excel template workbook | `anthropic-skills:xlsx` · `/template-import` | openpyxl, read-only on `sources/`, never modify the source |
| Report exports | `anthropic-skills:pdf` · `anthropic-skills:docx` · `anthropic-skills:pptx` · `anthropic-skills:xlsx` | Generate from run outputs only; snapshot-test the output |
| Drafting non-source methodologies (G21) | `/methodology-draft` · agent `methodology-author` | Standard published practice, marked Draft, owner approval required |

### 5.5 Risk, operations, compliance

| Situation | Skill | Fallback |
|---|---|---|
| New risk discovered | `operations:risk-assessment` | Add to `docs/RISKS.md` with likelihood, impact, owner, mitigation |
| Scope or design change request | `operations:change-request` | DECISIONS entry: change, reason, impact, approval |
| Privacy and security readiness (G30) | `operations:compliance-tracking` · agent `security-reviewer` | OWASP ASVS L1 checklist |
| Creating a new project skill | `anthropic-skills:skill-creator` · `superpowers:writing-skills` | Frontmatter `name` and `description`; steps; checks |

## 6. Project skills and subagents (in this repo)

### 6.1 Skills (`.claude/skills/`)

| Skill | Use |
|---|---|
| `/gate-kickoff` | Start the active gate: verify the previous PASS, restate scope and tests, list files and risks, wait for "go" |
| `/gate-review` | Run SC-1…SC-11 plus the gate's test cases, call the reviewer agents, build the evidence pack and owner script |
| `/stats-validate` | Validate a statistical or calculator function against NIST, R or textbook references; produce a validation table |
| `/new-plugin` | Scaffold a plugin per `docs/reference/04_PLUGIN_CONTRACT.md` with schemas, preconditions, tests and docs |
| `/template-import` | Import or refresh templates from `sources/88_Templates`; classify; report the diff |
| `/methodology-draft` | Draft a methodology not in the source (DMADV/DFSS, PDCA, 8D, A3, Kaizen, MoM, Action Plan, generic stage-gate, Yellow Belt subset) as Draft |

### 6.2 Subagents (`.claude/agents/`)

| Agent | Role | Writes code? |
|---|---|---|
| `statistician` | Six Sigma / statistics reviewer: methods, assumptions, formulas, wording | No |
| `gate-reviewer` | Skeptical independent check of a gate's evidence against its test cases | No |
| `security-reviewer` | Authorisation, uploads, secrets, AI data flow, OWASP | No |
| `ux-a11y-reviewer` | UX consistency with the spec, WCAG 2.2 AA, copy quality | No |
| `methodology-author` | Lean Six Sigma content author for Draft methodologies and template help text | Content only |
| `qa-engineer` | Designs test cases, fixtures and edge cases for the active gate | Tests and fixtures only |

### 6.3 Gate-specific skills (just in time)

- `docs/SKILLS_MAP.md` lists the planned gate skills, e.g. `/ide-component` (G04), `/data-quality-rule` (G08), `/template-type` (G18), `/pm-feature` (G22), `/guidance-rule` (G25), `/report-section` (G26), `/prompt-template` (G27), `/integration-plugin` (G29), `/release-check` (G30).
- At kick-off, `/gate-kickoff` runs a **skill check**. If the gate's skill is missing, creating it is the gate's first task, with `anthropic-skills:skill-creator` or `superpowers:writing-skills`. The owner approves it with the brief. Then RED tests start.
- Skills encode patterns proven in this repo. No speculative skills ahead of their gate.

### 6.4 Owner prompts and questionnaires

- **The owner never has to write prompts from scratch:** `docs/OWNER_PROMPTS.md` holds ready-to-paste prompts (kick-off, plain-English brief, change request, bug report, second opinion, validation script, record decision, status).
- **At kick-off, ask the owner the standard questionnaire for the gate type** (multiple choice where possible, using the ask-user tool). See `/gate-kickoff`.

### 6.5 Product prompts and questionnaires (content rules)

- Questionnaires (G25) live in `content/questionnaires/` and prompts (G28) in `content/prompts/`. Both are versioned content, never strings hard-coded in code.
- Every prompt has an id, version, variables (allow-listed context only), token budget, status (draft/approved) and ≥ 5 evaluation cases. A prompt change without a version bump and updated evals fails CI.
- Only owner-approved prompts run in production mode.
- Questionnaires and rule-based suggestion chips must work with AI switched off.

## 7. Repository layout

```
New_Stat_Forge_v2/                 # repository root
├── AGENTS.md · CLAUDE.md · README.md
├── .claude/skills/ · .claude/agents/
├── docs/                          # guidelines, gate map, GATE_LOG, DECISIONS, RISKS, adr/, reference/
├── sources/                       # moved here in G01 — read-only inputs
│   ├── 88_Templates/              # Project Phase Template v0.1.xlsx (authoritative methodology source)
│   └── Business_Cases_Examples/   # Minitab datasets — INTERNAL FIXTURES, git-ignored (88_Templates IS committed: owner's own material, private repo)
├── apps/web/                      # React IDE shell
├── apps/api/                      # FastAPI app (+ worker entrypoint when introduced)
├── packages/engine/               # pure-Python statistical engine (no web/DB/AI imports)
├── packages/plugin_sdk/           # plugin contract + registry
├── plugins/                       # built-in plugins
├── reference_data/                # NIST, R-oracle and textbook expected values
└── docker-compose.yml
```

- `sources/Business_Cases_Examples/` must be listed in `.gitignore` before the first commit. `sources/88_Templates/` is committed (owner's own material; private repo only).
- `docs/sessions/` holds session logs; `docs/TROUBLESHOOTING.md` holds known problems and fixes (§15).
- Never modify anything under `sources/`.

## 8. Pinned stack (verified Oct 2026; change only via ADR)

- **Frontend:**
  - React 19.3 · TypeScript 6.x (not 7 until typescript-eslint supports it) · Vite 8
  - Tailwind CSS 4 · shadcn/ui (Radix) · react-resizable-panels 4 + dockview 8
  - Zustand 5 · TanStack Query 5 · TanStack Router 1
  - Plotly.js (charts from server-built specs) · AG Grid Community (MIT) · pragmatic-drag-and-drop
- **Backend:**
  - Python 3.14 · FastAPI · Pydantic 2 · SQLAlchemy 2.1 (not SQLModel) · Alembic
  - PostgreSQL 18 · DuckDB + Parquet for datasets
  - S3-compatible storage (SeaweedFS in dev; S3 or R2 in prod)
- **Statistics:** pandas 3 (Copy-on-Write idioms) · NumPy 2.5 · SciPy 1.18 · statsmodels 0.15 · scikit-learn 1.9 · Matplotlib 3.11
  - SPC constants and run rules are implemented in-house.
- **Readers:** charset-normalizer + clevercsv + pandas (read as text first) · openpyxl · pypdf + pdfplumber
- **AI:** Pydantic AI provider abstraction: Anthropic, OpenAI, Gemini, Ollama. BYO keys only, envelope-encrypted.
- **Jobs:** no queue until a gate proves the need. When it does, use Procrastinate (Postgres-backed).
- **Tooling:**
  - Python: uv · ruff · mypy `--strict` · pytest
  - JavaScript: **Node 24 LTS** · pnpm (via `corepack enable pnpm`) · ESLint · Vitest · Playwright · axe-core
  - Python is managed by uv (`uv python install 3.14`). pre-commit and gitleaks run as uv tools or standalone binaries, never as system-wide installs.
- **Forbidden without an ADR:** MinIO, Redis 8+ (use Valkey), PyMuPDF, pingouin, Zitadel, Theia/OpenVSCode embedding, AG Grid Enterprise, golden-layout, SQLModel.

## 9. Reuse from the PMO app

- **Location (read-only):** `C:\Users\60073\Python\Project_Management`. Never modify it. The owner states he owns this code.
- **Port** (re-test inside StatForge):
  - `app/services/benefit_stats.py` → hypothesis-test plugins
  - `app/services/spc.py` → SPC plugins
  - `app/engines/` → critical path, priority score, slippage
  - gate/workflow logic → generalised methodology engine
  - the Mentor's confirm-first proposal/review pattern and evals
  - file text extraction
  - registers, Kanban and Gantt behaviour, exports
  - `tools/gateway-bridge` + mail questions → Outlook plugin (G29)
  - `app/playbooks/` → guidance content
- **Never port:**
  - `data/pm.db`, attachments or any Altius data
  - seeded OKRs
  - Altius-specific gates (NFA, SCM, PR/PO), except as a neutral generic stage-gate
  - Jinja/HTMX templates
  - SQLite usage
- Record every ported file in `docs/PORTING.md`: source path, target path, changes, tests.

## 10. Statistical integrity

- Every plugin declares its ID, version, input/output schema, preconditions, warnings and tests.
- Every plugin passes at least one external certified case (NIST, R or textbook) before it is shown in the UI.
- Every run stores: plugin id and version, dataset version, inputs, parameters, outputs, warnings, library versions, timestamp, run id.
- Report n, estimates, intervals, assumptions checked, diagnostics and limitations.
- Never describe a p-value as the probability that the null hypothesis is true.
- Document rule conventions explicitly (e.g., run rule: 8 or 9 points) and make them configurable.
- Template calculators are Python functions validated against their workbook sheet.

## 11. Security and privacy

- Authorise every request by user and workspace. Return 404 rather than leaking existence.
- Never put secrets in code, the browser bundle, logs, exports or plugin contexts.
- Validate uploads server-side: size, type, magic bytes. Never execute uploaded content.
- Statistics run with CPU, memory and time limits.
- Never log dataset contents.
- Send AI the minimum context. No raw rows without explicit consent. Record consent.
- Exports are CSV-injection-safe.

## 12. Coding standards

- **Python:** type hints everywhere, `mypy --strict`, ruff (line length 100), pure functions in the engine, no I/O in statistical functions.
- **TypeScript:** `strict: true`, no unexplained `any`, small typed components, design tokens only.
- **API:** versioned under `/api/v1`, Pydantic schemas at every boundary, plain-language errors.
- **Commands:** menus, palette, shortcuts and the AI all call one command registry.
- **Tests:** test-first per §4.1; coverage ≥ 85% on new code; 100% branch coverage on statistical validation paths; earlier gates' tests always run; every gate TC is traceable to a test.
- **Git and GitHub:** see §14.
- **Environment:** Windows host with Docker Desktop; commands must work in PowerShell and inside containers.

## 13. Communicating with the owner

- Bullet points, plain professional English, direct. Say clearly what failed and why.
- Every gate handover contains:
  - files changed
  - exact test commands and results
  - validation tables
  - limitations
  - risks
  - decisions needed
  - the owner validation script
- Never claim a test passed if it was not run. Never fabricate benchmarks, validation results or prices.
- When unsure, stop and ask one focused question, or log a reversible assumption in `docs/DECISIONS.md` and flag it.

## 14. Git and GitHub

- **Remote:** `https://github.com/Raghustatics/StatForge_Project_Management.git` (**private**). Use the GitHub CLI (`gh`), authenticated by the owner with `gh auth login`.
- **Branches:**
  - `main` holds only gates the owner has passed
  - one branch per gate: `gate/Gxx-<name>`
  - Conventional Commits (`test(Gxx): RED …`, `feat(Gxx): GREEN …`, `fix:`, `docs:`, `chore:`); small commits
- **Push policy (owner rule):**
  - **Never push `main` or a gate branch before the owner records PASS** in `docs/GATE_LOG.md`.
  - **Only exception:** temporary `ci-check/Gxx-<purpose>` branches may be pushed to prove a CI test case (e.g., TC-01.4, TC-01.9). Delete them on GitHub and locally once the evidence is captured, and record them in the session log.
- **After PASS (`/gate-close`):**
  1. Confirm PASS (or PASS WITH CONDITIONS) is recorded by the owner.
  2. Make sure the working tree is clean. Commit any remaining evidence, session logs and docs (`docs(Gxx): evidence and session logs`).
  3. Merge into `main` with `--no-ff` (message `gate(Gxx): PASS — <name>`).
  4. Tag: `gate-Gxx-pass`.
  5. Push `main`, the tag and the gate branch (`git push origin main gate/Gxx-… gate-Gxx-pass`).
  6. Verify that GitHub CI is green on `main`, and record the commit SHA and CI link in the Gate Log evidence column.
- **Never:**
  - force-push
  - rewrite pushed history
  - commit secrets, `.env` files, Minitab datasets, Altius data or dataset contents (gitleaks runs in pre-commit and CI)
  - push without a PASS, except `ci-check/*`

## 15. Session logs and troubleshooting

- **One log per working session:** `docs/sessions/YYYY-MM-DD_HHMM_Gxx.md`. Write it at the end of every session, and at once whenever something goes wrong.
- **Session log contents (bullets):**
  - goal of the session and active gate
  - what was done (tasks, files changed)
  - key commands run, with summarised results (pass/fail counts, not full dumps)
  - errors and problems: symptom → root cause → fix → test that now guards it
  - decisions and questions raised (link to DECISIONS entries)
  - skills and agents used
  - open items and the next step
- **`docs/TROUBLESHOOTING.md`:** a running table of recurring or non-obvious problems: date · gate · symptom · root cause · fix · prevention. Check it before debugging. Add to it after any fix that took more than one attempt.
- **Never log:** secrets, API keys, passwords, dataset contents, personal data, Altius information.
- Session logs and troubleshooting entries are committed with the gate's evidence and pushed by `/gate-close`.

