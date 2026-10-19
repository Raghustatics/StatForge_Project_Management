> **Reference spec (18 Oct 2026).** Subordinate to `docs/StatForge_Development_Guidelines_v1.1.md` and `docs/StatForge_Gate_Map_v1.0.md`. Where this file mentions pricing tiers, managed AI credits, a 13-phase roadmap or Keycloak-first auth, the guidelines v1.1 decisions win.

# StatForge Must Sell Trust, Not Features

**Bottom line:** StatForge's opening is not "Minitab in a browser". Minitab already ships web access, and MoreSteam's EngineRoom already sells a cloud tool with an AI guide for **$495/year**. The real gap is narrower and easier to defend: an affordable workspace where **validated, deterministic statistics, a mentor that asks about the business problem and explains why a method fits, and DMAIC tollgates linked to analyses you can re-run** all live in one place. Today these are spread across $2.4k+ Minitab bundles, Excel add-ins that offer no guidance, and AI notebooks that generate code non-programmers cannot audit. The AI-workspace market has standardised on "the agent writes code, the user approves it". StatForge's model is different: the AI only proposes a pre-validated plugin call, and Python computes. That is the one structural advantage no competitor surveyed offers, and it answers the top complaint about AI data tools ("confidently wrong" numbers). The stack should be deliberately boring: **React 19.3 + Vite 8 + FastAPI + PostgreSQL 18 + DuckDB/Parquet**, a **self-built SPC engine**, and avoidance of six specific licence traps (Redis 8, Zitadel, PyMuPDF, pingouin, MinIO, and to a lesser extent Theia). On money, the only analyst estimate puts Six Sigma training at **about USD 4.2B (2025)**, and **about 63%** of that is corporate-funded. That points to a cheap individual tier (about USD 10–15/month, about INR 499–799/month) for adoption, with revenue coming from cohort and team licences sold through training providers.

---

## 1. Incumbents own the toolkit; nobody owns coaching under $500

**Key takeaways**
- Core belt statistics (SPC, Cp/Cpk, tests, regression/ANOVA, DOE, Gage R&R) are **table stakes**. Without validated versions of these, nothing else matters.
- The price ladder has a hole between **about $400 (Excel add-ins, no guidance)** and **$1,390–$2,793/year (JMP/Minitab)**. EngineRoom alone sits in it, at $495/year.
- Minitab is the most aggressive AI mover, but its AI produces outputs (summaries, dashboards, formulas). It does not coach.

**Incumbent snapshot (October 2026)**

