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
    "recherche-juridique-fr-avancee",
]

WORKFLOW_INTAKE_METADATA = {
    "revue-conformite-interne": {
        "detected_type": "policy_or_contract",
        "legal_domain": "compliance",
    },
    "analyse-contrats-fournisseurs": {
        "detected_type": "supplier_agreement",
        "legal_domain": "contracts_supply",
    },
    "chronologie-contentieux": {
        "detected_type": "litigation_file",
        "legal_domain": "litigation",
    },
    "jurisprudence-multilingue": {
        "detected_type": "court_decision",
        "legal_domain": "case_law",
    },
    "revue-contrats-travail": {
        "detected_type": "employment_agreement",
        "legal_domain": "employment",
    },
    "red-flags-bail": {
        "detected_type": "lease_agreement",
        "legal_domain": "real_estate",
    },
    "note-information-amf": {
        "detected_type": "amf_disclosure_file",
        "legal_domain": "capital_markets",
    },
    "tabular-due-diligence": {
        "detected_type": "data_room_document",
        "legal_domain": "due_diligence",
    },
    "recherche-juridique-fr-avancee": {
        "detected_type": "legal_research_question",
        "legal_domain": "french_legal_research",
    },
}

COMMON_SCHEMAS = [
    "document-intake.schema.json",
    "source-citation.schema.json",
    "risk-score.schema.json",
    "finding.schema.json",
    "audit-trail.schema.json",
    "human-validation.schema.json",
    "workflow-run.schema.json",
    "source-ledger.schema.json",
    "review-queue.schema.json",
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

WORKFLOW_COMMANDS = ["init", "run", "review", "export", "eval"]

WORKFLOW_PLAYBOOKS = [
    "workflow-dd-ma",
    "workflow-audit-rh",
    "workflow-preparation-audience",
    "workflow-audit-baux",
    "workflow-conformite-fournisseurs",
    "workflow-recherche-source-first",
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

    def test_document_intake_schema_allows_workflow_eval_metadata(self) -> None:
        schema = load_json(LEGAL_FR / "schemas" / "common" / "document-intake.schema.json")
        detected_type_values = schema["properties"]["detected_type"]["enum"]
        legal_domain_values = schema["properties"]["legal_domain"]["enum"]
        self.assertEqual(len(detected_type_values), len(set(detected_type_values)))
        self.assertEqual(len(legal_domain_values), len(set(legal_domain_values)))
        detected_type_enum = set(detected_type_values)
        legal_domain_enum = set(legal_domain_values)

        for workflow, intake_metadata in WORKFLOW_INTAKE_METADATA.items():
            with self.subTest(workflow=workflow, field="detected_type"):
                self.assertIn(intake_metadata["detected_type"], detected_type_enum)
            with self.subTest(workflow=workflow, field="legal_domain"):
                self.assertIn(intake_metadata["legal_domain"], legal_domain_enum)

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

    def test_runtime_rules_are_skill_backed_not_only_plugin_claude_md(self) -> None:
        runtime_skill = LEGAL_FR / "skills" / "legal-fr-runtime" / "SKILL.md"
        self.assertTrue(runtime_skill.is_file())
        runtime_text = runtime_skill.read_text(encoding="utf-8")
        for required in [
            "OpenLegi avant Exa",
            "OpenLegi avant Parallel",
            "Parallel CLI",
            "--json",
            "PARALLEL_API_KEY",
            "DRAFT - Validation professionnelle requise",
            "A VERIFIER",
            "schema",
            "audit_trail",
            "quality gate",
            "stop",
        ]:
            with self.subTest(required=required):
                self.assertIn(required, runtime_text)

        for workflow in WORKFLOWS:
            prompt = (AGENT_PLUGINS / workflow / "agents" / f"{workflow}.md").read_text(encoding="utf-8")
            with self.subTest(workflow=workflow):
                self.assertIn("legal-fr-runtime", prompt)

        for command_file in sorted((LEGAL_FR / "commands").glob("*/*.md")):
            text = command_file.read_text(encoding="utf-8")
            with self.subTest(command=command_file.name):
                self.assertIn("legal-fr-runtime", text)

    def test_workflow_layer_is_materialized_in_plugin_components(self) -> None:
        for command in WORKFLOW_COMMANDS:
            command_file = LEGAL_FR / "commands" / "workflow" / f"{command}.md"
            with self.subTest(command=command):
                self.assertTrue(command_file.is_file())
                text = command_file.read_text(encoding="utf-8")
                self.assertIn("legal-fr-runtime", text)
                self.assertIn("workflow-playbooks", text)
                self.assertIn("source-ledger", text)
                self.assertIn("review-queue", text)
                self.assertIn("schema", text.lower())
                self.assertIn("audit trail", text.lower())
                self.assertIn("quality gate", text.lower())
                self.assertIn("DRAFT - Validation professionnelle requise", text)

        run_text = (LEGAL_FR / "commands" / "workflow" / "run.md").read_text(encoding="utf-8")
        self.assertIn("execute exactly one next workflow stage by default", run_text)
        self.assertIn("--full", run_text)
        self.assertIn("stop", run_text.lower())

    def test_workflow_playbooks_are_v2_and_machine_addressable(self) -> None:
        required_sections = [
            "## Intake",
            "## Documents Requis",
            "## Sources Autorisees",
            "## Agents Et Skills",
            "## Etapes Workflow",
            "## Tableau Principal",
            "## Red Flags",
            "## Quality Gates",
            "## Livrables",
            "## Validation Humaine",
        ]
        required_ids = [
            "schema_version",
            "playbook_id",
            "intake_id",
            "document_id",
            "source_rule_id",
            "assignment_id",
            "step_id",
            "rule_id",
            "quality_gate_id",
            "deliverable_id",
        ]
        for playbook in WORKFLOW_PLAYBOOKS:
            path = LEGAL_FR / "playbooks" / "workflows" / f"{playbook}.md"
            text = path.read_text(encoding="utf-8")
            with self.subTest(playbook=playbook):
                self.assertIn(f"playbook_id: {playbook}", text)
                self.assertIn("schema_version: 2.0.0", text)
                for section in required_sections:
                    self.assertIn(section, text)
                for field in required_ids:
                    self.assertIn(field, text)

    def test_workflow_common_and_pack_schemas_exist(self) -> None:
        for schema_name in ["workflow-run", "source-ledger", "review-queue"]:
            schema = load_json(LEGAL_FR / "schemas" / "common" / f"{schema_name}.schema.json")
            with self.subTest(common_schema=schema_name):
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertIn("required", schema)
                self.assertFalse(schema["additionalProperties"])

        for playbook in WORKFLOW_PLAYBOOKS:
            workflow_root = LEGAL_FR / "schemas" / "workflows" / playbook
            for schema_name in ["run.schema.json", "deliverables.schema.json"]:
                schema = load_json(workflow_root / schema_name)
                with self.subTest(playbook=playbook, schema=schema_name):
                    self.assertEqual(schema["type"], "object")
                    self.assertIn("playbook_id", schema["properties"])
                    self.assertIn("source_ledger", schema["properties"])
                    self.assertIn("review_queue", schema["properties"])
                    self.assertIn("human_validation", schema["properties"])

    def test_workflow_runner_is_documented_and_bound_to_commands(self) -> None:
        runner = ROOT / "scripts" / "legal_fr_workflow.py"
        self.assertTrue(runner.is_file())
        runner_text = runner.read_text(encoding="utf-8")
        for subcommand in ["init", "run", "review", "export", "eval"]:
            with self.subTest(subcommand=subcommand):
                self.assertIn(f'"{subcommand}"', runner_text)

        readme = (LEGAL_FR / "README.md").read_text(encoding="utf-8")
        self.assertIn("python scripts/legal_fr_workflow.py", readme)
        self.assertIn("workflow-run.json", readme)
        self.assertIn("source-ledger.json", readme)
        self.assertIn("review-queue.json", readme)

        for command in WORKFLOW_COMMANDS:
            command_text = (LEGAL_FR / "commands" / "workflow" / f"{command}.md").read_text(encoding="utf-8")
            with self.subTest(command=command):
                self.assertIn("python scripts/legal_fr_workflow.py", command_text)

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

    def test_no_piighost_or_hardcoded_tokens_reintroduced(self) -> None:
        checked_files = [
            *LEGAL_FR.rglob("*.md"),
            *LEGAL_FR.rglob("*.json"),
            *[path for workflow in WORKFLOWS for path in (AGENT_PLUGINS / workflow).rglob("*.md")],
            *[path for workflow in WORKFLOWS for path in (AGENT_PLUGINS / workflow).rglob("*.json")],
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in checked_files)
        self.assertNotIn("piighost", combined.lower())
        self.assertNotIn("OPENLEGI_TOKEN=", combined)
        self.assertIn("${OPENLEGI_TOKEN}", combined)


if __name__ == "__main__":
    unittest.main()
