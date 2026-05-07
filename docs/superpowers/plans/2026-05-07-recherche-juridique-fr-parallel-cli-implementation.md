# Recherche Juridique FR Parallel CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a ninth Legal-FR agent, `recherche-juridique-fr-avancee`, backed by Parallel CLI for French legal research and documented Task API second layer.

**Architecture:** Extend the existing Legal-FR generator so the new agent, skills, commands, schemas, docs, eval fixtures, and marketplace entries are deterministic. Keep OpenLegi first for French positive law, use Parallel CLI for public web research/extraction/enrichment/monitoring, and document Task API as production backend layer without making it mandatory for local Cowork usage.

**Tech Stack:** Python stdlib, existing Cowork plugin structure, Markdown commands/skills, JSON schemas, `parallel-cli`, OpenLegi MCP, Exa MCP, unittest.

---

## File Map

- `scripts/generate_legal_fr_scaffold.py`: source of truth for Legal-FR generated assets; add new skills, commands, workflow, schemas, docs, eval metadata, and generation helpers.
- `scripts/check_legal_fr_parallel_cli.py`: local/offline-ish checker for Parallel CLI presence/auth shape and Legal-FR command constraints.
- `scripts/check_legal_fr_parallel_task_api.py`: local checker for Task API layer files and schema fields; no network calls.
- `scripts/legal_fr_parallel_task.py`: thin Task API wrapper scaffold with argument parsing, env validation, JSON I/O, and clear unsupported-network test mode.
- `tests/test_legal_fr_scaffold.py`: structural tests for new commands, skills, agent plugin, and marketplace entry.
- `tests/test_legal_fr_production_grade.py`: production-grade tests for guardrails, no secrets, CLI `--json`, Task API second-layer docs/schemas.
- `tests/test_legal_fr_eval_fixtures.py`: eval fixture tests for the new workflow.
- `plugins/vertical-plugins/legal-fr/**`: generated Legal-FR vertical files.
- `plugins/agent-plugins/recherche-juridique-fr-avancee/**`: generated self-contained agent plugin.
- `docs/superpowers/specs/2026-05-07-recherche-juridique-fr-parallel-cli-design.md`: reference spec; do not edit unless implementation discovers a design contradiction.

## Task 1: RED Tests For New Legal-FR Research Agent

**Files:**
- Modify: `tests/test_legal_fr_scaffold.py`
- Modify: `tests/test_legal_fr_production_grade.py`
- Modify: `tests/test_legal_fr_eval_fixtures.py`

- [ ] **Step 1: Add expected commands, skills, and agent to scaffold tests**

In `tests/test_legal_fr_scaffold.py`, add this command family:

```python
EXPECTED_COMMANDS["recherche"] = [
    "chercher",
    "extraire-source",
    "deep-research",
    "verifier-sources",
    "enrichir-dossier",
    "veille",
    "task-run",
    "task-status",
    "task-poll",
]
```

Add these skills to `EXPECTED_SKILLS`:

```python
[
    "parallel-recherche-juridique-fr",
    "source-audit-juridique-fr",
    "veille-juridique-fr",
    "parallel-task-api-juridique-fr",
]
```

Add this agent entry to `EXPECTED_AGENTS`:

```python
EXPECTED_AGENTS["recherche-juridique-fr-avancee"] = [
    "confidentialite-donnees",
    "quality-gates-juridiques",
    "openlegi-recherche",
    "exa-recherche-juridique",
    "citation-juridique",
    "rapport-executif",
    "parallel-recherche-juridique-fr",
    "source-audit-juridique-fr",
    "veille-juridique-fr",
    "parallel-task-api-juridique-fr",
]
```

- [ ] **Step 2: Add production-grade tests for Parallel CLI and Task API layer**

Append to `tests/test_legal_fr_production_grade.py`:

