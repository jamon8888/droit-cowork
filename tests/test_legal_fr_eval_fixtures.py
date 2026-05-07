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

EVAL_CASES = [
    ("case-001", "compliant", "low"),
    ("case-002", "blocking_red_flag", "high"),
    ("case-003", "legal_uncertainty", "medium"),
    ("case-004", "unreadable_or_incomplete", "unknown"),
    ("case-005", "source_not_found", "medium"),
]

REQUIRED_SOURCE_STATUSES = {
    "compliant": "official",
    "blocking_red_flag": "official",
    "legal_uncertainty": "unverified",
    "unreadable_or_incomplete": "unverified",
    "source_not_found": "not_found",
}

REQUIRED_RUBRIC_SECTIONS = [
    "## Required sections",
    "## Case coverage",
    "## Source and confidence checks",
    "## Human validation gate",
    "## Audit trail requirements",
]


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class LegalFrEvalFixturesTest(unittest.TestCase):
    def test_each_workflow_has_five_eval_cases_with_inputs_and_metadata(self) -> None:
        for workflow in WORKFLOWS:
            for case_id, case_type, risk_level in EVAL_CASES:
                with self.subTest(workflow=workflow, case_id=case_id):
                    case_root = EVALS / "fixtures" / workflow / case_id
                    input_file = case_root / "input.md"
                    metadata_file = case_root / "metadata.json"
                    self.assertTrue(input_file.is_file(), str(input_file))
                    self.assertTrue(metadata_file.is_file(), str(metadata_file))

                    input_text = input_file.read_text(encoding="utf-8")
                    self.assertIn(workflow, input_text)
                    self.assertIn(case_id, input_text)
                    self.assertIn(case_type, input_text)
                    self.assertIn("DRAFT - Validation professionnelle requise", input_text)

                    metadata = load_json(metadata_file)
                    self.assertEqual(metadata["workflow"], workflow)
                    self.assertEqual(metadata["case_id"], case_id)
                    self.assertEqual(metadata["case_type"], case_type)
                    self.assertEqual(metadata["expected_risk"], risk_level)
                    self.assertIn("expected_source_status", metadata)
                    self.assertIn("expected_confidence_band", metadata)
                    self.assertIn("requires_human_validation", metadata)
                    self.assertTrue(metadata["requires_human_validation"])

    def test_expected_outputs_include_cabinet_grade_safety_fields(self) -> None:
        for workflow in WORKFLOWS:
            for case_id, case_type, _risk_level in EVAL_CASES:
                with self.subTest(workflow=workflow, case_id=case_id):
                    expected_file = EVALS / "expected" / workflow / f"{case_id}.expected.json"
                    self.assertTrue(expected_file.is_file(), str(expected_file))
                    expected = load_json(expected_file)

                    self.assertEqual(expected["workflow"], workflow)
                    self.assertEqual(expected["draft_notice"], "DRAFT - Validation professionnelle requise")
                    self.assertIn("document_intake", expected)
                    document_intake = expected["document_intake"]
                    self.assertEqual(document_intake["document_id"], f"{workflow}-{case_id}-document")
                    self.assertIn("filename", document_intake)
                    self.assertIn("detected_type", document_intake)
                    self.assertIn("language", document_intake)
                    self.assertIn("legal_domain", document_intake)
                    intake_metadata = WORKFLOW_INTAKE_METADATA[workflow]
                    self.assertEqual(
                        document_intake["detected_type"],
                        intake_metadata["detected_type"],
                    )
                    self.assertEqual(
                        document_intake["legal_domain"],
                        intake_metadata["legal_domain"],
                    )
                    self.assertIn("readability", document_intake)
                    self.assertIn("status", document_intake["readability"])
                    self.assertIn("confidence", document_intake["readability"])
                    self.assertIn("requires_human_triage", document_intake)
                    self.assertEqual(
                        document_intake["readability"]["status"],
                        "unreadable" if case_type == "unreadable_or_incomplete" else "ok",
                    )
                    self.assertIn("coverage", expected)
                    coverage = expected["coverage"]
                    self.assertEqual(coverage["documents_seen"], 1)
                    self.assertEqual(coverage["documents_processed"], 0 if case_type == "unreadable_or_incomplete" else 1)
                    self.assertEqual(coverage["documents_unreadable"], 1 if case_type == "unreadable_or_incomplete" else 0)
                    self.assertIn("findings", expected)
                    self.assertGreater(len(expected["findings"]), 0)
                    self.assertIn("audit_trail", expected)
                    self.assertGreater(len(expected["audit_trail"]), 0)
                    self.assertIn("human_validation", expected)
                    self.assertFalse(expected["human_validation"]["validated_by_human"])
                    self.assertTrue(expected["human_validation"]["validation_required"])

                    finding = expected["findings"][0]
                    self.assertIn("source_citation", finding)
                    self.assertEqual(
                        finding["source_citation"]["source_status"],
                        REQUIRED_SOURCE_STATUSES[case_type],
                    )
                    self.assertIn("risk_score", finding)
                    self.assertIn("confidence", finding["risk_score"])
                    self.assertIsInstance(finding["risk_score"]["confidence"], float)
                    self.assertGreaterEqual(finding["risk_score"]["confidence"], 0)
                    self.assertLessEqual(finding["risk_score"]["confidence"], 1)
                    self.assertIn("audit_trail", finding)
                    self.assertEqual(finding["audit_trail"]["finding_id"], finding["finding_id"])

    def test_workflow_rubrics_define_required_sections_and_case_types(self) -> None:
        for workflow in WORKFLOWS:
            with self.subTest(workflow=workflow):
                rubric_file = EVALS / "rubrics" / f"{workflow}.rubric.md"
                self.assertTrue(rubric_file.is_file(), str(rubric_file))
                rubric = rubric_file.read_text(encoding="utf-8")
                self.assertIn(f"# Legal-FR eval rubric: {workflow}", rubric)
                for section in REQUIRED_RUBRIC_SECTIONS:
                    self.assertIn(section, rubric)
                for _case_id, case_type, _risk_level in EVAL_CASES:
                    self.assertIn(case_type, rubric)


if __name__ == "__main__":
    unittest.main()
