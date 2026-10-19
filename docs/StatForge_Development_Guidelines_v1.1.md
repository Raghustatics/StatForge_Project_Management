# StatForge — Development Guidelines v1.1 (Frozen Scope — draft for sign-off)

- **Version:** 1.1 · 19 Oct 2026 · Owner: Raghu Sinha
- **Status:** APPROVED — governing baseline (signed off 19 Oct 2026)
- **Supersedes:** "StatForge — Development Guidelines v1.0" (PDF, 19 Oct 2026) and, where they conflict, the v2 doc set of 18 Oct 2026 (pricing tiers, managed AI credits and the 13-phase roadmap are withdrawn)
- **Rule:** no development plan and no code until this document is signed off

---

## 1. Product definition

- **What StatForge is:** a browser-based SaaS problem-solving platform that combines guided methodology, deterministic statistics, project management and optional AI assistance in one IDE-style workspace.
- **One-line positioning:** *Solve real operational problems with scientific rigour — and learn the method by doing it.*
- **Guiding principle (governs every decision):** **The platform guides. The statistical engine calculates. Optional AI assists. The user decides.**
- **StatForge is not:**
  - a scientific calculator, a template library, an AI chatbot or "a stats package with graphs" on its own
  - a rigid workflow that blocks users who skip a step
  - a service that pays for users' AI usage
  - a copy of the owner's internal PMO app (that app stays a separate internal tool — §13)

## 2. Objectives — human-centred assistance for real-world official work

- **Real-world official work assistance (primary)** — StatForge supports people doing their actual job: live improvement projects, reviews, tollgates and management reporting, not classroom exercises. Outputs must be fit to present to a sponsor, auditor or management.
- **Human-centred** — the person stays in charge; StatForge (and optional AI) assists, explains and prepares; it never decides, signs off or acts on the user's behalf.
- **Accessibility** — someone who knows only the problem statement gets meaningful guidance.
- **Scientific integrity** — every calculation, assumption, diagnostic and result is verifiable and reproducible.
- **Behavioural guidance** — surface missing information, stakeholders, dependencies, priorities and next actions.
- **Flexibility** — users adapt their project workflow without changing the standard methodology.
- **Extensibility** — new statistical modules, templates, AI connectors and (later) community plugins without redesign.
- **Business objective:** market acceptance and penetration first; **free at launch**; revenue later.

## 3. Users and modes

| User | Profile | StatForge behaviour |
|---|---|---|
| **A — Guided problem solver** | Knows a problem exists; limited stats/Six Sigma knowledge | Focused questions, plain language, recommended next action, learning moments |
| **B — Experienced practitioner** | Quality / engineering / statistics professional | Direct tool access, shortcuts, full configuration, transparent outputs |

- **Design rule:** guided mode by default for new users; expert mode one click away; never force an expert through an interview before a valid analysis.
- **Learning by doing:** guided mode explains *why* at each step; skills demonstrated through validated work are recorded (skill ledger) and can feed personal OKRs.

## 4. Core experience and journeys

- **First conversation** establishes three things, without demanding what the user does not know:
  - What is the problem? (statement, where, who is affected, what is known)
  - What is the objective? (intended improvement vs proven/achievable target)
  - Do you have data? (optional upload)
- **Do not** force a choice of methodology or test before the problem is understood.

| Journey | Flow |
|---|---|
| **A — Problem + data** | Problem + objective + data → profiling & EDA → candidate KPIs, measures, data-quality issues → user confirms → methodology recommendation or selection → workflow → analysis → interpretation → action plan |
| **B — Problem, no data** | Problem + objective → clarify process, symptoms, scope, impact, stakeholders → knowledge gaps, candidate KPIs, evidence needed → data-collection plan + next actions → resume when data arrives |
| **C — Expert direct** | Open any tool or template directly (e.g., a control chart, a fishbone, an MoM) without a project interview |

- All journeys work in Release 1 and converge on the same validated execution pipeline.

## 5. Methodology and template engine

### 5.1 Authoritative source

- **Source of truth:** `Project Phase Template v0.1.xlsx` (88 templates + "Worksheet Lists" index) in `C:\Users\60073\Python\New_Stat_Forge_v2\88_Templates`.
- Content is **extracted, reconciled and validated** from the source — never recreated from memory.

