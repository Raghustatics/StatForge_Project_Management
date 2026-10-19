> **Reference spec (18 Oct 2026).** Subordinate to `docs/StatForge_Development_Guidelines_v1.1.md` and `docs/StatForge_Gate_Map_v1.0.md`. Where this file mentions pricing tiers, managed AI credits, a 13-phase roadmap or Keycloak-first auth, the guidelines v1.1 decisions win.

# 02 · UX and IDE Specification

Visual direction: **modern minimal (Cursor / Antigravity)** — dark-first, calm surfaces, 1px hairlines, one accent colour, generous but dense-capable spacing, VS Code layout conventions and vocabulary.

## 1. Layout regions

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Title bar: ◈ StatForge │ File Edit View Project Data Analyze Graph Run Window Help │ ⌘K search │ AI ● │ 👤 │
├──┬───────────────┬──────────────────────────────────────┬──────────────┬─────────┤
│A │ PRIMARY       │ WORKBENCH (dockview editor groups)    │ INSIGHT PANE │ AGENT   │
│c │ SIDEBAR       │ ┌ Tabs: Charter · data.csv · I-MR ┐   │ KPIs         │ PANE    │
│t │ (Explorer /   │ │                                  │   │ Phase status │ Ask /   │
│i │  Plugins /    │ │  Custom editor for the open item │   │ Charts       │ Plan /  │
│v │  Projects /   │ │                                  │   │ To-do        │ Agent   │
│i │  Search ...)  │ └──────────────────────────────────┘   │ Next steps   │ Approvals│
│t │               ├──────────────────────────────────────┤              │         │
│y │               │ PANEL: Output · Problems · Runs · Log │              │         │
├──┴───────────────┴──────────────────────────────────────┴──────────────┴─────────┤
│ Status bar: workspace · project phase · worker ● · AI provider │ rows×cols · assumptions ✓ · UTF-8 │
└──────────────────────────────────────────────────────────────────────────────────┘
```

| Region | VS Code name | Purpose | Resizable / collapsible | Shortcut |
|---|---|---|---|---|
| Title bar + top menu | Title Bar / Menu Bar | Global commands, search, AI status, account | — | Alt (focus menu) |
| Activity rail | Activity Bar | Switch sidebar views | Fixed 48 px | Ctrl+Shift+E/P/K… |
| Primary sidebar | Primary Side Bar | Explorer, Plugins, Projects, Search, Learning | Yes | Ctrl+B |
| Workbench | Editor Groups | Tabs of custom editors; split, float, pop-out | Yes | Ctrl+\ (split) |
| Panel | Panel | Output, Problems, Runs, Execution log, Audit | Yes | Ctrl+J |
| Insight pane | Secondary Side Bar (view container 1) | KPIs, phase status, charts, to-do, next steps | Yes | Ctrl+Alt+I |
| Agent pane | Secondary Side Bar (view container 2) | AI agent / coach with approvals | Yes | Ctrl+L |
| Status bar | Status Bar | Left = workspace scope; right = active item scope | Fixed 24 px | — |

- Insight pane and Agent pane can **stack, tab or sit side by side** (user preference; default: side by side ≥1600 px, tabbed below).
- Layout state (sizes, open tabs, collapsed views) persists per workspace.
- Zen mode (Ctrl+K Z) hides everything except the workbench.

## 2. Top menu (full tree)

| Menu | Items |
|---|---|
| **File** | New Project… (template picker) · New Folder · New Note · Open Project · Open Recent ▸ · Import Data ▸ (CSV, Excel, PDF) · Save Run · Save All · Export ▸ (Report PDF/HTML, Chart PNG/SVG, Results CSV, Project Archive) · Close Tab · Close Project · Settings (Ctrl+,) |
| **Edit** | Undo · Redo · Cut · Copy · Paste · Find (Ctrl+F) · Find in Project (Ctrl+Shift+F) · Rename · Duplicate · Delete (to Trash) |
| **View** | Command Palette (Ctrl+Shift+P) · Explorer · Plugins · Projects · Search · Learning · Insight Pane · Agent Pane · Panel ▸ (Output, Problems, Runs, Log, Audit) · Appearance ▸ (Theme, Font, Density, Zoom, Zen Mode, Full Screen) · Layout ▸ (Reset, Save as preset) |
| **Project** | Charter · Phase ▸ (Define, Measure, Analyze, Improve, Control) · Tollgate Review… · Kanban Board · To-do · KPIs · OKRs · Team (Phase 12) · Project Settings |
| **Data** | Upload Dataset · Profile Data · Data Quality Review · Confirm Column Types · Transform ▸ (filter, recode, split, stack, compute column) · Dataset Versions · Compare Versions |
| **Analyze** | Assistant: Recommend a Method… · Basic Statistics ▸ · Hypothesis Tests ▸ · Regression ▸ · ANOVA ▸ · Control Charts ▸ · Capability ▸ · Calculators ▸ · (DOE ▸, MSA ▸ — later) |
| **Graph** | Graph Builder · Histogram · Boxplot · Scatter · Pareto · Run Chart · Dot Plot · Probability Plot · Time Series |
| **Run** | Run Analysis (Ctrl+Enter) · Re-run with New Data · Cancel Run · Run History · Validate Preconditions |
| **Window** | New Window · Split Editor · Move Tab to New Window · Toggle Panels · Workspaces ▸ |
| **Help** | Getting Started (walkthrough) · Learning Path · Method Guides · Keyboard Shortcuts · AI Governance · What's New · Report Issue · About |

All menu items are **commands**; every command is reachable from the Command Palette and can carry a shortcut.

## 3. Activity rail (top → bottom)

1. **Explorer** — workspace tree (files, folders, datasets, runs, reports).
2. **Search** — across projects, datasets, columns, runs, notes.
3. **Projects** — DMAIC / PDCA / 8D phase view, boards, OKRs.
4. **Analyze** — statistical tool catalogue (grouped like Minitab menus).
5. **Plugins** — installed / available / updates; enable/disable; settings.
6. **Learning** — skill ledger, learning path, method guides.
7. *(spacer)*
8. **Accounts** · **Settings** (gear).

Badges: Problems count on Explorer, updates on Plugins, pending approvals on the Agent toggle.

## 4. Explorer — drill-down with segments

```
WORKSPACE: Raghu's Workspace                     [+ ▾] [⟳] [⋯]
▾ PROJECTS
  ▾ ◆ Reduce Generator Downtime        DMAIC · Analyze
     ▾ Define        ✓ Tollgate passed
        📄 Charter
        📄 SIPOC
        🎯 Project OKR
     ▾ Measure       ✓
        ▤ downtime_jan_jun.csv        v3 · 1,248 rows
           ▸ Columns (5)
           ▸ Versions (3)
           ▸ Quality issues (2) ⚠
        📈 EDA · Run 004
        📈 Capability (baseline)  Cpk 0.71
     ▾ Analyze       ● In progress
        📈 2-sample t · Run 007
     ▸ Improve       ○
     ▸ Control       ○
     ▸ Board (Kanban)
     ▸ Reports
  ▸ ◆ Ops Pulse – Energy Meter Defects   8D · D4
