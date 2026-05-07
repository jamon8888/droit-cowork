# Legal-FR Workflow Runner Production Grade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn Legal-FR workflow playbooks into a deterministic local workflow runner with schema-backed state, fail-closed quality gates, and Cowork-compatible command documentation.

**Architecture:** Keep the Claude Desktop/Cowork plugin structure as the source of product behavior, then add a thin local runner under `scripts/` to materialize workflow state. The runner reads Playbook V2 files from `plugins/vertical-plugins/legal-fr/playbooks/workflows/`, writes JSON state files, validates them against local schemas, and never calls external networks.

**Tech Stack:** Python standard library, unittest, generated Claude plugin markdown, JSON Schema-like local validation, existing Legal-FR generator.

---

## File Structure

- Modify: `scripts/generate_legal_fr_scaffold.py`
  - Source of truth for generated Legal-FR commands, skills, playbooks, schemas and docs.
- Create: `scripts/legal_fr_workflow.py`
  - Local CLI runner for `init`, `run`, `review`, `export`, and `eval`.
- Modify: `tests/test_legal_fr_scaffold.py`
  - Ensures generated workflow commands, skills and playbooks exist.
- Modify: `tests/test_legal_fr_production_grade.py`
  - Ensures schemas, command bindings and runner documentation are present.
- Create: `tests/test_legal_fr_workflow_runner.py`
  - Exercises the runner as a CLI and checks fail-closed behavior.
- Generated: `plugins/vertical-plugins/legal-fr/commands/workflow/*.md`
  - Cowork command layer for workflow operations.
- Generated: `plugins/vertical-plugins/legal-fr/playbooks/workflows/*.md`
  - Playbook V2 workflow contracts.
- Generated: `plugins/vertical-plugins/legal-fr/schemas/common/*.schema.json`
  - Shared workflow state, source ledger and review queue schemas.
- Generated: `plugins/vertical-plugins/legal-fr/schemas/workflows/workflow-*/`
  - Per-workflow run and deliverables schemas.
- Generated: `plugins/vertical-plugins/legal-fr/skills/{legal-fr-runtime,workflow-playbooks,source-ledger,review-queue}/SKILL.md`
  - Runtime and workflow-control skills.
- Generated: `plugins/agent-plugins/*/skills/{legal-fr-runtime,workflow-playbooks,source-ledger,review-queue}/SKILL.md`
  - Bundled agent skill copies for self-contained agent plugins.

## Current Status Snapshot

This plan is written after the first implementation pass because the initial work continued from approved inline prompts. Treat these tasks as the canonical plan for review, stabilization and future continuation.

Verified current commands:

```powershell
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures tests.test_legal_fr_clean_repo tests.test_legal_fr_workflow_design_spec tests.test_legal_fr_workflow_runner -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
python scripts/check_legal_fr_parallel_task_api.py
python -m py_compile scripts/legal_fr_workflow.py
git diff --check
```

Known environment gaps:

```text
OPENLEGI_TOKEN is not set locally; connector config still validates with warning.
parallel-cli is not installed or not on PATH; Parallel CLI runtime remains unavailable locally.
```

---

### Task 1: Lock Workflow Layer Requirements With Tests

**Files:**
- Modify: `tests/test_legal_fr_scaffold.py`
- Modify: `tests/test_legal_fr_production_grade.py`
- Create: `tests/test_legal_fr_workflow_design_spec.py`

- [ ] **Step 1: Add scaffold expectations for workflow commands, skills and playbooks**

Add the workflow family to `EXPECTED_COMMANDS` in `tests/test_legal_fr_scaffold.py`:

```python
EXPECTED_COMMANDS["workflow"] = ["init", "run", "review", "export", "eval"]
```

Add workflow playbooks to `EXPECTED_PLAYBOOKS`:

