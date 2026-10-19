---
name: methodology-draft
description: Draft a StatForge methodology or standalone template that is NOT in the owner's source workbook (DMADV/DFSS, PDCA, 8D, A3, Kaizen, MoM, Action Plan, generic stage-gate, Yellow Belt subset) as a clearly marked Draft for owner approval. Use in G21 or when the owner requests new methodology content.
---

# Methodology draft

## Steps

1. Confirm the item isn't covered by `sources/88_Templates`. If it is, use `/template-import` instead.
2. Delegate drafting to the `methodology-author` agent with this brief:
   - Base it on standard, widely published practice. Name the sources it follows (e.g., the 8D discipline structure D0–D8; ASQ/AIAG conventions where relevant).
   - Use the same structure as the methodology engine: ordered steps, purpose, expected outputs, prerequisites, required/conditional/optional class, evidence needed, linked statistical methods, consequences of skipping.
   - Reuse existing source templates wherever they fit. For example, 8D D4 root cause → A01/A02/A04; PDCA Check → I10/I11.
   - Plain professional English; no copyrighted text copied from paid standards.
3. Save it under `content/methodologies/<id>/` with `status: draft`, version `0.x` and an author note.
4. Owner review packet (`docs/evidence/G21/<id>_review.md`):
   - a one-page summary
   - the step table
   - the reused templates
   - open questions for the owner
5. Only the owner sets `status: approved`. Record the approval in `docs/DECISIONS.md` with date and version.

## Rules

- A Draft must show a visible "Draft" badge in the product and can't be an organisation default.
- Never present drafted content as the owner's source material.
