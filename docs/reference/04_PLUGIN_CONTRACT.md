> **Reference spec (18 Oct 2026).** Subordinate to `docs/StatForge_Development_Guidelines_v1.1.md` and `docs/StatForge_Gate_Map_v1.0.md`. Where this file mentions pricing tiers, managed AI credits, a 13-phase roadmap or Keycloak-first auth, the guidelines v1.1 decisions win.

# 04 · Plugin Contract

Everything users can add, switch or extend is a plugin: statistical tools, readers, charts, calculators, themes, fonts, project templates, insight cards, AI providers and integrations.

## 1. Plugin kinds

| Kind | Example ids | Runs where |
|---|---|---|
| `analysis` | `stats.spc.imr`, `stats.ttest.paired`, `stats.regression.linear` | Worker (Python) |
| `reader` | `io.csv`, `io.xlsx`, `io.pdf` | Worker |
| `graph` | `graph.histogram`, `graph.pareto` | Worker builds spec; web renders |
| `calculator` | `calc.sample_size`, `calc.dpmo_sigma` | Worker (instant) |
| `template` | `template.dmaic`, `template.pdca`, `template.8d`, `template.a3` | Declarative (JSON) |
| `theme` | `theme.statforge-dark`, `theme.high-contrast` | Declarative (JSON tokens) |
| `font` | `font.inter`, `font.jetbrains-mono` | Declarative |
| `insightCard` | `card.kpi`, `card.phase-status` | Web (built-in components) |
| `aiProvider` | `ai.anthropic`, `ai.openai`, `ai.gemini`, `ai.ollama` | API agent gateway |
| `integration` | `integration.outlook-copilot` (Phase 11) | API (connector) |

MVP rule: **only trusted, built-in plugins**. Third-party plugins require sandboxing and review (Phase 12+).

## 2. Manifest — `statforge.plugin.json`

```json
{
  "id": "stats.spc.imr",
  "name": "I-MR Control Chart",
  "kind": "analysis",
  "version": "1.0.0",
  "engineCompat": ">=1.0 <2.0",
  "publisher": "statforge",
  "description": "Individuals and Moving Range chart with Nelson rules.",
  "category": ["Control Charts"],
  "dmaicPhases": ["Measure", "Control"],
  "skills": ["spc.individuals", "spc.rules"],
  "activationEvents": ["onCommand:stats.spc.imr.configure"],
  "contributes": {
    "commands": [
      {"id": "stats.spc.imr.configure", "title": "I-MR Chart…", "category": "Control Charts"}
    ],
    "menus": {
      "analyze/controlCharts": [{"command": "stats.spc.imr.configure", "when": "dataset.hasNumeric"}],
      "explorer/context": [{"command": "stats.spc.imr.configure", "when": "item.type == 'column' && column.type == 'numeric'"}]
    },
    "agentTools": [
      {"command": "stats.spc.imr.run", "riskClass": "runPlugin", "description": "Run I-MR chart on a numeric column."}
    ],
    "insightCards": [],
    "configuration": {"stats.spc.imr.defaultRules": {"type": "array", "default": [1, 2, 3, 4]}}
  },
  "inputs": {"$ref": "schemas/input.json"},
  "outputs": {"$ref": "schemas/output.json"},
  "preconditions": [
    {"id": "numeric_y", "level": "block", "message": "Y must be numeric."},
    {"id": "min_n", "level": "warn", "params": {"n": 20}, "message": "Fewer than 20 observations: limits are unreliable."},
    {"id": "time_order", "level": "warn", "message": "Confirm data are in time order."}
  ],
  "docs": "docs/README.md",
  "tests": "tests/"
}
```

- `when` clauses use context keys: `dataset.hasNumeric`, `dataset.hasDateColumn`, `project.phase`, `item.type`, `column.type`, `ai.enabled`, `workspace.plan`.
- `agentTools` declares which commands the AI may propose, and their risk class.
- Theme plugins contribute `themes` (token JSON); font plugins contribute `fonts`; templates contribute `projectTemplates`.