| Group | IDs | Count | Applies to |
|---|---|---|---|
| Lean | L01–L08 | 13 | Lean projects; optional for Six Sigma |
| Discovery | 01–11 | 11 | Black Belt; optional for Green Belt |
| Define | D01–D11 | 11 | Green Belt, Black Belt (D06, D07 BB only) |
| Measure | M01–M10 | 11 | Green Belt, Black Belt (M05 BB only) |
| Analyze | A01–A10 | 13 | Green Belt, Black Belt (A02.C BB only) |
| Improve | I01–I14 | 15 | Green Belt, Black Belt (I07 BB only) |
| Control | C01–C14 | 14 | Green Belt, Black Belt (C04, C10 BB only) |

### 5.2 Applicability rules (mapped from the source index)

- ✓ for the project track → **Required** for that track.
- "If applicable" → **Conditional** (asks a qualifying question; N/A allowed with reason).
- "Either of them should be applicable" → **Choose-one group** (e.g., A01 Why-Why or A02 Cause & Effect).
- "Optional for LSSGB / Six Sigma" → **Optional**.
- Yellow Belt track: subset of the Green Belt track — **to be defined by the owner** (open item §22).

### 5.3 Template types (each template is classified once)

| Type | Examples | Engine |
|---|---|---|
| Form / builder | D04 Problem Statement, D05 Charter, D03 Business Case | Workflow engine |
| Table / register | D07 RASCI, 06 Risk Analysis, 08 Stakeholder Analysis | Workflow engine |
| Checklist / tollgate | D10, M09, A09, I13, C12 | Workflow engine (soft/hard rule §5.6) |
| Calculator | L05 OEE, L07 Kanban card, L08 Line balancing, I03 FMEA RPN, 02 Financial savings, 03 Prioritizer | Statistical engine (validated functions) |
| Analysis-linked | M06, M07.A/B, I09, I10, I11, C08, M02/C06 GRR | Statistical engine (validated plugins) |
| Diagram | A02 Cause & Effect (fishbone), D09/I12 Process map, L06 VSM | Diagram editor |
| Narrative | Phase learnings, C11 Executive Summary | Workflow engine + report |

- Every template definition is **versioned data** (fields, tables, rules, help text, linked calculations), imported from the workbook — not 88 hand-built screens.
- Excel formulas are **re-implemented as tested Python functions**; the workbook formulas serve as reference cases.

### 5.4 Methodology catalogue — Release 1

| Methodology | Content source | Status at R1 |
|---|---|---|
| Lean (6S/5S, 8 Wastes, OEE, VSM, Kanban, Line balancing) | Owner source (L01–L08) | Source-backed |
| Discovery / project selection | Owner source (01–11) | Source-backed |
| DMAIC — Yellow / Green / Black Belt | Owner source (D/M/A/I/C) | Source-backed (YB subset to define) |
| DMADV / DFSS | Drafted by Claude from standard practice | **Draft → owner approval required** |
| PDCA, 8D, A3 | Drafted | **Draft → owner approval required** |
| Kaizen event | Drafted | **Draft → owner approval required** |
| Minutes of Meeting (MoM), Action Plan | Drafted | **Draft → owner approval required** |
| Generic stage-gate (neutral G0–G12 style) | Generalised from PMO app, Altius-specific gates removed | **Draft → owner approval required** |

- Drafted content is visibly marked **Draft** until signed off; nothing is presented as authoritative before approval.

### 5.5 Standalone use

- Any template can be used on its own, outside a methodology (e.g., only a fishbone, only a Pareto, only an MoM, only an action plan).

### 5.6 Workflow behaviour

- Each methodology has: versioned definition; ordered steps; purpose and expected outputs; prerequisites; Required/Conditional/Choose-one/Optional class; evidence requirements; linked statistical methods and validation rules; consequences of skipping.
- **Soft by default, hard optional:** users may skip, defer or mark N/A **for this project only**, with a reason; a template or (later) a team can switch on hard gates.
- A skipped step is **never** marked complete or validated; StatForge explains the risk (e.g., unresolved ownership after skipping stakeholder analysis).
- The standard definition never changes because a project deviates.

