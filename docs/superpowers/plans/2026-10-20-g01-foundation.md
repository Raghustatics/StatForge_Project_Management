# G01 Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A reproducible StatForge monorepo (web, api, db, s3 in Docker Compose) whose TDD rules are enforced by `tc_trace`, a commit guard, a Stop hook, pre-commit and CI.

**Architecture:** uv workspace (`apps/api`, `packages/engine`) plus pnpm workspace (`apps/web`) at the repo root. The api is FastAPI with injectable health checks; the web is a static Vite build served by nginx, which proxies `/api/` and `/health` to the api. The enforcement scripts are small, pure-Python modules in `scripts/` with thin CLIs, so they are unit-testable and shared by hooks, pre-commit and CI.

**Tech Stack:** Python 3.14 · uv · FastAPI · Pydantic 2 · pydantic-settings · psycopg 3 · boto3 · pytest · ruff · mypy · Node 24 · pnpm · React 19.3 · TypeScript 6 · Vite 8 · Vitest · Testing Library · Playwright · @axe-core/playwright · PostgreSQL 18 · SeaweedFS · nginx · gitleaks · pre-commit · GitHub Actions.

**Spec:** `docs/evidence/G01/kickoff_brief.md` (approved brief) and `docs/StatForge_Gate_Map_v1.0.md` §3 G01.

## Global Constraints

- Python `requires-python = ">=3.14"`; `mypy --strict` on `apps/api/src`, `packages/engine/src`, `scripts`, and all tests; ruff line length 100.
- Node 24 LTS; pnpm via corepack (user-scope shim, D-030); TypeScript 6.x (not 7); React 19.3; Vite 8; `strict: true`.
- PostgreSQL 18; SeaweedFS for S3. Forbidden: MinIO, Redis, SQLModel, AG Grid Enterprise, PyMuPDF, pingouin.
- Licences: no AGPL/SSPL/GPL runtime dependency. psycopg (LGPL-3.0) is approved (D-028).
- Coverage ≥ 85% lines on new Python and TS code; CI fails below it.
- TC traceability: pytest `@pytest.mark.tc("TC-01.x")`; Vitest/Playwright titles start `[TC-01.x]`.
- Commits: Conventional Commits. RED = `test(G01): RED for TC-01.x <what>`; GREEN = `feat(G01): GREEN TC-01.x <what>`; every message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- RED evidence: the failing run is saved to `docs/evidence/G01/red/<UTC yyyyMMddTHHmmssZ>_TC-01.x.txt` and committed in the RED commit.
- Never modify anything under `sources/`; never stage `sources/Business_Cases_Examples/`.
- Never push `main` or `gate/G01-foundation`; push only `ci-check/G01-*` (Task 10), then delete them.
- Every command must work in Windows PowerShell 5.1 (no `&&`, no `??`) and inside Linux containers.
- Error copy is plain English, action-first, with no stack traces, connection strings or secrets.

## Review Focus

