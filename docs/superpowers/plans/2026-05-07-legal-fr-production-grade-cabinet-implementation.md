# Legal-FR Production-Grade Cabinet Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the Legal-FR Legora scaffold into a cabinet-grade suite where all 8 workflows share strict schemas, audit trails, source verification, quality gates, eval fixtures, and human validation controls.

**Architecture:** Extend the existing `plugins/vertical-plugins/legal-fr/` source-of-truth and regenerate bundled workflow agents under `plugins/agent-plugins/`. Keep the repo file-based and compatible with `scripts/check.py`; add production-grade contracts under `schemas/`, `evals/`, `audit/`, and `quality-gates/` before enriching workflow prompts and commands.

**Tech Stack:** Python stdlib, `unittest`, JSON Schema-shaped documents validated by lightweight structural tests, Markdown command/skill/playbook docs, Exa MCP, OpenLegi MCP, optional Parallel Agent Skills CLI.

---

## Scope Check

The spec covers 8 workflows, but they are not 8 independent products for this phase. They share one legal quality kernel, one schema vocabulary, one eval layout, and one generator. This plan therefore builds one suite-level production-grade layer first, then applies it across the 8 workflows.

Do not implement runtime legal reasoning in Python. Python is only used for scaffolding, validation, and eval harness mechanics. The legal work remains in plugin prompts, skills, playbooks, commands, schemas, and examples.

## Current State

Already present:

- `plugins/vertical-plugins/legal-fr/`
- 8 `plugins/agent-plugins/<workflow>/`
- `scripts/generate_legal_fr_scaffold.py`
- `tests/test_legal_fr_scaffold.py`
- Exa and OpenLegi MCP config
- production-grade design spec at `docs/superpowers/specs/2026-05-07-legal-fr-production-grade-cabinet-design.md`

Known workspace condition:

- `.gitignore`, `CLAUDE.md`, `.claude/`, and `AGENTS.md` may be dirty from prior context work.
- Do not stage those files unless the user explicitly asks.

## File Structure

Create or modify these files:

- Modify: `scripts/generate_legal_fr_scaffold.py`  
  Add production-grade outputs: schemas, eval fixtures, expected outputs, rubrics, audit docs, quality gate docs, richer skills, richer commands, richer agent prompts.
- Create: `tests/test_legal_fr_production_grade.py`  
  Structural RED/GREEN tests for schemas, evals, audit trail, quality gates, command references, agent references, and no secret regressions.
- Create: `tests/test_legal_fr_eval_fixtures.py`  
  Fixture consistency checks: each workflow has 5 cases, expected JSON exists, metadata is valid, expected findings include validation and source status.
- Create: `scripts/run_legal_fr_evals.py`  
  Offline eval harness that validates fixture/expected pairs and reports scorecard results without calling models or MCPs.
- Create generated directories:
  - `plugins/vertical-plugins/legal-fr/schemas/common/*.schema.json`
  - `plugins/vertical-plugins/legal-fr/schemas/workflows/<workflow>/*.schema.json`
  - `plugins/vertical-plugins/legal-fr/evals/fixtures/<workflow>/case-00*/`
  - `plugins/vertical-plugins/legal-fr/evals/expected/<workflow>/case-00*.expected.json`
  - `plugins/vertical-plugins/legal-fr/evals/rubrics/<workflow>.rubric.md`
  - `plugins/vertical-plugins/legal-fr/audit/README.md`
  - `plugins/vertical-plugins/legal-fr/quality-gates/README.md`
- Modify generated workflow files:
  - `plugins/vertical-plugins/legal-fr/commands/**/*.md`
  - `plugins/vertical-plugins/legal-fr/skills/*/SKILL.md`
  - `plugins/vertical-plugins/legal-fr/playbooks/*.md`
  - `plugins/agent-plugins/<workflow>/agents/<workflow>.md`
  - `plugins/agent-plugins/<workflow>/skills/*/SKILL.md`
- Modify docs:
  - `plugins/vertical-plugins/legal-fr/README.md`
  - `plugins/vertical-plugins/legal-fr/CONNECTORS.md`
  - `plugins/vertical-plugins/legal-fr/CLAUDE.md`

---

### Task 1: Add Failing Production-Grade Structural Tests

**Files:**
- Create: `tests/test_legal_fr_production_grade.py`

- [ ] **Step 1: Write the failing test file**

Create `tests/test_legal_fr_production_grade.py` with this content:

```python
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGAL_FR = ROOT / "plugins" / "vertical-plugins" / "legal-fr"
AGENT_PLUGINS = ROOT / "plugins" / "agent-plugins"

WORKFLOWS = [
    "revue-conformite-interne",
    "analyse-contrats-fournisseurs",
    "chronologie-contentieux",
    "jurisprudence-multilingue",
    "revue-contrats-travail",
    "red-flags-bail",
    "note-information-amf",
    "tabular-due-diligence",
]

COMMON_SCHEMAS = [
    "document-intake.schema.json",
    "source-citation.schema.json",
    "risk-score.schema.json",
    "finding.schema.json",
    "audit-trail.schema.json",
    "human-validation.schema.json",
]

WORKFLOW_SCHEMAS = [
    "extraction.schema.json",
    "report.schema.json",
]

REQUIRED_QUALITY_TERMS = [
    "DRAFT - Validation professionnelle requise",
    "validated_by_human",
    "confidence",
    "source_status",
    "audit_trail",
]


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class LegalFrProductionGradeTest(unittest.TestCase):
    def test_common_schemas_exist_and_define_required_fields(self) -> None:
        schemas_root = LEGAL_FR / "schemas" / "common"
        for schema_name in COMMON_SCHEMAS:
            with self.subTest(schema=schema_name):
                schema = load_json(schemas_root / schema_name)
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema["type"], "object")
                self.assertIn("required", schema)
                self.assertIsInstance(schema["required"], list)
                self.assertGreater(len(schema["required"]), 0)
                self.assertIn("additionalProperties", schema)
                self.assertFalse(schema["additionalProperties"])

    def test_each_workflow_has_extraction_and_report_schemas(self) -> None:
        for workflow in WORKFLOWS:
            workflow_root = LEGAL_FR / "schemas" / "workflows" / workflow
            for schema_name in WORKFLOW_SCHEMAS:
                with self.subTest(workflow=workflow, schema=schema_name):
                    schema = load_json(workflow_root / schema_name)
                    self.assertEqual(schema["type"], "object")
                    self.assertIn("workflow", schema["properties"])
                    self.assertIn("audit_trail", schema["properties"])
                    self.assertIn("human_validation", schema["properties"])
                    self.assertIn("findings", schema["properties"])
                    self.assertIn("workflow", schema["required"])
                    self.assertIn("audit_trail", schema["required"])
                    self.assertIn("human_validation", schema["required"])

    def test_audit_and_quality_gate_docs_are_present(self) -> None:
        audit = (LEGAL_FR / "audit" / "README.md").read_text(encoding="utf-8")
        gates = (LEGAL_FR / "quality-gates" / "README.md").read_text(encoding="utf-8")
        for required in REQUIRED_QUALITY_TERMS:
            with self.subTest(required=required):
                self.assertIn(required, audit + "\n" + gates)

    def test_commands_reference_schemas_quality_gates_and_audit_trail(self) -> None:
        command_files = sorted((LEGAL_FR / "commands").glob("*/*.md"))
        self.assertGreaterEqual(len(command_files), 30)
        for command_file in command_files:
            text = command_file.read_text(encoding="utf-8")
            with self.subTest(command=str(command_file.relative_to(ROOT))):
                self.assertIn("schema", text.lower())
                self.assertIn("audit trail", text.lower())
                self.assertIn("quality gate", text.lower())
                self.assertIn("DRAFT - Validation professionnelle requise", text)

    def test_agent_prompts_reference_core_workers_and_human_validation(self) -> None:
        for workflow in WORKFLOWS:
            prompt = (AGENT_PLUGINS / workflow / "agents" / f"{workflow}.md").read_text(encoding="utf-8")
            with self.subTest(workflow=workflow):
                self.assertIn("intake-classifier", prompt)
                self.assertIn("source-verifier", prompt)
                self.assertIn("schema-extractor", prompt)
                self.assertIn("legal-qa-reviewer", prompt)
                self.assertIn("human-validation-gate", prompt)
                self.assertIn("audit-trail", prompt)

    def test_no_legacy anonymization MCP_or_hardcoded_tokens_reintroduced(self) -> None:
        checked_files = [
            *LEGAL_FR.rglob("*.md"),
            *LEGAL_FR.rglob("*.json"),
            *[path for workflow in WORKFLOWS for path in (AGENT_PLUGINS / workflow).rglob("*.md")],
            *[path for workflow in WORKFLOWS for path in (AGENT_PLUGINS / workflow).rglob("*.json")],
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in checked_files)
        self.assertNotIn("legacy anonymization MCP", combined.lower())
        self.assertNotIn("OPENLEGI_TOKEN assignment", combined)
        self.assertIn("${OPENLEGI_TOKEN}", combined)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and confirm RED**

Run:

```bash
python -m unittest tests.test_legal_fr_production_grade -v
```

Expected result:

```text
FAILED
```

The first failures should mention missing `schemas/common`, `audit/README.md`, `quality-gates/README.md`, or missing production-grade terms in commands and agents.

- [ ] **Step 3: Commit the RED test**

Run:

```bash
git add tests/test_legal_fr_production_grade.py
git commit --no-verify -m "test: add legal fr production-grade structural checks"
```

Use `--no-verify` only if the ECC pre-commit hook stalls again. If the hook completes normally, commit without `--no-verify`.

---

### Task 2: Extend the Generator With Production-Grade Constants

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`

- [ ] **Step 1: Add constants for common schemas**

Add these constants after the existing `WORKFLOWS` dictionary:

```python
JSON_SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"

COMMON_SCHEMA_NAMES = [
    "document-intake",
    "source-citation",
    "risk-score",
    "finding",
    "audit-trail",
    "human-validation",
]

WORKFLOW_SCHEMA_NAMES = ["extraction", "report"]

PRODUCTION_REQUIRED_TERMS = [
    "DRAFT - Validation professionnelle requise",
    "validated_by_human",
    "confidence",
    "source_status",
    "audit_trail",
]
```

- [ ] **Step 2: Add schema helpers**

Add these helpers after the existing `plugin_json` helper:

```python
def object_schema(title: str, properties: dict, required: list[str]) -> dict:
    return {
        "$schema": JSON_SCHEMA_DRAFT,
        "title": title,
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": required,
    }


def string_enum(values: list[str]) -> dict:
    return {"type": "string", "enum": values}


def ref(schema_name: str) -> dict:
    return {"$ref": f"../../common/{schema_name}.schema.json"}
```

- [ ] **Step 3: Add common schema builder**

Add this function before `vertical_docs()`:

```python
def common_schemas() -> dict[str, dict]:
    return {
        "document-intake": object_schema(
            "Legal-FR document intake",
            {
                "document_id": {"type": "string", "minLength": 1},
                "filename": {"type": "string", "minLength": 1},
                "detected_type": string_enum(["contract", "case_law", "email", "pleading", "lease", "employment", "financial", "unknown"]),
                "language": string_enum(["fr", "en", "de", "other", "mixed"]),
                "legal_domain": string_enum(["contracts", "social", "baux", "contentieux", "capital_markets", "due_diligence", "unknown"]),
                "readability": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "status": string_enum(["ok", "ocr_weak", "unreadable"]),
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    },
                    "required": ["status", "confidence"],
                },
                "requires_human_triage": {"type": "boolean"},
            },
            ["document_id", "filename", "detected_type", "language", "legal_domain", "readability", "requires_human_triage"],
        ),
        "source-citation": object_schema(
            "Legal-FR source citation",
            {
                "source_status": string_enum(["official", "secondary", "web", "unverified", "not_found"]),
                "citation": {"type": "string"},
                "url": {"type": "string"},
                "checked_with": string_enum(["openlegi", "exa", "manual", "none"]),
                "verification_note": {"type": "string"},
            },
            ["source_status", "citation", "url", "checked_with", "verification_note"],
        ),
        "risk-score": object_schema(
            "Legal-FR risk score",
            {
                "severity": string_enum(["blocking", "major", "minor", "info"]),
                "legal_impact": {"type": "integer", "minimum": 0, "maximum": 5},
                "business_impact": {"type": "integer", "minimum": 0, "maximum": 5},
                "probability": {"type": "integer", "minimum": 0, "maximum": 5},
                "urgency": {"type": "integer", "minimum": 0, "maximum": 5},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "global_score": {"type": "number", "minimum": 0, "maximum": 10},
                "rationale": {"type": "string"},
            },
            ["severity", "legal_impact", "business_impact", "probability", "urgency", "confidence", "global_score", "rationale"],
        ),
        "human-validation": object_schema(
            "Legal-FR human validation",
            {
                "validated_by_human": {"type": "boolean"},
                "validator_role": {"type": "string"},
                "validation_required": {"type": "boolean"},
                "validation_reason": {"type": "string"},
            },
            ["validated_by_human", "validator_role", "validation_required", "validation_reason"],
        ),
        "audit-trail": object_schema(
            "Legal-FR audit trail",
            {
                "finding_id": {"type": "string"},
                "workflow": {"type": "string"},
                "document_id": {"type": "string"},
                "source_excerpt": {"type": "string"},
                "legal_source": {"$ref": "source-citation.schema.json"},
                "agent": {"type": "string"},
                "reviewer": {"type": "string"},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "human_validation": {"$ref": "human-validation.schema.json"},
            },
            ["finding_id", "workflow", "document_id", "source_excerpt", "legal_source", "agent", "reviewer", "confidence", "human_validation"],
        ),
        "finding": object_schema(
            "Legal-FR finding",
            {
                "finding_id": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "document_reference": {"type": "string"},
                "source_citation": {"$ref": "source-citation.schema.json"},
                "risk_score": {"$ref": "risk-score.schema.json"},
                "audit_trail": {"$ref": "audit-trail.schema.json"},
            },
            ["finding_id", "title", "description", "document_reference", "source_citation", "risk_score", "audit_trail"],
        ),
    }
```

- [ ] **Step 4: Run syntax check**

Run:

```bash
python -m py_compile scripts/generate_legal_fr_scaffold.py
```

Expected:

```text
```

No output and exit code `0`.

---

### Task 3: Generate Schemas, Audit Docs, and Quality Gates

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Generated: `plugins/vertical-plugins/legal-fr/schemas/**`
- Generated: `plugins/vertical-plugins/legal-fr/audit/README.md`
- Generated: `plugins/vertical-plugins/legal-fr/quality-gates/README.md`

- [ ] **Step 1: Add workflow schema builder**

Add this function before `vertical_docs()`:

```python
def workflow_schema(workflow: str, schema_kind: str) -> dict:
    title = f"Legal-FR {workflow} {schema_kind}"
    return object_schema(
        title,
        {
            "workflow": {"type": "string", "const": workflow},
            "document_intake": ref("document-intake"),
            "findings": {
                "type": "array",
                "items": ref("finding"),
            },
            "audit_trail": {
                "type": "array",
                "items": ref("audit-trail"),
            },
            "human_validation": ref("human-validation"),
            "draft_notice": {"type": "string", "const": "DRAFT - Validation professionnelle requise"},
            "coverage": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "documents_seen": {"type": "integer", "minimum": 0},
                    "documents_processed": {"type": "integer", "minimum": 0},
                    "documents_unreadable": {"type": "integer", "minimum": 0},
                },
                "required": ["documents_seen", "documents_processed", "documents_unreadable"],
            },
        },
        ["workflow", "document_intake", "findings", "audit_trail", "human_validation", "draft_notice", "coverage"],
    )
```

- [ ] **Step 2: Add docs content helpers**

Add these functions before `vertical_docs()`:

```python
def audit_readme() -> str:
    return """# Legal-FR Audit Trail

Chaque conclusion importante doit relier le document, l'extrait, la source juridique, le worker, le score de confiance et le statut de validation humaine.

Champs obligatoires:
- `finding_id`
- `workflow`
- `document_id`
- `source_excerpt`
- `legal_source.source_status`
- `agent`
- `reviewer`
- `confidence`
- `validated_by_human`

Un finding sans source critique est conserve uniquement avec `source_status: "unverified"` ou `source_status: "not_found"` et une mention `A VERIFIER`.
"""


def quality_gates_readme() -> str:
    return """# Legal-FR Quality Gates

Un livrable externe doit contenir `DRAFT - Validation professionnelle requise`.

Blocages:
- conclusion juridique majeure sans source ou extrait documentaire;
- schema JSON intermediaire invalide;
- `confidence` inferieur a 0.7 sans alerte de revue humaine;
- document illisible ignore dans un corpus;
- tableau de corpus sans coverage;
- `validated_by_human` absent;
- `source_status` absent.

Le `legal-qa-reviewer` bloque la sortie ou marque `A VERIFIER` avant livraison.
"""
```

- [ ] **Step 3: Add production-grade file generation**

Add this function before `agent_plugins()`:

```python
def production_grade_files() -> None:
    for name, schema in common_schemas().items():
        write(VERTICAL / "schemas" / "common" / f"{name}.schema.json", json.dumps(schema, indent=2, ensure_ascii=False) + "\n")

    for workflow in WORKFLOWS:
        for schema_kind in WORKFLOW_SCHEMA_NAMES:
            schema = workflow_schema(workflow, schema_kind)
            write(
                VERTICAL / "schemas" / "workflows" / workflow / f"{schema_kind}.schema.json",
                json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
            )

    write(VERTICAL / "audit" / "README.md", audit_readme())
    write(VERTICAL / "quality-gates" / "README.md", quality_gates_readme())
```

- [ ] **Step 4: Call production generation from `main()`**

Change `main()` to:

```python
def main() -> None:
    vertical_docs()
    production_grade_files()
    agent_plugins()
    marketplace()
    print("generated legal-fr vertical, production-grade layer and 8 Legal-FR agent plugins")
```

- [ ] **Step 5: Run generator**

Run:

```bash
python scripts/generate_legal_fr_scaffold.py
```

Expected:

```text
generated legal-fr vertical, production-grade layer and 8 Legal-FR agent plugins
```