### 5.7 Data model (separation of definition and instance)

| Entity | Responsibility |
|---|---|
| Methodology definition | Official method, steps, order, rules, version |
| Step / template definition | Purpose, fields, evidence, prerequisites, guidance, linked calculations |
| Project workflow instance | Selected methodology and customised step states |
| Template instance | The user's filled template for this project |
| Evidence record | Data, notes, documents, decisions, runs |
| Workflow event | Who changed what, when |
| Recommendation | Suggested action, rationale, dependencies, acceptance status |

### 5.8 Source cleanup (before import)

- Index lists "A02.A" twice — sheets are A02.A (Service) and A02.B (Manufacturing).
- Typos: "Allignment", "Kanaban", "Continouos", "Effor-Impact".
- Empty/placeholder sheets needing content: D09, I12, A07, 10 Balance Score Card, C10.
- A02.C Brainstorming has formatting bloat (1,048,576 rows).

## 6. Human guidance layer

- Identify missing information and unresolved assumptions; explain why each matters.
- Suggest who to consult and what to obtain; recommend the next action from project state.
- Flag overdue actions and dependencies when dates and owners exist.
- Suggest stakeholder communications when context is sufficient.
- Distinguish **facts, hypotheses, recommendations and user decisions**.
- User can accept, reject, defer or edit every recommendation.
- Never claim a stakeholder was informed, a meeting happened or an action is done without user or connected-system evidence.
- **Goal: proactive guidance, not automated bureaucracy.**

## 7. Statistical engine and data integrity

### 7.1 Release 1 capabilities

- **Data:** CSV/XLSX upload (10 MB initial limit), safe preview, profiling, type detection and ambiguity reporting, missing/duplicate analysis.
- **EDA and graphs:** descriptive statistics, distributions, normality, histogram, boxplot, scatter, Pareto, run chart, dot plot, probability plot, time series.
- **Hypothesis tests:** 1-/2-sample t (Welch), paired t, 1-/2-proportion (z / Fisher), chi-square, equal variances, Mann-Whitney, Wilcoxon, Kruskal-Wallis.
- **Models:** correlation, simple and multiple linear regression with diagnostics, one-way ANOVA with post-hoc.
- **SPC (moved into R1):** I-MR, Xbar-R, Xbar-S, p, np, c, u; configurable run rules (Nelson / Western Electric — rule thresholds documented, e.g., 8 vs 9 points).
- **Capability (moved into R1):** Cp, Cpk, Pp, Ppk, PPM, Z-bench / sigma level, DPMO↔sigma (discrete).
- **Template calculators:** OEE, Kanban card, line balancing, GRR-discrete (attribute agreement), FMEA RPN, financial savings, prioritiser, effort-impact, takt time.
- Any method is shown as available **only when implemented and validated** — never because a menu item exists.

### 7.2 Data-quality rules

- Preserve the original uploaded file (immutable).
- Record every transformation as a derived, reviewable operation.
- Detect numeric-as-text, ambiguous dates, mixed types, missing markers (blank, NA, −999), category-code confusion, identifiers.
- Flag unusual values; never delete automatically.
- Ask for confirmation when ambiguity materially affects analysis.
- Validate method assumptions and report violations.
- Show sample size, exclusions, missingness, estimates, uncertainty and limitations.
- Each run stores: method + version, inputs, parameters, diagnostics, results, warnings, software versions, run id — every result traceable to its run.
- Statistical significance is never presented as business significance.

### 7.3 Validation

- **Reference sources:** NIST StRD certified values; NIST/SEMATECH handbook and textbook examples; R (base `stats`, `qcc`) as an independent oracle; PMO app outputs as regression comparison; workbook formulas for template calculators.
- **Minitab example datasets** (~147 unique across two workbooks): **internal test fixtures only, never shipped**; they carry no Minitab outputs, so correctness comes from the reference sources above; Minitab trial outputs may be added later.
- Large sets (Semiconductor 178k rows, Debt 108k, Diamonds 54k, Insurance 12k×29) are used to test limits and performance.
- StatForge ships its own original sample datasets.

## 8. Project management (ported from the PMO app, generalised)

