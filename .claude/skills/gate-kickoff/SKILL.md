---
name: gate-kickoff
description: Start the next StatForge gate safely. Use at the beginning of any gate (G01–G30) or when the owner says "start gate", "next gate" or "kick off". Verifies the previous gate passed, restates scope and test cases, lists files and risks, and waits for the owner's go.
---

# Gate kick-off

## Steps

1. Read `docs/GATE_LOG.md`.
   - Identify the next gate.
   - Confirm the previous gate's Result is **PASS** or **PASS WITH CONDITIONS**.
   - If not, **stop** and tell the owner what is outstanding.
2. Read the gate's section in `docs/StatForge_Gate_Map_v1.0.md`, plus the relevant guideline sections and `docs/reference/*` specs.
3. Read open items in `docs/DECISIONS.md` and `docs/RISKS.md`. List any conditions carried from earlier gates.
4. Inspect the current code and tests that the gate touches. Summarise what exists in 3–6 bullets.
5. **Skill check** (AGENTS.md §6.3): read `docs/SKILLS_MAP.md`. If this gate's skill is "Planned" and missing, put "Create `/<skill>` with skill-creator" as the first task in the brief.
6. **Owner questionnaire** (AGENTS.md §6.4): ask the owner the standard questions for this gate type with the ask-user tool (multiple choice, max 4 per round, recommended option first). Record the answers in the brief.
   - **All gates:**
     - anything to change in scope or test cases?
     - the time available for validation
   - **UI gates (G04–G06, G18–G20, G22–G26):**
     - density (compact/comfortable)
     - keyboard vs mouse priority
     - which screens matter most
     - copy tone (formal/plain)
   - **Data and statistics gates (G07–G17):**
     - conventions (run rule 8 vs 9; n−1; default α; 1.5σ shift labelled)
     - which reference datasets to show you
     - tolerance for warnings vs blocks
   - **Methodology and content gates (G18–G21, G25):**
     - which templates or methods to review first
     - who besides you may review content
     - the depth of help text
   - **AI and integration gates (G27–G29):**
     - which providers you'll test with
     - the default context policy
     - which prompts you'll approve first
     - your test mailbox or account
7. Produce the **kick-off brief** (bullets only):
   - Goal (one line)
   - In scope / Out of scope
   - Dependencies and preconditions
   - Test cases: copy TC-xx.y verbatim; add any extra edge cases you propose, marked "proposed"
   - Standard checks SC-1…SC-11 that need special attention
   - TDD plan: which TCs get RED tests first, test names and markers (`tc("TC-xx.y")`), expected RED evidence (AGENTS.md §4.1)
   - Owner validation scenarios S1–S6 for this gate: a one-line outline of each, or N/A with a reason (AGENTS.md §4.0)
   - Files and folders to create or change
   - New dependencies (with licence) or "none"
   - Risks and mitigations
   - Skills and agents you will use (AGENTS.md §4)
   - Size check: if the gate looks larger than one week of focused work, propose an a/b split
8. Create the branch `gate/Gxx-<short-name>` (do not commit yet).
9. Add a row to `docs/GATE_LOG.md` with Started = today; leave the other columns empty.
10. **Wait for the owner's explicit "go".** Do not write implementation code before it.

## Rules

- Never pull work from a later gate.
- If a test case is ambiguous, ask one focused question instead of guessing.
- Use `superpowers:brainstorming` only when the scope itself is unclear; use `superpowers:writing-plans` for the step plan after "go".