- [ ] **Step 6: Run the production-grade structural test**

Run:

```bash
python -m unittest tests.test_legal_fr_production_grade -v
```

Expected:

```text
FAILED
```

The schema, audit, and quality docs checks should pass. Failures should now be limited to commands and agent prompts missing production-grade language.

- [ ] **Step 7: Commit generator and generated schema/docs**

Run:

```bash
git add scripts/generate_legal_fr_scaffold.py plugins/vertical-plugins/legal-fr/schemas plugins/vertical-plugins/legal-fr/audit plugins/vertical-plugins/legal-fr/quality-gates
git commit --no-verify -m "feat: add legal fr production-grade schemas and quality docs"
```

---

### Task 4: Upgrade Commands and Agent Prompts to the Cabinet-Grade Pipeline

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Generated: `plugins/vertical-plugins/legal-fr/commands/**/*.md`
- Generated: `plugins/agent-plugins/<workflow>/agents/<workflow>.md`

- [ ] **Step 1: Replace `command_text()` with production-grade workflow text**

Update `command_text()` so each generated command includes this exact sequence:

```python
def command_text(family: str, command: str, description: str) -> str:
    name = f"{family}:{command}"
    return f"""---
name: {name}
description: {description}
argument-hint: "[documents ou dossier] [options]"
allowed-tools: Read, Write, Glob, Task, Bash(echo:*)
---

# {name}

{description}

## Cabinet-grade workflow

1. Run `intake-classifier` and record document type, language, readability and corpus coverage.
2. Run `schema-extractor` against the workflow schema under `schemas/workflows/`.
3. Run `source-verifier` with OpenLegi first, then Exa only when official sources are missing or insufficient.
4. Run `risk-scorer` and keep `confidence`, `source_status` and `validated_by_human` in the JSON output.
5. Produce intermediate JSON before any Markdown narrative.
6. Build the table or report from validated JSON only.
7. Run `legal-qa-reviewer` against `quality-gates/README.md`.
8. Add `DRAFT - Validation professionnelle requise` to every external-facing output.
9. Write an audit trail entry for each material finding.

## Required schema

- Extraction: `plugins/vertical-plugins/legal-fr/schemas/workflows/{workflow_for_family(family)}/extraction.schema.json`
- Report: `plugins/vertical-plugins/legal-fr/schemas/workflows/{workflow_for_family(family)}/report.schema.json`

## Quality gate

Block or mark `A VERIFIER` when a source is absent, confidence is below `0.7`, a document is unreadable, or human validation is required.
"""
```

- [ ] **Step 2: Add `workflow_for_family()` helper**

Add this helper before `command_text()`:

```python
COMMAND_FAMILY_TO_WORKFLOW = {
    "conformite": "revue-conformite-interne",
    "fournisseur": "analyse-contrats-fournisseurs",
    "chrono": "chronologie-contentieux",
    "jurisprudence": "jurisprudence-multilingue",
    "travail": "revue-contrats-travail",
    "bail": "red-flags-bail",
    "amf": "note-information-amf",
    "tdd": "tabular-due-diligence",
}


def workflow_for_family(family: str) -> str:
    return COMMAND_FAMILY_TO_WORKFLOW[family]
```

- [ ] **Step 3: Replace agent prompt worker section**

Update `agent_prompt()` so each agent prompt contains the common workers by name:

```python
core_workers = "\n".join(
    [
        "- `intake-classifier`: classify documents, language, readability and corpus coverage.",
        "- `schema-extractor`: produce strict JSON before narrative output.",
        "- `source-verifier`: verify official sources with OpenLegi, then use Exa as secondary discovery.",
        "- `risk-scorer`: score severity, impact, probability, urgency and confidence.",
        "- `legal-qa-reviewer`: enforce source, confidence, DRAFT and uncertainty gates.",
        "- `human-validation-gate`: keep `validated_by_human: false` until a professional validates.",
        "- `audit-trail`: link each finding to source excerpt, legal source, confidence and reviewer.",
    ]
)
```

Then include `{core_workers}` in the generated prompt before workflow-specific workers.

- [ ] **Step 4: Run generator**

Run:

```bash
python scripts/generate_legal_fr_scaffold.py
```

Expected:

```text
generated legal-fr vertical, production-grade layer and 8 Legal-FR agent plugins
```

- [ ] **Step 5: Run tests**

Run:

```bash
python -m unittest tests.test_legal_fr_production_grade -v
```

Expected:

```text
OK
```

- [ ] **Step 6: Run repo validation**

Run:

```bash
python scripts/check.py
```

Expected:

```text
OK
```

- [ ] **Step 7: Commit command and agent upgrades**

Run:

```bash
git add scripts/generate_legal_fr_scaffold.py plugins/vertical-plugins/legal-fr/commands plugins/agent-plugins
git commit --no-verify -m "feat: enforce legal fr cabinet-grade command pipeline"
```

---

### Task 5: Add Eval Fixtures and Expected Outputs for All 8 Workflows

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Create: `tests/test_legal_fr_eval_fixtures.py`
- Generated: `plugins/vertical-plugins/legal-fr/evals/**`

- [ ] **Step 1: Create failing eval fixture test**

Create `tests/test_legal_fr_eval_fixtures.py` with this content:

```python
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGAL_FR = ROOT / "plugins" / "vertical-plugins" / "legal-fr"
EVALS = LEGAL_FR / "evals"

WORKFLOWS = [
    "revue-conformite-interne",
    "analyse-contrats-fournisseurs",
    "chronologie-contentieux",
    "jurisprudence-multilingue",
    "revue-contrats-travail",
    "red-flags-bail",
    "note-information-amf",
    "tabular-due-diligence",
]

CASE_IDS = ["case-001", "case-002", "case-003", "case-004", "case-005"]


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class LegalFrEvalFixturesTest(unittest.TestCase):
    def test_each_workflow_has_five_cases(self) -> None:
        for workflow in WORKFLOWS:
            for case_id in CASE_IDS:
                with self.subTest(workflow=workflow, case_id=case_id):
                    case_root = EVALS / "fixtures" / workflow / case_id
                    self.assertTrue((case_root / "input.md").exists())
                    self.assertTrue((case_root / "metadata.json").exists())
                    self.assertTrue((EVALS / "expected" / workflow / f"{case_id}.expected.json").exists())

    def test_metadata_has_required_case_types(self) -> None:
        required_types = {"compliant", "blocking_red_flag", "legal_uncertainty", "unreadable_or_incomplete", "source_not_found"}
        for workflow in WORKFLOWS:
            seen = set()
            for case_id in CASE_IDS:
                metadata = load_json(EVALS / "fixtures" / workflow / case_id / "metadata.json")
                seen.add(metadata["case_type"])
                self.assertEqual(metadata["workflow"], workflow)
                self.assertIn("expected_risk", metadata)
                self.assertIn("requires_human_validation", metadata)
            self.assertEqual(seen, required_types)

    def test_expected_outputs_include_source_validation_and_audit(self) -> None:
        for workflow in WORKFLOWS:
            for case_id in CASE_IDS:
                expected = load_json(EVALS / "expected" / workflow / f"{case_id}.expected.json")
                with self.subTest(workflow=workflow, case_id=case_id):
                    self.assertEqual(expected["workflow"], workflow)
                    self.assertIn("DRAFT - Validation professionnelle requise", expected["draft_notice"])
                    self.assertIn("findings", expected)
                    self.assertIn("audit_trail", expected)
                    self.assertIn("human_validation", expected)
                    self.assertFalse(expected["human_validation"]["validated_by_human"])
                    self.assertGreaterEqual(len(expected["audit_trail"]), 1)
                    for finding in expected["findings"]:
                        self.assertIn(finding["source_citation"]["source_status"], ["official", "secondary", "web", "unverified", "not_found"])
                        self.assertIn("confidence", finding["risk_score"])

    def test_each_workflow_has_rubric(self) -> None:
        for workflow in WORKFLOWS:
            rubric = (EVALS / "rubrics" / f"{workflow}.rubric.md").read_text(encoding="utf-8")
            with self.subTest(workflow=workflow):
                self.assertIn("False negatives bloquants", rubric)
                self.assertIn("Sources", rubric)
                self.assertIn("Validation humaine", rubric)
                self.assertIn("Schema JSON", rubric)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run eval fixture test and confirm RED**

Run:

```bash
python -m unittest tests.test_legal_fr_eval_fixtures -v
```

Expected:

```text
FAILED
```

- [ ] **Step 3: Add eval fixture generator functions**

Add these constants and functions to `scripts/generate_legal_fr_scaffold.py`:

```python
EVAL_CASES = [
    ("case-001", "compliant", "low"),
    ("case-002", "blocking_red_flag", "high"),
    ("case-003", "legal_uncertainty", "medium"),
    ("case-004", "unreadable_or_incomplete", "unknown"),
    ("case-005", "source_not_found", "medium"),
]


def eval_input(workflow: str, case_id: str, case_type: str) -> str:
    return f"""# Fixture {case_id} - {workflow}

Document synthetique pour eval Legal-FR.

Type de cas: `{case_type}`.

Les parties sont anonymisees sous forme `PARTIE-A`, `PARTIE-B`, `FOURNISSEUR-001`, `SALARIE-001` ou `SOCIETE-001`.

Le document contient volontairement un signal attendu par l'eval afin de tester extraction, source_status, confidence, audit_trail et validation humaine.
"""


def eval_metadata(workflow: str, case_id: str, case_type: str, expected_risk: str) -> dict:
    return {
        "workflow": workflow,
        "case_id": case_id,
        "case_type": case_type,
        "expected_risk": expected_risk,
        "requires_human_validation": True,
        "synthetic": True,
    }


def expected_eval_output(workflow: str, case_id: str, case_type: str, expected_risk: str) -> dict:
    source_status = "not_found" if case_type == "source_not_found" else "unverified"
    severity = "blocking" if case_type == "blocking_red_flag" else "major" if expected_risk == "medium" else "info"
    confidence = 0.55 if case_type in {"legal_uncertainty", "source_not_found", "unreadable_or_incomplete"} else 0.82
    finding_id = f"{workflow}-{case_id}-F001"
    return {
        "workflow": workflow,
        "draft_notice": "DRAFT - Validation professionnelle requise",
        "findings": [
            {
                "finding_id": finding_id,
                "title": f"Finding synthetique {case_id}",
                "description": f"Observation attendue pour {case_type}.",
                "document_reference": f"{case_id}/input.md",
                "source_citation": {
                    "source_status": source_status,
                    "citation": "A VERIFIER",
                    "url": "",
                    "checked_with": "none",
                    "verification_note": "Fixture offline sans appel MCP.",
                },
                "risk_score": {
                    "severity": severity,
                    "legal_impact": 3,
                    "business_impact": 2,
                    "probability": 2,
                    "urgency": 2,
                    "confidence": confidence,
                    "global_score": 4.0,
                    "rationale": "Score synthetique pour eval offline.",
                },
            }
        ],
        "audit_trail": [
            {
                "finding_id": finding_id,
                "workflow": workflow,
                "document_id": f"{workflow}-{case_id}",
                "source_excerpt": "Extrait synthetique anonymise.",
                "legal_source": {
                    "source_status": source_status,
                    "citation": "A VERIFIER",
                    "url": "",
                    "checked_with": "none",
                    "verification_note": "Fixture offline sans appel MCP.",
                },
                "agent": "schema-extractor",
                "reviewer": "legal-qa-reviewer",
                "confidence": confidence,
                "human_validation": {
                    "validated_by_human": False,
                    "validator_role": "",
                    "validation_required": True,
                    "validation_reason": "Production cabinet-grade impose une validation professionnelle.",
                },
            }
        ],
        "human_validation": {
            "validated_by_human": False,
            "validator_role": "",
            "validation_required": True,
            "validation_reason": "Production cabinet-grade impose une validation professionnelle.",
        },
    }