```python
EXPECTED_PLAYBOOKS.extend(
    [
        "workflows/workflow-dd-ma.md",
        "workflows/workflow-audit-rh.md",
        "workflows/workflow-preparation-audience.md",
        "workflows/workflow-audit-baux.md",
        "workflows/workflow-conformite-fournisseurs.md",
        "workflows/workflow-recherche-source-first.md",
    ]
)
```

Add shared workflow skills to `EXPECTED_SKILLS`:

```python
for skill in ["legal-fr-runtime", "workflow-playbooks", "source-ledger", "review-queue"]:
    self.assertTrue((VERTICAL / "skills" / skill / "SKILL.md").is_file())
```

- [ ] **Step 2: Add production-grade tests for runtime-backed rules**

In `tests/test_legal_fr_production_grade.py`, assert:

```python
runtime_skill = LEGAL_FR / "skills" / "legal-fr-runtime" / "SKILL.md"
self.assertTrue(runtime_skill.is_file())
runtime_text = runtime_skill.read_text(encoding="utf-8")
self.assertIn("OpenLegi avant Exa", runtime_text)
self.assertIn("DRAFT - Validation professionnelle requise", runtime_text)
```

- [ ] **Step 3: Add spec tests for Superpowers design findings**

Create `tests/test_legal_fr_workflow_design_spec.py` with checks for:

```python
self.assertIn("schema_version", text)
self.assertIn("playbook_id", text)
self.assertIn("execute exactly one next workflow stage by default", text)
self.assertNotIn("## Open Questions", text)
self.assertNotIn("...", architecture_block)
```

- [ ] **Step 4: Run tests and verify RED**

Run:

```powershell
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_workflow_design_spec -v
```

Expected before implementation:

```text
FAILED
```

The expected failures are missing workflow commands, missing workflow skills, missing workflow playbooks, missing schemas, or missing design-spec guarantees.

- [ ] **Step 5: Commit test lock**

```powershell
git add tests/test_legal_fr_scaffold.py tests/test_legal_fr_production_grade.py tests/test_legal_fr_workflow_design_spec.py
git commit -m "test: lock legal fr workflow layer requirements"
```

---

### Task 2: Generate Workflow Skills, Commands, Playbooks And Schemas

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Generated: `plugins/vertical-plugins/legal-fr/commands/workflow/*.md`
- Generated: `plugins/vertical-plugins/legal-fr/playbooks/workflows/*.md`
- Generated: `plugins/vertical-plugins/legal-fr/schemas/common/*.schema.json`
- Generated: `plugins/vertical-plugins/legal-fr/schemas/workflows/workflow-*/*.schema.json`
- Generated: `plugins/vertical-plugins/legal-fr/skills/*/SKILL.md`
- Generated: `plugins/agent-plugins/*/skills/*/SKILL.md`

- [ ] **Step 1: Add shared workflow skills to the generator**

In `scripts/generate_legal_fr_scaffold.py`, add:

```python
SHARED_WORKFLOW_SKILLS = ["legal-fr-runtime", "workflow-playbooks", "source-ledger", "review-queue"]

for meta in WORKFLOWS.values():
    meta["skills"] = [*SHARED_WORKFLOW_SKILLS, *meta["skills"]]
```

- [ ] **Step 2: Add workflow commands to the generator**

Add:

```python
"workflow": {
    "init": "Initialiser un run workflow Legal-FR depuis un playbook V2.",
    "run": "Executer la prochaine etape d'un workflow Legal-FR ou un full-run explicite.",
    "review": "Ouvrir et traiter la file de validation humaine du workflow.",
    "export": "Exporter les livrables valides, tableaux et audit trail.",
    "eval": "Evaluer un workflow contre fixtures, schemas et gates metier.",
}
```

Ensure `workflow:run` contains:

```text
execute exactly one next workflow stage by default
--full
stop
DRAFT - Validation professionnelle requise
python scripts/legal_fr_workflow.py
```