## 3. Python interface (analysis / reader / graph / calculator)

```python
from statforge_sdk import Plugin, RunContext, RunResult
from .schemas import IMRInput, IMROutput

class IMRChart(Plugin[IMRInput, IMROutput]):
    id = "stats.spc.imr"
    version = "1.0.0"

    def check_preconditions(self, ctx: RunContext, inp: IMRInput) -> list[Finding]: ...
    def run(self, ctx: RunContext, inp: IMRInput) -> RunResult[IMROutput]: ...
```

- `RunContext` gives: read-only dataset version (pandas/DuckDB), parameters, seed, logger, temp dir. **No network, no DB, no AI.**
- `RunResult` contains: `status`, `output` (typed), `tables`, `metrics` (named numbers usable as KPI sources), `assumptions` (check, result, evidence), `warnings`, `chart_specs` (Plotly JSON), `summary_facts` (structured facts for plain-language text), `provenance` (library versions, timings).
- Discovery: Python entry points group `statforge.plugins`; registry stores manifest + checksum in PostgreSQL.

## 4. Output conventions

- Every numeric output carries `name`, `value`, `unit`, `precision`, and optional `ci_low`/`ci_high`.
- `metrics` are the only values that can feed KPIs, OKRs and AI explanations (grounding source).
- Warnings use codes (`SPC_LT20`, `NORM_REJECT`) so the coach can explain them consistently.

## 5. Versioning and compatibility

- SemVer. Patch = bug fix with identical outputs on reference data; minor = new options; major = output/semantics change.
- Runs store `plugin_id@version`; re-runs default to the same version; "upgrade and compare" shows differences.
- Deprecation: a plugin version stays executable for 12 months after a major release.

## 6. Plugin definition of done

- Manifest valid against schema; commands appear in menus/palette with correct `when`.
- Input/output Pydantic schemas; preconditions implemented.
- Reference tests pass (see 07) — including at least one external certified case.
- Edge cases: empty, n=1, constant column, missing values, non-numeric, huge values.
- Docs: what it does, when to use, assumptions, interpretation, common mistakes (feeds the coach).
- Skill ids declared for the skill ledger.

## 7. Initial plugin catalogue

| Group | Plugins (phase) |
|---|---|
| Readers | CSV (3), Excel .xlsx (3), PDF reference + table extraction (9) |
| Data | Profile, Quality checks, Type confirm, Transform set (3) |
| EDA | Descriptive stats, Normality test, Correlation, Group summary (4) |
| Graphs | Histogram, Boxplot, Scatter, Pareto, Run chart, Dot plot, Probability plot, Time series (4) |
| SPC | I-MR, Xbar-R, Xbar-S, p, np, c, u, Nelson/WE rules (5) |
| Capability | Normal capability (Cp, Cpk, Pp, Ppk, PPM, sigma level), Attribute capability (DPMO) (5) |
| Tests | 1-sample t, 2-sample t (Welch), paired t, 1-/2-proportion, chi-square, equal variances, Mann-Whitney, Wilcoxon, Kruskal-Wallis (6) |
| Models | Simple + multiple linear regression (diagnostics), one-way ANOVA + Tukey (6) |
| Calculators | Sample size/power, DPMO↔sigma, COPQ, takt time, OEE (6) |
| Templates | DMAIC (3), PDCA, 8D, A3 (7) |
| Themes / fonts | Dark, Light, Dim, HC Dark, HC Light; Inter, JetBrains Mono, system (2) |
| Insight cards | Phase status, KPI, Control chart thumb, To-do, Next steps, OKR, Data health (2→7) |
| AI providers | Anthropic, OpenAI, Gemini, Ollama (8) |
| Integrations | Outlook / MS Copilot gateway (11) |
| Later | DOE, MSA/Gage R&R, multi-vari, logistic regression, nonnormal capability (11) |