def rubric_text(workflow: str) -> str:
    return f"""# Rubric - {workflow}

## False negatives bloquants

Le workflow echoue si un red flag bloquant documente dans `metadata.json` est absent des findings.

## Sources

Chaque finding critique doit inclure `source_status`. Une source absente doit etre marquee `not_found` ou `unverified`, jamais presentee comme officielle.

## Validation humaine

`validated_by_human` reste `false` dans les expected outputs. Le livrable final doit porter `DRAFT - Validation professionnelle requise`.

## Schema JSON

Les outputs doivent contenir `workflow`, `findings`, `audit_trail` et `human_validation`.
"""
```

- [ ] **Step 4: Add eval file generation**

Add this code to `production_grade_files()` after schema and docs generation:

```python
    for workflow in WORKFLOWS:
        for case_id, case_type, expected_risk in EVAL_CASES:
            case_root = VERTICAL / "evals" / "fixtures" / workflow / case_id
            write(case_root / "input.md", eval_input(workflow, case_id, case_type))
            write(case_root / "metadata.json", json.dumps(eval_metadata(workflow, case_id, case_type, expected_risk), indent=2, ensure_ascii=False) + "\n")
            expected = expected_eval_output(workflow, case_id, case_type, expected_risk)
            write(VERTICAL / "evals" / "expected" / workflow / f"{case_id}.expected.json", json.dumps(expected, indent=2, ensure_ascii=False) + "\n")
        write(VERTICAL / "evals" / "rubrics" / f"{workflow}.rubric.md", rubric_text(workflow))
```

- [ ] **Step 5: Run generator**

Run:

```bash
python scripts/generate_legal_fr_scaffold.py
```

Expected:

```text
generated legal-fr vertical, production-grade layer and 8 Legal-FR agent plugins
```

- [ ] **Step 6: Run eval fixture test**

Run:

```bash
python -m unittest tests.test_legal_fr_eval_fixtures -v
```

Expected:

```text
OK
```

- [ ] **Step 7: Commit eval fixtures**

Run:

```bash
git add tests/test_legal_fr_eval_fixtures.py scripts/generate_legal_fr_scaffold.py plugins/vertical-plugins/legal-fr/evals
git commit --no-verify -m "test: add legal fr cabinet-grade eval fixtures"
```

---

### Task 6: Add Offline Eval Runner

**Files:**
- Create: `scripts/run_legal_fr_evals.py`

- [ ] **Step 1: Create runner script**

Create `scripts/run_legal_fr_evals.py` with this content:

```python
#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "plugins" / "vertical-plugins" / "legal-fr" / "evals"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def score_expected_output(expected: dict) -> list[str]:
    failures: list[str] = []
    if expected.get("draft_notice") != "DRAFT - Validation professionnelle requise":
        failures.append("missing draft notice")
    if not expected.get("findings"):
        failures.append("missing findings")
    if not expected.get("audit_trail"):
        failures.append("missing audit trail")
    human_validation = expected.get("human_validation", {})
    if human_validation.get("validated_by_human") is not False:
        failures.append("validated_by_human must be false in offline expected output")
    for finding in expected.get("findings", []):
        source_status = finding.get("source_citation", {}).get("source_status")
        if source_status not in {"official", "secondary", "web", "unverified", "not_found"}:
            failures.append(f"invalid source_status {source_status!r}")
        confidence = finding.get("risk_score", {}).get("confidence")
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            failures.append("invalid confidence")
    return failures


