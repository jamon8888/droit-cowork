#!/usr/bin/env python3
"""Operate Legal-FR Playbook V2 workflow runs with local JSON state."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEGAL_FR = ROOT / "plugins" / "vertical-plugins" / "legal-fr"
PLAYBOOK_ROOT = LEGAL_FR / "playbooks" / "workflows"
SCHEMA_ROOT = LEGAL_FR / "schemas"
COMMON_SCHEMA_ROOT = SCHEMA_ROOT / "common"
WORKFLOW_SCHEMA_ROOT = SCHEMA_ROOT / "workflows"
DRAFT_NOTICE = "DRAFT - Validation professionnelle requise"
STAGES = ["intake", "extract", "source", "risk", "review", "export"]
REQUIRED_PLAYBOOK_FIELDS = [
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
COMMON_SCHEMAS = [
    "workflow-run.schema.json",
    "source-ledger.schema.json",
    "review-queue.schema.json",
    "audit-trail.schema.json",
    "human-validation.schema.json",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class SchemaValidationError(ValueError):
    """Raised when local Legal-FR workflow JSON does not match its schema."""


def load_schema(schema_path: Path) -> dict[str, Any]:
    schema = load_json(schema_path)
    if not isinstance(schema, dict):
        raise SchemaValidationError(f"{schema_path.name}: schema must be a JSON object")
    return schema


def resolve_ref(ref_value: str, schema_path: Path) -> Path:
    if ref_value.startswith("../../common/") or ref_value.startswith("../common/"):
        return COMMON_SCHEMA_ROOT / Path(ref_value).name
    if ref_value.endswith(".schema.json"):
        return COMMON_SCHEMA_ROOT / Path(ref_value).name
    return (schema_path.parent / ref_value).resolve()


def type_matches(expected: str, value: Any) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    return True


def validate_against_schema(payload: Any, schema: dict[str, Any], schema_path: Path, location: str = "$") -> None:
    if "$ref" in schema:
        referenced_path = resolve_ref(str(schema["$ref"]), schema_path)
        validate_against_schema(payload, load_schema(referenced_path), referenced_path, location)
        return

    if "const" in schema and payload != schema["const"]:
        raise SchemaValidationError(f"{schema_path.name}: {location} must equal {schema['const']!r}, got {payload!r}")

    if "enum" in schema and payload not in schema["enum"]:
        raise SchemaValidationError(f"{schema_path.name}: {location} has invalid value {payload!r}")

    expected_type = schema.get("type")
    if expected_type and not type_matches(str(expected_type), payload):
        raise SchemaValidationError(f"{schema_path.name}: {location} must be {expected_type}, got {type(payload).__name__}")

    if expected_type == "object":
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in payload:
                raise SchemaValidationError(f"{schema_path.name}: {location}.{key} is required")
        if schema.get("additionalProperties") is False:
            for key in payload:
                if key not in properties:
                    raise SchemaValidationError(f"{schema_path.name}: {location}.{key} is not allowed")
        for key, subschema in properties.items():
            if key in payload:
                validate_against_schema(payload[key], subschema, schema_path, f"{location}.{key}")

    if expected_type == "array":
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(payload):
                validate_against_schema(item, item_schema, schema_path, f"{location}[{index}]")


def validate_common_payload(schema_name: str, payload: Any) -> None:
    schema_path = COMMON_SCHEMA_ROOT / schema_name
    validate_against_schema(payload, load_schema(schema_path), schema_path)


def validate_pack_payload(playbook_id: str, schema_name: str, payload: Any) -> None:
    schema_path = WORKFLOW_SCHEMA_ROOT / playbook_id / schema_name
    validate_against_schema(payload, load_schema(schema_path), schema_path)


def validate_run_payloads(state: dict[str, Any], source_ledger: list[Any], review_queue: list[Any], audit_trail: list[Any]) -> None:
    validate_common_payload("workflow-run.schema.json", state)
    for item in source_ledger:
        validate_common_payload("source-ledger.schema.json", item)
    for item in review_queue:
        validate_common_payload("review-queue.schema.json", item)
    for item in audit_trail:
        validate_common_payload("audit-trail.schema.json", item)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path.name} has no frontmatter")
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def playbook_path(playbook_id: str) -> Path:
    path = PLAYBOOK_ROOT / f"{playbook_id}.md"
    if not path.is_file():
        raise ValueError(f"unknown Legal-FR workflow playbook: {playbook_id}")
    return path


def playbook_text(playbook_id: str) -> str:
    return playbook_path(playbook_id).read_text(encoding="utf-8")


def audit_entry(playbook_id: str, run_id: str, stage: str, note: str) -> dict[str, Any]:
    human_validation = {
        "validated_by_human": False,
        "validator_role": "avocat ou juriste senior",
        "validation_required": True,
        "validation_reason": "Workflow Legal-FR local runner state transition.",
    }
    legal_source = {
        "source_status": "unverified",
        "citation": "",
        "url": "",
        "checked_with": "none",
        "verification_note": note,
    }
    return {
        "finding_id": f"{run_id}-{stage}",
        "workflow": playbook_id,
        "document_id": "workflow-state",
        "source_excerpt": note,
        "legal_source": legal_source,
        "agent": "legal-fr-workflow-runner",
        "reviewer": "legal-qa-reviewer",
        "confidence": 1.0,
        "human_validation": human_validation,
    }


def review_item(playbook_id: str, run_id: str, quality_gate_id: str, action: str, status: str = "blocked") -> dict[str, Any]:
    return {
        "review_item_id": f"{run_id}-{quality_gate_id}",
        "playbook_id": playbook_id,
        "run_id": run_id,
        "finding_id": f"{run_id}-{quality_gate_id}",
        "quality_gate_id": quality_gate_id,
        "severity": "blocking",
        "owner_role": "avocat ou juriste senior",
        "action": action,
        "status": status,
        "human_validation": {
            "validated_by_human": status == "validated",
            "validator_role": "avocat ou juriste senior",
            "validation_required": status != "validated",
            "validation_reason": action,
        },
    }


def run_dir_from_args(path: str) -> Path:
    run_dir = Path(path).resolve()
    if not run_dir.is_dir():
        raise ValueError(f"run directory not found: {run_dir}")
    return run_dir


def load_run(run_dir: Path) -> tuple[dict[str, Any], list[Any], list[Any], list[Any]]:
    state = load_json(run_dir / "workflow-run.json")
    source_ledger = load_json(run_dir / "source-ledger.json")
    review_queue = load_json(run_dir / "review-queue.json")
    audit_trail = load_json(run_dir / "audit-trail.json")
    validate_run_payloads(state, source_ledger, review_queue, audit_trail)
    return state, source_ledger, review_queue, audit_trail


def save_run(run_dir: Path, state: dict[str, Any], source_ledger: list[Any], review_queue: list[Any], audit_trail: list[Any]) -> None:
    state["audit_trail"] = audit_trail
    validate_run_payloads(state, source_ledger, review_queue, audit_trail)
    write_json(run_dir / "workflow-run.json", state)
    write_json(run_dir / "source-ledger.json", source_ledger)
    write_json(run_dir / "review-queue.json", review_queue)
    write_json(run_dir / "audit-trail.json", audit_trail)


def command_init(args: argparse.Namespace) -> int:
    path = playbook_path(args.playbook)
    metadata = parse_frontmatter(path)
    if metadata.get("schema_version") != "2.0.0":
        raise ValueError(f"{args.playbook} must use schema_version 2.0.0")

    run_id = f"lfr-{uuid.uuid4().hex[:12]}"
    run_dir = (Path(args.workdir).resolve() / run_id)
    documents = list(args.document or [])
    missing_docs = not documents
    audit_trail = [
        audit_entry(args.playbook, run_id, "intake", "Initialized Legal-FR workflow run.")
    ]
    review_queue = []
    if missing_docs:
        review_queue.append(
            review_item(
                args.playbook,
                run_id,
                f"quality_gate_id:{args.playbook}-intake",
                "Ajouter au moins un document ou une reference corpus avant execution.",
            )
        )

    state = {
        "run_id": run_id,
        "schema_version": "2.0.0",
        "playbook_id": args.playbook,
        "status": "blocked" if missing_docs else "initialized",
        "current_stage": "intake",
        "full_run_requested": False,
        "intake": {
            "matter": args.matter,
            "objective": args.objective,
            "draft_notice": DRAFT_NOTICE,
        },
        "document_inventory": documents,
        "audit_trail": audit_trail,
        "quality_gate_status": "failed" if missing_docs else "passed",
        "failure_state": "missing_document" if missing_docs else "none",
        "blocked_reason": "document_inventory is empty" if missing_docs else "",
        "remediation_required": missing_docs,
    }
    save_run(run_dir, state, [], review_queue, audit_trail)
    print(json.dumps({"status": state["status"], "run_dir": str(run_dir), "run_id": run_id}))
    return 0


def source_ledger_entry(playbook_id: str, run_id: str) -> dict[str, Any]:
    return {
        "ledger_id": f"{run_id}-source-001",
        "playbook_id": playbook_id,
        "run_id": run_id,
        "finding_id": f"{run_id}-source-check",
        "source_status": "unverified",
        "source_locator": "",
        "source_excerpt": "Source verification pending in local runner.",
        "checked_with": "none",
        "confidence": 0.5,
        "gap_reason": "Runtime source lookup must be completed by workflow agent or connector.",
    }


def advance_one(state: dict[str, Any], source_ledger: list[Any], review_queue: list[Any], audit_trail: list[Any]) -> bool:
    if state["remediation_required"] and state["failure_state"] != "none":
        state["status"] = "blocked"
        return False

    stage = state["current_stage"]
    playbook_id = state["playbook_id"]
    run_id = state["run_id"]
    if stage == "intake":
        state["current_stage"] = "extract"
        state["status"] = "running"
        state["quality_gate_status"] = "passed"
        audit_trail.append(audit_entry(playbook_id, run_id, "extract", "Advanced to extraction stage."))
        return True
    if stage == "extract":
        state["current_stage"] = "source"
        audit_trail.append(audit_entry(playbook_id, run_id, "source", "Advanced to source-ledger stage."))
        if not source_ledger:
            source_ledger.append(source_ledger_entry(playbook_id, run_id))
        return True
    if stage == "source":
        state["current_stage"] = "risk"
        audit_trail.append(audit_entry(playbook_id, run_id, "risk", "Advanced to risk scoring stage."))
        return True
    if stage == "risk":
        state["current_stage"] = "review"
        state["status"] = "blocked"
        state["quality_gate_status"] = "failed"
        state["failure_state"] = "blocked_until_validated"
        state["blocked_reason"] = "Human validation is required before export."
        state["remediation_required"] = True
        review_queue.append(
            review_item(
                playbook_id,
                run_id,
                f"quality_gate_id:{playbook_id}-human",
                "Valider humainement les findings et sources avant export.",
            )
        )
        audit_trail.append(audit_entry(playbook_id, run_id, "review", "Blocked for human validation."))
        return False
    if stage in {"review", "export"}:
        state["status"] = "blocked" if stage == "review" else state["status"]
        state["failure_state"] = "blocked_until_validated"
        state["blocked_reason"] = "Human validation is required before export."
        state["remediation_required"] = True
        return False
    raise ValueError(f"unknown workflow stage: {stage}")


def command_run(args: argparse.Namespace) -> int:
    run_dir = run_dir_from_args(args.run_dir)
    state, source_ledger, review_queue, audit_trail = load_run(run_dir)
    state["full_run_requested"] = bool(args.full)

    advanced = advance_one(state, source_ledger, review_queue, audit_trail)
    while args.full and advanced:
        advanced = advance_one(state, source_ledger, review_queue, audit_trail)

    save_run(run_dir, state, source_ledger, review_queue, audit_trail)
    print(json.dumps({"status": state["status"], "current_stage": state["current_stage"], "run_dir": str(run_dir)}))
    return 0


def command_review(args: argparse.Namespace) -> int:
    run_dir = run_dir_from_args(args.run_dir)
    state, source_ledger, review_queue, audit_trail = load_run(run_dir)
    if not args.validate:
        print(json.dumps({"status": state["status"], "review_items": len(review_queue), "run_dir": str(run_dir)}))
        return 0

    for item in review_queue:
        item["status"] = "validated"
        item["human_validation"]["validated_by_human"] = True
        item["human_validation"]["validation_required"] = False
        item["human_validation"]["validation_reason"] = "Validated by explicit local runner --validate action."
    state["status"] = "validated"
    state["failure_state"] = "none"
    state["blocked_reason"] = ""
    state["remediation_required"] = False
    state["quality_gate_status"] = "passed"
    audit_trail.append(audit_entry(state["playbook_id"], state["run_id"], "review", "Human validation recorded by local runner."))
    save_run(run_dir, state, source_ledger, review_queue, audit_trail)
    print(json.dumps({"status": state["status"], "review_items": len(review_queue), "run_dir": str(run_dir)}))
    return 0


def command_export(args: argparse.Namespace) -> int:
    run_dir = run_dir_from_args(args.run_dir)
    state, source_ledger, review_queue, audit_trail = load_run(run_dir)
    if state["status"] != "validated":
        state["status"] = "blocked"
        state["failure_state"] = "blocked_until_validated"
        state["blocked_reason"] = "Export requires validated workflow state."
        state["remediation_required"] = True
        save_run(run_dir, state, source_ledger, review_queue, audit_trail)
        print(json.dumps({"status": "blocked", "reason": state["blocked_reason"], "run_dir": str(run_dir)}))
        return 0

    deliverables = {
        "playbook_id": state["playbook_id"],
        "schema_version": "2.0.0",
        "workflow_run": state,
        "source_ledger": source_ledger,
        "review_queue": review_queue,
        "audit_trail": audit_trail,
        "human_validation": {
            "validated_by_human": True,
            "validator_role": "avocat ou juriste senior",
            "validation_required": False,
            "validation_reason": "Validated workflow state.",
        },
        "deliverables": [
            {
                "deliverable_id": f"deliverable_id:{state['playbook_id']}-local-export",
                "path": str(run_dir / "deliverables.json"),
                "status": "exported",
            }
        ],
        "draft_notice": DRAFT_NOTICE,
    }
    state["status"] = "exported"
    state["current_stage"] = "export"
    validate_pack_payload(state["playbook_id"], "deliverables.schema.json", deliverables)
    write_json(run_dir / "deliverables.json", deliverables)
    save_run(run_dir, state, source_ledger, review_queue, audit_trail)
    print(json.dumps({"status": "exported", "deliverables": str(run_dir / "deliverables.json"), "run_dir": str(run_dir)}))
    return 0


def workflow_playbooks() -> list[Path]:
    return sorted(PLAYBOOK_ROOT.glob("workflow-*.md"))


def command_eval(args: argparse.Namespace) -> int:
    errors: list[str] = []
    playbooks = workflow_playbooks()
    for schema in COMMON_SCHEMAS:
        if not (COMMON_SCHEMA_ROOT / schema).is_file():
            errors.append(f"missing common schema: {schema}")
    for path in playbooks:
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(path)
        playbook_id = metadata.get("playbook_id", "")
        if metadata.get("schema_version") != "2.0.0":
            errors.append(f"{path.name}: schema_version must be 2.0.0")
        if playbook_id != path.stem:
            errors.append(f"{path.name}: playbook_id must match filename")
        for field in REQUIRED_PLAYBOOK_FIELDS:
            if field not in text:
                errors.append(f"{path.name}: missing {field}")
        for schema_name in ["run.schema.json", "deliverables.schema.json"]:
            if not (WORKFLOW_SCHEMA_ROOT / path.stem / schema_name).is_file():
                errors.append(f"{path.stem}: missing workflow schema {schema_name}")
    if errors:
        print(json.dumps({"status": "error", "errors": errors}))
        return 1
    print(
        json.dumps(
            {
                "status": "ok",
                "playbooks_checked": len(playbooks),
                "playbooks": [path.stem for path in playbooks],
                "checked_at": utc_now(),
            }
        )
    )
    return 0


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

    run = subcommands.add_parser("run")
    run.add_argument("--run-dir", required=True)
    run.add_argument("--full", action="store_true")
    run.set_defaults(func=command_run)

    review = subcommands.add_parser("review")
    review.add_argument("--run-dir", required=True)
    review.add_argument("--validate", action="store_true")
    review.set_defaults(func=command_review)

    export = subcommands.add_parser("export")
    export.add_argument("--run-dir", required=True)
    export.set_defaults(func=command_export)

    eval_command = subcommands.add_parser("eval")
    eval_command.set_defaults(func=command_eval)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
