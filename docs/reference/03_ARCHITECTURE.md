> **Reference spec (18 Oct 2026).** Subordinate to `docs/StatForge_Development_Guidelines_v1.1.md` and `docs/StatForge_Gate_Map_v1.0.md`. Where this file mentions pricing tiers, managed AI credits, a 13-phase roadmap or Keycloak-first auth, the guidelines v1.1 decisions win.

# 03 · Architecture

> Target architecture. ADR-001 (audit of the existing build) may adjust details; principles do not change.

## 1. System context

```
 Browser (React IDE shell)
   │  HTTPS (REST /api/v1 + Server-Sent Events for run & agent streams)
   ▼
 API service (FastAPI) ───────────────┐
   │  auth · projects · datasets ·     │  enqueue jobs (same DB transaction)
   │  plugins registry · agent gateway │
   ▼                                   ▼
 PostgreSQL 18  ◄──── Procrastinate ──► Worker service (stats engine + plugins)
   metadata, JSONB outputs, queue           │ read/write
                                            ▼
                                   Object storage (S3 API: SeaweedFS dev / R2 prod)
                                     originals (immutable) · Parquet versions · artefacts
 AI providers (Anthropic, OpenAI, Gemini, Ollama) ◄── API agent gateway only (never the browser)
 Identity provider (Keycloak, OIDC) — SaaS hardening phase
```

## 2. Services (Docker Compose)

| Service | Image / tech | Responsibility | Notes |
|---|---|---|---|
| `web` | Node 22 LTS build → static assets served by Caddy/nginx | IDE shell | Dev: Vite dev server with HMR |
| `api` | Python 3.14, FastAPI, Uvicorn | REST + SSE, auth, authorisation, validation, agent gateway, enqueue | Stateless; horizontally scalable |
| `worker` | Same Python image, `procrastinate worker` | Executes plugins, profiling, chart specs, exports | CPU/mem/time limits, read-only root FS, no outbound internet, per-job temp dir |
| `db` | postgres:18 | Metadata, run outputs (JSONB), job queue, audit log | Daily backups; RLS-ready |
| `s3` | SeaweedFS (dev) | Files and artefacts | Prod: Cloudflare R2 or AWS S3 |
| `ollama` (optional profile) | ollama/ollama | Local LLM for privacy mode | `docker compose --profile local-ai up` |
| `idp` (Phase 10) | Keycloak 26 | OIDC login, organisations | Dev uses local single user |

## 3. Packages and boundaries

```
statforge_engine  (pure Python; no FastAPI/DB imports)
  ├── io/          readers: csv, xlsx, pdf  → typed frames + reader report
  ├── profile/     type inference, quality checks (DuckDB + pandas)
  ├── stats/       descriptive, tests, regression, anova, spc, capability, calculators
  ├── charts/      Plotly JSON spec builders (+ Matplotlib for static export)
  └── contracts/   Pydantic models for plugin inputs/outputs
plugin_sdk_py     manifest schema, registry, discovery (entry points), run context
apps/api          HTTP layer, persistence, auth, agent gateway, job enqueue
apps/web          IDE shell, command registry, contribution registry, editors
plugins/*         one folder per built-in plugin (manifest + python + ui form hints + tests)
```

Rules:
- The engine never imports web, DB or AI code → it can ship inside a desktop app later.
- Plugins never import UI components or AI SDKs.
- The agent can only call **commands**; commands call API endpoints; endpoints enqueue plugin runs.

## 4. Key flows

### 4.1 Upload → profile → confirm
1. Browser uploads file (≤10 MB) → API validates size/type/magic bytes → stores **original** in S3 (`originals/{sha256}`) → creates `dataset` + `dataset_version v1 (raw)`.
2. API enqueues `profile` job → worker detects encoding (charset-normalizer), dialect (clevercsv), reads **all columns as text**, infers candidate types, runs quality checks → writes profile JSON.
3. UI shows Data Quality Review; user confirms types / treatments → each confirmation is a **transformation** record → worker materialises `dataset_version v2` as Parquet.

