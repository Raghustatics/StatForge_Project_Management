# StatForge

A guided problem-solving platform: Lean Six Sigma methodology, deterministic statistics, project management and optional AI in a browser-based IDE.

**Status:** pre-build. Governance files are in place; the next step is gate **G01** (see `docs/GATE_LOG.md`).

## Start here

- Rules for AI coding agents: `AGENTS.md` (Claude Code loads it through `CLAUDE.md`)
- Scope baseline: `docs/StatForge_Development_Guidelines_v1.1.md`
- Delivery plan: `docs/StatForge_Gate_Map_v1.0.md` (30 gates)
- Progress: `docs/GATE_LOG.md` · Decisions: `docs/DECISIONS.md` · Risks: `docs/RISKS.md`

## How to work with Claude Code

1. Open this folder in Claude Code.
2. Type `/gate-kickoff`. Claude reads the Gate Log, prepares the kick-off brief for the next gate, and waits for your "go".
3. When Claude finishes the gate, it runs `/gate-review` and hands you the evidence pack and a validation script.
4. Validate it yourself, then record PASS or FAIL in `docs/GATE_LOG.md`.

## Inputs

- `88_Templates/` and `Business_Cases_Examples/` move to `sources/` during G01.
- The Minitab example datasets are internal test fixtures only and are never committed to a public repository.