- Kanban (drag-drop, WIP, cards linked to steps, templates, runs and evidence) and To-do.
- Next steps from the guidance layer.
- KPIs fed by analysis runs (baseline → current → target).
- OKRs: project OKRs bound to KPIs; personal OKRs bound to the skill ledger; org cascade later.
- Gantt with planned/actual, milestones and **critical path** (finish-to-start).
- Registers: risk & dependency, decision & change log, benefits & KPIs, requirements, options appraisal, stakeholders.
- Delay monitoring and attention list.

## 9. Optional AI

- **Bring your own AI only:** user's own API key (Anthropic, OpenAI, Google Gemini) or local **Ollama**. StatForge pays nothing for AI.
- **Confirm-first (from the PMO app):** every AI proposal goes to a review step with tick-boxes and editable values; nothing applies without the user's approval.
- AI may: clarify the problem; explain methodologies; interpret validated outputs; explain skipped-step risk; draft data-collection plans and stakeholder communications; suggest follow-ups; draft template content for review.
- AI may not: compute or alter numbers (every number must trace to a run); silently change data; decide the business objective; execute code.
- Minimum context by default (problem, measures, workflow state, validated results); raw rows only with explicit consent.
- **Credential and cost controls:** never ask for provider passwords; never store third-party logins; API keys encrypted, never exposed to browser, logs, analytics or plugins; explain which provider receives data; consent before transfer; disconnect and delete keys at any time.
- Consumer chat websites (ChatGPT/Claude logged-in sessions) are **not** treated as APIs.
- The full product works with AI switched off.

## 10. Outlook Copilot Gateway (optional plugin, Release 1)

- Ported from the PMO app's Gateway bridge as an **opt-in plugin**.
- **Conditions:**
  - Enabled per user; off by default.
  - Runs only in the user's own browser, with their own Microsoft 365 Copilot licence; StatForge never holds Microsoft credentials.
  - Every answer goes to the review step with confidence, basis and source; nothing auto-applies.
  - Clear notice that the user's organisation policy may not permit it; user accepts responsibility to comply.
  - Admin/global kill switch; manual copy-paste fallback always available.
  - Extension targets the StatForge domain (not localhost); passes a security review before R1 release.
- Official Microsoft Graph integration is a later-roadmap item.

## 11. IDE experience (full shell in R1)

- Top menu (File, Edit, View, Project, Data, Analyze, Graph, Run, Window, Help).
- Activity rail; project/file explorer with drill-down and segments.
- Workbench with tabs and splits (templates, datasets, runs, boards, reports).
- Insights pane (status, KPIs, charts, to-do, next steps, OKR progress).
- AI pane (modes, provider choice, proposals, approvals).
- Output / problems / runs / audit panel; status bar; command palette; keyboard shortcuts.
- Theme and font plugins (dark, light, high contrast); WCAG 2.2 AA.
- Both conversational and direct interaction; users can revisit earlier decisions.
- Reference: 18 Oct prototype and `02_UX_IDE_SPEC.md`.

## 12. Reports and export (R1)

- Saved analyses and charts; re-open and re-run past runs.
- Project storyboard report (charter → baseline → analysis → improvement → control → learnings / executive summary).
- Export: PDF, Excel, CSV, PNG/SVG; template export back to Excel layout where useful.

## 13. Relationship to the PMO app and reuse

- **PMO app stays internal** (local, Altius portfolio governance). StatForge is a **new repository**.
- **Owner states he owns the PMO app code personally** — keep written confirmation on file before commercial launch.
- **Port (re-tested in StatForge):**
  - benefit statistics (`benefit_stats.py`) → hypothesis-test plugins
  - SPC/capability (`spc.py`) → SPC plugins (after reference validation)
  - engines: critical path, priority score, slippage
  - gates/workflow logic → generalised workflow engine
  - Mentor confirm-first proposal/review pattern and evals
  - file text extraction (PDF, Word, PowerPoint, Excel, .msg)
  - registers, Kanban/Gantt behaviour, exports
  - Gateway bridge + mail question builder → Outlook plugin (§10)
  - playbooks → methodology guidance content
- **Do not port:** any Altius data (`pm.db`, attachments, seeded OKRs); Altius-specific gates (NFA, SCM, PR/PO) except as a neutral generic stage-gate; Jinja/HTMX UI; SQLite.