1. **A database that accepts TCP but never answers** (paused container, firewall black-hole): `/health` must return 503 within about 5 s, not hang. Test in Task 3.
2. **Secrets leaking through errors:** a driver exception whose message contains the DSN or password must not appear in the `/health` body or in logs. Test in Task 3.
3. **Commit-guard bypass shapes:** `git commit -am`, `git -C <dir> commit`, `git -c user.name=x commit`, and PowerShell here-string messages must all be recognised; with `-a`/`--all`, unstaged tracked changes count as staged. Tests in Task 7.
4. **Hook environment without tools** (pnpm or docker not on the hook's PATH): `verify.ps1` must report `[FAIL] <step>: pnpm not found — see README "Setup"` rather than crash or pass. Test in Task 9.
5. **Stop-hook loop:** a failure that can't be fixed in-session must not trap the session forever. After 3 consecutive blocks, the hook lets the stop through with a visible "verify is FAILING — the work is NOT done" message. Test in Task 9.

---

### Task 1: Baseline commit, sources move, workspace config

**Files:**
- Move: `88_Templates/` → `sources/88_Templates/`; `Business_Cases_Examples/` → `sources/Business_Cases_Examples/` (with `Move-Item`; contents untouched)
- Create: `.gitignore`, `.gitattributes`, `.dockerignore`, `pyproject.toml` (uv workspace root + ruff/mypy/pytest/coverage config), `package.json`, `pnpm-workspace.yaml`, `.npmrc` (`engine-strict=true`)
- Test: `tests/repo/test_repo_hygiene.py`

**Interfaces:**
- Produces: pytest marker `tc(id: str)` registered in `[tool.pytest.ini_options] markers`; markers `integration` (needs the running compose stack) and `slow` (cold start). `addopts = "--strict-markers"`. `pythonpath = ["scripts"]`, so tests `import tc_trace`.
- Produces: the uv workspace `members = ["apps/api", "packages/engine"]`; a dev dependency group with pytest, pytest-cov, ruff, mypy, httpx, pyyaml, types-pyyaml, boto3-stubs[s3].

- [ ] **Step 1:** Move the two folders into `sources/`. Write `.gitignore` with: `sources/Business_Cases_Examples/`, `.env`, `.venv/`, `node_modules/`, `dist/`, `coverage/`, `.coverage*`, `htmlcov/`, `playwright-report/`, `test-results/`, `.claude/settings.local.json`, `.claude/.stop_hook_state.json`, `__pycache__/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`.
- [ ] **Step 2:** `.gitattributes`: `* text=auto eol=lf`; `*.ps1 text eol=crlf`; `*.xlsx binary`. `.dockerignore`: `sources/`, `docs/`, `.git/`, `**/node_modules`, `.venv`, `**/dist`, `.env`.
- [ ] **Step 3:** Write the root `pyproject.toml` and the pnpm root files as in Interfaces. The root `package.json` pins `"packageManager": "pnpm@12.14.0"` (D-032d) and `"engines": {"node": ">=24 <25"}`. Run `uv sync` and `pnpm install`. Expected: both succeed and produce `uv.lock` and `pnpm-lock.yaml`.
- [ ] **Step 4: Write the guard-rail tests** in `tests/repo/test_repo_hygiene.py`:
  - `test_tc01_5_minitab_fixtures_never_tracked`, marked `tc("TC-01.5")`: `git ls-files sources/Business_Cases_Examples` prints nothing, and `git check-ignore -q sources/Business_Cases_Examples/Minitab_Datasets_1.xlsx` exits 0.
  - `test_env_file_ignored`: `git check-ignore -q .env` exits 0.
  - `test_governance_docs_are_tracked` (D-032f): `git ls-files --error-unmatch` succeeds for `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/StatForge_Development_Guidelines_v1.1.md`, `docs/StatForge_Gate_Map_v1.0.md`, `docs/GATE_LOG.md`, `docs/DECISIONS.md`, `docs/RISKS.md`, `docs/PORTING.md`, `docs/TROUBLESHOOTING.md`, `docs/OWNER_PROMPTS.md`, `docs/SKILLS_MAP.md`, `docs/reference/`, `docs/sessions/`, `.claude/agents/`, `.claude/skills/`, `sources/88_Templates/Project Phase Template v0.1.xlsx`; and `git check-ignore` reports none of them as ignored.
  - `test_pnpm_version_pinned` (D-032d): the root `package.json` has `packageManager` matching `^pnpm@\d+\.\d+\.\d+`.
- [ ] **Step 5:** Run `git add -A`, then `git status --short`. Expected: no path under `sources/Business_Cases_Examples/` appears. Stop if one does.
- [ ] **Step 6:** Run `uv run pytest tests/repo -q`. Expected: 4 passed.
- [ ] **Step 7:** Commit with `chore(G01): baseline governance docs, sources/ move, workspace config`.
- [ ] **Step 8:** Run `git remote add origin https://github.com/Raghustatics/StatForge_Project_Management.git`. **Do not push.**

### Task 2: `tc_trace` (TC-01.6) and RED-capture helper

**Files:**
- Create: `scripts/tc_trace.py`, `scripts/capture_red.ps1`
- Test: `scripts/tests/test_tc_trace.py` (with tmp_path fake repos)

**Interfaces:**
- Produces (in `tc_trace`):
  - `TC_PATTERN = re.compile(r"TC-\d{2}\.\d+")`
  - `active_gate(gate_log: Path) -> str`: parses `**Active gate:** G01:` → `"G01"`.
  - `gate_test_cases(gate_map: Path, gate: str) -> list[str]`: the TC ids inside the `#### G01 ·` section, up to the next `####`, in order.
  - `is_test_file(path: str) -> bool`: true for `test_*.py` and `*_test.py` under any `tests/` dir, `*.test.ts(x)`, `*.spec.ts(x)`, and anything under `e2e/`.
  - `tc_ids_in(text: str) -> set[str]`
  - `@dataclass(frozen=True) TestRef(path: str, name: str, tc: str, disabled: bool)`
  - `scan_tests(root: Path) -> list[TestRef]`: static only. Python is parsed with `ast`: a test maps a TC through the `pytest.mark.tc("…")` decorator, a module-level `pytestmark`, or the name `test_tcXX_Y_…` (→ `TC-XX.Y`). It is `disabled` if decorated with `pytest.mark.skip`, `skipif` or `xfail`. TS is scanned by regex: `(test|it|describe)(\.(skip|fixme|todo))?\(\s*['"`]\[(TC-\d{2}\.\d+)\]`; `disabled` if `.skip`, `.fixme` or `.todo`. Skips `node_modules`, `.venv` and `dist`.
  - `@dataclass(frozen=True) TraceResult(mapped: dict[str, list[TestRef]], unmapped: list[str], disabled: list[TestRef])` with property `ok: bool`.
  - `trace(root: Path, gate: str | None = None) -> TraceResult`
  - `main(argv: Sequence[str] | None = None) -> int`: CLI `python scripts/tc_trace.py [--gate G01] [--root .]`. It prints one line per TC (`TC-01.2  OK  apps/api/tests/test_health.py::test_...` or `TC-01.4  MISSING`) and returns 0 if `ok`, else 1.
- Produces: `scripts/capture_red.ps1 -Tc "TC-01.x" -Command "<cmd>"`. It runs the command, tees output to `docs/evidence/G01/red/<UTC yyyyMMddTHHmmssZ>_<Tc>.txt`, and exits 0 only if the command **failed** (if it passed, it prints "Expected a failing run for <Tc> — this is not RED evidence" and exits 1). It takes the gate from `tc_trace` via `uv run python -c`.

- [ ] **Step 1: Write the failing tests**, all marked `tc("TC-01.6")`:
  - `test_active_gate_parsed` → `"G01"`
  - `test_gate_test_cases_reads_only_that_section`: a fake map with G01 (TC-01.1, TC-01.2) and G02 (TC-02.1) → `["TC-01.1","TC-01.2"]`
  - `test_trace_fails_when_tc_unmapped`: only TC-01.1 has a test → `ok is False`, `unmapped == ["TC-01.2"]`, and `main` returns 1
  - `test_trace_passes_when_all_mapped`: marker, name convention and `[TC-01.2]` Vitest title → `ok is True`, `main` returns 0
  - `test_skipped_or_xfail_mapping_fails`: a mapped test with `@pytest.mark.skip` and one with `it.skip('[TC-01.2]…')` → `ok is False`, both listed in `disabled`
  - `test_ignores_node_modules`
- [ ] **Step 2:** Run `scripts/capture_red.ps1`… this helper doesn't exist yet. For this one TC, capture by hand: `uv run pytest scripts/tests/test_tc_trace.py -q *>&1 | Tee-Object docs/evidence/G01/red/<ts>_TC-01.6.txt`. Expected: collection error / ModuleNotFoundError `tc_trace`.
- [ ] **Step 3:** Commit `test(G01): RED for TC-01.6 tc_trace traceability` (tests + evidence).
- [ ] **Step 4:** Implement `scripts/tc_trace.py` per Interfaces, and `scripts/capture_red.ps1`.
- [ ] **Step 5:** Run `uv run pytest scripts/tests/test_tc_trace.py -q`, then `uv run mypy scripts`. Expected: all pass, and mypy reports no errors.
- [ ] **Step 6:** Run `uv run python scripts/tc_trace.py` on the real repo. Expected: exit 1, with TC-01.6 and TC-01.5 OK and the rest MISSING. Save this output as `docs/evidence/G01/tc_trace_unmapped_demo.txt` (TC-01.6 "fails" demonstration).
- [ ] **Step 7:** Commit `feat(G01): GREEN TC-01.6 tc_trace and RED capture helper`.

### Task 3: API health and version (TC-01.2 unit) and engine skeleton

**Files:**
- Create: `apps/api/pyproject.toml` (name `statforge-api`, version `0.1.0`; deps fastapi, uvicorn[standard], pydantic, pydantic-settings, psycopg[binary], boto3), `apps/api/src/statforge_api/{__init__,main,settings,health,version}.py`, `apps/api/src/statforge_api/py.typed`
- Create: `packages/engine/pyproject.toml` (name `statforge-engine`, no runtime deps), `packages/engine/src/statforge_engine/__init__.py` (`__version__ = "0.1.0"`), `py.typed`
- Test: `apps/api/tests/test_health.py`, `apps/api/tests/test_version.py`, `packages/engine/tests/test_engine_purity.py`

**Interfaces:**
- Produces:
  - `settings.Settings(BaseSettings)`: `database_url: str`, `s3_endpoint_url: str`, `s3_access_key: str`, `s3_secret_key: str`, `app_env: str = "dev"`; env vars `DATABASE_URL`, `S3_ENDPOINT_URL`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `APP_ENV`.
  - `health.CheckResult(BaseModel)`: `status: Literal["ok","down"]`, `detail: str | None = None`.
  - `health.HealthResponse(BaseModel)`: `status: Literal["ok","unavailable"]`, `components: dict[str, CheckResult]`.
  - `health.check_db(database_url: str, timeout_s: float = 2.0) -> CheckResult`: `psycopg.connect(..., connect_timeout=…)`, `SELECT 1`, statement timeout = `timeout_s`. On any exception it returns `down` with the detail `"The database is not reachable."` and logs only `type(exc).__name__`.
  - `health.check_s3(endpoint_url: str, access_key: str, secret_key: str, timeout_s: float = 2.0) -> CheckResult`: boto3 `list_buckets` with `Config(connect_timeout, read_timeout, retries={"max_attempts": 1})`. Detail when down: `"File storage is not reachable."`
  - `Check = Callable[[], CheckResult]`
  - `main.create_app(checks: Mapping[str, Check] | None = None) -> FastAPI`. If `checks` is None it builds `{"db": …, "s3": …}` from `Settings()` lazily, at the first `/health` call. `GET /health` → 200 if every component is `ok`, else 503, body `HealthResponse`. `GET /api/v1/version` → `VersionResponse(name="StatForge API", version=<importlib.metadata.version("statforge-api")>, api="v1")`. Module-level `app = create_app()` for uvicorn.
- Consumes: the `tc` marker from Task 1.

- [ ] **Step 1: Write the failing tests**, using `fastapi.testclient.TestClient` with injected fake checks. Health tests are marked `tc("TC-01.2")`:
  - `test_health_ok_when_all_components_ok` → 200, `{"status":"ok","components":{"db":{"status":"ok","detail":null},"s3":{…ok}}}`
  - `test_health_503_when_db_down` → 503, `status == "unavailable"`, `components.db.status == "down"`, `components.s3.status == "ok"`
  - `test_health_503_when_s3_down` (proposed) → 503, `components.s3.status == "down"`
  - `test_check_db_hides_connection_details` (Review Focus 2): `check_db("postgresql://u:s3cretpw@127.0.0.1:1/x", 0.5)` → `down`; `"s3cretpw"` and `"postgresql://"` are absent from `detail` and from `caplog.text`
  - `test_check_db_times_out_on_silent_server` (Review Focus 1): a `socket` server thread that accepts and never replies; `check_db(f"postgresql://u:p@127.0.0.1:{port}/x", 1.0)` returns `down` in < 3 s (measured with `time.monotonic`)
  - `test_version_endpoint` (in `test_version.py`, marked `tc("TC-01.3")`) → 200, `{"name":"StatForge API","version":"0.1.0","api":"v1"}`
  - `test_engine_has_no_web_db_ai_imports` (engine purity; AGENTS.md §12): the AST of every module in `packages/engine/src` imports none of `fastapi, starlette, sqlalchemy, psycopg, boto3, httpx, requests, anthropic, openai, pydantic_ai`
- [ ] **Step 2:** Run `scripts/capture_red.ps1 -Tc "TC-01.2" -Command "uv run pytest apps/api/tests -q"`. Expected: it fails with an import error. The evidence file is written.
- [ ] **Step 3:** Commit `test(G01): RED for TC-01.2 health and version endpoints`.
- [ ] **Step 4:** Implement per Interfaces, then run `uv sync`.
- [ ] **Step 5:** Run `uv run pytest apps/api packages/engine -q`, then `uv run mypy`. Expected: everything passes.
- [ ] **Step 6:** Commit `feat(G01): GREEN TC-01.2 health and version endpoints`.

### Task 4: Web placeholder page (TC-01.3 unit)

**Files:**
- Create: `apps/web/` with `package.json` (name `@statforge/web`; scripts `dev`, `build`, `lint` (eslint), `typecheck` (`tsc -b --noEmit`), `test` (`vitest run`), `test:coverage`, `e2e` (`playwright test`)), `index.html`, `vite.config.ts` (dev proxy `/api` and `/health` → `http://localhost:8000`; Vitest env jsdom; coverage v8 with thresholds `lines: 85`), `tsconfig.json`, `eslint.config.js` (typescript-eslint strict), `src/main.tsx`, `src/App.tsx`, `src/api/version.ts`, `src/styles.css`
- Test: `apps/web/src/App.test.tsx`, `apps/web/src/api/version.test.ts`

