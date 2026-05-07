import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-05-07-legal-fr-cowork-playbook-workflows-design.md"


class LegalFrWorkflowDesignSpecTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SPEC.read_text(encoding="utf-8")

    def test_spec_has_decisions_not_open_questions(self) -> None:
        self.assertIn("## Decisions", self.text)
        self.assertNotIn("## Open Questions", self.text)
        self.assertIn("Keep source workflow playbooks in `legal-fr`", self.text)
        self.assertIn("Run one stage by default", self.text)
        self.assertIn("Document commercial bundles as install recipes first", self.text)

    def test_workflow_run_is_stage_by_stage_by_default(self) -> None:
        self.assertIn("`workflow:run`: execute exactly one next workflow stage by default", self.text)
        self.assertIn("full execution only with an explicit `--full` argument", self.text)
        self.assertIn("must stop when intake, required documents, citations, source ledger, or human validation gates are incomplete", self.text)

    def test_playbook_v2_has_stable_machine_ids(self) -> None:
        for field in [
            "schema_version",
            "playbook_id",
            "step_id",
            "rule_id",
            "deliverable_id",
            "quality_gate_id",
        ]:
            with self.subTest(field=field):
                self.assertIn(field, self.text)

    def test_lifecycle_models_failure_and_remediation_states(self) -> None:
        for state in [
            "Missing required documents",
            "Official source not found",
            "Low confidence extraction",
            "Quality gate failed",
            "Human review rejected",
            "Intake remediation",
        ]:
            with self.subTest(state=state):
                self.assertIn(state, self.text)

    def test_architecture_tree_has_no_placeholder_ellipsis(self) -> None:
        self.assertNotIn("\n      ...\n", self.text)


if __name__ == "__main__":
    unittest.main()