- [ ] **Step 3: Add Playbook V2 workflow packs**

Generate six playbooks:

```python
WORKFLOW_PACKS = {
    "workflow-dd-ma": {"primary_agent": "tabular-due-diligence"},
    "workflow-audit-rh": {"primary_agent": "revue-contrats-travail"},
    "workflow-preparation-audience": {"primary_agent": "chronologie-contentieux"},
    "workflow-audit-baux": {"primary_agent": "red-flags-bail"},
    "workflow-conformite-fournisseurs": {"primary_agent": "analyse-contrats-fournisseurs"},
    "workflow-recherche-source-first": {"primary_agent": "recherche-juridique-fr-avancee"},
}
```

Each generated playbook must include:

```text
schema_version: 2.0.0
playbook_id: workflow-dd-ma
## Intake
## Documents Requis
## Sources Autorisees
## Agents Et Skills
## Etapes Workflow
## Tableau Principal
## Red Flags
## Quality Gates
## Livrables
## Validation Humaine
```

- [ ] **Step 4: Add common workflow schemas**

Generate:

```text
plugins/vertical-plugins/legal-fr/schemas/common/workflow-run.schema.json
plugins/vertical-plugins/legal-fr/schemas/common/source-ledger.schema.json
plugins/vertical-plugins/legal-fr/schemas/common/review-queue.schema.json
```

`workflow-run.schema.json` must require:

```json
[
  "run_id",
  "schema_version",
  "playbook_id",
  "status",
  "current_stage",
  "full_run_requested",
  "intake",
  "document_inventory",
  "audit_trail",
  "quality_gate_status",
  "failure_state",
  "blocked_reason",
  "remediation_required"
]
```

- [ ] **Step 5: Generate files**

Run:

```powershell
python scripts/generate_legal_fr_scaffold.py
```

Expected:

```text
generated legal-fr vertical, production-grade layer and 9 Legal-FR agent plugins
```

- [ ] **Step 6: Run tests and verify GREEN**

Run:

```powershell
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_workflow_design_spec -v
```

Expected:

```text
OK
```

- [ ] **Step 7: Commit generated workflow layer**

```powershell
git add scripts/generate_legal_fr_scaffold.py plugins/vertical-plugins/legal-fr plugins/agent-plugins tests/test_legal_fr_scaffold.py tests/test_legal_fr_production_grade.py tests/test_legal_fr_workflow_design_spec.py
git commit -m "feat: add legal fr workflow layer"
```

---

### Task 3: Add Local Workflow Runner CLI

**Files:**
- Create: `scripts/legal_fr_workflow.py`
- Create: `tests/test_legal_fr_workflow_runner.py`
- Modify: `tests/test_legal_fr_production_grade.py`
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Generated: `plugins/vertical-plugins/legal-fr/README.md`
- Generated: `plugins/vertical-plugins/legal-fr/commands/workflow/*.md`

- [ ] **Step 1: Write failing CLI tests**

Create `tests/test_legal_fr_workflow_runner.py`:

```python
def test_init_creates_schema_backed_workflow_state(self) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        result = run_cli(
            "init",
            "--playbook",
            "workflow-dd-ma",
            "--matter",
            "Acquisition PME industrielle",
            "--objective",
            "Audit vendeur",
            "--document",
            "data-room/contrats/MSA-A.md",
            "--workdir",
            tmp,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        response = json.loads(result.stdout)
        state = json.loads((Path(response["run_dir"]) / "workflow-run.json").read_text(encoding="utf-8"))
        self.assertEqual(state["schema_version"], "2.0.0")
        self.assertEqual(state["playbook_id"], "workflow-dd-ma")
```

- [ ] **Step 2: Verify RED**

Run:

```powershell
python -m unittest tests.test_legal_fr_workflow_runner -v
```

Expected before runner exists:

```text
can't open file
FAILED
```

- [ ] **Step 3: Implement CLI skeleton**