## 14. Architecture

- **Most important decision:** the **workflow engine**, **statistical engine** and **guidance layer** are separate, coordinated components; the user keeps control.

| Layer | Responsibility | Technology |
|---|---|---|
| Web frontend | IDE shell, workspace, data views, templates, chat, reports | React + TypeScript |
| Application backend | Auth, projects, workflow state, orchestration, entitlements | Python + FastAPI |
| Statistical services | Validated computations and calculators | pandas, NumPy, SciPy, statsmodels |
| Data and metadata | Projects, templates, runs, history; original files and derived artefacts | PostgreSQL + S3-compatible object storage |
| Integration boundary | AI connectors, Outlook plugin, future services | Provider abstraction |
| Entitlement layer | Access rules now, subscription eligibility later | Backend service |
| Plugin framework | Internal contracts and extension points | Manifest-based, trusted built-ins only |

- Introduce a worker queue only when execution time justifies it; no microservices or distributed runtime before a proven need.
- Plugin strategy: Phase 1 internal contracts → Phase 2 expanded modules → Phase 3 public catalogue with permissions, review, isolation.

## 15. Accounts, entitlements, hosting

- Individual sign-up in R1; organisation/membership model present for later teams.
- **India region first**; data residency stated to users.
- Entitlement layer from day one; **no billing in R1**; free access at launch.
- Transition to paid access: explicit, tested and communicated before it takes effect.
- Free-personal vs paid-commercial licensing: **deferred** until commercial and legal review.

## 16. Security, privacy, reliability (MVP — not postponed)

- Server-side authentication and authorisation; project-level access controls.
- File size/type validation; safe parsing; uploaded content never executed.
- Execution, resource and time limits.
- No cross-user data access (tested).
- Secret handling; restricted logs (no dataset contents).
- Clear retention and deletion; user can delete projects and data.
- Explicit disclosure and consent for external AI transfer.
- Graceful failure for files, calculations, providers and integrations.
- 10 MB is a starting limit — measure actual use before raising.

## 17. Release 1 scope (frozen)

- This is the **scope of Release 1**, delivered stage-wise through 20–30 small gates (§18) — not built in one go.

- **A. IDE shell** — §11.
- **B. Journeys A, B and C** — §4, guided and expert modes.
- **C. Methodology & template engine** — 88 source templates + drafted methodologies (§5.4), standalone templates, soft/hard gates.
- **D. Data & statistics** — §7.1 including SPC, capability and template calculators.
- **E. Project management** — §8.
- **F. Optional AI** — §9.
- **G. Outlook Copilot Gateway plugin** — §10.
- **H. Reports & export, security baseline, provenance** — §12, §16.

**Deferred (roadmap, not dropped):**

- DOE, MSA/Gage R&R (continuous), multi-vari, logistic regression, nonnormal capability, reliability.
- Team workspaces, mentor review, org OKR cascade.
- Billing and subscriptions; managed/hosted AI.
- Public plugin marketplace and third-party plugins.
- Official Microsoft Graph integration; other third-party integrations.
- Desktop app; additional regions and languages.

## 18. Quality gates and definition of done

- A feature is not complete because it appears in the UI.
- Every feature: documented user problem and acceptance criteria; defined inputs, outputs and failure cases; tested behaviour; independently validated statistics; clear warnings for ambiguous/unsupported cases; results traceable to inputs and parameters; verified access controls; understandable explanation to the user; no regression of existing workflows; updated docs and version history.
- Guidance layer is tested on whether inexperienced users can identify the next action and why — not only complete the screen.
- **Delivery gates (stage-wise, never all in one go):**
  - Release 1 is the destination, not one delivery. It is reached through **20–30 small, sequential gates**.
  - Each gate delivers one small, testable capability (a vertical slice), not a layer of half-finished parts.
  - Each gate defines, before work starts: scope, out-of-scope, dependencies, **test cases**, **individual checks**, evidence to produce, and the owner's validation steps.
  - A gate passes only when **every** test case and individual check passes, evidence is recorded, and the owner records PASS in the gate log.
  - The next gate's implementation does **not** start until the current gate has passed.
  - A failed check sends the gate back for rework; scope is never moved to a later gate silently — only by a logged decision.
  - Earlier gates' tests keep running at every later gate (no regression).

