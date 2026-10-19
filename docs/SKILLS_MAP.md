# Skills Map — gate-specific skills (created just in time)

**Rule (AGENTS.md §6.3):**
- At each gate kick-off, check this map.
- If the gate needs a skill that doesn't exist yet, creating it is the **first task of the gate**: write it with `anthropic-skills:skill-creator` / `superpowers:writing-skills`, the owner approves it with the kick-off brief, then work moves on to the RED tests.
- Skills encode patterns proven in this repo. Don't write speculative skills ahead of their gate.

| Gates | Skill | Status | Purpose | Builds on |
|---|---|---|---|---|
| All | `/gate-kickoff` | Built | Start a gate; skill check; owner questionnaire | — |
| All | `/gate-close` | Built | After owner PASS: commit, merge, tag, push to GitHub, verify CI, session log | — |
| All | `/gate-review` | Built | Checks SC-1…SC-11, TDD proof, reviews, evidence, S1–S6 script | — |
| G04–G06 | `/ide-component` | Planned (G04) | Add a pane, view, menu command, palette entry or theme token per `02_UX_IDE_SPEC.md` | `frontend-design`, `design:design-system`, `design:accessibility-review` |
| G07–G09 | `/data-quality-rule` | Planned (G08) | Add a reader or data-quality detector with a messy fixture and expected profile | `data:validate-data` |
| G10–G17 | `/new-plugin`, `/stats-validate` | Built | Statistical, SPC and calculator plugins with reference validation | `data:statistical-analysis` |
| G18 | `/template-import` | Built | Import the 88 templates from the workbook | `anthropic-skills:xlsx` |
| G18–G20 | `/template-type` | Planned (G18) | Add a renderer for a new template type (form, table, checklist, calculator, analysis-linked, diagram, narrative) | `frontend-design` |
| G21 | `/methodology-draft` | Built | Draft methodologies not in the source, owner-approved | agent `methodology-author` |
| G22–G24 | `/pm-feature` | Planned (G22) | Port a Kanban, register or OKR feature from the PMO app, with a PORTING entry | `engineering:code-review` |
| G25 | `/guidance-rule` | Planned (G25) | Add a recommendation rule or questionnaire item with scenario tests | `product-management:write-spec`, `design:ux-copy` |
| G26 | `/report-section` | Planned (G26) | Add a report or export section with a number-to-run trace test | `anthropic-skills:pdf`, `anthropic-skills:docx`, `anthropic-skills:xlsx` |
| G27–G28 | `/prompt-template` | Planned (G27) | Add or change an AI prompt: version, variables, evals, multi-provider and grounding tests | `anthropic-skills:skill-creator` |
| G29 | `/integration-plugin` | Planned (G29) | Opt-in integration with consent, review step, kill switch, security review | agent `security-reviewer` |
| G30 | `/release-check` | Planned (G30) | Hardening, performance, backup and restore, deployment checklist | `engineering:deploy-checklist`, `operations:runbook` |

**When a skill is created:** set its Status to "Built (Gxx)" and log it in `docs/DECISIONS.md`.
