---
name: workflow:init
description: Initialiser un run workflow Legal-FR depuis un playbook V2.
argument-hint: "[playbook|run-id] [--full optionnel]"
allowed-tools: Read, Write, Glob, Task
---

# workflow:init

## Runtime Skills

- `legal-fr-runtime`
- `workflow-playbooks`
- `source-ledger`
- `review-queue`

## Scope

This command operates the native Legal-FR workflow layer for Claude Desktop/Cowork plugins. It consumes Playbook V2 files from `plugins/vertical-plugins/legal-fr/playbooks/workflows/` and writes schema-backed workflow state before any Markdown deliverable.

## Schemas

- `plugins/vertical-plugins/legal-fr/schemas/common/workflow-run.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/source-ledger.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/review-queue.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/audit-trail.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/human-validation.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/workflows/<playbook_id>/run.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/workflows/<playbook_id>/deliverables.schema.json`

## Workflow

1. Load the selected Playbook V2 and verify `schema_version`, `playbook_id`, stable ids and required quality gates.
2. Create or read the `workflow-run` state, then append an audit trail entry for every material transition.
3. Update the source-ledger for each finding with source status, checked tool, excerpt, confidence and source gaps.
4. Update the review-queue for missing documents, low confidence, source gaps, schema errors and human validation decisions.
5. Apply the quality gate before moving to the next stage or before export.
6. Every generated deliverable includes `DRAFT - Validation professionnelle requise`.


## Stop Conditions

Stop and return blocking issues when intake is incomplete, a required document is missing, a critical official source cannot be found, confidence is too low, a schema is invalid, a quality gate fails, or human review rejects a finding.

## Local Runner

Use the local runner for executable state transitions:

```bash
python scripts/legal_fr_workflow.py init --help
```

The runner validates `workflow-run.json`, `source-ledger.json`, `review-queue.json`, `audit-trail.json` and exported deliverables against the local Legal-FR schemas before each transition.

## Output Contract

Return a short operational summary plus paths to JSON state, source-ledger, review-queue, audit trail and draft deliverables. Do not produce client-ready wording unless the playbook state records professional validation.
