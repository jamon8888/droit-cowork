import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "legal_fr_workflow.py"


def run_cli(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


class LegalFrWorkflowRunnerTest(unittest.TestCase):
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
            run_dir = Path(response["run_dir"])
            state = json.loads((run_dir / "workflow-run.json").read_text(encoding="utf-8"))
            ledger = json.loads((run_dir / "source-ledger.json").read_text(encoding="utf-8"))
            queue = json.loads((run_dir / "review-queue.json").read_text(encoding="utf-8"))

            self.assertEqual(state["schema_version"], "2.0.0")
            self.assertEqual(state["playbook_id"], "workflow-dd-ma")
            self.assertEqual(state["status"], "initialized")
            self.assertEqual(state["current_stage"], "intake")
            self.assertEqual(state["failure_state"], "none")
            self.assertFalse(state["full_run_requested"])
            self.assertEqual(state["document_inventory"], ["data-room/contrats/MSA-A.md"])
            self.assertEqual(ledger, [])
            self.assertEqual(queue, [])

    def test_run_advances_one_stage_by_default_and_blocks_full_run_on_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            init = run_cli(
                "init",
                "--playbook",
                "workflow-dd-ma",
                "--matter",
                "Acquisition PME industrielle",
                "--objective",
                "Audit acheteur",
                "--document",
                "data-room/contrats/MSA-A.md",
                "--workdir",
                tmp,
            )
            self.assertEqual(init.returncode, 0, init.stderr + init.stdout)
            run_dir = Path(json.loads(init.stdout)["run_dir"])

            first_step = run_cli("run", "--run-dir", str(run_dir))
            self.assertEqual(first_step.returncode, 0, first_step.stderr + first_step.stdout)
            first_state = json.loads((run_dir / "workflow-run.json").read_text(encoding="utf-8"))
            self.assertEqual(first_state["current_stage"], "extract")
            self.assertEqual(first_state["status"], "running")
            self.assertFalse(first_state["full_run_requested"])

            full_run = run_cli("run", "--run-dir", str(run_dir), "--full")
            self.assertEqual(full_run.returncode, 0, full_run.stderr + full_run.stdout)
            final_state = json.loads((run_dir / "workflow-run.json").read_text(encoding="utf-8"))
            queue = json.loads((run_dir / "review-queue.json").read_text(encoding="utf-8"))

            self.assertEqual(final_state["status"], "blocked")
            self.assertEqual(final_state["current_stage"], "review")
            self.assertTrue(final_state["full_run_requested"])
            self.assertEqual(final_state["failure_state"], "blocked_until_validated")
            self.assertEqual(queue[0]["quality_gate_id"], "quality_gate_id:workflow-dd-ma-human")

    def test_run_rejects_corrupted_workflow_state_before_transition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            init = run_cli(
                "init",
                "--playbook",
                "workflow-dd-ma",
                "--matter",
                "Acquisition PME industrielle",
                "--objective",
                "Audit acheteur",
                "--document",
                "data-room/contrats/MSA-A.md",
                "--workdir",
                tmp,
            )
            self.assertEqual(init.returncode, 0, init.stderr + init.stdout)
            run_dir = Path(json.loads(init.stdout)["run_dir"])
            state_path = run_dir / "workflow-run.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            del state["playbook_id"]
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

            result = run_cli("run", "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 1)
            self.assertIn("workflow-run.schema.json", result.stderr)
            self.assertIn("playbook_id", result.stderr)

    def test_export_rejects_corrupted_review_queue_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            init = run_cli(
                "init",
                "--playbook",
                "workflow-dd-ma",
                "--matter",
                "Acquisition PME industrielle",
                "--objective",
                "Audit acheteur",
                "--document",
                "data-room/contrats/MSA-A.md",
                "--workdir",
                tmp,
            )
            self.assertEqual(init.returncode, 0, init.stderr + init.stdout)
            run_dir = Path(json.loads(init.stdout)["run_dir"])
            self.assertEqual(run_cli("run", "--run-dir", str(run_dir), "--full").returncode, 0)
            queue_path = run_dir / "review-queue.json"
            queue = json.loads(queue_path.read_text(encoding="utf-8"))
            queue[0]["status"] = "approved-but-not-schema-valid"
            queue_path.write_text(json.dumps(queue, indent=2) + "\n", encoding="utf-8")

            result = run_cli("export", "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 1)
            self.assertIn("review-queue.schema.json", result.stderr)
            self.assertIn("approved-but-not-schema-valid", result.stderr)

    def test_eval_reports_all_workflow_playbooks_and_required_schemas(self) -> None:
        result = run_cli("eval")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        response = json.loads(result.stdout)
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["playbooks_checked"], 6)
        self.assertIn("workflow-dd-ma", response["playbooks"])


if __name__ == "__main__":
    unittest.main()