**Interfaces:**
- Produces:
  - `type VersionInfo = { name: string; version: string; api: string }`
  - `fetchVersion(fetchFn: typeof fetch = fetch): Promise<VersionInfo>`: GET `/api/v1/version`. It throws `Error("version request failed")` on non-2xx or on a body without string `name`, `version` and `api`.
  - `App({ loadVersion = fetchVersion }: { loadVersion?: () => Promise<VersionInfo> })`
- Exact copy:
  - loading: `Connecting to the StatForge API…`
  - success: `<h1>StatForge</h1>` with the text `API v1 · version 0.1.0` (formatted `API ${api} · version ${version}`)
  - error (`role="alert"`): `Can't reach the StatForge API. Check that the api service is running, then reload the page.`

- [ ] **Step 1: Write the failing tests:**
  - `[TC-01.3] shows the api version from /api/v1/version` (resolved loader → text `API v1 · version 0.1.0`)
  - `[TC-01.3] shows a loading message first`
  - `[TC-01.3] shows a plain error when the api is unreachable` (rejected loader → alert with the exact copy)
  - `[TC-01.3] fetchVersion rejects a malformed body` and `[TC-01.3] fetchVersion rejects non-2xx`
- [ ] **Step 2:** Run `scripts/capture_red.ps1 -Tc "TC-01.3" -Command "pnpm --filter @statforge/web test"`. Expected: FAIL (module not found).
- [ ] **Step 3:** Commit `test(G01): RED for TC-01.3 placeholder page`.
- [ ] **Step 4:** Implement per Interfaces. Plain CSS only: system font, readable contrast, visible `:focus-visible` outline. No Tailwind yet (that comes in G04).
- [ ] **Step 5:** Run `pnpm --filter @statforge/web test:coverage`, then `lint`, `typecheck` and `build`. Expected: all pass, with coverage ≥ 85%.
- [ ] **Step 6:** Commit `feat(G01): GREEN TC-01.3 placeholder page`.

