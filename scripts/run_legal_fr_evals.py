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


def score_expected_output(expected: Any) -> list[str]:
    failures: list[str] = []

    if not isinstance(expected, dict):
        return ["expected root must be an object"]

    if expected.get("draft_notice") != DRAFT_NOTICE:
        failures.append(f"draft_notice must be {DRAFT_NOTICE!r}")

    human_validation = expected.get("human_validation")
    if not isinstance(human_validation, dict):
        failures.append("human_validation missing or not an object")
    elif human_validation.get("validated_by_human") is not False:
        failures.append("human_validation.validated_by_human must be False")

    if not isinstance(expected.get("document_intake"), dict):
        failures.append("document_intake missing or not an object")
    if not isinstance(expected.get("coverage"), dict):
        failures.append("coverage missing or not an object")

    findings = expected.get("findings")
    if not isinstance(findings, list) or not findings:
        failures.append("missing findings")
    else:
        for index, finding in enumerate(findings, start=1):
            finding_prefix = f"findings[{index}]"
            if not isinstance(finding, dict):
                failures.append(f"{finding_prefix} must be an object")
                continue

            source_citation = finding.get("source_citation")
            if not isinstance(source_citation, dict):
                failures.append(f"{finding_prefix}.source_citation must be an object")
            elif source_citation.get("source_status") not in ALLOWED_SOURCE_STATUSES:
                failures.append(
                    f"{finding_prefix}.source_citation.source_status must be one of "
                    f"{sorted(ALLOWED_SOURCE_STATUSES)}"
                )

            risk_score = finding.get("risk_score")
            if not isinstance(risk_score, dict):
                failures.append(f"{finding_prefix}.risk_score must be an object")
            elif not is_confidence(risk_score.get("confidence")):
                failures.append(f"{finding_prefix}.risk_score.confidence must be a number from 0 to 1")

    if not isinstance(expected.get("audit_trail"), list) or not expected.get("audit_trail"):
        failures.append("missing audit trail")

    return failures


def validate_expected(path: Path) -> list[str]:
    try:
        expected = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel(path)}: invalid JSON: {exc}"]

    prefix = rel(path)
    failures = score_expected_output(expected)
    if failures:
        return [f"{prefix}: {failure}" for failure in failures]
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
