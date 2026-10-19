> **Reference spec (18 Oct 2026).** Subordinate to `docs/StatForge_Development_Guidelines_v1.1.md` and `docs/StatForge_Gate_Map_v1.0.md`. Where this file mentions pricing tiers, managed AI credits, a 13-phase roadmap or Keycloak-first auth, the guidelines v1.1 decisions win.

# 05 · Data Model

Solo-first, team-ready: every row belongs to a `workspace`; `organization` and `membership` exist from day one even if each workspace has one member.

## 1. Entity map

```
organization 1─* workspace 1─* project 1─* phase 1─* tollgate_review
     │              │            │  └─* task (Kanban card) *─1 board_column
     │              │            ├─* dataset 1─* dataset_version 1─* transformation
     │              │            ├─* analysis_run *─1 plugin_version
     │              │            ├─* kpi 1─* kpi_value  (source: analysis_run.metric)
     │              │            ├─* note / file
     │              │            └─* objective 1─* key_result ─(optional)→ kpi
     │              └─* agent_session 1─* agent_message 1─* proposal
user *─* membership(role) ─* workspace
user 1─* personal_objective 1─* key_result (learning)
user 1─* skill_evidence *─1 skill
audit_event (append-only, references any entity)
plugin 1─* plugin_version (manifest JSONB, checksum)
ai_credential (encrypted BYOK) *─1 workspace
```

## 2. Core tables (key columns)

| Table | Key columns | Notes |
|---|---|---|
| `organization` | id, name, plan, region | One per paying customer/team |
| `user` | id, email, display_name, locale, idp_subject | |
| `membership` | user_id, workspace_id, role (`owner`/`editor`/`viewer`/`mentor`) | |
| `workspace` | id, organization_id, name, settings JSONB, data_retention_days | |
| `project` | id, workspace_id, name, template_id (`dmaic`/`pdca`/`8d`/`a3`/`blank`), status, current_phase, charter JSONB, started_at, target_end | |
| `phase` | id, project_id, key (`define`…), order, status, entered_at, closed_at | Generated from template |
| `tollgate_review` | id, phase_id, checklist JSONB, evidence_refs JSONB, coach_review JSONB, decision (`pass`/`rework`), decided_by, decided_at | |
| `board_column` | id, project_id, name, order, wip_limit, phase_key nullable | |
| `task` | id, project_id, column_id, title, description, assignee_id, due_date, priority, phase_key, links JSONB (runs, datasets), order | Kanban card & to-do |
| `dataset` | id, project_id, name, source_reader, original_object_key, original_sha256, size_bytes | Original immutable |
| `dataset_version` | id, dataset_id, number, parent_version_id, parquet_object_key, schema JSONB (columns, confirmed types, roles), profile JSONB, row_count | |
| `transformation` | id, dataset_version_id, kind, params JSONB, rows_affected, evidence JSONB, approved_by, approved_at, proposal_id nullable | Every change recorded |
| `plugin` / `plugin_version` | id, kind; version, manifest JSONB, checksum, status | |
| `analysis_run` | id, project_id, phase_key, plugin_version_id, dataset_version_id, inputs JSONB, status, output JSONB, metrics JSONB, warnings JSONB, provenance JSONB, started_at, finished_at, created_by, proposal_id nullable | |
| `kpi` | id, project_id, name, unit, direction (`up`/`down`), baseline, target, source_type (`run_metric`/`manual`), source_ref JSONB | |
| `kpi_value` | id, kpi_id, value, as_of, run_id nullable | |
| `objective` | id, owner_type (`project`/`user`/`team`), owner_id, title, period, status, parent_objective_id nullable | Parent enables cascade later |
| `key_result` | id, objective_id, title, metric_type, baseline, target, current, kpi_id nullable, skill_id nullable, confidence, updated_at | KR can bind to a KPI (project) or a skill (learning) |
| `skill` | id, key (`hypothesis.paired_t`), name, belt_level, category | |
| `skill_evidence` | id, user_id, skill_id, run_id, quality (assumptions checked, interpretation confirmed), earned_at | Feeds learning KRs |
| `agent_session` / `agent_message` | session: workspace, project, provider, mode; message: role, content, grounding JSONB, tokens, cost | |
| `proposal` | id, session_id, command, args JSONB, risk_class, rationale, status (`pending`/`approved`/`edited`/`rejected`/`executed`/`failed`), decided_by, decided_at, result_ref | |
| `ai_credential` | id, workspace_id, provider, key_ciphertext, data_key_wrapped, kms_key_id, last4, created_by | Never returned to client |
| `audit_event` | id, workspace_id, actor_id, actor_type (`user`/`agent`/`system`), action, entity_type, entity_id, details JSONB, at | Append-only |

## 3. Key rules

- `dataset.original_*` is write-once; deleting a project soft-deletes, then hard-deletes after retention.
- `analysis_run.metrics` is the **only** source for KPI values and AI-quoted numbers.
- KR progress = (current − baseline) / (target − baseline), clamped; computed, not typed, when bound to a KPI.
- Personal learning KRs bind to skills: e.g., "Demonstrate 3 SPC skills" → count of distinct `skill_evidence` in category `spc`.
- All timestamps UTC; display in user locale (Asia/Kolkata default for India).

## 4. Template definition (DMAIC excerpt)

```json
{
  "id": "template.dmaic",
  "phases": [
    {"key": "define",  "deliverables": ["charter", "sipoc", "project_okr"], "tollgate": ["Problem statement is measurable", "Sponsor identified", "Scope in/out agreed"]},
    {"key": "measure", "deliverables": ["dataset", "data_quality_review", "baseline_capability"], "tollgate": ["Data quality issues resolved or accepted", "Baseline KPI recorded"]},
    {"key": "analyze", "deliverables": ["root_cause", "hypothesis_test_or_regression"], "tollgate": ["Root causes verified with data"]},
    {"key": "improve", "deliverables": ["action_plan", "pilot_comparison"], "tollgate": ["Improvement statistically and practically significant"]},
    {"key": "control", "deliverables": ["control_chart", "control_plan"], "tollgate": ["Process stable", "Owner handover"]}
  ],
  "defaultColumns": ["Backlog", "To do", "In progress", "Review", "Done"]
}
```