### Task 5: Docker Compose stack, live integration and cold start (TC-01.1, TC-01.2 live, TC-01.3 e2e)

**Files:**
- Create: `docker-compose.yml`, `.env.example`, `apps/api/Dockerfile`, `apps/web/Dockerfile`, `apps/web/nginx.conf`, `apps/web/playwright.config.ts`, `apps/web/e2e/placeholder.spec.ts`, `scripts/cold_start.py`
- Test: `tests/integration/conftest.py`, `tests/integration/test_health_live.py`, `tests/integration/test_cold_start.py`, `scripts/tests/test_cold_start_unit.py`

**Interfaces:**
- Compose (`name: statforge`):
  - `db`: `postgres:18-alpine`, volume `db-data:/var/lib/postgresql`, healthcheck `pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB` (interval 2s, retries 30, start_period 5s), no host port.
  - `s3`: `chrislusf/seaweedfs:<latest stable tag, pinned>`, `server -dir=/data -s3 -s3.port=8333`, volume `s3-data:/data`, healthcheck on `http://127.0.0.1:9333/cluster/healthz` (verify the endpoint against the pinned version; if it differs, use the S3 port and record it in TROUBLESHOOTING), no host port.
  - `api`: build `context: .`, `dockerfile: apps/api/Dockerfile` (python:3.14-slim, uv from `ghcr.io/astral-sh/uv`, `uv sync --frozen --no-dev --package statforge-api`, non-root user, `uvicorn statforge_api.main:app --host 0.0.0.0 --port 8000`). Environment: `DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}` and the S3 variables. `depends_on` db and s3 `service_healthy`. Port `${API_PORT:-8000}:8000`. Healthcheck: python urllib GET `/health` must return 200.
  - `web`: build `context: .`, `dockerfile: apps/web/Dockerfile` (node:24-alpine + corepack pnpm build stage → `nginx:1-alpine` serving `dist/`, with `nginx.conf` proxying `/api/` and `/health` to `http://api:8000`). `depends_on` api `service_healthy`. Port `${WEB_PORT:-8080}:80`. Healthcheck: `wget -q -O /dev/null http://127.0.0.1/`.
  - Required variables use `${POSTGRES_PASSWORD:?Copy .env.example to .env first (see README Setup)}`, and the same for `POSTGRES_USER`, `POSTGRES_DB`, `S3_ACCESS_KEY` and `S3_SECRET_KEY`.
- `.env.example`: `POSTGRES_USER=statforge`, `POSTGRES_DB=statforge`, `POSTGRES_PASSWORD=change-me-local-only`, `S3_ACCESS_KEY=change-me-local-only`, `S3_SECRET_KEY=change-me-local-only`, `S3_ENDPOINT_URL=http://s3:8333`, `API_PORT=8000`, `WEB_PORT=8080`.
- **TC-01.1 condition = "clean pull" (D-032c).** Before the timer starts, none of these exist locally:
  - the project's built images (`statforge-coldstart-api`, `statforge-coldstart-web`)
  - its volumes
  - the base and service images `postgres:18-alpine`, `chrislusf/seaweedfs:<pinned>`, `python:3.14-slim`, `ghcr.io/astral-sh/uv:<pinned>`, `node:24-alpine`, `nginx:1-alpine`

  The timed run then pulls everything from the registries and builds with `--no-cache`. The "cached" condition (images already present) is **not** the TC condition; it's recorded only as an informational second timing.
- `cold_start.py`:
  - `BASE_IMAGES: tuple[str, ...]` = the six images above (kept in sync with the Dockerfiles and compose by a unit test that parses them)
  - `@dataclass ColdStartResult(condition: Literal["clean-pull","cached"], seconds: float, healthy: dict[str, bool], absent_before: dict[str, bool])`
  - `ensure_clean_pull() -> dict[str, bool]`: `docker image rm` each base image, then `docker image inspect` each one. It raises `ColdStartPreconditionError("<image> is still present (in use by another container?) — stop that container and retry")` if any remains.
  - `run_cold_start(repo: Path, workdir: Path, project: str = "statforge-coldstart", ports: Mapping[str,int] = {"API_PORT": 18000, "WEB_PORT": 18080}, limit_s: float = 180.0) -> ColdStartResult`. Steps:
    1. `git clone --no-hardlinks <repo> <workdir>`
    2. copy `.env.example` → `.env`
    3. `docker compose -p <project> down -v --rmi all` (project-scoped clean), then `ensure_clean_pull()`
    4. **timer starts**
    5. `docker compose -p <project> build --no-cache --pull`
    6. `up -d --wait --wait-timeout <limit>`
    7. **timer stops**
    8. read health via `docker compose ps --format json`
    9. always `down -v --rmi local` in `finally`
  - `main` writes `docs/evidence/G01/cold_start_<UTC ts>.json`.
  - It never runs a global `docker builder prune` or `docker system prune`.
- Integration `conftest.py`: fixture `api_base` (`http://localhost:${API_PORT:-8000}`). If it's unreachable, it calls `pytest.fail("Start the stack first: docker compose up -d --wait")`. It never skips.

- [ ] **Step 1: Write the failing tests:**
  - `tests/integration/test_health_live.py`, marked `integration`, `tc("TC-01.2")`:
    - `test_live_health_ok`: 200, both components ok
    - `test_live_health_503_when_db_stopped`: `docker compose stop db`, then poll `/health` ≤ 10 s → 503 with db down; the body text contains neither `POSTGRES_PASSWORD`'s value nor `postgresql://`; `finally`: `docker compose start db` and poll ≤ 30 s → 200 (recovery)
    - `test_live_health_503_when_s3_stopped` (proposed): same shape for s3
  - `tests/integration/test_cold_start.py`, marked `integration`, `slow`, `tc("TC-01.1")`: `test_tc01_1_clean_pull_cold_start_under_3_minutes` → `result.condition == "clean-pull"`, every value in `result.absent_before` is True, `result.seconds < 180`, and every service in `{"web","api","db","s3"}` is healthy
  - `scripts/tests/test_cold_start_unit.py`, `tc("TC-01.1")`, with `subprocess.run` monkeypatched:
    - `test_command_sequence`: clone → `.env` copy → `down -v --rmi all` → `image rm` of each base image → `build --no-cache --pull` → `up -d --wait` → `down -v --rmi local`
    - `test_down_runs_even_when_up_fails`
    - `test_never_prunes`: no command contains `prune`
    - `test_precondition_fails_when_base_image_remains`: `ColdStartPreconditionError` names the image, and the timer never starts
    - `test_base_images_match_dockerfiles_and_compose`: parses the `FROM` lines and the compose `image:` keys, and the set equals `BASE_IMAGES`
  - `apps/web/e2e/placeholder.spec.ts`: `[TC-01.3] page shows the version served by /api/v1/version` (it fetches `/api/v1/version` through the web origin and expects the page to contain `API v1 · version <that version>`); `[TC-01.3] placeholder page has no serious or critical axe violations`