### 4.2 Run a plugin
1. User (or approved agent proposal) submits command `analysis.run` with plugin id, version, dataset version, roles, options.
2. API validates against the plugin input schema + preconditions → inserts `analysis_run (queued)` and job **in one transaction**.
3. Worker loads dataset version, executes plugin, returns output (tables, metrics, warnings, assumptions, chart specs) validated against output schema.
4. API stores output JSONB, streams status via SSE, updates linked KPIs → OKRs → insight pane.

### 4.3 Agent proposal
1. User message → API agent gateway builds context (project, phase, profiles, run outputs — **never raw rows unless the user allows**).
2. LLM returns text + **tool calls** restricted to the command allow-list.
3. Gateway converts each tool call into a `proposal` record (pending) → UI shows Approve/Edit/Reject.
4. On approve → command executes as the user → audit log entry.
5. Before display, the **grounding check** verifies every number in AI text matches a value in referenced run outputs (tolerance by display precision); unmatched numbers are blocked and flagged.

## 5. Data storage strategy

| Data | Store | Why |
|---|---|---|
| Users, workspaces, projects, tasks, OKRs, KPIs, runs metadata, proposals, audit | PostgreSQL tables | Relational integrity |
| Plugin manifests, run outputs, chart specs, profiles | PostgreSQL JSONB (+ GIN where queried) | Flexible schemas, versioned |
| Original uploads | Object storage, content-addressed (sha256), write-once | Immutability, dedup |
| Working dataset versions | Parquet in object storage | Columnar, fast, typed |
| Profiling / filtering queries | DuckDB over Parquet (in worker) | Fast analytics without loading everything |
| Job queue | Procrastinate tables in PostgreSQL | No extra broker; atomic with run row |

## 6. Security model

- **AuthN:** OIDC (Keycloak) from Phase 10; before that, a single dev user with the same token interface.
- **AuthZ:** every query filtered by `workspace_id`; PostgreSQL Row-Level Security enabled from Phase 10; role model (owner, editor, viewer, mentor) present in schema from Phase 1.
- **Uploads:** size, extension + magic-byte check, CSV injection-safe exports (prefix `=+-@`), PDF parsed in worker only.
- **Worker isolation:** non-root, read-only FS, resource limits, no egress; plugins are trusted built-ins only.
- **Secrets:** env vars / Docker secrets; BYOK keys envelope-encrypted (AES-GCM data key wrapped by master key/KMS); decrypted only in the API agent gateway at call time; never logged or sent to the browser.
- **AI data minimisation:** send schema, profiles and computed outputs by default; raw rows only with explicit per-project consent; Ollama for "nothing leaves my machine/server".
- **Audit:** append-only `audit_event` table for approvals, transformations, exports, provider calls (metadata only).
- **Privacy:** retention settings per workspace, hard delete on request, data residency choice at SaaS phase (India / EU / US region).

## 7. Observability

- Structured JSON logs (no dataset content), request ids propagated to worker.
- Metrics: run durations, failure rate per plugin, AI tokens and cost per workspace, queue depth.
- Error tracking (Sentry-compatible, self-hosted GlitchTip option).

## 8. Deployment path

| Stage | Where | How |
|---|---|---|
| Dev | Laptop | `docker compose up` (web, api, worker, db, s3, optional ollama) |
| Pilot | Single VM (e.g., 4 vCPU / 16 GB, India region) | Compose + Caddy TLS + nightly pg_dump to object storage |
| Scale | Managed Postgres + container platform | Separate worker pool autoscaled on queue depth |
| Desktop (Phase 12) | Tauri shell | Bundles web build + local engine (Python sidecar) + SQLite/DuckDB; same plugins |

## 9. Performance budgets (MVP)

- Upload + profile of 10 MB CSV: < 10 s p95.
- Standard plugin run (≤100k rows): < 5 s p95.
- IDE shell initial load: < 2.5 s on broadband; interactions < 100 ms.
- Agent first token: < 3 s (cloud providers).
