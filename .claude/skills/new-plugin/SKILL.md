---
name: new-plugin
description: Scaffold a new built-in StatForge plugin (analysis, graph, calculator, reader, template, theme, font, AI provider or integration) that follows the plugin contract. Use whenever a gate adds a capability that should be a plugin.
---

# New plugin

## Steps

1. Confirm the plugin belongs to the **active gate**. If not, stop.
2. Read `docs/reference/04_PLUGIN_CONTRACT.md`.
3. Create `plugins/<id>/` with:
   - `statforge.plugin.json`: id, name, kind, version, engineCompat, description, category, dmaicPhases, skills, activationEvents, contributes (commands, menus, agentTools with riskClass, configuration), inputs, outputs, preconditions
   - `schemas/input.json` and `schemas/output.json` (generated from Pydantic models)
   - engine code in `packages/engine/...` (pure functions, no I/O)
   - a thin plugin adapter implementing `check_preconditions` and `run`
   - `tests/`: contract tests, edge cases, and reference tests via `/stats-validate`
   - `docs/README.md`: what it does, when to use it, assumptions, interpretation, common mistakes (this feeds the guidance layer)
4. Register commands with correct `when` clauses (e.g., `dataset.hasNumeric`, `project.phase == 'Measure'`).
5. Declare `agentTools` only if the AI may propose it. A data transformation always uses riskClass `transform`, which is never auto-approvable.
6. Outputs: every number has name, value, unit and precision. `metrics` are the only values that can feed KPIs, OKRs or AI text.
7. Run `/stats-validate` (analysis and calculator kinds), then `/gate-review` steps 2–4.

## Rules

- Plugins never import UI components, database code or AI SDKs.
- Third-party code execution is out of scope.
- A plugin isn't visible in the UI until its reference tests pass.
