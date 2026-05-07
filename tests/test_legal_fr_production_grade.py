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
}

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
