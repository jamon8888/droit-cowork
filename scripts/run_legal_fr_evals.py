#!/usr/bin/env python3
"""Offline validation runner for Legal-FR expected eval outputs."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ROOT = ROOT / "plugins" / "vertical-plugins" / "legal-fr" / "evals" / "expected"
DRAFT_NOTICE = "DRAFT - Validation professionnelle requise"
ALLOWED_SOURCE_STATUSES = {"official", "secondary", "web", "unverified", "not_found"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def is_confidence(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 1


def validate_expected(path: Path) -> list[str]:
    failures: list[str] = []

    try:
        expected = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel(path)}: invalid JSON: {exc}"]

    prefix = rel(path)
    if expected.get("draft_notice") != DRAFT_NOTICE:
        failures.append(f"{prefix}: draft_notice must be {DRAFT_NOTICE!r}")
    if "findings" not in expected:
        failures.append(f"{prefix}: findings is missing")
    if "audit_trail" not in expected:
        failures.append(f"{prefix}: audit_trail is missing")
    if expected.get("human_validation", {}).get("validated_by_human") is not False:
        failures.append(f"{prefix}: human_validation.validated_by_human must be False")
    if "document_intake" not in expected:
        failures.append(f"{prefix}: document_intake is missing")
    if "coverage" not in expected:
        failures.append(f"{prefix}: coverage is missing")

    findings = expected.get("findings")
    if not isinstance(findings, list):
        failures.append(f"{prefix}: findings must be a list")
        return failures

    for index, finding in enumerate(findings, start=1):
        finding_prefix = f"{prefix}: findings[{index}]"
        if not isinstance(finding, dict):
            failures.append(f"{finding_prefix} must be an object")
            continue

        source_status = finding.get("source_citation", {}).get("source_status")
        if source_status not in ALLOWED_SOURCE_STATUSES:
            failures.append(
                f"{finding_prefix}.source_citation.source_status must be one of "
                f"{sorted(ALLOWED_SOURCE_STATUSES)}"
            )

        confidence = finding.get("risk_score", {}).get("confidence")
        if not is_confidence(confidence):
            failures.append(f"{finding_prefix}.risk_score.confidence must be a number from 0 to 1")

    return failures


def main() -> int:
    expected_files = sorted(EXPECTED_ROOT.glob("*/*.expected.json"))
    if not expected_files:
        print("No Legal-FR eval expected files found")
        return 1

    failures: list[str] = []
    for expected_file in expected_files:
        failures.extend(validate_expected(expected_file))

    if failures:
        print("Legal-FR evals failed")
        for failure in failures:
            print(failure)
        return 1

    print(f"Legal-FR evals passed: {len(expected_files)} expected outputs checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