▾ PERSONAL
  ▸ Learning OKRs
  ▸ Notes
▾ SAMPLE DATA
```

- **Segments** (toggle chips above the tree): `All · Data · Analyses · Reports · Tasks`. Filtering keeps the hierarchy.
- **Group by**: Phase (default) · Type · Date.
- Inline status: version, row count, tollgate state, key result value.
- Context menu per item: Open, Open to Side, Rename, Duplicate, Move to Phase, Show Versions, Reveal in Runs, Delete.
- Drag a dataset onto an Analyze tool to start configuration.
- Keyboard: arrows, Enter open, Space preview, F2 rename, Delete.

## 5. Workbench — custom editors

| Editor | Opens | Key features |
|---|---|---|
| **Charter** | Charter doc | Structured form: problem, goal (SMART), scope in/out, CTQs, team, timeline, financials; coach prompts |
| **Dataset** | CSV/XLSX | Virtualised grid; column header shows detected type + quality badges; profile side sheet; type confirmation |
| **Data Quality Review** | Dataset issues | Issue list → evidence → proposed treatment → impact preview → Approve / Reject (transformation diff) |
| **Analysis Configurator** | Any plugin | Form generated from plugin input schema; role pickers (Y, X, subgroup); precondition checklist live |
| **Run Result** | A run | Result tables, Plotly charts, assumptions report card, warnings, plain-language summary (from computed values), provenance |
| **Graph Builder** | New graph | Drag columns to x / y / colour / facet; chart type gallery |
| **Kanban Board** | Project board | Columns per phase or custom; cards link to runs/datasets; WIP limits |
| **OKR** | Objective | KRs with baseline → target → current; source = KPI or run metric; confidence; check-ins |
| **Tollgate Review** | Phase gate | Checklist + evidence links + coach review + owner sign-off |
| **Report** | Report | Storyboard assembled from charter + runs; export |
| **Welcome / Walkthrough** | First run | Two entry paths: Start with data · Start with a business question |

Tabs: preview (italic) vs pinned, dirty indicator, split right/down, drag to float, pop-out window.

## 6. Insight pane

Context-aware: shows the **active project** (or the active run when one is focused).

| Card | Content |
|---|---|
| **Phase status** | D-M-A-I-C stepper; current phase; tollgate readiness % |
| **KPIs** | 2–4 KPI tiles (baseline, current, target, sparkline); source run linked |
| **Mini charts** | Latest control chart thumbnail; capability gauge |
| **To-do** | Open tasks for the current phase (from Kanban), checkbox to complete |
| **Next steps** | 3 suggested actions from the coach (each is a command; click → proposal) |
| **OKR progress** | Project OKR + personal learning OKR progress bars |
| **Data health** | Problems count by severity |

Cards are themselves plugin contributions (`insightCards`), so later plugins can add cards.

## 7. Agent pane

```
┌ AI Coach ───────────────── Claude ▾ · Coach ● ┐
│ Mode: [Ask] [Plan] [Agent]          ⋯  ⟲     │
│ Context: @Project @downtime.csv @Analyze      │
├───────────────────────────────────────────────┤
│ 🧑 Did the fix reduce downtime?               │
│ 🤖 Before I recommend a test I need two facts:│
│    1. Same sites before and after? [Yes][No]  │
│    2. Is downtime_min your Y? [Confirm]       │
│ ┌ PLAN ─────────────────────────────────────┐ │
│ │ 1 Check normality of differences  ✓ auto  │ │
│ │ 2 Paired t-test (α 0.05)        ⏸ approve │ │
│ │ 3 Add result to Analyze tollgate ⏸ approve│ │
│ └───────────────────────────── [Approve all]┘ │
│ ┌ PROPOSAL · Run plugin ─────────────────────┐│
│ │ stats.ttest.paired v1.0 on downtime.csv v3 ││
│ │ Y=downtime_min · pairs by site_id          ││
│ │ Why: same sites measured twice → paired    ││
│ │ [Approve] [Edit] [Reject]                  ││
│ └────────────────────────────────────────────┘│
│ Learning: "paired designs" · Explain more ▸   │
├───────────────────────────────────────────────┤
│ Ask or @mention…                    ⏎  🎙    │
└───────────────────────────────────────────────┘
```

- **Modes:** Ask (read-only explanations) · Plan (clarify + editable plan artefact) · Agent (executes approved steps). Shift+Tab cycles.
- **Coach toggle:** Socratic hints first; "Just tell me" reveals the answer.
- **Proposal card** shows: command, plugin + version, inputs, why, risk class, expected output. Buttons: Approve / Edit / Reject.
- **Risk classes:** read/profile → auto-allowed · run plugin → ask (default) · data transformation → always ask (cannot be auto-approved) · export/share/email → always ask.
- **@-mentions:** `@dataset`, `@column`, `@run`, `@chart`, `@phase`, `@okr`, `@task`, `@file`.
- **Checkpoints:** every approved step creates a restore point (dataset + run state).
- **Provider picker** (Claude / OpenAI / Gemini / Ollama) with key status; **"Local only"** badge when Ollama.
- **Numbers rule:** any number in agent text is rendered as a chip linked to its source run; numbers without a source are blocked by the grounding check (see 06).
- Plugin enablement inside the pane: a "Tools" popover lists which plugins the agent may call; users toggle per project.

## 8. Panel (bottom)

- **Output** — human-readable run log.
- **Problems** — data-quality issues and failed assumptions; click jumps to column/run; severity filter.
- **Runs** — queued / running / done / failed, duration, plugin version, re-run.
- **Audit** — approvals, transformations, exports (who, what, when).
- **Log** — technical log (developer mode only).

## 9. Command palette

- Ctrl+Shift+P (commands), Ctrl+P (go to item), `>` `@` `#` `?` prefixes like VS Code.
- Fuzzy search, recent first, shows shortcut and plugin source.
- Commands respect `when` context (e.g., `Capability Analysis` only when a numeric column exists).