| Vendor | Delivery | Price (per user) | Guidance / AI | DMAIC project layer | Main weakness |
|---|---|---|---|---|---|
| **Minitab Solution Center** | Cloud + desktop | **$2,394 (Core) / $2,593.50 (Analytics) / $2,793 (Copilot) per year**; add-on modules incl. MSA **$528/year** each ([Minitab](https://www.minitab.com/try-buy/)) | Rule-based Assistant + AI summaries, NL data prep, AI dashboards, AI Brainstorm (Nov 2025) ([Minitab blog](https://blog.minitab.com/en/blog/the-future-of-analytics-introducing-new-ai-powered-solutions)) | Workspace (Core/Copilot only); Engage (quote only) | Price and licensing: **68% negative sentiment** on that topic ([Capterra](https://www.capterra.com/p/109731/Minitab-17/)) |
| **JMP / JMP Pro** | Desktop; JMP Live for sharing | **$1,390 / $8,820 per year** ([JMP Store](https://store.jmp.com/)) | JMP Assistant (NL to JSL) is a **separate marketplace extension**, not in core ([JMP Blog](https://community.jmp.com/t5/JMP-Blog/How-JMP-s-groundbreaking-visual-interface-is-bolstered-by/bc-p/898311)) | None found | "Quite expensive for small business", learning curve ([Software Advice](https://www.softwareadvice.com/bi/jmp-profile/)) |
| **SigmaXL** | Excel add-in | **$399 perpetual**, no subscriptions ([SigmaXL](https://sigmaxl.com/Pricing.html)) | None (no generative AI) | None | Hidden functions, macro friction ([Capterra](https://www.capterra.com/p/109733/SigmaXL/)) |
| **QI Macros** | Excel add-in | **$379 perpetual** ([QI Macros](https://www.qimacros.com/support/purchasing/)) | Chart-selection wizard, no AI | None | Users ask for "a description of WHY to pick one stat over the other" ([Capterra](https://capterra.com/p/106996/QI-Macros-SPC-Software-Excel/)) |
| **EngineRoom (MoreSteam)** | Cloud, PC + Mac | **$495/year**, 30-day trial ([MoreSteam](https://www.moresteam.com/engineroom/)) | **"Hexie" AI** for tool selection, next steps and interpretation | VSM, fishbone, CTQ; DMAIC tracking in separate TRACtion | MSA and regression coverage not confirmed |
| **Statgraphics** | Desktop + Online (Stratus) | Not published; third-party figure of $990/year is unverified ([Zoftwarehub](https://zoftwarehub.com/products/statgraphics-centurion/pricing)) | StatAdvisor plain-language output; ML wizard (v20 beta) ([Statgraphics](https://www.statgraphics.com/)) | None found | Low visibility; site partly stale |

**What the evidence says**
- **Minitab's Assistant is still the guidance benchmark.** It is a deterministic decision tree with Report Cards that check normality, unusual points and sample size, and it exports to Word and PowerPoint ([Minitab Assistant](https://www.minitab.com/en-us/products/minitab/assistant/)). It explains *which* test to use, not *why it fits your business problem*.
- **Minitab is iterating fast on AI.** The March 2026 release extended AI summaries to more graph types and added "AI-generated calculated columns" ([Minitab readme](https://www.minitab.com/content/dam/www/en/uploadedfiles/documents/readme/MinitabSolutionCenter_March_2026_ES.pdf)).
- **Minitab splits statistics and projects across products.** Workspace has DMAIC/PDCA/Kaizen roadmaps, charters, FMEA, VSM and fishbone ([Workspace features](https://www.minitab.com/en-us/products/workspace/features/)). Formal stage-gate reviews are only in Engage ([Engage features](https://www.minitab.com/en-us/products/engage/features/)). Analyses reach a tollgate as *captured documentation*, not live, re-runnable runs.
- **No incumbent was found doing 8D templates or OKR linkage.** Engage's idea scoring against "strategic priorities" is the closest thing ([Minitab Engage](https://minitab.com/products/engage)). This finding rests on absence of evidence.
- **Training is sold separately everywhere.** Official Minitab courses ran **$450–$1,600 per person** (2023 figure) ([Learn Lean Sigma](https://www.learnleansigma.com/data-analysis/is-minitab-worth-it/)). MoreSteam bundles courses, simulations and coaching around EngineRoom, which makes it the closest "learn by doing" incumbent.

**Direct verdict:** EngineRoom, not Minitab, is your most dangerous direct competitor. It already has browser delivery, an AI guide, training and a sub-$500 price. Benchmark it hands-on before writing positioning copy.

---

## 2. AI notebooks write code that belts cannot audit

**Key takeaways**
- Hex, Deepnote, Posit, Jupyter, Colab, Databricks and Snowflake all target **data teams or coders**. Julius, ChatGPT and Claude target **generalists**. None targets the Six Sigma belt.
- **Every one follows the same pattern:** the LLM writes Python/SQL/R, a sandbox runs it, and the user approves the cell or diff. Their safeguards amount to "review the code", which a non-programmer cannot do.
- **No surveyed AI workspace ships validated SPC, capability, Gage R&R or DOE modules.** The LLM picks the library and the formula on the fly.

**AI workspace snapshot**

| Product | Target user | Entry paid price | Approval model | Statistical depth |
|---|---|---|---|---|
| **Hex** | Data teams / BI | **$36/editor/month** Pro, $75 Team; AI is credit-metered ([Hex](https://hex.tech/pricing/)) | Per-cell Confirm/Undo, lineage checks before deletes ([Hex docs](https://learn.hex.tech/docs/explore-data/notebook-view/notebook-agent)) | Generic BI cells (Pivot, Chart) |
| **Deepnote** | Data teams | **$39/editor/month** Team, incl. $39 AI credits ([Deepnote](https://deepnote.com/pricing)) | Agent; BYO-LLM is Enterprise-only | Generic notebook |
| **Julius AI** | Business users | **$20 / $45 / $450 per month** ([Julius](https://julius.ai/pricing)) | Chat-first; execution not disclosed | Generic |
| **MLJAR Studio** | AutoML users | $20/month or **$199 perpetual** with local LLMs ([MLJAR](https://mljar.com/pricing/)) | Local execution | ML-focused |
| **Posit AI** | R/Python coders | **From $20/month** (launched 5 May 2026) ([Posit](https://posit.co/blog/posit-ai-now-available-all)) | Plan mode, granular permissions, also "YOLO" mode ([Positron docs](https://positron.posit.co/assistant.html)) | tidymodels prediction skill only |
| **Jupyter AI v3** | Developers | Free / open source | Bring-your-own agent; permission prompts ([Jupyter AI](https://jupyter-ai.readthedocs.io/en/v3/getting-started.html)) | Whatever the agent writes |
| **Databricks / Snowflake** | Enterprise data platforms | Platform pricing | Allow/Skip or Auto-approve ([Databricks](https://docs.databricks.com/gcp/en/notebooks/ds-agent)) | Generic |
| **ChatGPT / Claude** | Everyone (substitute) | Consumer plans | ChatGPT "may choose a method or chart type that doesn't match your intent" ([OpenAI Help](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt)); Claude runs Python in a sandbox ([Claude Help](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)) | Generic |

**Patterns that matter for StatForge**
- **Credit-metered AI is now standard** (Hex, Deepnote, Julius, Posit), and it is also the **top churn trigger**. Julius sits at **1.8/5 on Trustpilot (20 reviews)**, with complaints about credits draining and "invented data and analyzed the wrong variables" ([Trustpilot](https://pl.trustpilot.com/review/julius.ai)). The sample is small and the profile is unclaimed, so treat this as a signal, not proof.
- **Audit logs and long version history sit behind Enterprise tiers.** Hex and Deepnote keep 7 days of history on free and 30 days on mid tiers, and audit logs are Enterprise-only ([Hex](https://hex.tech/pricing/), [Deepnote](https://deepnote.com/pricing)). These are security logs, not *statistical provenance* such as data hash, confirmed transformations, method rationale or assumption results.
- **Auto-approve and "YOLO" modes exist** (Databricks, Posit). That is the opposite of what an audit-conscious quality professional needs.
- **The ~$20/month individual anchor** (Julius Plus, MLJAR Pro, Posit AI) is the price your buyers will mentally compare you against.

**Direct verdict:** The biggest substitution threat is not Hex. It is a belt who already pays for ChatGPT or Claude and decides "good enough". You win only if you can **show, side by side, a generic LLM getting a control limit or Cpk wrong** (for example, an I-chart using overall SD instead of MR-bar/d2) while StatForge gets it right, with assumption checks.

---

## 3. Competitive brief

### Positioning statement
- **For** Six Sigma belts (in training and practising) and operations managers who must turn messy operational data into tollgate-ready evidence,
- **StatForge is** a browser-based statistical workspace that coaches you through DMAIC/PDCA/8D,
- **that** runs validated Python statistics, checks assumptions before it runs any method, and links every result to your project phase and KPIs/OKRs,
- **with** an AI mentor that clarifies the problem, explains *why* a method fits, and proposes actions you approve, **but never produces a number itself**,
- **unlike** Minitab (stats and project management split across $2.4k+ bundles), Excel add-ins (no guidance on *why*) and AI notebooks/ChatGPT (code you cannot audit, methods chosen for you).
- **One-liner:** *"The system guides. Python calculates. AI explains. You decide."* This is already your principle, and it is also your best headline.

### Messaging comparison matrix

| Dimension | **StatForge (target)** | Minitab | JMP | SigmaXL / QI Macros | EngineRoom | Hex / Deepnote | Julius / ChatGPT / Claude |
|---|---|---|---|---|---|---|---|
| **Core promise** | Learn by doing on real projects with trustworthy statistics | All-in-one OpEx platform | Visual statistical discovery | Cheap Minitab alternative in Excel | Web tool + training + AI guide | Collaborative data notebooks | Ask your data anything |
| **Price signal** | ~$10–15/month (proposed) | $2,394–$2,793/year | $1,390–$8,820/year | ~$380–400 one-time | $495/year | $36–75/editor/month | $20–45/month |
| **Who computes numbers** | Validated plugins only | Deterministic engine | Deterministic engine | Excel macros | Deterministic engine | LLM-written code | LLM-written code |
| **Guidance style** | Socratic: asks about Y, X, design; explains *why* | Rule-based Assistant + AI summaries | Optional add-on AI | Wizard, no *why* | Hexie AI picks tools | Code agent | Chat |
| **Assumption gates** | Mandatory, plain language | Report Cards | Manual | Minimal | Unclear | None | None |
| **DMAIC / 8D / OKR** | Integrated; KRs computed from re-runnable analyses | Separate Workspace/Engage; no OKR | None | None | Separate TRACtion | None | None |
| **Data-change policy** | Never silent; transformation diff + approval | Not documented | Not documented | Manual | Not documented | Cell undo | Not documented |
| **Learning built in** | Yes, skills credited only after correct use | Paid separately | Free student licence | Webinars | Courses sold alongside | No | No |
| **Message to own** | "KRs you can trust" / "never an invented number" | — | — | — | — | — | — |

### Opportunities (ranked by evidence strength)
1. **Price-to-guidance gap.** Minitab-grade guidance plus a generative mentor at near add-in prices. This is backed by the 68% negative sentiment on Minitab price and licensing ([Capterra](https://www.capterra.com/p/109731/Minitab-17/)).
2. **"Explain the why" coaching.** Directly requested by QI Macros users ([Capterra](https://capterra.com/p/106996/QI-Macros-SPC-Software-Excel/)). No incumbent was shown asking clarifying business questions first.
3. **Live DMAIC + OKR + analysis linkage.** Minitab splits this across three products, and no OKR tool validates the metric. The OKR market tracks numbers via BI/CRM connectors but **does not compute Cpk or control-chart status** ([Tability](https://www.tability.io/compare/pricing/perdoo), [Mooncamp](https://mooncamp.com/blog/perdoo-vs-quantive)).
4. **Statistical provenance at SMB prices.** Competitors gate audit logs behind Enterprise. A "methods and evidence" record per tollgate is a concrete deliverable a belt can show an assessor.
5. **Include MSA and 8D in the base product.** Minitab charges $528/year for MSA, and 8D is absent from Engage templates.
6. **Certification-project evidence.** Green Belt projects often must show **USD 10K–50K** impact and Black Belt **USD 100K+** ([iSixSigma](https://www.isixsigma.com/methodology/what-is-the-cost-of-lean-six-sigma-training-and-certification/)). A storyboard export (charter → baseline → analysis → control plan → savings) maps directly onto that requirement.
7. **B2B2C via training providers.** Online programmes already use "simulated projects" ([iSixSigma](https://www.isixsigma.com/methodology/what-is-the-cost-of-lean-six-sigma-training-and-certification/)). StatForge can be their practice lab.

### Threats
- **EngineRoom** already combines web delivery, AI guidance, training and a $495 price. It is the closest analogue.
- **Minitab's brand plus AI velocity.** Training programmes standardise on Minitab, and it has shipped AI updates in Mar 2024, Nov 2025 and Mar 2026.
- **ChatGPT/Claude "good enough".** These are near-zero marginal cost for users who already subscribe.
- **AI cost exposure.** Credit models are standard, but customers punish opaque credits (the Julius complaints). If you subsidise AI too generously, gross margin dies.
- **Credibility gap.** Quality professionals and assessors trust Minitab output. One wrong Cpk in a public demo would be fatal. Validation against reference cases is a survival requirement, not polish.
- **Solo-builder scope risk.** The full vision spans statistics, PM, OKR, learning and an agent. Each competitor does one or two of these with a team.

### Recommended actions
- **Benchmark EngineRoom hands-on** (30-day free trial). Document exactly where Hexie fails to ask business questions or check assumptions.
- **Build a public "reference case" suite** of NIST-style datasets with known Cpk, control limits and t-test results. Publish StatForge vs. generic-LLM comparisons as marketing proof.
- **Lead the MVP with the belt-project loop:** CSV → data-quality review → I-MR/Xbar-R + capability + 2-sample t/ANOVA → DMAIC storyboard export. Defer the full OKR module. A single "KR = computed metric" link is enough to prove the concept.
- **Make deterministic computation unmetered.** Meter only AI mentor usage. Users should never pay credits to compute a Cpk.
- **Sign two or three Indian training providers** as design partners for cohort pilots before building Team features.
- **Write the "AI governance" page on day one:** what the AI can and cannot do, with BYOK, no-training and data-handling statements. Incumbents publish nothing comparable.

---

## 4. Build the IDE shell from VS Code's skeleton and Kiro's gates

**Key takeaways**
- Copy VS Code's **naming and declarative contribution model**, not its runtime.
- Copy the agent-IDE convergence (**modes, editable plan artifacts, task lists, hunk-level review, checkpoints, permission policies, @-mentions, steering files**), translated into statistical terms.
- **Kiro's Requirements → Design → Tasks with gates maps almost one-to-one onto DMAIC tollgates.**

### Shell layout: VS Code containers mapped to StatForge
VS Code's official parts are the Activity Bar, Primary Sidebar, Secondary Sidebar, Editor Groups, Panel and Status Bar. Left Status Bar items are workspace-scoped and right items are file-scoped ([VS Code UX overview](https://code.visualstudio.com/api/ux-guidelines/overview)).

| VS Code part | StatForge use |
|---|---|
| Activity Bar | Mode switcher: Explorer · Data Quality · Analyses/Plugins · Projects (DMAIC/Kanban/OKR) · Mentor · Settings |
| Primary Sidebar | Project/dataset/run tree; DMAIC phase tree; plugin catalogue |
| Editor Groups | **Custom editors** in tabs: dataset grid, EDA dashboard, analysis run, report, Kanban board; split to compare data vs. result |
| Secondary Sidebar | AI Mentor pane (matches Cursor / VS Code Chat practice) |
| Panel | Output/execution log · **Problems** (data-quality and assumption failures, click to jump to column) · run console |
| Status Bar (left / right) | Left: project, worker status, plan, AI provider. Right: rows × cols, assumption status, date-parse status |
| Welcome views / Walkthroughs | Empty states ("No dataset → Upload CSV") and the two entry workflows (dataset-first, question-first) |

### Plugin and command model
- **VS Code has 38 contribution points**, including `commands`, `menus`, `views`, `configuration`, `walkthroughs`, `customEditors`, and newer AI points such as `languageModelTools` ([Contribution Points](https://code.visualstudio.com/api/references/contribution-points)).
- **Give each plugin a `statforge.plugin.json`** declaring commands, views, menus, input/output schema, validators and activation events, with `when` clauses (for example `dataset.hasDateColumn`, `project.phase == Analyze`). This gives an extensible UI **without running third-party UI code**.
- **Make every action a registered command.** The palette, menus, shortcuts **and the AI agent's tool calls** then hit the same registry. That makes agent actions auditable and approval-gated by construction.
- **Themes:** use a flat token map like VS Code's `colors`, with defaults for dark, light, highContrast and highContrastLight ([Color Theme guide](https://code.visualstudio.com/api/extension-guides/color-theme)). Put chart palettes in the token map so plots follow the theme.

### Agent UX patterns to borrow

| Pattern | Source | StatForge translation |
|---|---|---|
| **Ask / Plan / Agent modes**, `Shift+Tab` rotation | Cursor Plan Mode asks clarifying questions and writes an editable Markdown plan ([Cursor](https://cursor.com/docs/agent/modes)); Devin Desktop/Windsurf Code/Plan/Ask ([Devin docs](https://docs.devin.ai/desktop/cascade/modes)) | **Explain** (read-only) · **Clarify & Recommend** (editable Analysis Plan: objective, Y, design, candidate methods, assumptions, limits) · **Execute** (run approved plugins) |
| **Artifacts with inline comments** | Antigravity: Task List, Implementation Plan, Walkthrough, review policy incl. "Always Proceed" ([Google Codelab](https://codelabs.developers.google.com/getting-started-google-antigravity)) | Analysis Plan, Data-Quality Report, Run Walkthrough (what was computed, parameters, dataset version), evidence charts. All commentable. |
| **Spec trio + gates** | Kiro: `requirements.md`, `design.md`, `tasks.md`; Quick Spec skips gates; tasks run in dependency waves ([Kiro Specs](https://kiro.dev/docs/specs/)) | Define = requirements/CTQs · Measure+Analyze = data plan, MSA, method selection · Improve+Control = task list. **"Approve phase" = tollgate.** Quick mode for experienced belts. |
| **Steering files** | Kiro `.kiro/steering/` with always/fileMatch/manual/auto inclusion ([Kiro Steering](https://kiro.dev/docs/steering/)) | `context/business.md`, `data-dictionary.md`, `standards.md` (alpha, CI conventions): user-owned and visible |
| **Hooks** | Kiro `PostFileSave`, `PreToolUse` ([Kiro Hooks](https://kiro.dev/docs/hooks/)) | "On upload → profile", "on run → regenerate report". **Built-in commands only, no shell.** |
| **Hunk-level review** | Zed Review Changes, accept or reject per hunk ([Zed](https://zed.dev/docs/ai/agent-panel)) | **Transformation diff:** before/after column profile, rows affected, effect on summary stats; accept per transformation |
| **Checkpoints** | Cursor: restore reverts files but keeps the conversation ([Cursor](https://cursor.com/docs/agent/overview)) | Versioned dataset + analysis snapshots; original upload always preserved |
| **Permission policies** | Antigravity security presets; Zed allow/deny/confirm | Risk classes: read/profile = allow · run plugin = ask (default) · **any data transformation = always ask** · export/share = ask |
| **@-mentions** | Zed: files, symbols, threads, diagnostics ([Zed](https://zed.dev/docs/ai/agent-panel)) | `@dataset`, `@column`, `@run`, `@chart`, `@phase`, `@okr` |

### What to deliberately *not* copy
- **Auto-approve / YOLO modes for data transformations.** These would contradict your data-integrity rules.
- **Code-first surfaces.** Point-and-click plugin forms must lead. Code (Monaco) stays an optional, secondary view for power users.
- **Embedding Theia or OpenVSCode.** Both assume a file-system workspace and code editing, are heavy to host per user, and need deep framework expertise. Theia is EPL-2.0/GPL-2.0 ([EclipseSource](https://eclipsesource.com/blogs/2024/07/12/vs-code-vs-theia-ide/)). A custom React shell that borrows VS Code's *vocabulary* is lighter and better suited to datasets, runs and boards.

### Accessibility (bake in from day one)
- **F6 / Shift+F6 to cycle between parts**, a Tab-trap toggle, an "Accessible View" for chat output and context-sensitive help (`Alt+F1`) ([VS Code Accessibility](https://code.visualstudio.com/docs/configure/accessibility/accessibility)).
- **Agent stream:** use `aria-live="polite"` for state changes only ("Approval required: impute 12 values"), never for streamed tokens.
- **Charts:** auto-generated text summary **from computed stats (not AI)** plus a "view as table" toggle, with a colour-blind-safe palette.
- **Approvals:** keyboard-operable, and status shown with icon plus text, never colour alone.

---

## 5. Recommended stack: boring core, owned SPC engine

**Key takeaways**
- **Database answer:** **PostgreSQL 18** for metadata (JSONB, row-level security, job queue on the same DB), **DuckDB 1.5 over Parquet** for dataset profiling, and **S3-compatible object storage** for immutable originals. **Do not use MinIO.**
- **Build SPC yourself.** Python has no mature SPC library. Even the newest one says R has had `qcc` since 2004 and "Python does not" ([PyPI shewhart](https://pypi.org/project/shewhart/)).
- **Hold back on brand-new majors:** TypeScript 7.0, Python 3.15, Polars 2.0, PostgreSQL 19 and Jotai 3.

### Recommended stack (versions as of 18 Oct 2026)

| Layer | Choice | Version | Licence | Why / caution |
|---|---|---|---|---|
| UI framework | **React** | 19.3.1 ([npm](https://www.npmjs.com/package/react)) | MIT | Mainstream, recently patched |
| Build | **Vite** + `@vitejs/plugin-react` | 8.3.4 / 6.1.2 ([npm](https://www.npmjs.com/package/vite)) | MIT | Rolldown bundler, about 7 months stable; needs Node 20.19+/22.12+ ([Vite 8](https://vite.dev/blog/announcing-vite8)) |
| Language | **TypeScript 6.x pinned** (or TS 7 + Biome) | 7.0.2 is latest ([npm](https://www.npmjs.com/package/typescript)) | Apache-2.0 | TS 7 has **no programmatic API until 7.1**, so typescript-eslint breaks ([InfoQ](https://infoq.com/news/2026/08/typescript-7-released/)) |
| Server state | **TanStack Query** | 5.104.4 ([npm](https://www.npmjs.com/package/@tanstack/react-query)) | MIT | Projects, runs, tasks |
| Client/UI state | **Zustand** | 5.0.15 ([npm](https://www.npmjs.com/package/zustand)) | MIT | Panel/tab/selection state; low boilerplate |
| Routing | **TanStack Router** (or React Router 8) | 1.170.45 ([npm](https://www.npmjs.com/package/@tanstack/react-router)) | MIT | Type-safe deep links to project/run |
| UI kit | **shadcn/ui + Radix or Base UI + Tailwind** | shadcn 4.22.0, radix-ui 1.8.1, Tailwind 4.3.3 ([npm](https://www.npmjs.com/package/tailwindcss)) | MIT | Accessible primitives |
| Outer frame | **react-resizable-panels** (or `allotment`) | 4.14.5 ([npm](https://www.npmjs.com/package/react-resizable-panels)) | MIT | Activity bar / sidebar / workbench / mentor / panel |
| Docking workbench | **dockview** | 8.6.0, released 2026-10-16 ([dockview](https://dockview.dev/)) | MIT | Zero-dependency; tabs, splits, floating, popout. **Verify keyboard/ARIA support.** |
| Kanban DnD | **pragmatic-drag-and-drop** | 4.0.0 ([npm](https://www.npmjs.com/package/@atlaskit/pragmatic-drag-and-drop)) | Apache-2.0 | Atlassian-maintained |
| Charts | **Plotly** (Python 7.1.0 → plotly.js 4.1.2) + **Matplotlib 3.11** for static reports | ([npm](https://www.npmjs.com/package/plotly.js), [PyPI](https://pypi.org/project/plotly/)) | MIT | Python emits a JSON spec the browser renders unchanged; store it in JSONB. Use the `-dist-min` bundle. |
| Data grid | **TanStack Table 9 + Virtual** (or AG Grid Community 36) | 9.3.1 / 36.2.0 ([npm](https://www.npmjs.com/package/@tanstack/react-table)) | MIT | AG Grid enterprise features are paid |
| Code view (optional) | **monaco-editor** directly | 0.57.0 ([npm](https://www.npmjs.com/package/monaco-editor)) | MIT | Skip `@monaco-editor/react` (no release since Feb 2025) |
| Validation (TS) | **zod** | 4.6.7 ([npm](https://www.npmjs.com/package/zod)) | MIT | |
| Python runtime | **Python 3.14** | bugfix to 2030-10 ([devguide](https://devguide.python.org/versions/)) | PSF | NumPy/SciPy need ≥3.12; **avoid 3.15** (LiteLLM caps <3.15) ([PyPI litellm](https://pypi.org/project/litellm/)) |
| API | **FastAPI + Pydantic 2** | 0.146.0 / 2.14.1 ([PyPI](https://pypi.org/project/fastapi/)) | MIT | Plugin schemas double as API schemas; OpenAPI gives a typed TS client |
| ORM / migrations | **SQLAlchemy 2.1 + Alembic** | 2.1.5 / 1.20.0 ([PyPI](https://pypi.org/project/sqlalchemy/)) | MIT | Skip SQLModel (still 0.0.48) |
| PG driver | asyncpg (or psycopg 3) | 0.32.0 / 3.3.6 ([PyPI](https://pypi.org/project/asyncpg/)) | Apache-2.0 / **LGPL-3.0** | psycopg is LGPL: fine in SaaS; log it in the licence register |
| Metadata DB | **PostgreSQL 18** | PG19 only RC1 on 2026-10-15 ([postgresql.org](https://www.postgresql.org/about/newsarchive/-/20260928/)) | PostgreSQL | JSONB + GIN, RLS for tenancy; upgrade to 19 in 2027 |
| Job queue | **Procrastinate** (Postgres-backed) | 3.10.0 ([PyPI](https://pypi.org/project/procrastinate/)) | MIT | Run row + job created atomically; no broker in the MVP. Alternative: Dramatiq 2.2.1 + Valkey |
| Cache/broker (later) | **Valkey** | 9.1 (May 2026) ([Prompt Shelf](https://thepromptshelf.dev/blog/redis-valkey-license-claude-code-claude-md-2026)) | BSD-3 | Avoids the Redis 8 tri-licence |
| Dataset engine | **DuckDB + Parquet (pyarrow)** | 1.5.6 / 26.0.0 ([PyPI](https://pypi.org/project/duckdb/)) | MIT / Apache-2.0 | Fast profiling; original bytes kept untouched |
| Dataframes | **pandas 3.0** (defer Polars 2.0) | 3.0.6 ([PyPI](https://pypi.org/project/pandas/)) | BSD-3 | Copy-on-Write only, new `str` dtype: **tell Claude Code to use pandas 3 idioms** ([pandas 3.0](https://pandas.pydata.org/community/blog/pandas-3.0.html)) |
| Statistics | **NumPy 2.5 · SciPy 1.18 · statsmodels 0.15 · scikit-learn 1.9** | ([PyPI](https://pypi.org/project/statsmodels/)) | BSD | Authoritative engine; confirm cp314 wheels for statsmodels |
| SPC | **Own plugin** (constants A2…d2/c4, Western Electric/Nelson rules, I-MR, X̄-R/S, p/np/c/u, Cp/Cpk/Pp/Ppk) | — | Yours | Use `shewhart` (0.1.1, alpha, MIT) / `statprocon` and R `qcc` only as **test oracles** |
| CSV ingest | **charset-normalizer + clevercsv + pandas `dtype=str`** | 3.5.2 / 0.8.5 ([PyPI](https://pypi.org/project/clevercsv/)) | MIT | Nothing coerced silently |
| PDF | **pypdf + pdfplumber** | 6.21.1 / 0.11.10 ([PyPI](https://pypi.org/project/pypdf/)) | BSD-3 / MIT | Not PyMuPDF (AGPL) |
| LLM layer | **Pydantic AI** (LiteLLM optional gateway) | 2.57.0 ([PyPI](https://pypi.org/project/pydantic-ai/)) | MIT | Typed tools match plugin schemas; multi-provider; approval gate enforced in your app layer |
| BYOK secrets | **cryptography** envelope encryption + KMS | 50.0.2 ([PyPI](https://pypi.org/project/cryptography/)) | Apache/BSD | Ciphertext + key-id only; decrypt in the worker |
| Auth | **Keycloak 26** (or Clerk managed) via OIDC + Authlib | 26.7.0 ([Skycloak](https://skycloak.io/?p=3288)) | Apache-2.0 | Organizations = tenants. Avoid fastapi-users (maintenance mode) ([PyPI](https://pypi.org/project/fastapi-users/)) |
| Object storage | **S3 / Cloudflare R2** in prod; **SeaweedFS** for dev/self-host | — | Apache-2.0 | MinIO CE archived ([glukhov.org](https://glukhov.org/data-infrastructure/object-storage/minio-dead/)) |
| Python tooling | **uv · ruff · pytest** | 0.13.1 / 0.17.1 / 9.1.1 ([PyPI](https://pypi.org/project/uv/)) | MIT/Apache | `uv sync --frozen` in Docker |
| JS tooling | **pnpm · Vitest · Playwright · Biome** | 12.14.0 / 5.0.5 / 1.64.1 / 2.5.15 ([npm](https://www.npmjs.com/package/pnpm)) | MIT/Apache | All recent majors: pin exact versions |
| Plugin discovery | **`importlib.metadata` entry points** (pluggy 1.7 only if hooks are needed) | stdlib | — | Trusted built-ins first; registry with checksum in Postgres |

**Docker Compose for the MVP:** `web` · `api` (FastAPI) · `worker` (Procrastinate; read-only rootfs, CPU/memory caps, **no egress**, per-job temp dir) · `db` (postgres:18) · `s3` (SeaweedFS) · `idp` (Keycloak 26). Valkey only when needed.

### Licence and maintenance risk register

| Item | Risk | Action |
|---|---|---|
| **Redis 8+** | RSALv2 / SSPLv1 / AGPLv3 tri-licence ([SD Times](https://sdtimes.com/os/open-source-wins-again-redis-adds-gnu-agpl-license-to-its-offering/)) | Use Valkey (BSD-3) |
| **MinIO CE** | Binaries stopped Oct 2025; repo archived Feb 2026 ([glukhov.org](https://glukhov.org/data-infrastructure/object-storage/minio-dead/)) | SeaweedFS / managed S3 / R2 |
| **Zitadel v3+** | AGPL-3.0 since Mar 2025 ([Skycloak](https://skycloak.io/?p=3288)) | Keycloak (Apache-2.0) |
| **PyMuPDF** | AGPL-3.0 or commercial ([PyPI](https://pypi.org/project/pymupdf/)) | pypdf + pdfplumber |
| **pingouin** | GPL-3.0 ([PyPI](https://pypi.org/project/pingouin/)) | Re-implement with SciPy/statsmodels; keep out of core |
| **Theia** | EPL-2.0 / GPL-2.0 + Classpath | Not needed; custom shell |
| **Garage** (S3) | Believed AGPL; **unverified** | Check before choosing |
| **psycopg 3** | LGPL-3.0 | Acceptable; record it |
| **Stale packages** | golden-layout (last release 2022), `@dnd-kit/core` (Dec 2024), Glide Data Grid (Feb 2024), Observable Plot (Feb 2025), `@monaco-editor/react` (Feb 2025) | Do not adopt |
| **Too new** | TS 7.0, Python 3.15, Polars 2.0, PG 19, Jotai 3, React Router 8 | Pin the previous major; revisit in 2027 |

---

## 6. A USD 4.2B training market says sell through providers, not to individuals

**Key takeaways**
- No credible *software* market size exists in the research. The only proxy is **Six Sigma training at about USD 4.2B (2025) → USD 8.1B (2034), 7.8% CAGR**, from a single, low-tier publisher ([Market Intelo](https://marketintelo.com/report/six-sigma-training-market)). **Treat it as indicative only.**
- **Corporates fund 62.8%, individuals 22.5%, academia 10.1%. Online delivery is 52.3%** (same source). Go-to-market should therefore be **B2B2C**.
- **Green Belts (28.7%) plus Black Belts (35.2%) are about 64% of spend.** Those are exactly the belts who need statistics and a real project.

### Sizing proxies (derived from the cited shares; no software figure exists)
- **Individual-funded spend:** about 22.5% × USD 4.2B ≈ **USD 0.95B**, the pool a direct-to-learner tier competes in.
- **Asia-Pacific:** 18.3% ≈ **USD 0.77B**. India is named as a growth market (TCS, Infosys, Wipro), but **no India figure exists** ([Market Intelo](https://marketintelo.com/report/six-sigma-training-market)).
- **North America:** 50% ≈ USD 2.1B (same source).
- **Sector mix:** manufacturing 28.5%, healthcare 22.3%, IT & telecom 18.7%, BFSI 16.4%. Telecom ops is a credible first vertical given your domain.
- **What is missing:** the number of belts certified per year, the Minitab/JMP installed base and software market share. **Validate with interviews or a landing-page test** before quoting any TAM to investors.

### Price anchors

| Anchor | Price | Source |
|---|---|---|
| Minitab Solution Center | **~$200–233/month** ($2,394–2,793/year) | [Minitab](https://www.minitab.com/try-buy/) |
| JMP | ~$116/month ($1,390/year) | [JMP Store](https://store.jmp.com/) |
| EngineRoom | ~$41/month ($495/year) | [MoreSteam](https://www.moresteam.com/engineroom/) |
| DataCamp Premium | $28/month (annual) | [DataCamp](https://www.datacamp.com/blog/is-datacamp-worth-it) |
| Julius Plus / MLJAR Pro / Posit AI | ~$20/month | [Julius](https://julius.ai/pricing), [MLJAR](https://mljar.com/pricing/), [Posit](https://posit.co/blog/posit-ai-now-available-all) |
| OKR tools (median) | **$8/user/month**; free for 3–5 users | [Tability](https://www.tability.io/compare/pricing/perdoo) |
| GoLeanSixSigma courses | Yellow $99 · Green $599 · Black $899 | [GLSS](https://goleansixsigma.com/best-lean-six-sigma-certification-training/) |
| ASQ exam only (member/non-member) | CSSGB $338/438 · CSSBB $438/538 | [TrainingCost](https://trainingcost.com/certifications/six-sigma-certification-cost) |
| Khanmigo | ~$4/month (aggregator, inconsistent) | [DevToolLab](https://devtoollab.com/ai-tools/khanmigo) |

- **The wedge in one number:** a cheap online Green Belt costs about **$600**, while one Minitab seat costs about **$2,400/year, roughly 4x the training itself**.

### Recommended tiers (inference, not sourced; validate with willingness-to-pay tests)

| Tier | Global | India | Contents | Purpose |
|---|---|---|---|---|
| **Free / Learner** | $0 | ₹0 | Sample datasets, 1 project, EDA + basic tests, small AI quota | Funnel from exam-only candidates |
| **Belt Project Pass** (4–6 months) | ~$49–79 one-time | **₹1,999–3,999 one-time** | Full DMAIC/8D template, storyboard export, higher AI quota | Matches the GB project cycle; **avoids mandate friction** |
| **Pro** | **~$10–15/month** | **₹499–799/month** or ₹2,499–5,999/year | Unlimited projects, full stats library, KPI-linked OKRs, exports | "Under 1/10th of Minitab" |
| **Team** | ~$12–20/user/month, 3–5 seat minimum | Local pricing | Shared Kanban, project-KPI OKRs, MBB review workflow | Compare OKR $7–11 and DataCamp Teams $28 |
| **Academy / Partner** | Cohort licence | Cohort licence | Bulk seats, white-label "practice lab" | **Primary revenue engine** (the 63% corporate spend) |
| **AI** | Credits on top, or BYOK | Same | Metered mentor only | **Never meter deterministic computation** |

### India specifics
- **Price reality:** Green Belt programmes range from **INR 3,499 (Udemy)** to **INR 11,800–23,500** (Simplilearn, ISI, Henry Harvin, KPMG). ASQ CSSGB is about **INR 32–34K** ([Collegedunia](https://collegedunia.com/courses/six-sigma)).
- **Salary context:** Green Belt roles pay about **INR 5–8.5 lakh/year**, Black Belt about **INR 7–10 lakh/year** (same source). ₹499–799/month is about 1–2% of monthly GB pay.
- **Payments:** UPI AutoPay / RBI e-mandate allows **recurring debits up to INR 15,000 per transaction without extra authentication** after the first PIN/OTP approval ([EximPe](https://eximpe.com/blog/saas/upi-autopay-for-saas-setup-limits-and-what-global-founders-need-to-know)). UPI AutoPay has lower approval ratios than cards, which run around 70%+ (same source).
  - **Action:** offer **annual prepaid UPI or one-time passes** alongside AutoPay. Use **Razorpay Subscriptions or Chargebee** for dunning ([Razorpay](https://razorpay.com/blog/upi-autopay-vs-card-e-mandates/), [Chargebee](https://support.chargebee.com/support/solutions/articles/260014-razorpay-upi-autopay-supported-applications-and-their-handles)).
- **Channel:** bundle seats into cohorts with providers such as Benchmark Six Sigma, Henry Harvin, KPMG and ISI. This is likely the fastest route to volume (inference).

### Learning-design patterns to monetise
- **Socratic first, answer on request.** Khanmigo "guides with hints and questions rather than giving direct answers" ([DevToolLab](https://devtoollab.com/ai-tools/khanmigo)). Example: "What is your Y? Continuous or attribute?"
- **Role/goal intake** before lessons, as DataCamp's AI tutor does ([DataCamp](https://www.datacamp.com/blog/is-datacamp-worth-it)). Ask belt level, industry and goal at onboarding.
- **Free first chapter → free first DMAIC phase.**
- **Skills credited only after correct use on data** (for example, "2-sample t: assumptions checked, interpreted"). These feed personal learning OKRs.
- **Do not become a certifying body.** That space is crowded. Issue verifiable **project-evidence artefacts** instead.
- **Gamification is contested in CI.** Rever uses points and badges; KaiNexus deliberately avoids leaderboards ([KaiNexus](https://blog.kainexus.com/kainexus-vs-rever)). Keep it to private skill progress.

---

## What is still unverified (check before you commit)
- **EngineRoom:** MSA/Gage R&R coverage, and how Hexie actually behaves.
- **Minitab:** academic pricing, whether standalone Statistical Software is still sold, and which LLM and data governance sit behind its AI.
- **Software market:** no market size, no belt-certification volumes, no Indian willingness-to-pay data.
- **Tech:** dockview's accessibility and serialization APIs, statsmodels/pingouin cp314 wheels, the current Node LTS, Pydantic AI's native human-in-the-loop support, the latest Keycloak minor, and Garage's licence.
- **Learners:** no Reddit/community learner sentiment was retrievable, and no data exists on certification-project completion rates.

## Conclusion
- **Your moat is the architecture, not the feature list.** Competitors can copy the features in a quarter. They cannot easily retrofit "the AI only proposes validated plugin calls" onto products built around LLM-generated code (the AI notebooks) or bolt-on summaries (Minitab). Put that principle in the product, the marketing and the governance page, and prove it with public reference cases.
- **Scope ruthlessly.** The winning MVP is the *Green Belt project loop*, not the full IDE: messy CSV → data-quality confirmation → SPC/capability/tests → tollgate storyboard. OKRs, Kanban depth and the agent "Execute" mode come after a training-provider cohort has used that loop on real projects.
- **Monetisation follows the money.** Corporates and training providers fund about two-thirds of the market, so the individual tier is a funnel and cohort licences are the business. In India, one-time project passes beat subscriptions.
- **Pick the stack for stability, not novelty.** Every "latest" major in October 2026 (TS 7, Python 3.15, Polars 2, PG 19) is a trap for an AI-assisted solo build. Pin the previous major and let Claude Code work against well-documented APIs.
