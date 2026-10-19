# TC-01.7 Stop hook demonstration

- Date (UTC): 2026-10-19T19:37:15Z
- Branch: `scratch/G01-stop-hook-demo` (local only, never pushed, deleted after this run)
- Deliberate failing test: `tests/repo/test_zz_deliberate_failure.py` (`assert sum([1]) == 2`; type-clean, so only pytest fails)
- Command (exactly as configured in `.claude/settings.json`): `uv run --frozen --project "$CLAUDE_PROJECT_DIR" python "$CLAUDE_PROJECT_DIR/scripts/stop_hook.py"`

## Attempt 1: exit code 2

```
verify.ps1 is failing — the work is not done. Fix these before stopping:
[PASS] ruff-check
[PASS] ruff-format
[PASS] mypy
[FAIL] pytest: ================================== FAILURES ===================================
    >       assert sum([1]) == 2
    E       assert 1 == 2
[PASS] web-lint
[PASS] web-typecheck
[PASS] web-test
[PASS] tc-trace
verify: FAIL (pytest)
```

## Attempt 2: exit code 2

```
verify.ps1 is failing — the work is not done. Fix these before stopping:
[PASS] ruff-check
[PASS] ruff-format
[PASS] mypy
[FAIL] pytest: ================================== FAILURES ===================================
    >       assert sum([1]) == 2
    E       assert 1 == 2
[PASS] web-lint
[PASS] web-typecheck
[PASS] web-test
[PASS] tc-trace
verify: FAIL (pytest)
```

## Attempt 3: exit code 2

```
verify.ps1 is failing — the work is not done. Fix these before stopping:
[PASS] ruff-check
[PASS] ruff-format
[PASS] mypy
[FAIL] pytest: ================================== FAILURES ===================================
    >       assert sum([1]) == 2
    E       assert 1 == 2
[PASS] web-lint
[PASS] web-typecheck
[PASS] web-test
[PASS] tc-trace
verify: FAIL (pytest)
```

## Attempt 4: exit code 0

```
{"systemMessage": "verify.ps1 is FAILING after 3 attempts \u2014 the work is NOT done. Report the failures to the owner."}
```

## After removing the failing test: exit code 0 (stop allowed)

## Result

- Attempts 1-3: exit 2, so Claude Code refuses to stop and receives the failing summary (`[FAIL] pytest`).
- Attempt 4: exit 0 with a visible "NOT done" systemMessage (the 3-block release, which prevents an endless loop; /gate-close still re-verifies independently, D-032e).
- With the suite green again: exit 0.