- [ ] **Step 2:** Run `scripts/capture_red.ps1 -Tc "TC-01.1" -Command "uv run pytest scripts/tests/test_cold_start_unit.py tests/integration -q"`. Expected: it fails (`cold_start` is missing and the stack isn't running).
- [ ] **Step 3:** Commit `test(G01): RED for TC-01.1 TC-01.2 TC-01.3 compose stack, live health, e2e`.
- [ ] **Step 4:** Implement the compose file, Dockerfiles, nginx.conf, `.env.example`, `cold_start.py` and the Playwright config (`baseURL` from `WEB_BASE_URL`, default `http://localhost:8080`, chromium only).
- [ ] **Step 5:** Run `Copy-Item .env.example .env`, then `docker compose up -d --build --wait`. Expected: 4 services healthy.
- [ ] **Step 6:** Run `uv run pytest -m "integration and not slow" -q`, then `pnpm --filter @statforge/web exec playwright install chromium` and `pnpm --filter @statforge/web e2e`. Expected: all pass.
- [ ] **Step 7:** Run `uv run pytest tests/integration/test_cold_start.py -q`. Expected: PASS, and a timing JSON (with condition `clean-pull`) is written to `docs/evidence/G01/`. Also run `uv run python scripts/cold_start.py --cached` once and save it as the informational cached timing. If clean-pull takes ≥ 180 s, debug with `superpowers:systematic-debugging`; don't raise the limit. If the cause is download bandwidth, report the measured pull time separately to the owner rather than changing the condition.
- [ ] **Step 8:** Run `Remove-Item .env`, then `docker compose config`. Expected: the message `Copy .env.example to .env first (see README Setup)`. Save the output to `docs/evidence/G01/missing_env_message.txt`. Restore `.env` afterwards.
- [ ] **Step 9:** Commit `feat(G01): GREEN TC-01.1 TC-01.2 TC-01.3 compose stack and cold start`.

### Task 6: Secret scan (TC-01.5)

**Files:**
- Create: `.gitleaks.toml` (`[extend] useDefault = true`; allowlist only for the literal `change-me-local-only`), `scripts/install_tools.ps1` (downloads a pinned gitleaks 8.x release zip from GitHub into `$env:USERPROFILE\.local\bin` and checks the SHA-256 against the release's checksums file; `uv tool install pre-commit`)
- Test: `tests/repo/test_secret_scan.py`

**Interfaces:**
- Produces: `gitleaks` on PATH; the `.gitleaks.toml` path used by pre-commit (Task 9) and CI (Task 10).

- [ ] **Step 1: Write the failing tests**, marked `tc("TC-01.5")`. If `shutil.which("gitleaks")` is None, they **fail** with `"gitleaks not installed — run scripts/install_tools.ps1"`.
  - `test_repo_history_has_zero_secrets`: `gitleaks git --config .gitleaks.toml --redact --exit-code 1 --report-format json --report-path <tmp>` → exit 0 and the report is `[]`
  - `test_working_tree_has_zero_secrets`: `gitleaks dir . --config .gitleaks.toml --redact` (excluding `sources/`, `node_modules`, `.venv`) → exit 0
  - `test_planted_secret_is_detected` (proposed, D-032b): it generates the token **at runtime**: `"ghp_" + "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(36))`. It writes it to a file in a `tmp_path` git repo (never inside the project tree), commits it there, and runs `gitleaks git <tmp repo>` → exit 1 and ≥ 1 finding. The test source must not contain a literal token; `test_repo_history_has_zero_secrets` proves this.
- [ ] **Step 2:** Run `scripts/capture_red.ps1 -Tc "TC-01.5" -Command "uv run pytest tests/repo/test_secret_scan.py -q"`. Expected: it fails (gitleaks not installed, config missing).
- [ ] **Step 3:** Commit `test(G01): RED for TC-01.5 secret scan`.
- [ ] **Step 4:** Write `.gitleaks.toml` and `scripts/install_tools.ps1`, then run the installer.
- [ ] **Step 5:** Run `uv run pytest tests/repo -q`. Expected: all pass. Save the scan's JSON report as `docs/evidence/G01/gitleaks_report.json`.
- [ ] **Step 6:** Commit `feat(G01): GREEN TC-01.5 gitleaks config and tool installer`.

### Task 7: Commit guard (TC-01.8)

**Files:**
- Create: `scripts/commit_guard.py`
- Test: `scripts/tests/test_commit_guard.py`

**Interfaces:**
- Consumes: `tc_trace.active_gate`, `tc_trace.is_test_file`, `tc_trace.tc_ids_in`.
- Produces:
  - `PRODUCT_ROOTS = ("apps/", "packages/", "plugins/")`
  - `is_git_commit(command: str) -> bool`: matches `git` followed by optional global options (`-C <x>`, `-c <k=v>`, `--git-dir=…`), then `commit`.
  - `uses_all_flag(command: str) -> bool`: `-a`, `-am…`, `--all`.
  - `unit_of(path: str) -> str | None`: `apps/api/src/x.py` → `apps/api`; `plugins/foo/x.py` → `plugins/foo`; non-product paths → None.
  - `@dataclass(frozen=True) GuardDecision(allowed: bool, reason: str)`
  - `evaluate(staged: Sequence[str], test_files: Mapping[str, str], gate: str) -> GuardDecision`. Every product unit touched by a staged non-test file must have at least one test file (path → content, staged or in HEAD) under the same unit, or under root `tests/`, that contains a TC id starting `TC-<gate number>.`. Block reason: `"Blocked by test-first guard: <unit> has no tests for <gate>. Commit the RED tests first (AGENTS.md §4.1)."`
  - `main(argv) -> int` with modes:
    - `--hook`: reads Claude Code PreToolUse JSON from stdin, uses `tool_input.command`, and returns 0 when it isn't a commit. On a block it writes the reason to stderr and returns **2**.
    - `--precommit`: runs on the staged index and returns 1 on a block.
  - The staged list comes from `git diff --cached --name-only`, plus `git diff --name-only` when `uses_all_flag`. Test contents come from `git show :<path>` for staged files and `git ls-files` + read for tracked ones.

- [ ] **Step 1: Write the failing tests**, marked `tc("TC-01.8")`:
  - `test_blocks_product_code_without_tests` → `allowed is False`; the reason contains `apps/api` and `G01`
  - `test_allows_tests_first_then_code`: commit 1 (staged tests only) is allowed; commit 2 (code, with those tests now in `test_files`) is allowed
  - `test_docs_only_commit_allowed`
  - `test_tests_for_other_gate_do_not_count` (tests carry only `TC-02.1` → blocked)
  - `test_is_git_commit_shapes`, parametrised: `git commit -m x`, `git commit -am x`, `git -C repo commit`, `git -c user.name=a commit -m x`, `git commit -m @'\nmsg\n'@` → True; `git status`, `git log --grep commit`, `echo commit` → False
  - `test_all_flag_includes_unstaged_changes` (Review Focus 3)
  - `test_hook_mode_end_to_end`: a tmp git repo with a fake GATE_LOG and product file staged; `subprocess.run([sys.executable, "scripts/commit_guard.py", "--hook"], input=<JSON with tool_input.command "git commit -m x">, cwd=tmp)` → exit 2 and stderr contains "test-first guard"; after staging a G01 test as well → exit 0
- [ ] **Step 2:** Run `scripts/capture_red.ps1 -Tc "TC-01.8" -Command "uv run pytest scripts/tests/test_commit_guard.py -q"`. Expected: FAIL.
- [ ] **Step 3:** Commit `test(G01): RED for TC-01.8 commit guard`.
- [ ] **Step 4:** Implement per Interfaces.
- [ ] **Step 5:** Run `uv run pytest scripts/tests -q`, then `uv run mypy`. Expected: pass.
- [ ] **Step 6:** Commit `feat(G01): GREEN TC-01.8 commit guard`.

### Task 8: RED-before-GREEN checker (TC-01.10)

**Files:**
- Create: `scripts/red_green_check.py`
- Test: `scripts/tests/test_red_green_check.py`

**Interfaces:**
- Consumes: `tc_trace.active_gate`, `tc_trace.gate_test_cases`, `tc_trace.TC_PATTERN`.
- Produces:
  - `@dataclass(frozen=True) Commit(sha: str, timestamp: int, subject: str)`
  - `@dataclass(frozen=True) Evidence(name: str, timestamp: int, tcs: frozenset[str], text: str)`: the timestamp is parsed from the filename prefix `yyyyMMddTHHmmssZ` (UTC), and the TCs from the filename.
  - RED subject regex: `^test\((?P<gate>G\d{2})\): RED for `; GREEN subject regex: `^(feat|fix)\((?P<gate>G\d{2})\): GREEN `. TC ids come from the subject via `TC_PATTERN`.
  - `check(commits: Sequence[Commit], evidence: Sequence[Evidence], tcs: Sequence[str], gate: str) -> list[str]`: returns problems, empty = pass. Rules for each TC:
    1. a RED commit exists
    2. a GREEN commit exists
    3. the earliest RED timestamp is **strictly earlier** than the earliest GREEN timestamp
    4. an evidence file names the TC, has a timestamp ≤ the earliest RED commit timestamp, and its text contains `fail` or `error` (case-insensitive)
  - `main(argv) -> int`: reads `git log --format=%H%x09%ct%x09%s` and `docs/evidence/<gate>/red/`, prints a table, and returns 0 or 1.

- [ ] **Step 1: Write the failing tests**, marked `tc("TC-01.10")`:
  - `test_passes_when_red_precedes_green`
  - `test_fails_when_green_before_red`
  - `test_fails_when_red_and_green_same_second`
  - `test_fails_without_evidence_file`
  - `test_fails_when_evidence_shows_no_failure`
  - `test_fails_when_evidence_newer_than_red_commit`
  - `test_multiple_tcs_in_one_subject` (`RED for TC-01.1 TC-01.2 …` counts for both)
- [ ] **Step 2:** Run `scripts/capture_red.ps1 -Tc "TC-01.10" -Command "uv run pytest scripts/tests/test_red_green_check.py -q"`. Expected: FAIL.
- [ ] **Step 3:** Commit `test(G01): RED for TC-01.10 red-green checker`.
- [ ] **Step 4:** Implement per Interfaces.
- [ ] **Step 5:** Run the tests. Expected: pass. Run `uv run python scripts/red_green_check.py`. Expected: OK for TC-01.1, 01.2, 01.3, 01.5, 01.6, 01.8 and 01.10; MISSING for TC-01.4, 01.7 and 01.9 (Tasks 9–10).
- [ ] **Step 6:** Commit `feat(G01): GREEN TC-01.10 red-green checker`.

### Task 9: CI workflow (TC-01.4, TC-01.9 static)

> Ordering: this task comes before the hooks (Task 10), so that every TC except TC-01.7 is already mapped when pre-commit and the Stop hook switch on. Otherwise `tc_trace` would block every commit and stop in between.

**Files:**
- Create: `.github/workflows/ci.yml`
- Test: `tests/repo/test_ci_workflow.py`

**Interfaces:**
- `ci.yml`:
  - Triggers: `on: push` (all branches) and `pull_request` (branches `main`, `ci-check/**`).
  - Jobs, all on `ubuntu-latest`:
    - `python`: `astral-sh/setup-uv` with Python 3.14 · `uv sync --frozen` · ruff check · ruff format --check · mypy · `pytest -m "not integration" --cov --cov-fail-under=85`
    - `web`: `actions/setup-node` with Node 24 · `corepack enable pnpm` · `pnpm install --frozen-lockfile` · lint · typecheck · `test:coverage` (thresholds 85) · build
    - `trace`: `fetch-depth: 0` · `uv run python scripts/tc_trace.py` · `uv run python scripts/red_green_check.py`
    - `secrets`: `fetch-depth: 0` · the pinned gitleaks binary from its GitHub release (checksum verified) · `gitleaks git --redact --config .gitleaks.toml`
    - `compose`: needs `[python, web]` · `cp .env.example .env` · `docker compose up -d --build --wait` · `uv run pytest -m "integration and not slow"` · Playwright e2e · on failure, `docker compose logs` · always `docker compose down -v`
  - Every job has `timeout-minutes: 20` and `permissions: contents: read`.

- [ ] **Step 1: Write the failing tests** in `tests/repo/test_ci_workflow.py` (PyYAML):
  - `test_ci_runs_lint_and_tests_on_push_and_pr`, marked `tc("TC-01.4")`: the triggers above; the `python` job contains `ruff check` and `pytest`; the `web` job contains `lint` and `test`
  - `test_ci_enforces_coverage_and_trace`, marked `tc("TC-01.9")`: `--cov-fail-under=85` is present, the `trace` job runs `tc_trace.py`, and the `pull_request` trigger is present
  - `test_ci_jobs_have_timeouts_and_readonly_permissions`
- [ ] **Step 2:** Run `scripts/capture_red.ps1 -Tc "TC-01.4_TC-01.9" -Command "uv run pytest tests/repo/test_ci_workflow.py -q"`. Expected: FAIL (no workflow file).
- [ ] **Step 3:** Commit `test(G01): RED for TC-01.4 TC-01.9 CI workflow`.
- [ ] **Step 4:** Write `ci.yml` per Interfaces. Run `uv run pytest tests/repo -q`. Expected: pass.
- [ ] **Step 5:** Commit `feat(G01): GREEN TC-01.4 TC-01.9 CI workflow`.

### Task 10: `verify.ps1`, Stop hook, pre-commit, Claude settings (TC-01.7; wires TC-01.8)

> RED→GREEN for each TC happens within one working turn: the Stop hook (correctly) refuses to end a turn while RED tests fail. This is recorded in ADR-0001.

**Files:**
- Create: `scripts/verify.ps1`, `scripts/stop_hook.py`, `.pre-commit-config.yaml`, `.claude/settings.json`
- Test: `scripts/tests/test_stop_hook.py`, `scripts/tests/test_verify_ps1.py`, `tests/repo/test_claude_settings.py`

**Interfaces:**
- `verify.ps1 -Mode Hook|Full` (default `Full`):
  - Each step prints `[PASS] <name>` or `[FAIL] <name>: <first error line>`. All steps run, then a summary prints and it exits 1 if any step failed.
  - Before each step it checks the tool with `Get-Command`. A missing tool gives `[FAIL] <name>: <tool> not found — see README "Setup"`.
  - Hook mode runs: `ruff check .`, `ruff format --check .`, `mypy`, `pytest -m "not integration" -q`, `pnpm -r --if-present lint`, `pnpm -r --if-present typecheck`, `pnpm -r --if-present test`, `tc_trace`.
  - Full mode adds:
    - `pytest -m "not integration" --cov --cov-fail-under=85`
    - `pnpm -r --if-present test:coverage`
    - `pnpm -r --if-present build`
    - `gitleaks git --redact`
    - `red_green_check`
    - `pytest -m "integration and not slow"` (needs the stack)
    - `-IncludeColdStart` switch adds `pytest -m slow`
- `stop_hook.py`:
  - `@dataclass(frozen=True) VerifyResult(ok: bool, summary: str)`
  - `@dataclass(frozen=True) HookOutcome(exit_code: int, stderr: str, stdout: str)`
  - `run_hook(payload: Mapping[str, object], verify: Callable[[], VerifyResult], state_path: Path, max_blocks: int = 3) -> HookOutcome`:
    - When it passes: exit 0, and the state is reset.
    - When it fails and the consecutive-block count is under `max_blocks`: exit 2, and stderr = `"verify.ps1 is failing — the work is not done. Fix these before stopping:\n" + summary`. The count increments.
    - When it fails at `max_blocks`: exit 0, stdout = JSON `{"systemMessage": "verify.ps1 is FAILING after 3 attempts — the work is NOT done. Report the failures to the owner."}`, and the count resets.
  - `main() -> int`: wires `verify` to `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify.ps1 -Mode Hook`, with the last 40 output lines as the summary. The state file is `.claude/.stop_hook_state.json`.
- `.claude/settings.json`:
  - `hooks.Stop`: a command running `uv run python scripts/stop_hook.py`, timeout 600
  - `hooks.PreToolUse`: matcher `Bash|PowerShell`, a command running `uv run python scripts/commit_guard.py --hook`, timeout 60
  - permissions deny `Bash(git push --force*)`, `Bash(git reset --hard*)`, `PowerShell(git push --force*)`, `PowerShell(git reset --hard*)`
- `.pre-commit-config.yaml`: local hooks (`language: system`):
  - `uv run ruff check`, `uv run ruff format --check`, `uv run mypy`
  - `pnpm -r --if-present lint`
  - `gitleaks git --pre-commit --staged --redact --config .gitleaks.toml`
  - `uv run python scripts/tc_trace.py`
  - `uv run python scripts/commit_guard.py --precommit`

- [ ] **Step 1: Write the failing tests:**
  - `test_stop_hook.py`, marked `tc("TC-01.7")`:
    - `test_blocks_stop_when_verify_fails` → exit 2, stderr contains `the work is not done` and the summary line `[FAIL] pytest`
    - `test_allows_stop_when_verify_passes` → exit 0
    - `test_releases_after_three_blocks_with_warning` (Review Focus 5)
    - `test_state_resets_after_pass`
  - `test_verify_ps1.py`, marked `tc("TC-01.7")`, Windows-only via `sys.platform` (it fails on other platforms with a message, not a skip): runs `verify.ps1 -Mode Hook` with a PATH lacking pnpm → exit 1 and output contains `pnpm not found — see README "Setup"` (Review Focus 4)
  - `test_claude_settings.py`:
    - `test_stop_hook_wired`, marked `tc("TC-01.7")`
    - `test_commit_guard_wired_for_bash_and_powershell`, marked `tc("TC-01.8")`: it parses `.claude/settings.json` and asserts the commands and matcher above
    - `test_gate_close_reruns_verify_independently`, marked `tc("TC-01.7")` (D-031, D-032e): `.claude/skills/gate-close/SKILL.md` preconditions contain `scripts/verify.ps1 -Mode Full`, the words "run it yourself" and "even if the Stop hook released", and the instruction to stop (no merge, no tag, no push) on any `[FAIL]`
- [ ] **Step 2:** Run `scripts/capture_red.ps1 -Tc "TC-01.7" -Command "uv run pytest scripts/tests/test_stop_hook.py scripts/tests/test_verify_ps1.py tests/repo/test_claude_settings.py -q"`. Expected: FAIL.
- [ ] **Step 3:** Commit `test(G01): RED for TC-01.7 stop hook and verify script`.
- [ ] **Step 4:** Implement `verify.ps1`, `stop_hook.py`, `.pre-commit-config.yaml` and `.claude/settings.json`. Then run `pre-commit install`. In `.claude/skills/gate-close/SKILL.md`, replace the precondition "`scripts/verify.ps1` is green" with:
  - "Run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify.ps1 -Mode Full -IncludeColdStart` yourself, with the stack up, in this session, even if the Stop hook released earlier with "NOT done" or reported green. Never rely on an earlier run. On any `[FAIL]`, stop: no merge, no tag, no push. Report the failures to the owner."
  - Also add: "Free plan (D-031): GitHub doesn't block merges server-side, so this refusal is the merge gate."
- [ ] **Step 5:** Run `powershell -File scripts/verify.ps1 -Mode Hook`. Expected: every step `[PASS]` (all 10 TCs are mapped by now). Then, with the stack up, run `powershell -File scripts/verify.ps1 -Mode Full`. Expected: every step `[PASS]`.
- [ ] **Step 6:** Commit `feat(G01): GREEN TC-01.7 verify script, stop hook, pre-commit, Claude hooks`. Expected: pre-commit passes, including tc_trace and the commit guard.
- [ ] **Step 7: Live demonstration, TC-01.7** (scratch branch `scratch/G01-stop-hook-demo` off the gate branch):
  1. Add `assert 1 == 2` to a new test.
  2. End a turn. Expected: the Stop hook blocks with the failing summary.
  3. Save the transcript excerpt and a screenshot to `docs/evidence/G01/stop_hook_demo.md`.
  4. Delete the branch (local only, never pushed).
- [ ] **Step 8: Live demonstration, TC-01.8:**
  1. On a scratch branch, stage a new `apps/api/src/statforge_api/demo.py` with no tests and run `git commit`. Expected: blocked (exit 2).
  2. Then commit a G01-marked test, then the code. Expected: both allowed.
  3. Save to `docs/evidence/G01/commit_guard_demo.md`, then delete the branch.

### Task 11: ci-check demonstrations on GitHub (TC-01.4, TC-01.9 live)

**Files:**
- Evidence: `docs/evidence/G01/ci/` (`runs.md` with run URLs, conclusions, and screenshots)

**Interfaces:**
- Consumes: `ci.yml` (Task 9), with hooks active (Task 10).
- **No ruleset** (D-031, Free plan). The enforcement shown is the PR's red required-looking checks, plus `/gate-close` refusal. The text below is kept for reference only; don't run it.
- Ruleset (not used): `gh api -X POST repos/Raghustatics/StatForge_Project_Management/rulesets`, targeting `main` and `ci-check/G01-base`, requiring status checks `python`, `web`, `trace`, `secrets`, `compose`. **If GitHub returns 403 (needs a paid plan for private repos):** record it in RISKS and DECISIONS as a limitation. The evidence then shows the PR's failing required checks, and `/gate-close` refuses to merge while checks are red.

- [ ] **Step 1: Push the clean baseline** as `ci-check/G01-base`, using `git push origin HEAD:refs/heads/ci-check/G01-base` (allowed by D-024). Watch it with `gh run watch`. Expected: every job green. If not, debug and fix on the gate branch, then re-push.
- [ ] **Step 2:** No ruleset (D-031). Write in `docs/evidence/G01/ci/runs.md` that enforcement is red CI plus `/gate-close` refusal.
- [ ] **Step 3: TC-01.4 demonstrations.** Each branch comes off `ci-check/G01-base`, gets one commit, is pushed, and is opened as a PR into `ci-check/G01-base`:
  - `ci-check/G01-lint-fail`: an unused import in `apps/api/src/statforge_api/version.py`. Expected: the `python` job fails on ruff.
  - `ci-check/G01-test-fail`: `assert 1 == 2` in a new test. Expected: the `python` job fails on pytest.
  - The local commit guard and pre-commit will block these commits. Commit with `git -c core.hooksPath=/dev/null commit` **only on these ci-check branches**, and note it in the session log. This is the deliberate-failure demonstration the TC requires, not a bypass of product work.
- [ ] **Step 4: TC-01.9 demonstrations,** the same way:
  - `ci-check/G01-coverage-drop`: adds an untested 40-line module under `packages/engine/src`. Expected: the `python` job fails `--cov-fail-under=85`, and the PR shows blocked or failing checks.
  - `ci-check/G01-tc-unmapped`: removes the `tc("TC-01.2")` markers. Expected: the `trace` job fails.
- [ ] **Step 5:** **Before deleting anything** (D-032a): record each PR URL, run URL and failing step in `docs/evidence/G01/ci/runs.md` (from `gh pr view --json url,statusCheckRollup` and `gh run view --json url,conclusion,jobs`), save screenshots of each failing PR and run page into `docs/evidence/G01/ci/` (Playwright MCP), and confirm the files exist. Then close the PRs and delete every `ci-check/G01-*` branch on GitHub (`git push origin --delete <branch>`) and locally. Run `git ls-remote origin`. Expected: no `ci-check` refs remain. Log every pushed and deleted branch in the session log.
- [ ] **Step 6:** Commit `docs(G01): CI demonstration evidence`.

### Task 12: Docs, ADR, final verification

**Files:**
- Modify: `README.md` (Setup, with prerequisites and exact PowerShell commands; Quick start; Expert per-service commands; Troubleshooting link), `docs/TROUBLESHOOTING.md`, `docs/DECISIONS.md`, `docs/RISKS.md` (add R-08 Stop hook friction and R-09 no server-side branch protection on the Free plan, mitigated per D-031), `docs/sessions/2026-10-20_0003_G01.md`
- Create: `docs/adr/0001-monorepo-and-tooling.md` (uv + pnpm workspaces, nginx proxy, static enforcement scripts, hook design including the 3-block release), `docs/CHANGELOG.md` (`0.1.0 — G01 foundation`), `docs/evidence/G01/README.md` (an index of every evidence file, mapped to TCs)

- [ ] **Step 1:** Write the docs. The README's Setup section reproduces exactly the commands used this gate: `uv python install 3.14`, `corepack enable pnpm --install-directory "$env:USERPROFILE\.local\bin"`, `scripts/install_tools.ps1`, `Copy-Item .env.example .env`, `docker compose up -d --wait`, then open `http://localhost:8080`.
- [ ] **Step 2: Fresh-eyes README check.** A subagent that has seen only the README follows it in a new temp clone (it may run commands and must report each step's result). Fix any gap it finds.
- [ ] **Step 3:** Run `powershell -File scripts/verify.ps1 -Mode Full -IncludeColdStart`. Expected: every step `[PASS]`. Save the output to `docs/evidence/G01/verify_full.txt`.
- [ ] **Step 4:** Run `uv run python scripts/tc_trace.py` and `uv run python scripts/red_green_check.py`. Expected: all 10 TCs OK. Save the outputs to `docs/evidence/G01/`.
- [ ] **Step 5:** Commit `docs(G01): README setup, ADR-0001, changelog, evidence index`.
- [ ] **Step 6:** Hand over to `/gate-review`, which runs SC-1…SC-11, the `gate-reviewer` and `security-reviewer` agents, and writes the owner validation script for S1–S6.
