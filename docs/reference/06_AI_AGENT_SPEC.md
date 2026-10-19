> **Reference spec (18 Oct 2026).** Subordinate to `docs/StatForge_Development_Guidelines_v1.1.md` and `docs/StatForge_Gate_Map_v1.0.md`. Where this file mentions pricing tiers, managed AI credits, a 13-phase roadmap or Keycloak-first auth, the guidelines v1.1 decisions win.

# 06 · AI Agent and Coach Specification

## 1. Role

- **Coach** — teaches by asking, hinting and explaining *why*.
- **Orchestrator** — proposes commands (run plugin, create task, draft charter, update OKR) for the user to approve.
- **Never** — computes or edits numbers, transforms data without approval, decides the business objective, executes code.

## 2. Modes

| Mode | Can read | Can propose | Executes | Use |
|---|---|---|---|---|
| **Ask** | Project context, profiles, run outputs, docs | No | No | "What does Cpk mean here?" |
| **Plan** | Same | Plan artefact (editable checklist) | No | Clarify question → method plan |
| **Agent** | Same | Commands (proposal cards) | Only approved proposals, step by step | Carry out the plan |

Coach style setting: **Socratic** (default for Learner plan) · **Direct** · **Expert** (terse, for experienced belts).

## 3. Tools (= commands)

The agent sees only commands listed in plugin manifests' `agentTools` plus core commands:

| Command | Risk class | Approval |
|---|---|---|
| `context.read` (project, profile, run output) | read | Auto |
| `data.profile` | read | Auto |
| `analysis.recommend` (returns candidate methods with reasons, from deterministic rules + LLM explanation) | read | Auto |
| `analysis.run` (any analysis plugin) | runPlugin | Ask (user may auto-allow per project) |
| `data.transform` (impute, remove, recode, coerce, filter) | transform | **Always ask — cannot be auto-approved** |
| `project.task.create/update`, `project.charter.draft`, `okr.kr.update`, `kpi.link` | write | Ask |
| `report.export`, `integration.outlook.send` | external | **Always ask** |

## 4. Method recommendation (hybrid)

1. **Deterministic rules engine** (versioned decision tree like Minitab Assistant): inputs = Y type, X type, groups, pairing, sample size, normality result, independence → candidate methods with preconditions.
2. **LLM** explains the candidates in plain language, asks for missing facts, and relates them to the business question.
3. The user selects; preconditions are re-checked by the plugin before run.

The LLM cannot add a method that the rules engine did not return (it can say "I'd also consider X — not available yet").

## 5. Grounding (no invented numbers)

- Context passed to the model includes run `metrics` with ids.
- The model must cite numbers as `{{metric:run_007.p_value}}` placeholders; the UI renders real values from the run.
- Post-check: any free-typed number (regex for digits) in the reply is compared to referenced metrics at display precision; mismatches are replaced with a warning chip "Unverified number removed" and logged.
- Allowed literals: user-provided numbers, method constants (α = 0.05 if set), counts of items in context.
- Evaluation suite (see 07) measures grounding violations per 100 replies — release gate: **0**.

## 6. Provider abstraction

- Library: Pydantic AI (typed tools mirror plugin schemas). LiteLLM optional as gateway later.
- Providers: Anthropic (Claude), OpenAI, Google Gemini, **Ollama** (local; OpenAI-compatible endpoint).
- Modes of access: **BYOK** (user key, encrypted at rest) · **Managed** (platform key, metered credits) · **Local** (Ollama; "nothing leaves your server").
- Capability flags per model: tool-calling, context window, JSON reliability; models without reliable tool-calling are limited to Ask mode.
- Fallback: provider error → clear message; deterministic features unaffected.

## 7. Context and privacy

- Default context: project charter, phase, dataset **schema + profile**, run outputs, open tasks, OKRs. **No raw rows.**
- Per-project toggle "Allow sample rows to AI (max 50)" — off by default; disabled when workspace policy forbids.
- Steering files (user-owned, visible): `context/business.md`, `context/data-dictionary.md`, `context/standards.md` — always included when present.
- Prompt-injection defence: content from files/PDFs/datasets is wrapped as untrusted data; tool allow-list enforced server-side regardless of model output.

## 8. Coach behaviour

- Start with the question: "What decision will this analysis support?" then Y, X, unit, time window, design.
- Explain *why* a method fits and *what it cannot show*.
- After a run: plain-language interpretation from `summary_facts`, practical vs statistical significance, next step.
- Learning moments: a short "Concept" card linked to method docs; quiz-free (no gamification pressure).
- Skill evidence is recorded only when: preconditions checked, run succeeded, user confirmed interpretation.

## 9. Proposal card contract

```json
{
  "proposal_id": "prp_123",
  "command": "analysis.run",
  "args": {"plugin": "stats.ttest.paired@1.0.0", "dataset_version": "dsv_3", "y": "downtime_min", "pair_by": "site_id", "alpha": 0.05},
  "risk_class": "runPlugin",
  "rationale": "Same 24 sites measured before and after → paired design.",
  "expected_output": ["mean difference", "95% CI", "p-value", "normality of differences"],
  "reversible": true
}
```

## 10. Cost controls

- Token and cost tracked per message and workspace; monthly budgets per plan; warning at 80%.
- Explanations for identical run outputs are cached.
- Deterministic computation is **never** metered.

## 11. Integration: Outlook / MS Copilot gateway (Phase 11)

- Ported from the existing build as an `integration` plugin.
- Example commands: send tollgate summary email, create meeting for tollgate review, import action items.
- Always-ask risk class; OAuth via Microsoft identity; audit logged. Scope confirmed during ADR-001 audit.
