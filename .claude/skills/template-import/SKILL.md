---
name: template-import
description: Import or refresh StatForge methodology templates from the owner's workbook (sources/88_Templates/Project Phase Template v0.1.xlsx) into versioned template definitions, classify each template, and report differences. Use in G18 and whenever the source workbook changes.
---

# Template import

## Source facts (verified 19 Oct 2026)

- 89 sheets: the "Worksheet Lists" index plus 88 templates.
- Groups:
  - Lean L01–L08 (13)
  - Discovery 01–11 (11)
  - Define D01–D11 (11)
  - Measure M01–M10 (11)
  - Analyze A01–A10 (13)
  - Improve I01–I14 (15)
  - Control C01–C14 (14)
- Index columns: #, Project Phase, Worksheet Name, Remarks, Lean Project, LSSGB, LSSBB, Comments.
- **Known cleanup:**
  - the index lists "A02.A" twice (the sheets are A02.A Service and A02.B Manufacturing)
  - typos: Allignment, Kanaban, Continouos, Effor-Impact
  - empty sheets: D09, I12, A07, 10 Balance Score Card, C10
  - A02.C has formatting bloat (1,048,576 rows)

## Steps

1. Open the workbook **read-only** (`anthropic-skills:xlsx` or openpyxl with `read_only=True, data_only=True`). Never modify `sources/`.
2. Parse the index. Map applicability:
   - ✓ → **required** for that track
   - "If applicable" → **conditional**
   - "Either of them…" → **choose-one** group
   - "Optional for …" → **optional**
3. For each sheet, extract the title, fields, tables, checklists, instructions and formulas. Then classify it as one of: form, table/register, checklist/tollgate, calculator, analysis-linked, diagram or narrative.
4. Formulas: record them as reference cases for `/stats-validate`. Never execute Excel formulas at runtime.
5. Apply the cleanup list. Keep the original names in `source_name` and the corrected ones in `display_name`.
6. Write the definitions as versioned data (JSON/YAML) under `content/templates/`, with a source checksum.
7. Mark the empty sheets **content pending**.
8. Diff report (`docs/evidence/Gxx/template_import_diff.md`): added, changed, unchanged, unclassified (must be 0) and pending.

## Rules

- A re-import with an unchanged checksum creates nothing new.
- Never invent template content. Missing content is marked pending, and the owner decides.