## 10. Keyboard map (defaults)

| Action | Shortcut |
|---|---|
| Command palette | Ctrl+Shift+P |
| Quick open | Ctrl+P |
| Toggle sidebar / panel | Ctrl+B / Ctrl+J |
| Toggle agent / insight | Ctrl+L / Ctrl+Alt+I |
| Run analysis | Ctrl+Enter |
| Cycle regions | F6 / Shift+F6 |
| Agent mode cycle | Shift+Tab (in agent input) |
| Approve focused proposal | Ctrl+Shift+Enter |
| Accessibility help | Alt+F1 |

Mac uses ⌘ for Ctrl. All bindings remappable (Settings → Keyboard Shortcuts).

## 11. Themes, fonts and density (plugins)

- Themes are JSON token maps → CSS variables. Built-in: **StatForge Dark (default)**, **Light**, **Dim**, **High Contrast Dark**, **High Contrast Light**.
- Tokens include UI colours, semantic colours (success/warn/error/info), **chart palette** (8 categorical, colour-blind-safe), and **SPC colours** (centre line, limits, out-of-control point).
- Font plugins: UI font (Inter default), mono font (JetBrains Mono default), size (12–16), line height.
- Density: Compact · Comfortable (default) · Spacious.

## 12. States every view must handle

Empty (with a primary action) · Loading (skeleton) · Running (progress + cancel) · Success · Partial (warnings) · Error (plain message + fix + details) · Offline / AI unavailable (deterministic features still work) · No permission.

## 13. Accessibility (WCAG 2.2 AA)

- Full keyboard operation; visible focus ring; F6 region cycling; skip links.
- Contrast ≥ 4.5:1 text, ≥ 3:1 UI; high-contrast themes shipped day one.
- Charts: text summary generated **from computed statistics**, "View as table" toggle, colour + shape for series, never colour alone.
- Agent: `aria-live="polite"` for state changes only (e.g., "Approval required"), not for streamed tokens.
- Grids follow the ARIA grid pattern; reduced-motion setting respected.

## 14. Responsive behaviour

- ≥1600 px: all regions visible.
- 1280–1599 px: insight + agent tabbed in the secondary sidebar.
- 1024–1279 px: sidebar collapses to rail; secondary sidebar overlays.
- <1024 px: read-only "review mode" (view projects, KPIs, approve proposals); analysis authoring is desktop-browser only.
