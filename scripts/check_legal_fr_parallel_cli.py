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
INSTALL_GUIDANCE = [
    'Install recommended for agent skills: pipx install "parallel-web-tools[cli]" && pipx ensurepath',
    'Alternative with uv: uv tool install "parallel-web-tools[cli]"',
    "Alternative with npm: npm install -g parallel-web-cli",
    "Authenticate headless/Cowork: parallel-cli login --device",
    "Authenticate with environment: set PARALLEL_API_KEY in the user environment, never in repo files",
    "Verify auth: parallel-cli auth --json",
]


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
        if any("parallel-cli is not installed" in message for message in errors):
            print("\nInstallation options:")
            for guidance in INSTALL_GUIDANCE:
                print(f"- {guidance}")
        return 1

    if "PARALLEL_API_KEY" not in os.environ:
        print(TOKEN_WARN)
    print(OK_MESSAGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
