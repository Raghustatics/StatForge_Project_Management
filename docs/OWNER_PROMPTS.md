# Owner Prompt Pack — ready-to-paste prompts for Claude Code

Replace `[...]` and paste. Each prompt already follows AGENTS.md, so you don't need to restate the rules.

## 1. Start the next gate
```
/gate-kickoff
```
If Claude doesn't ask the standard questionnaire for this gate type, say: "Run the owner questionnaire for this gate type."

## 2. I don't understand the brief: explain it in business terms
```
Explain the current gate brief in plain business English for a product owner. Bullets only:
what users will be able to do after this gate, what could go wrong, what you need from me, and which
decisions are mine. No code, no jargon. Then list 3 questions I should ask you before saying "go".
```

## 3. Go / no-go on a kick-off
```
Go for [Gxx] with these changes: [none | list]. Follow the TDD sequence in AGENTS.md §4.1: RED first.
```

## 4. Change request (scope, design or rule)
```
Change request for [Gxx]: [what I want changed and why].
Assess the impact on scope, gates, tests, risks and effort (operations:change-request). Propose the
DECISIONS.md entry and the gate-map edits. Do not implement until I approve.
```

## 5. Bug report
```
Bug in [Gxx / screen / feature]. Steps: [1, 2, 3]. Expected: [...]. Actual: [...]. Data used: [...].
Use superpowers:systematic-debugging: reproduce, find the root cause, add a failing test (RED) that
reproduces it, then fix. Report root cause, fix, and the new test id.
```

## 6. Second opinion before I approve a gate
```
Run the gate-reviewer, security-reviewer, statistician and ux-a11y-reviewer agents (whichever apply)
on [Gxx]. Give me only the Blocker and Major findings, and tell me whether you would sign off. Be direct.
```

## 7. Prepare my validation session
```
Prepare my owner validation script for [Gxx] with scenarios S1–S6 (AGENTS.md §4.0), ≤ 45 minutes.
For each step: what to click, what I should see, and a ✓/✗ box. Seed any test data I need.
```

## 8. Record my decision
```
Record my gate decision for [Gxx]: [PASS | PASS WITH CONDITIONS: list + due gate | FAIL: rework list].
Update docs/GATE_LOG.md exactly as I wrote it and nothing else.
```

## 9. Explain a statistical result as the users will see it
```
Show me how StatForge explains [run / plugin] to a guided user and to an expert. Confirm every
number traces to the run output. Flag any wording that implies business significance.
```

## 10. Weekly status
```
Give me a weekly status (operations:status-report): gates done, gate in progress, test health,
risks (docs/RISKS.md), decisions needed from me. One screen, bullets.
```