Create `scripts/legal_fr_workflow.py` with:

```python
def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subcommands = root.add_subparsers(dest="command", required=True)
    init = subcommands.add_parser("init")
    init.add_argument("--playbook", required=True)
    init.add_argument("--matter", required=True)
    init.add_argument("--objective", required=True)
    init.add_argument("--document", action="append")
    init.add_argument("--workdir", required=True)
    init.set_defaults(func=command_init)
    return root
```

- [ ] **Step 4: Implement run state files**

`command_init` must write:

```text
workflow-run.json
source-ledger.json
review-queue.json
audit-trail.json
```

State payload must include:

```python
state = {
    "run_id": run_id,
    "schema_version": "2.0.0",
    "playbook_id": args.playbook,
    "status": "initialized",
    "current_stage": "intake",
    "full_run_requested": False,
    "intake": {"matter": args.matter, "objective": args.objective, "draft_notice": DRAFT_NOTICE},
    "document_inventory": documents,
    "audit_trail": audit_trail,
    "quality_gate_status": "passed",
    "failure_state": "none",
    "blocked_reason": "",
    "remediation_required": False,
}
```

- [ ] **Step 5: Implement stage transitions**

`run` must advance one stage by default:

```python
if stage == "intake":
    state["current_stage"] = "extract"
    state["status"] = "running"
    return True
```

`run --full` must stop at human review:

```python
if stage == "risk":
    state["current_stage"] = "review"
    state["status"] = "blocked"
    state["failure_state"] = "blocked_until_validated"
    state["remediation_required"] = True
    review_queue.append(review_item(...))
    return False
```

- [ ] **Step 6: Implement review and export**

`review --validate` must set queue items to `validated`.

`export` must refuse unvalidated state:

```python
if state["status"] != "validated":
    state["status"] = "blocked"
    state["failure_state"] = "blocked_until_validated"
    state["blocked_reason"] = "Export requires validated workflow state."
    return 0
```

- [ ] **Step 7: Implement runner eval**

`python scripts/legal_fr_workflow.py eval` must return:

```json
{
  "status": "ok",
  "playbooks_checked": 6,
  "playbooks": [
    "workflow-audit-baux",
    "workflow-audit-rh",
    "workflow-conformite-fournisseurs",
    "workflow-dd-ma",
    "workflow-preparation-audience",
    "workflow-recherche-source-first"
  ]
}
```

- [ ] **Step 8: Bind runner into generated docs and commands**

Update generator so `README.md` and each `commands/workflow/*.md` include:

```text
python scripts/legal_fr_workflow.py
workflow-run.json
source-ledger.json
review-queue.json
```

- [ ] **Step 9: Verify GREEN**

Run:

```powershell
python -m unittest tests.test_legal_fr_workflow_runner tests.test_legal_fr_production_grade.LegalFrProductionGradeTest.test_workflow_runner_is_documented_and_bound_to_commands -v
```

Expected:

```text
OK
```

- [ ] **Step 10: Commit runner**

```powershell
git add scripts/legal_fr_workflow.py tests/test_legal_fr_workflow_runner.py tests/test_legal_fr_production_grade.py scripts/generate_legal_fr_scaffold.py plugins/vertical-plugins/legal-fr
git commit -m "feat: add legal fr workflow runner"
```

---

### Task 4: Add Fail-Closed Schema Validation

**Files:**
- Modify: `scripts/legal_fr_workflow.py`
- Modify: `tests/test_legal_fr_workflow_runner.py`
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Generated: `plugins/vertical-plugins/legal-fr/README.md`
- Generated: `plugins/vertical-plugins/legal-fr/commands/workflow/*.md`

- [ ] **Step 1: Write failing corruption tests**

Add:

