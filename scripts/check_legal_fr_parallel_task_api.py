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
