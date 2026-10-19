> **Reference spec (18 Oct 2026).** Subordinate to `docs/StatForge_Development_Guidelines_v1.1.md` and `docs/StatForge_Gate_Map_v1.0.md`. Where this file mentions pricing tiers, managed AI credits, a 13-phase roadmap or Keycloak-first auth, the guidelines v1.1 decisions win.

# 07 · Statistical Validation and Test Strategy

Trust is the product. One wrong Cpk in a demo is fatal. Validation is a release gate, not a task.

## 1. Reference sources (independent of our code)

| Source | Covers | Status |
|---|---|---|
| **NIST StRD** (Statistical Reference Datasets) | Univariate summary (certified mean, SD, autocorrelation), linear regression, one-way ANOVA, nonlinear regression | Public, certified values to 15 digits — primary |
| **NIST/SEMATECH e-Handbook** examples | Control charts, capability, tests | Public |
| **Textbook worked examples** (Montgomery, *Introduction to Statistical Quality Control*) | SPC constants, Xbar-R, p/np/c/u, capability | Cite page; store only our re-entered numbers |
| **R** (`qcc`, base `stats`) | Independent cross-check of SPC, tests, ANOVA | Script in `reference_data/oracles/` |
| **Minitab demo / trial** | Belt-familiar outputs (I-MR, capability, t-tests) | Owner runs during validation window; outputs stored as expected values; **demo files never shipped** |
| **Existing build outputs** | Regression vs prior implementation | After ADR-001 audit |

## 2. Tolerances

| Quantity | Tolerance |
|---|---|
| NIST certified values (mean, SD, regression coefficients) | ≥ 9 significant digits (lower difficulty), ≥ 6 (higher difficulty) |
| Control limits, centre lines | Absolute ≤ 1e-6 × scale |
| Cp, Cpk, Pp, Ppk | ≤ 0.005 vs Minitab display; exact vs R |
| p-values | Relative ≤ 1e-4 (or both < 1e-10) |
| Confidence intervals | ≤ 1e-6 relative |

## 3. Test layers

| Layer | Tool | What |
|---|---|---|
| Unit (engine) | pytest + hypothesis (property tests) | Each function vs reference; invariants (e.g., Cpk ≤ Cp, limits symmetric for I chart) |
| Plugin contract | pytest | Manifest schema, input validation, preconditions, output schema |
| Data foundation fixtures | pytest | Messy CSVs: ambiguous dates, `1,200` strings, `-999`/`NA`/blank, duplicates, mixed types, BOM/UTF-16, semicolon delimiter, duplicate headers, empty file, 10 MB + 1 byte |
| API | pytest + httpx | Auth, authorisation per workspace, upload limits, error messages |
| Web unit | Vitest + Testing Library | Command registry, `when` evaluation, stores, components |
| E2E | Playwright | Flagship journey: create DMAIC project → upload → confirm → EDA → capability → t-test → control chart → tollgate |
| Accessibility | axe-core in Playwright | No serious/critical violations on key screens |
| AI evaluation | Scripted conversations + grading | Grounding violations = 0; correct method recommendation ≥ 95% on 50 scenario set; refusal to transform without approval = 100% |
| Performance | Locust/k6 (light) | Budgets in 03 §9 |

## 4. Reference data layout

```
reference_data/
  nist/            # downloaded StRD files + certified values (JSON)
  textbook/        # re-entered examples with citation
  messy_csv/       # data-quality fixtures with expected profile JSON
  minitab_checked/ # our datasets + expected outputs recorded from Minitab (no Minitab files)
  oracles/         # R scripts producing expected values
  scenarios/       # AI evaluation conversations
```

## 5. SPC implementation notes (in-house)

- Constants table (n = 2…25): A2, A3, B3, B4, D3, D4, d2, d3, c4 — unit-tested against published tables.
- I-MR: σ̂ = MR̄ / d2(2) = MR̄ / 1.128; never overall SD (common LLM error — use in marketing demos).
- Rules: Nelson 1–8 configurable; Western Electric preset.
- Capability: within (σ̂ from subgroups/MR) vs overall (sample SD); report both Cp/Cpk and Pp/Ppk; normality check precondition; one-sided specs supported.

## 6. Release gates (every phase that ships statistics)

- 100% of plugin reference tests pass in CI.
- No plugin without ≥ 1 external certified case.
- Property tests run ≥ 200 examples per function.
- Owner reviews a validation report (auto-generated table: case, expected, actual, diff, pass).