```python
def test_run_rejects_corrupted_workflow_state_before_transition(self) -> None:
    state = json.loads(state_path.read_text(encoding="utf-8"))
    del state["playbook_id"]
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    result = run_cli("run", "--run-dir", str(run_dir))
    self.assertEqual(result.returncode, 1)
    self.assertIn("workflow-run.schema.json", result.stderr)
    self.assertIn("playbook_id", result.stderr)
```

Add:

```python
def test_export_rejects_corrupted_review_queue_schema(self) -> None:
    queue[0]["status"] = "approved-but-not-schema-valid"
    queue_path.write_text(json.dumps(queue, indent=2) + "\n", encoding="utf-8")
    result = run_cli("export", "--run-dir", str(run_dir))
    self.assertEqual(result.returncode, 1)
    self.assertIn("review-queue.schema.json", result.stderr)
```

- [ ] **Step 2: Verify RED**

Run:

```powershell
python -m unittest tests.test_legal_fr_workflow_runner -v
```

Expected before validation:

```text
FAILED
```

Expected failure reasons:

```text
KeyError raw error for missing playbook_id
corrupted review queue still exports or blocks without schema error
```

- [ ] **Step 3: Implement minimal schema validator**

Add:

```python
class SchemaValidationError(ValueError):
    """Raised when local Legal-FR workflow JSON does not match its schema."""
```

Add:

```python
def validate_common_payload(schema_name: str, payload: Any) -> None:
    schema_path = COMMON_SCHEMA_ROOT / schema_name
    validate_against_schema(payload, load_schema(schema_path), schema_path)
```

Support:

```text
required
additionalProperties: false
type
enum
const
$ref
array items
object properties
```

- [ ] **Step 4: Validate state on load and save**

Modify `load_run`:

```python
validate_run_payloads(state, source_ledger, review_queue, audit_trail)
```

Modify `save_run`:

```python
state["audit_trail"] = audit_trail
validate_run_payloads(state, source_ledger, review_queue, audit_trail)
```

- [ ] **Step 5: Validate deliverables before export**

Add:

```python
validate_pack_payload(state["playbook_id"], "deliverables.schema.json", deliverables)
```

before writing `deliverables.json`.

- [ ] **Step 6: Verify GREEN**

Run:

```powershell
python -m unittest tests.test_legal_fr_workflow_runner -v
```

Expected:

```text
OK
```

- [ ] **Step 7: Add docs through generator**

Add to generated workflow command docs:

```text
The runner validates workflow-run.json, source-ledger.json, review-queue.json, audit-trail.json and exported deliverables against the local Legal-FR schemas before each transition.
```

Add to README:

```text
The runner validates each state file against local schemas before transitions, so corrupted workflow-run.json, source-ledger.json, review-queue.json or audit-trail.json files fail closed.
```

- [ ] **Step 8: Regenerate**

Run:

```powershell
python scripts/generate_legal_fr_scaffold.py
```

Expected:

```text
generated legal-fr vertical, production-grade layer and 9 Legal-FR agent plugins
```

- [ ] **Step 9: Commit fail-closed validation**

```powershell
git add scripts/legal_fr_workflow.py tests/test_legal_fr_workflow_runner.py scripts/generate_legal_fr_scaffold.py plugins/vertical-plugins/legal-fr
git commit -m "fix: fail closed on corrupted legal fr workflow state"
```

---

### Task 5: Run Full Verification Suite

**Files:**
- Read: all Legal-FR generated plugin files
- Read: all Legal-FR tests and scripts

- [ ] **Step 1: Run scaffold check**

```powershell
python scripts/check.py
```

Expected:

```text
OK - 20 file(s) checked, 0 issues.
```

- [ ] **Step 2: Run full unittest suite**

```powershell
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures tests.test_legal_fr_clean_repo tests.test_legal_fr_workflow_design_spec tests.test_legal_fr_workflow_runner -v
```

Expected:

```text
Ran 40 tests
OK
```

- [ ] **Step 3: Run eval fixtures**

