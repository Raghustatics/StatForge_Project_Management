---
name: stats-validate
description: Validate a StatForge statistical or calculator function against independent reference values (NIST StRD, R oracles, textbook or workbook examples) and produce a validation table. Use for every new or changed statistical plugin, SPC/capability function, or template calculator.
---

# Statistical validation

## Reference hierarchy

1. **NIST StRD** certified values (univariate, linear regression, ANOVA) in `reference_data/nist/`.
2. **R oracle** scripts in `reference_data/oracles/` (base `stats`, `qcc`, `irr`, `nortest`, `car`). Store the expected values as JSON together with the R version used.
3. **Textbook / NIST-SEMATECH examples** in `reference_data/textbook/`, each cited with its source and page.
4. **Workbook formulas** (template calculators) from `sources/88_Templates`. Re-enter the numbers; never link to the file at runtime.
5. **Minitab example datasets** (`sources/Business_Cases_Examples`): internal **inputs** only. They carry no Minitab outputs, so pair them with reference values from 1–3.

## Tolerances

- NIST: ≥ 9 significant digits (lower difficulty), ≥ 6 (higher difficulty)
- Control limits and centre lines: absolute ≤ 1e-6 × scale
- Cp, Cpk, Pp, Ppk: exact vs R; ≤ 0.005 vs any Minitab display
- p-values: relative ≤ 1e-4, or both < 1e-10
- Confidence intervals: relative ≤ 1e-6

## Steps

1. List the function's cases: the normal case, edge cases (n = 1, n = 2, constant data, missing values, ties, one-sided specs, zero counts) and invalid inputs.
2. Get at least one **external certified case**. If none exists, stop and tell the owner.
3. Write pytest parametrised tests that load the expected values from `reference_data/` and assert within tolerance.
4. Add property tests (hypothesis, ≥ 200 examples) for invariants. Examples: Cpk ≤ Cp; limits symmetric for an I chart; p in [0, 1].
5. Ask the `statistician` agent to review the method, assumptions and output wording.
6. Produce the validation table: case · source · expected · actual · difference · tolerance · PASS/FAIL. Save it to `docs/evidence/Gxx/validation_<function>.md`.

## Rules

- Never adjust expected values to make a test pass.
- If two references disagree, document both and ask the owner.
- Document conventions explicitly: n−1 vs n, d2 constants, run-rule thresholds, the 1.5σ shift.
