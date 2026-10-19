# TC-01.8 commit guard demonstration

- Date (UTC): 2026-10-19T19:41:25Z
- Branch: `scratch/G01-commit-guard-demo` (local only, never pushed, deleted after this run)
- Hook command (as configured in `.claude/settings.json`): `uv run --frozen --project "$CLAUDE_PROJECT_DIR" python "$CLAUDE_PROJECT_DIR/scripts/commit_guard.py" --hook`
- Exit codes are from the real run, whose shell printed `H1=2 G1=1 H3=0 G3=0 H4=0 G4=0` (session log 2026-10-20).

| Step | Staged | PreToolUse hook exit | `git commit` (pre-commit) exit |
|---|---|---|---|
| 1. Product code, no tests | `plugins/demo/demo.py` | 2 (blocked) | 1 (blocked) |
| 2. Tests first | `plugins/demo/tests/test_demo_plugin.py` (TC-01.8 marker) | 0 | 0 |
| 3. Code after its tests | `plugins/demo/demo.py` | 0 | 0 |

Hook message (step 1):
```
Blocked by test-first guard: plugins/demo has no tests for G01. Commit the RED tests first (AGENTS.md §4.1).
```

pre-commit output (step 1):
```
test-first commit guard..................................................Failed
- hook id: commit-guard
- exit code: 1

```

Note: the first run of this demonstration (before `8175f2e`) showed the guard wrongly *allowing* step 1, because repo-level `tests/` counted for every unit. Fixed in `8175f2e`, with regression test `test_root_tests_do_not_vouch_for_a_unit`.