## 19. Market-acceptance metrics

| Metric | Question |
|---|---|
| Activation rate | Can users start a project and reach a useful first result? |
| Time to first meaningful result | Does guidance reduce effort to start? |
| Workflow completion | Do users progress from problem to evidence-backed conclusions? |
| Return usage | Is it useful beyond the first demo? |
| Guidance usefulness | Are recommendations accepted, modified or rejected for clear reasons? |
| Statistical reliability | Are results correct, reproducible and qualified? |
| User trust | Do users understand evidence, limitations and next steps? |

- Pilot with both inexperienced employees and experienced practitioners.

## 20. Delivery approach (sequence only — the detailed gate plan follows sign-off)

- The stages below are delivered through the 20–30 small gates defined in §18; each stage spans several gates.
- The gate map (gate list, test cases, checks, owner validation per gate) is the first deliverable **after** sign-off.

1. **Research & specification** — source import design, template classification, traceable requirements spec.
2. **Architecture & contracts** — data models, plugin/statistics interfaces, AI and Outlook boundaries, security, acceptance tests.
3. **Deterministic core** — data, statistics, SPC, workflow, templates, PM, reports.
4. **AI and Outlook plugins** — on top of a working deterministic core.
5. **Guided pilot** — real users; measure completion and trust; fix friction.
6. **Expansion** — deferred roadmap items by evidence.

## 21. Risks (direct)

- **Release 1 is large:** 88 templates + 8 drafted methodologies + full PM suite + SPC + AI + Outlook + IDE shell. Mitigation: data-driven template engine, ported PMO engines, gated increments.
- **Content load on the owner:** approving drafted methodologies and defining the Yellow Belt subset is owner work that can block release.
- **Validation without Minitab outputs:** relies on NIST/R/textbook references; budget time for it.
- **Outlook plugin:** depends on Microsoft's web UI (can break) and customers' tenant policies.
- **IP:** keep written confirmation of personal ownership of ported code.
- **Solo bandwidth:** Claude Code accelerates coding, not owner reviews and validation sign-offs.

## 22. Open items (owner)

- Define the Yellow Belt track subset.
- Review and approve drafted methodologies (§5.4) as they are produced.
- Provide content for empty source sheets (D09, I12, A07, 10, C10) or approve drafts.
- Trademark search for "StatForge".
- Choose hosting provider within India region (before pilot).
- Identify pilot users (guided and expert).

## 23. Decision log (19 Oct 2026)

| # | Decision |
|---|---|
| 1 | StatForge is a new clean product; PMO app stays internal |
| 2 | Owner states personal ownership of PMO app code; reuse allowed |
| 3 | Positioning: guided problem-solving; learning by doing |
| 4 | BYO AI (API key or Ollama), free first, entitlements only, no billing |
| 5 | R1 analysis: profiling/EDA/graphs, tests, regression/ANOVA, **plus SPC and capability** |
| 6 | R1 project: methodology engine, Kanban/To-do/next steps, KPIs/OKRs, Gantt/CPM/registers |
| 7 | Gates soft by default, hard optional |
| 8 | Outlook Copilot Gateway: optional plugin in R1 with conditions |
| 9 | Reuse: port Python engines; new React IDE shell; PostgreSQL |
| 10 | Methodologies: Lean, Discovery, DMAIC (source) + DMADV/DFSS, PDCA, 8D, A3, Kaizen, MoM, generic stage-gate (drafted, owner-approved) + standalone templates |
| 11 | Source: `New_Stat_Forge_v2` (88 templates; Minitab datasets) |
| 12 | Individual accounts, team-ready model; India region first |
| 13 | AI mentor in R1, confirm-first |
| 14 | Template calculations become validated Python functions |
| 15 | Minitab datasets: internal test fixtures only |
| 16 | Full IDE shell and reports/export in R1 |
| 17 | Stage-wise delivery through 20–30 small gates; every test case and check must pass before the next gate starts |

---

**Sign-off:** ☑ Approved as the Release 1 baseline — Raghu Sinha · 19 Oct 2026