```python
    def test_recherche_juridique_fr_agent_keeps_fr_only_scope(self) -> None:
        prompt = (
            AGENT_PLUGINS
            / "recherche-juridique-fr-avancee"
            / "agents"
            / "recherche-juridique-fr-avancee.md"
        ).read_text(encoding="utf-8")
        self.assertIn("droit francais uniquement", prompt.lower())
        self.assertIn("OpenLegi avant Parallel", prompt)
        self.assertIn("parallel-cli", prompt)
        self.assertIn("DRAFT - Validation professionnelle requise", prompt)
        self.assertIn("jurisprudence-multilingue", prompt)

    def test_recherche_commands_use_parallel_cli_json(self) -> None:
        command_files = sorted((LEGAL_FR / "commands" / "recherche").glob("*.md"))
        self.assertEqual(len(command_files), 9)
        for command_file in command_files:
            text = command_file.read_text(encoding="utf-8")
            with self.subTest(command=command_file.name):
                if command_file.stem.startswith("task-"):
                    self.assertIn("legal_fr_parallel_task.py", text)
                else:
                    self.assertIn("parallel-cli", text)
                    self.assertIn("--json", text)
                self.assertIn("DRAFT - Validation professionnelle requise", text)

    def test_parallel_task_api_layer_is_second_layer_not_required_path(self) -> None:
        readme = (LEGAL_FR / "README.md").read_text(encoding="utf-8")
        self.assertIn("Parallel Task API", readme)
        self.assertIn("deuxieme couche", readme.lower())
        self.assertIn("Parallel CLI", readme)
        schema = load_json(
            LEGAL_FR
            / "schemas"
            / "parallel-task"
            / "recherche-juridique-fr.output.schema.json"
        )
        properties = schema["properties"]
        self.assertIn("draft_notice", properties)
        self.assertIn("audit_trail", properties)
        self.assertIn("human_validation", properties)
        self.assertIn("parallel", properties)
```

- [ ] **Step 3: Add eval fixture coverage for the ninth workflow**

In `tests/test_legal_fr_eval_fixtures.py`, extend the workflow list/dictionary with:

```python
"recherche-juridique-fr-avancee"
```

If the file uses explicit expected metadata mappings, add:

```python
"recherche-juridique-fr-avancee": {
    "detected_type": "legal_research_question",
    "legal_domain": "french_legal_research",
}
```

- [ ] **Step 4: Run tests and confirm RED**

Run:

```bash
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v
```

Expected: failures for missing `recherche` commands, missing skills, missing `recherche-juridique-fr-avancee` agent, missing Task API schemas, and missing eval fixtures.

- [ ] **Step 5: Commit RED tests**

```bash
git add tests/test_legal_fr_scaffold.py tests/test_legal_fr_production_grade.py tests/test_legal_fr_eval_fixtures.py
git commit -m "test: add legal fr parallel research agent expectations"
```