```powershell
python scripts/run_legal_fr_evals.py
```

Expected:

```text
Legal-FR evals passed: 45 expected outputs checked
```

- [ ] **Step 4: Run connector checks**

```powershell
python scripts/check_legal_fr_connectors.py
```

Expected when `OPENLEGI_TOKEN` is absent locally:

```text
WARN: OPENLEGI_TOKEN is not set; runtime OpenLegi calls will fail until configured.
Legal-FR connector config OK
```

- [ ] **Step 5: Run Parallel Task API scaffold check**

```powershell
python scripts/check_legal_fr_parallel_task_api.py
```

Expected:

```text
Legal-FR Parallel Task API scaffold OK
```

- [ ] **Step 6: Run Parallel CLI check**

```powershell
python scripts/check_legal_fr_parallel_cli.py
```

Expected in the current local environment:

```text
ERROR: parallel-cli is not installed or not on PATH
```

This is an environment gap, not a scaffold failure.

- [ ] **Step 7: Run Python compile check**

```powershell
python -m py_compile scripts/legal_fr_workflow.py
```

Expected:

```text
```

Exit code must be 0.

- [ ] **Step 8: Run manual fail-closed probe**

```powershell
$tmp = Join-Path $env:TEMP ('legal-fr-corrupt-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tmp | Out-Null
$init = python scripts/legal_fr_workflow.py init --playbook workflow-dd-ma --matter 'Acquisition PME' --objective 'Audit acheteur' --document data-room/index.md --workdir $tmp | ConvertFrom-Json
$statePath = Join-Path $init.run_dir 'workflow-run.json'
$state = Get-Content -Raw $statePath | ConvertFrom-Json
$state.PSObject.Properties.Remove('playbook_id')
$state | ConvertTo-Json -Depth 50 | Set-Content -Encoding UTF8 $statePath
python scripts/legal_fr_workflow.py run --run-dir $init.run_dir
$code = $LASTEXITCODE
Remove-Item -LiteralPath $tmp -Recurse -Force
exit $code
```

Expected:

```text
ERROR: workflow-run.schema.json: $.playbook_id is required
```

Exit code must be 1.

- [ ] **Step 9: Run diff whitespace check**

```powershell
git diff --check
```

Expected:

```text
```

Exit code must be 0.

- [ ] **Step 10: Commit verification notes if docs changed**

If this task changes only this plan, commit only the plan:

```powershell
git add docs/superpowers/plans/2026-05-07-legal-fr-workflow-runner-production-grade.md
git commit -m "docs: add legal fr workflow runner plan"
```

---

## Self-Review

### Spec Coverage

- Runtime rules not only in plugin `CLAUDE.md`: covered by Task 2 shared skills and Task 1 production tests.
- `workflow:run` stage-by-stage default: covered by Task 2 command docs and Task 3 runner tests.
- Stable machine IDs: covered by Task 2 playbooks and Task 1 design-spec tests.
- Failure/remediation states: covered by Task 2 schemas and Task 4 fail-closed validation.
- No open questions or architecture placeholders: covered by Task 1 design-spec tests.
- Local executable layer: covered by Task 3 runner and Task 4 schema validation.
- Deterministic verification: covered by Task 5.

### Placeholder Scan

This plan uses concrete files, commands, expected outputs and code snippets. It contains no deferred implementation marker and no unspecified test instruction.

### Type Consistency

The same field names are used across tasks:

- `workflow-run.json`
- `source-ledger.json`
- `review-queue.json`
- `audit-trail.json`
- `deliverables.json`
- `schema_version`
- `playbook_id`
- `failure_state`
- `remediation_required`
- `validated_by_human`

### Execution Choice

Plan complete and saved to `docs/superpowers/plans/2026-05-07-legal-fr-workflow-runner-production-grade.md`.

Two execution options:

1. **Subagent-Driven (recommended)** - Dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints for review.