def main() -> int:
    expected_files = sorted((EVALS / "expected").glob("*/*.expected.json"))
    if not expected_files:
        print("No Legal-FR eval expected files found")
        return 1

    failures: list[str] = []
    for expected_file in expected_files:
        expected = load_json(expected_file)
        case_failures = score_expected_output(expected)
        for failure in case_failures:
            failures.append(f"{expected_file.relative_to(ROOT)}: {failure}")

    if failures:
        print("Legal-FR evals failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Legal-FR evals passed: {len(expected_files)} expected outputs checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run eval runner**

Run:

```bash
python scripts/run_legal_fr_evals.py
```

Expected:

```text
Legal-FR evals passed: 40 expected outputs checked
```

- [ ] **Step 3: Run all Legal-FR tests**

Run:

```bash
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v
```

Expected:

```text
OK
```

- [ ] **Step 4: Commit eval runner**

Run:

```bash
git add scripts/run_legal_fr_evals.py
git commit --no-verify -m "feat: add legal fr offline eval runner"
```

---

### Task 7: Enrich Core Skills for Production-Grade Cabinet Use

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Generated: `plugins/vertical-plugins/legal-fr/skills/*/SKILL.md`
- Generated: `plugins/agent-plugins/<workflow>/skills/*/SKILL.md`

- [ ] **Step 1: Add richer skill sections in `skill_text()`**

Update `skill_text()` so each generated skill contains:

```python
## Cabinet-grade requirements

- Work from extracted facts, quoted passages and verified sources.
- Use `source_status` for every legal assertion.
- Use `confidence` between 0 and 1 for each material conclusion.
- Keep `validated_by_human: false` until professional review.
- Mark uncertain law, missing source or incomplete document as `A VERIFIER`.
- Preserve `DRAFT - Validation professionnelle requise` for external outputs.

## JSON discipline

- Extraction workers return JSON, not narrative Markdown.
- Markdown reports are generated from validated JSON.
- Each finding must link to `audit_trail`.

## French legal sourcing

- Prefer OpenLegi or an official French/EU source.
- Use Exa for discovery and secondary research.
- Do not treat web results as final legal authority without verification.
```

- [ ] **Step 2: Add domain-specific red flag lines**

Add a `SKILL_RED_FLAGS` dictionary near `SKILLS`:

```python
SKILL_RED_FLAGS = {
    "conformite-contractuelle": ["clause non sourcee", "desequilibre significatif", "juridiction incoherente"],
    "droit-achats-fr": ["delai de paiement excessif", "penalites absentes", "dependance fournisseur"],
    "procedure-civile-delais": ["forclusion potentielle", "date procedurale incertaine", "piece manquante"],
    "droit-social-fr": ["non-concurrence sans contrepartie", "periode essai non sourcee", "CCN absente"],
    "statut-baux-commerciaux": ["renonciation droit imperatif", "charges Pinel non detaillees", "indexation incoherente"],
    "droit-marches-financiers": ["facteur de risque generique", "materialite absente", "source AMF manquante"],
    "tabular-extraction": ["coverage incomplete", "JSON batch invalide", "score sans audit trail"],
}
```

In `skill_text()`, append a `## Red flags a surveiller` section when the skill is present in this dictionary.

- [ ] **Step 3: Run generator**

Run:

```bash
python scripts/generate_legal_fr_scaffold.py
```

Expected:

```text
generated legal-fr vertical, production-grade layer and 8 Legal-FR agent plugins
```

- [ ] **Step 4: Run tests and check**

Run:

```bash
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v
python scripts/run_legal_fr_evals.py
python scripts/check.py
```

Expected:

```text
OK
Legal-FR evals passed: 40 expected outputs checked
OK
```

- [ ] **Step 5: Commit skill enrichment**

Run:

```bash
git add scripts/generate_legal_fr_scaffold.py plugins/vertical-plugins/legal-fr/skills plugins/agent-plugins/*/skills
git commit --no-verify -m "feat: enrich legal fr cabinet-grade skills"
```

---

### Task 8: Enrich Playbooks With Executable Cabinet Rules

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Generated: `plugins/vertical-plugins/legal-fr/playbooks/*.md`

- [ ] **Step 1: Replace thin playbook content with structured sections**

Update the generator so every playbook includes:

```markdown
## Metadata

- Version: 1.0.0
- Domaine: <domain>
- Sortie attendue: JSON intermediaire + tableau Markdown
- Validation: DRAFT - Validation professionnelle requise

## Termes a extraire

| Terme | Description | Format | Valeur si absent |
|---|---|---|---|
| document_id | Identifiant stable du document | string | nom fichier |
| source_excerpt | Extrait qui justifie l'observation | string | A VERIFIER |
| source_status | official, secondary, web, unverified, not_found | enum | unverified |
| confidence | Confiance 0-1 | number | 0.5 |

## Regles de conformite

| ID | Regle | Niveau | Source attendue | Action si echec |
|---|---|---|---|---|
| R-001 | Toute conclusion critique cite une source ou reste A VERIFIER | blocking | audit trail | Bloquer le livrable |
| R-002 | Toute sortie externe porte la mention DRAFT | blocking | quality gate | Ajouter la mention |
| R-003 | Toute observation a un score de confiance | major | risk score | Ajouter confidence |

## Red flags automatiques

| ID | Signal | Niveau | Action |
|---|---|---|---|
| RF-001 | Source absente sur conclusion majeure | blocking | Marquer A VERIFIER |
| RF-002 | Document illisible ignore | blocking | Ajouter a coverage |
| RF-003 | validated_by_human absent | major | Ajouter human validation |
```

Use domain-specific additions for:

- `playbook-cgv-standard.md`: delai paiement, penalites, juridiction, limitation responsabilite.
- `playbook-dpa-art28.md`: sous-traitant, finalites, duree, mesures securite, sort donnees.
- `playbook-contrats-fournisseurs.md`: duree, preavis, prix, revision, penalites, exclusivite.
- `playbook-contrats-travail.md`: non-concurrence, remuneration, periode essai, CCN.
- `playbook-bail-commercial.md`: duree, charges, indexation, renouvellement, eviction.
- `playbook-cession-pme.md`: GAP, conditions suspensives, cession, changement controle.
- `playbook-lbo.md`: dette, covenants, suretes, restrictions.
- `playbook-immobilier.md`: titres, baux, charges, urbanisme.
- `playbook-dette.md`: maturite, taux, covenants, defaut.

- [ ] **Step 2: Run generator**

Run:

```bash
python scripts/generate_legal_fr_scaffold.py
```

Expected:

```text
generated legal-fr vertical, production-grade layer and 8 Legal-FR agent plugins
```

- [ ] **Step 3: Verify playbooks contain core rules**

Run:

```bash
Select-String -Path plugins\vertical-plugins\legal-fr\playbooks\*.md -Pattern "source_status","validated_by_human","confidence","DRAFT - Validation professionnelle requise"
```

Expected:

```text
```

PowerShell should print matches from each playbook. If one playbook is absent from the output, inspect that file and update the generator data.

- [ ] **Step 4: Run full validation**

Run:

```bash
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v
python scripts/run_legal_fr_evals.py
python scripts/check.py
```

Expected:

```text
OK
Legal-FR evals passed: 40 expected outputs checked
OK
```

- [ ] **Step 5: Commit playbook enrichment**

Run:

```bash
git add scripts/generate_legal_fr_scaffold.py plugins/vertical-plugins/legal-fr/playbooks
git commit --no-verify -m "feat: enrich legal fr cabinet-grade playbooks"
```

---

### Task 9: Add Connector Runtime Checks Without Network Calls

**Files:**
- Create: `scripts/check_legal_fr_connectors.py`
- Modify: `plugins/vertical-plugins/legal-fr/CONNECTORS.md`

- [ ] **Step 1: Create connector checker**

Create `scripts/check_legal_fr_connectors.py` with this content:

```python
#!/usr/bin/env python3
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "plugins" / "vertical-plugins" / "legal-fr" / ".mcp.json"


def main() -> int:
    data = json.loads(MCP.read_text(encoding="utf-8"))
    servers = data.get("mcpServers", {})
    failures: list[str] = []

    exa = servers.get("exa")
    if not exa or exa.get("url") != "https://mcp.exa.ai/mcp":
        failures.append("exa MCP endpoint is missing or unexpected")

    openlegi = servers.get("openlegi")
    if not openlegi:
        failures.append("openlegi MCP entry is missing")
    else:
        joined_args = " ".join(openlegi.get("args", []))
        if "${OPENLEGI_TOKEN}" not in joined_args:
            failures.append("openlegi MCP must reference ${OPENLEGI_TOKEN}")

    if "OPENLEGI_TOKEN" not in os.environ:
        print("WARN: OPENLEGI_TOKEN is not set; runtime OpenLegi calls will fail until configured.")

    if failures:
        print("Legal-FR connector config failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Legal-FR connector config OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run connector checker**

Run:

```bash
python scripts/check_legal_fr_connectors.py
```

Expected when token is not configured:

```text
WARN: OPENLEGI_TOKEN is not set; runtime OpenLegi calls will fail until configured.
Legal-FR connector config OK
```

Expected when token is configured:

```text
Legal-FR connector config OK
```

- [ ] **Step 3: Update connector docs**

Update `plugins/vertical-plugins/legal-fr/CONNECTORS.md` to include:

```markdown
## Verification locale

Run:

```bash
python scripts/check_legal_fr_connectors.py
```

Expected without token:

```text
WARN: OPENLEGI_TOKEN is not set; runtime OpenLegi calls will fail until configured.
Legal-FR connector config OK
```

Expected with token:

```text
Legal-FR connector config OK
```
```

- [ ] **Step 4: Run validation**

Run:

```bash
python scripts/check_legal_fr_connectors.py
python scripts/check.py
```

Expected:

```text
Legal-FR connector config OK
OK
```

The warning about `OPENLEGI_TOKEN` is acceptable when the variable is not set.

- [ ] **Step 5: Commit connector checks**

Run:

```bash
git add scripts/check_legal_fr_connectors.py plugins/vertical-plugins/legal-fr/CONNECTORS.md
git commit --no-verify -m "feat: add legal fr connector config checks"
```

---

### Task 10: Update Legal-FR Documentation for Cabinet Deployment

**Files:**
- Modify: `plugins/vertical-plugins/legal-fr/README.md`
- Modify: `plugins/vertical-plugins/legal-fr/CLAUDE.md`
- Modify: `README.md`

- [ ] **Step 1: Update Legal-FR README**

Replace `plugins/vertical-plugins/legal-fr/README.md` with:

```markdown
# Legal-FR

Vertical juridique francais pour workflows Legora-FR et Harvey-FR adaptes au contexte cabinet.

## Production-grade cabinet

Tous les workflows suivent la meme chaine:

```text
intake -> extraction JSON -> source verification -> risk scoring -> audit trail -> legal QA -> human validation -> DRAFT output
```

## Workflows

- `revue-conformite-interne`
- `analyse-contrats-fournisseurs`
- `chronologie-contentieux`
- `jurisprudence-multilingue`
- `revue-contrats-travail`
- `red-flags-bail`
- `note-information-amf`
- `tabular-due-diligence`

## Verification

```bash
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
```
```

- [ ] **Step 2: Update Legal-FR CLAUDE instructions**

Replace `plugins/vertical-plugins/legal-fr/CLAUDE.md` with:

```markdown
# Legal-FR Instructions

Tous les livrables externes sont des drafts: `DRAFT - Validation professionnelle requise`.

## Regles cabinet

- Extraire en JSON avant de rediger en Markdown.
- Citer une source officielle quand une conclusion juridique est critique.
- Utiliser OpenLegi avant Exa pour le droit positif francais.
- Marquer `A VERIFIER` quand la source est absente, incertaine ou recente.
- Ne pas exposer inutilement de donnees personnelles.
- Garder `validated_by_human: false` tant qu'un professionnel n'a pas valide.
- Produire un audit trail pour chaque finding materiel.
```

- [ ] **Step 3: Update root README Legal-FR row**

In `README.md`, expand the Legal-FR entry to mention:

```markdown
| `legal-fr` | Cabinet-grade legal workflows: schemas, evals, audit trail, OpenLegi/Exa source verification, human validation gates. |
```

Use the table format already present in the README.

- [ ] **Step 4: Run validation**

Run:

```bash
python scripts/check.py
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
```

Expected:

```text
OK
Legal-FR evals passed: 40 expected outputs checked
Legal-FR connector config OK
```

The OpenLegi warning is acceptable when `OPENLEGI_TOKEN` is absent.

- [ ] **Step 5: Commit docs**

Run:

```bash
git add README.md plugins/vertical-plugins/legal-fr/README.md plugins/vertical-plugins/legal-fr/CLAUDE.md
git commit --no-verify -m "docs: document legal fr cabinet deployment workflow"
```

---

### Task 11: Final Full Verification and GitNexus Refresh

**Files:**
- No planned file edits.

- [ ] **Step 1: Run full structural validation**

Run:

```bash
python scripts/check.py
```

Expected:

```text
OK
```

- [ ] **Step 2: Run all Legal-FR tests**

Run:

```bash
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v
```

Expected:

```text
OK
```

- [ ] **Step 3: Run offline evals**

Run:

```bash
python scripts/run_legal_fr_evals.py
```

Expected:

```text
Legal-FR evals passed: 40 expected outputs checked
```

- [ ] **Step 4: Run connector config check**

Run:

```bash
python scripts/check_legal_fr_connectors.py
```

Expected without token:

```text
WARN: OPENLEGI_TOKEN is not set; runtime OpenLegi calls will fail until configured.
Legal-FR connector config OK
```

Expected with token:

```text
Legal-FR connector config OK
```

- [ ] **Step 5: Refresh GitNexus index**

Run:

```bash
npx gitnexus analyze --embeddings
npx gitnexus status
```

Expected status:

```text
Status: up-to-date
```

- [ ] **Step 6: Inspect final diff**

Run:

```bash
git status --short
git log --oneline -5
```

Expected:

```text
```

Only unrelated pre-existing files may remain dirty: `.gitignore`, `CLAUDE.md`, `.claude/`, `AGENTS.md`.

---

## Execution Notes

- Use frequent commits after each task.
- Keep generated content source-of-truth in `scripts/generate_legal_fr_scaffold.py`.
- Do not hand-edit generated skill bundles in `plugins/agent-plugins/*/skills`; update the generator and rerun it.
- Do not reintroduce legacy anonymization MCP in this phase.
- Do not hardcode tokens or secrets.
- Treat Exa as discovery and secondary research, not final legal authority.
- Treat OpenLegi as the primary configured source for French legal text verification.
- Keep all external legal outputs as `DRAFT - Validation professionnelle requise`.

## Completion Criteria

Implementation is complete when:

- `python scripts/check.py` passes.
- `python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v` passes.
- `python scripts/run_legal_fr_evals.py` reports 40 checked expected outputs.
- `python scripts/check_legal_fr_connectors.py` reports connector config OK.
- `npx gitnexus status` reports current commit up-to-date.
- The final diff excludes unrelated dirty files unless the user asks to include them.