## Task 2: Extend Generator Metadata

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`

- [ ] **Step 1: Add new skills to `SKILLS`**

Add entries:

```python
"parallel-recherche-juridique-fr": "Recherche juridique francaise avancee via Parallel CLI: search, extract, research, enrich, findall et monitor.",
"source-audit-juridique-fr": "Classement des sources juridiques FR, source officielle, institutionnelle, doctrine, presse et confiance.",
"veille-juridique-fr": "Veille juridique francaise sur autorites, juridictions, textes, doctrine publique et signaux reglementaires.",
"parallel-task-api-juridique-fr": "Deuxieme couche Parallel Task API pour workflows juridiques FR batchables, schemas et run_id.",
```

- [ ] **Step 2: Add command family**

Add to `COMMANDS`:

```python
"recherche": {
    "chercher": "Rechercher des sources juridiques francaises avec OpenLegi et Parallel CLI.",
    "extraire-source": "Extraire et auditer une source publique avec Parallel CLI.",
    "deep-research": "Lancer une recherche juridique francaise approfondie avec Parallel CLI.",
    "verifier-sources": "Verifier et classer les sources d'une note juridique FR.",
    "enrichir-dossier": "Enrichir un dossier ou tableau juridique avec sources publiques FR.",
    "veille": "Preparer ou configurer une veille juridique francaise.",
    "task-run": "Lancer une recherche juridique FR via la couche Parallel Task API.",
    "task-status": "Lire le statut d'un run Parallel Task API.",
    "task-poll": "Recuperer le resultat d'un run Parallel Task API.",
},
```

- [ ] **Step 3: Add workflow metadata**

Add to `WORKFLOWS`:

```python
"recherche-juridique-fr-avancee": {
    "description": "Recherche juridique francaise avancee avec OpenLegi, Parallel CLI, audit des sources et couche Task API.",
    "workers": [
        "legal-query-classifier",
        "official-source-researcher",
        "parallel-cli-researcher",
        "source-auditor",
        "task-api-coordinator",
        "report-drafter",
        "legal-qa-reviewer",
    ],
    "skills": [
        "confidentialite-donnees",
        "quality-gates-juridiques",
        "openlegi-recherche",
        "exa-recherche-juridique",
        "citation-juridique",
        "rapport-executif",
        "parallel-recherche-juridique-fr",
        "source-audit-juridique-fr",
        "veille-juridique-fr",
        "parallel-task-api-juridique-fr",
    ],
    "output": "RECHERCHE-JURIDIQUE-FR-[sujet]-[YYYY-MM-DD].md",
},
```

- [ ] **Step 4: Add intake metadata**

Add to `WORKFLOW_INTAKE_METADATA`:

```python
"recherche-juridique-fr-avancee": {
    "detected_type": "legal_research_question",
    "legal_domain": "french_legal_research",
},
```

- [ ] **Step 5: Add domain-specific red flags**

Add to `SKILL_RED_FLAGS`:

```python
"parallel-recherche-juridique-fr": [
    "source officielle absente",
    "source secondaire presentee comme officielle",
    "parallel-cli sans sortie JSON",
],
"source-audit-juridique-fr": [
    "citation sans extrait",
    "source non datee",
    "confidence elevee sans source officielle",
],
"parallel-task-api-juridique-fr": [
    "run_id absent",
    "schema non versionne",
    "donnee client brute envoyee",
],
```

- [ ] **Step 6: Run syntax check**

```bash
python -m py_compile scripts/generate_legal_fr_scaffold.py
```

Expected: no output and exit code `0`.

- [ ] **Step 7: Commit generator metadata**

```bash
git add scripts/generate_legal_fr_scaffold.py
git commit -m "feat: add legal fr parallel research metadata"
```

## Task 3: Generate Agent, Skills, Commands, Schemas, And Evals

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Generated: `plugins/vertical-plugins/legal-fr/**`
- Generated: `plugins/agent-plugins/recherche-juridique-fr-avancee/**`
- Generated: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Add command rendering branches for `recherche`**

In `command_text()`, add a branch:

```python
    if family == "recherche":
        if command.startswith("task-"):
            invocation = "python scripts/legal_fr_parallel_task.py"
        else:
            invocation = "parallel-cli"
        return f"""---
name: recherche:{command}
description: {description}
argument-hint: "[question|url|fichier] [options]"
allowed-tools: Read, Write, Glob, Task, Bash(parallel-cli:*), Bash(python:*)
---

# recherche:{command}

## Regles

- DRAFT - Validation professionnelle requise.
- Perimetre: droit francais uniquement.
- OpenLegi avant Parallel pour droit positif francais.
- Toute commande Parallel CLI doit produire du JSON avec `--json`.
- Ne jamais afficher `PARALLEL_API_KEY`.
- Marquer `A VERIFIER` si aucune source officielle ne soutient une conclusion critique.

## Invocation technique

Outil principal: `{invocation}`

## Sortie attendue

Produire une extraction JSON schema-backed avant tout Markdown:

```json
{{
  "workflow": "recherche-juridique-fr-avancee",
  "draft_notice": "DRAFT - Validation professionnelle requise",
  "official_sources": [],
  "secondary_sources": [],
  "source_gaps": [],
  "audit_trail": [],
  "human_validation": {{"required": true, "status": "pending"}}
}}
```
"""
```

- [ ] **Step 2: Add Task API schema generation**

Create helper:

```python
def parallel_task_schemas() -> dict[str, dict]:
    return {
        "recherche-juridique-fr.input": object_schema(
            "Legal-FR Parallel Task input",
            {
                "workflow": {"const": "recherche-juridique-fr-avancee"},
                "question": {"type": "string", "minLength": 1},
                "legal_domain": {"type": "string"},
                "official_source_required": {"type": "boolean"},
                "processor": {"type": "string", "enum": ["lite", "base", "core", "pro", "ultra"]},
            },
            ["workflow", "question", "official_source_required"],
        ),
        "recherche-juridique-fr.output": object_schema(
            "Legal-FR Parallel Task output",
            {
                "workflow": {"const": "recherche-juridique-fr-avancee"},
                "draft_notice": {"const": "DRAFT - Validation professionnelle requise"},
                "question": {"type": "string"},
                "answer": {"type": "string"},
                "official_sources": {"type": "array", "items": ref("../common/source-citation.schema.json")},
                "secondary_sources": {"type": "array", "items": ref("../common/source-citation.schema.json")},
                "source_gaps": {"type": "array", "items": {"type": "string"}},
                "findings": {"type": "array", "items": ref("../common/finding.schema.json")},
                "audit_trail": {"type": "array", "items": ref("../common/audit-trail.schema.json")},
                "human_validation": ref("../common/human-validation.schema.json"),
                "parallel": object_schema(
                    "Parallel run metadata",
                    {
                        "run_id": {"type": "string"},
                        "processor": {"type": "string"},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    },
                    ["run_id", "processor", "confidence"],
                ),
            },
            ["workflow", "draft_notice", "question", "answer", "audit_trail", "human_validation", "parallel"],
        ),
    }
```

Write these files in `production_grade_files()`:

```python
    for name, schema in parallel_task_schemas().items():
        write(
            VERTICAL / "schemas" / "parallel-task" / f"{name}.schema.json",
            json.dumps(schema, indent=2) + "\n",
        )
```

- [ ] **Step 3: Generate scaffold**

Run:

```bash
python scripts/generate_legal_fr_scaffold.py
```

Expected output:

```text
generated legal-fr vertical, production-grade layer and 9 Legal-FR agent plugins
```

If the generator still prints `8`, update the final print statement to derive the count:

```python
print(f"generated legal-fr vertical, production-grade layer and {len(WORKFLOWS)} Legal-FR agent plugins")
```

- [ ] **Step 4: Run structural tests**

```bash
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v
```

Expected: tests pass or fail only on checker/wrapper files not yet implemented. If failures reference missing generated skills, commands, schemas, or agent plugin, fix generation before continuing.

- [ ] **Step 5: Commit generated assets**

```bash
git add scripts/generate_legal_fr_scaffold.py plugins/vertical-plugins/legal-fr plugins/agent-plugins/recherche-juridique-fr-avancee .claude-plugin/marketplace.json tests
git commit -m "feat: generate legal fr advanced research agent"
```

## Task 4: Parallel CLI Checker

**Files:**
- Create: `scripts/check_legal_fr_parallel_cli.py`
- Modify: `tests/test_legal_fr_production_grade.py`
- Modify: `plugins/vertical-plugins/legal-fr/CONNECTORS.md`

- [ ] **Step 1: Add checker tests**

Append to `tests/test_legal_fr_production_grade.py`:

```python
    def test_parallel_cli_checker_exists_and_documents_no_secret_policy(self) -> None:
        checker = ROOT / "scripts" / "check_legal_fr_parallel_cli.py"
        self.assertTrue(checker.is_file())
        text = checker.read_text(encoding="utf-8")
        self.assertIn("PARALLEL_API_KEY", text)
        self.assertIn("parallel-cli", text)
        self.assertNotIn("PARALLEL_API_KEY=", text)
        connectors = (LEGAL_FR / "CONNECTORS.md").read_text(encoding="utf-8")
        self.assertIn("python scripts/check_legal_fr_parallel_cli.py", connectors)
        self.assertIn("Legal-FR Parallel CLI config OK", connectors)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m unittest tests.test_legal_fr_production_grade.LegalFrProductionGradeTest.test_parallel_cli_checker_exists_and_documents_no_secret_policy -v
```

Expected: fail because checker does not exist.

- [ ] **Step 3: Create checker**

Create `scripts/check_legal_fr_parallel_cli.py`:

```python
#!/usr/bin/env python3
"""Validate Legal-FR Parallel CLI integration without running paid research."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = ROOT / "plugins" / "vertical-plugins" / "legal-fr" / "commands" / "recherche"
OK_MESSAGE = "Legal-FR Parallel CLI config OK"
TOKEN_WARN = (
    "WARN: PARALLEL_API_KEY is not set; parallel-cli must be authenticated by local login or device flow."
)


def error(message: str) -> str:
    return f"ERROR: {message}"


def run_json(command: list[str]) -> tuple[int, dict | None, str]:
    completed = subprocess.run(command, capture_output=True, text=True, timeout=20)
    output = completed.stdout.strip()
    if not output:
        return completed.returncode, None, completed.stderr.strip()
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return completed.returncode, None, output[:300]
    return completed.returncode, data, ""


def validate_command_docs() -> list[str]:
    errors: list[str] = []
    if not COMMANDS.is_dir():
        return [error("plugins/vertical-plugins/legal-fr/commands/recherche is missing")]
    for path in sorted(COMMANDS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if path.stem.startswith("task-"):
            continue
        if "parallel-cli" not in text:
            errors.append(error(f"{path.relative_to(ROOT)} must mention parallel-cli"))
        if "--json" not in text:
            errors.append(error(f"{path.relative_to(ROOT)} must require --json"))
    return errors


def main() -> int:
    errors = validate_command_docs()
    if shutil.which("parallel-cli") is None:
        errors.append(error("parallel-cli is not installed or not on PATH"))
    else:
        code, data, detail = run_json(["parallel-cli", "auth", "--json"])
        if code not in (0, 3):
            errors.append(error(f"parallel-cli auth --json failed with exit code {code}: {detail}"))
        elif data is None:
            errors.append(error("parallel-cli auth --json did not return parseable JSON"))

    if errors:
        for message in errors:
            print(message)
        return 1

    if "PARALLEL_API_KEY" not in os.environ:
        print(TOKEN_WARN)
    print(OK_MESSAGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Update connectors doc**

Append to `plugins/vertical-plugins/legal-fr/CONNECTORS.md`:

```markdown
## Parallel CLI

Parallel CLI is the local/Cowork execution layer for advanced French legal research.

Install options:

```bash
pipx install "parallel-web-tools[cli]"
```

or:

```bash
npm install -g parallel-web-cli
```

Verification:

```bash
python scripts/check_legal_fr_parallel_cli.py
```

Expected when the CLI is installed and local auth or `PARALLEL_API_KEY` is available:

```text
Legal-FR Parallel CLI config OK
```

If `PARALLEL_API_KEY` is not set, local login or device flow may still work. The checker prints:

```text
WARN: PARALLEL_API_KEY is not set; parallel-cli must be authenticated by local login or device flow.
Legal-FR Parallel CLI config OK
```
```

- [ ] **Step 5: Run tests**

```bash
python -m unittest tests.test_legal_fr_production_grade.LegalFrProductionGradeTest.test_parallel_cli_checker_exists_and_documents_no_secret_policy -v
python -m py_compile scripts/check_legal_fr_parallel_cli.py
```

Expected: both pass. If local `parallel-cli` is absent, do not require `python scripts/check_legal_fr_parallel_cli.py` to pass in CI until the team decides to install it; the checker itself must provide a clear error.

- [ ] **Step 6: Commit**

```bash
git add scripts/check_legal_fr_parallel_cli.py tests/test_legal_fr_production_grade.py plugins/vertical-plugins/legal-fr/CONNECTORS.md
git commit -m "feat: add legal fr parallel cli checker"
```

## Task 5: Task API Wrapper And Checker

**Files:**
- Create: `scripts/legal_fr_parallel_task.py`
- Create: `scripts/check_legal_fr_parallel_task_api.py`
- Modify: `tests/test_legal_fr_production_grade.py`
- Modify: `plugins/vertical-plugins/legal-fr/README.md`

- [ ] **Step 1: Add tests for Task API wrapper/checker**

Append to `tests/test_legal_fr_production_grade.py`:

```python
    def test_parallel_task_api_wrapper_and_checker_exist(self) -> None:
        wrapper = ROOT / "scripts" / "legal_fr_parallel_task.py"
        checker = ROOT / "scripts" / "check_legal_fr_parallel_task_api.py"
        self.assertTrue(wrapper.is_file())
        self.assertTrue(checker.is_file())
        wrapper_text = wrapper.read_text(encoding="utf-8")
        checker_text = checker.read_text(encoding="utf-8")
        self.assertIn("run", wrapper_text)
        self.assertIn("status", wrapper_text)
        self.assertIn("poll", wrapper_text)
        self.assertIn("PARALLEL_API_KEY", wrapper_text)
        self.assertNotIn("PARALLEL_API_KEY=", wrapper_text)
        self.assertIn("recherche-juridique-fr.output.schema.json", checker_text)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m unittest tests.test_legal_fr_production_grade.LegalFrProductionGradeTest.test_parallel_task_api_wrapper_and_checker_exist -v
```

Expected: fail because scripts are missing.

- [ ] **Step 3: Create Task API wrapper**

Create `scripts/legal_fr_parallel_task.py`:

```python
#!/usr/bin/env python3
"""Run Legal-FR Parallel Task API jobs with schema-backed JSON I/O."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "plugins" / "vertical-plugins" / "legal-fr" / "schemas" / "parallel-task"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def require_api_key() -> str:
    token = os.environ.get("PARALLEL_API_KEY")
    if not token:
        raise RuntimeError("PARALLEL_API_KEY is required for Parallel Task API calls")
    return token


def command_run(args: argparse.Namespace) -> int:
    require_api_key()
    payload = load_json(Path(args.input))
    result = {
        "status": "not_executed",
        "reason": "Network Task API execution is intentionally not implemented in the scaffold.",
        "workflow": args.workflow,
        "input": payload,
        "processor": args.processor,
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "not_executed", "output": args.output}))
    return 0


def command_status(args: argparse.Namespace) -> int:
    require_api_key()
    print(json.dumps({"run_id": args.run_id, "status": "not_executed"}))
    return 0


def command_poll(args: argparse.Namespace) -> int:
    require_api_key()
    result = {"run_id": args.run_id, "status": "not_executed"}
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subcommands = root.add_subparsers(dest="command", required=True)
    run = subcommands.add_parser("run")
    run.add_argument("--workflow", required=True)
    run.add_argument("--input", required=True)
    run.add_argument("--processor", default="pro")
    run.add_argument("--output", required=True)
    run.set_defaults(func=command_run)
    status = subcommands.add_parser("status")
    status.add_argument("--run-id", required=True)
    status.set_defaults(func=command_status)
    poll = subcommands.add_parser("poll")
    poll.add_argument("--run-id", required=True)
    poll.add_argument("--output")
    poll.set_defaults(func=command_poll)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Create Task API checker**

Create `scripts/check_legal_fr_parallel_task_api.py`:

```python
#!/usr/bin/env python3
"""Validate Legal-FR Parallel Task API scaffold without network calls."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts" / "legal_fr_parallel_task.py"
SCHEMA = (
    ROOT
    / "plugins"
    / "vertical-plugins"
    / "legal-fr"
    / "schemas"
    / "parallel-task"
    / "recherche-juridique-fr.output.schema.json"
)
OK_MESSAGE = "Legal-FR Parallel Task API scaffold OK"


def error(message: str) -> str:
    return f"ERROR: {message}"


def main() -> int:
    errors: list[str] = []
    if not WRAPPER.is_file():
        errors.append(error("scripts/legal_fr_parallel_task.py is missing"))
    if not SCHEMA.is_file():
        errors.append(error("recherche-juridique-fr.output.schema.json is missing"))
    else:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        properties = schema.get("properties", {})
        for required in ["draft_notice", "audit_trail", "human_validation", "parallel"]:
            if required not in properties:
                errors.append(error(f"Task API output schema must define {required}"))
        parallel = properties.get("parallel", {}).get("properties", {})
        if "run_id" not in parallel:
            errors.append(error("Task API output schema must define parallel.run_id"))
    if errors:
        for message in errors:
            print(message)
        return 1
    print(OK_MESSAGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Update README**

Add to `plugins/vertical-plugins/legal-fr/README.md`:

```markdown
## Parallel Task API Layer

Parallel CLI is the default local/Cowork execution path. Parallel Task API is the second layer for backend production, long-running research, batch enrichment, polling, webhooks, and schema-backed outputs.

Local scaffold verification:

```bash
python scripts/check_legal_fr_parallel_task_api.py
```
```

- [ ] **Step 6: Run tests and compile**

```bash
python -m py_compile scripts/legal_fr_parallel_task.py scripts/check_legal_fr_parallel_task_api.py
python scripts/check_legal_fr_parallel_task_api.py
python -m unittest tests.test_legal_fr_production_grade.LegalFrProductionGradeTest.test_parallel_task_api_wrapper_and_checker_exist -v
```

Expected: all pass.

- [ ] **Step 7: Commit**

```bash
git add scripts/legal_fr_parallel_task.py scripts/check_legal_fr_parallel_task_api.py tests/test_legal_fr_production_grade.py plugins/vertical-plugins/legal-fr/README.md
git commit -m "feat: scaffold legal fr parallel task api layer"
```

## Task 6: Eval Fixtures For Advanced Research Workflow

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Generated: `plugins/vertical-plugins/legal-fr/evals/fixtures/recherche-juridique-fr-avancee/**`
- Generated: `plugins/vertical-plugins/legal-fr/evals/expected/recherche-juridique-fr-avancee/**`
- Generated: `plugins/vertical-plugins/legal-fr/evals/rubrics/recherche-juridique-fr-avancee.rubric.md`
- Modify: `tests/test_legal_fr_eval_fixtures.py`

- [ ] **Step 1: Add workflow-specific eval case descriptions**

Add a helper mapping:

```python
RESEARCH_FR_EVAL_CASES = {
    "case-001": "Question simple avec source officielle disponible.",
    "case-002": "Conclusion critique sans source officielle, doit marquer A VERIFIER.",
    "case-003": "Doctrine secondaire utile mais non suffisante seule.",
    "case-004": "Veille AMF avec source institutionnelle.",
    "case-005": "Deep research async avec run_id et interaction_id.",
}
```

In `eval_fixture_input()`, branch for `workflow == "recherche-juridique-fr-avancee"` and include:

```markdown
# Cas eval recherche-juridique-fr-avancee

Question: verifier l'etat du droit francais applicable.
Contrainte: OpenLegi doit etre interroge avant Parallel.
Source attendue: officielle si conclusion critique.
```

- [ ] **Step 2: Add expected output fields**

In `expected_eval_output()`, if workflow is `recherche-juridique-fr-avancee`, set:

```python
expected["parallel"] = {
    "run_id": "trun_eval_reference",
    "processor": "pro",
    "confidence": 0.78,
}
expected["official_sources"] = expected["source_citations"][:1]
expected["secondary_sources"] = []
expected["source_gaps"] = ["A VERIFIER si aucune source officielle n'est confirmee"]
```

- [ ] **Step 3: Add tests for advanced research expected outputs**

In `tests/test_legal_fr_eval_fixtures.py`, add:

```python
    def test_recherche_juridique_fr_expected_outputs_track_parallel_metadata(self) -> None:
        expected_root = EXPECTED_ROOT / "recherche-juridique-fr-avancee"
        self.assertTrue(expected_root.is_dir())
        for expected_file in sorted(expected_root.glob("*.expected.json")):
            data = load_json(expected_file)
            with self.subTest(file=expected_file.name):
                self.assertEqual(data["workflow"], "recherche-juridique-fr-avancee")
                self.assertEqual(
                    data["document_intake"]["detected_type"],
                    "legal_research_question",
                )
                self.assertEqual(
                    data["document_intake"]["legal_domain"],
                    "french_legal_research",
                )
                self.assertIn("parallel", data)
                self.assertIn("run_id", data["parallel"])
                self.assertIn("source_gaps", data)
```

- [ ] **Step 4: Regenerate and run eval tests**

```bash
python scripts/generate_legal_fr_scaffold.py
python -m unittest tests.test_legal_fr_eval_fixtures -v
python scripts/run_legal_fr_evals.py
```

Expected: eval tests pass and runner reports `45 expected outputs checked` if the suite now covers 9 workflows x 5 cases.

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_legal_fr_scaffold.py tests/test_legal_fr_eval_fixtures.py plugins/vertical-plugins/legal-fr/evals
git commit -m "test: add legal fr advanced research evals"
```

## Task 7: Documentation And Marketplace Polish

**Files:**
- Modify: `plugins/vertical-plugins/legal-fr/README.md`
- Modify: `plugins/vertical-plugins/legal-fr/CLAUDE.md`
- Modify: `plugins/vertical-plugins/legal-fr/CONNECTORS.md`
- Modify: `README.md`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Update Legal-FR README workflow table**

Add row:

```markdown
| `recherche-juridique-fr-avancee` | Research French legal questions with OpenLegi-first source discipline, Parallel CLI deep research, source audit, veille, and Task API second-layer scaffolding. |
```

- [ ] **Step 2: Update Legal-FR CLAUDE instructions**

Add:

```markdown
## Recherche juridique FR avancee

- Utiliser OpenLegi avant Parallel pour toute question de droit positif francais.
- Utiliser Parallel CLI seulement avec `--json`.
- Ne jamais exposer `PARALLEL_API_KEY`.
- Classer chaque source: officielle, institutionnelle, doctrine, presse, inconnue.
- La couche Parallel Task API est une deuxieme couche backend; elle ne remplace pas le CLI pour Cowork local.
- Marquer `A VERIFIER` si une conclusion critique ne dispose pas de source officielle.
```

- [ ] **Step 3: Update root README Legal-FR row**

Change the Legal-FR row to mention:

```text
plus advanced FR legal research via OpenLegi-first source discipline and Parallel CLI/Task API layering.
```

- [ ] **Step 4: Validate marketplace entry**

Run:

```bash
python scripts/check.py
```

Expected: all plugin manifest/source paths resolve.

- [ ] **Step 5: Commit docs**

```bash
git add plugins/vertical-plugins/legal-fr/README.md plugins/vertical-plugins/legal-fr/CLAUDE.md plugins/vertical-plugins/legal-fr/CONNECTORS.md README.md .claude-plugin/marketplace.json
git commit -m "docs: document legal fr advanced research workflow"
```

## Task 8: Final Verification And Review

**Files:**
- No planned edits.

- [ ] **Step 1: Run full validation**

```bash
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
python scripts/check_legal_fr_parallel_task_api.py
```

Expected:

- `scripts/check.py`: `OK`
- unittest: all tests pass
- eval runner: `45 expected outputs checked`
- connector checker: existing OpenLegi warning acceptable if `OPENLEGI_TOKEN` absent
- Task API checker: `Legal-FR Parallel Task API scaffold OK`

- [ ] **Step 2: Run Parallel CLI checker conditionally**

Run:

```bash
python scripts/check_legal_fr_parallel_cli.py
```

Expected if `parallel-cli` is installed and auth is configured:

```text
Legal-FR Parallel CLI config OK
```

Expected acceptable development failure if CLI is absent:

```text
ERROR: parallel-cli is not installed or not on PATH
```

If the CLI is absent locally, record that as an environment limitation, not a code failure.

- [ ] **Step 3: Check for secrets and piighost**

Run:

```powershell
Get-ChildItem -Path plugins\vertical-plugins\legal-fr,plugins\agent-plugins\recherche-juridique-fr-avancee,scripts,tests -Recurse -File -Include *.md,*.json,*.py |
  Select-String -Pattern 'PARALLEL_API_KEY=|OPENLEGI_TOKEN=|piighost' -CaseSensitive:$false
```

Expected: no matches for hardcoded token assignment or piighost requirement. Mentions of `PARALLEL_API_KEY` and `${OPENLEGI_TOKEN}` without assignment are acceptable.

- [ ] **Step 4: Refresh GitNexus**

```bash
npx gitnexus analyze --embeddings
npx gitnexus status
```

Expected: indexed commit equals current commit.

- [ ] **Step 5: Dispatch final code review**

Use a fresh reviewer with this scope:

```text
Review the new Legal-FR `recherche-juridique-fr-avancee` agent, Parallel CLI checker, Task API scaffold, generated skills/commands/evals, tests, and docs. Verify FR-only scope, OpenLegi-first discipline, no secret leakage, no piighost reintroduction, and no replacement of `jurisprudence-multilingue`.
```

- [ ] **Step 6: Finish branch**

If reviewer approves, use `superpowers:finishing-a-development-branch` and present merge/PR/keep/discard options.
