#!/usr/bin/env python3
"""Run Legal-FR Parallel Task API jobs with schema-backed JSON I/O."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "plugins" / "vertical-plugins" / "legal-fr" / "schemas" / "parallel-task"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def require_api_key() -> str:
    token = os.environ.get("PARALLEL_API_KEY")
    if not token:
        raise RuntimeError("PARALLEL_API_KEY is required for Parallel Task API calls")
    return token


def command_run(args: argparse.Namespace) -> int:
    require_api_key()
    payload = load_json(Path(args.input))
    result = {
        "status": "not_executed",
        "reason": "Network Task API execution is intentionally not implemented in the scaffold.",
        "workflow": args.workflow,
        "input": payload,
        "processor": args.processor,
        "schema_root": str(SCHEMA_ROOT.relative_to(ROOT)),
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "not_executed", "output": args.output}))
    return 0


def command_status(args: argparse.Namespace) -> int:
    require_api_key()
    print(json.dumps({"run_id": args.run_id, "status": "not_executed"}))
    return 0


def command_poll(args: argparse.Namespace) -> int:
    require_api_key()
    result = {"run_id": args.run_id, "status": "not_executed"}
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subcommands = root.add_subparsers(dest="command", required=True)

    run = subcommands.add_parser("run")
    run.add_argument("--workflow", required=True)
    run.add_argument("--input", required=True)
    run.add_argument("--processor", default="pro")
    run.add_argument("--output", required=True)
    run.set_defaults(func=command_run)

    status = subcommands.add_parser("status")
    status.add_argument("--run-id", required=True)
    status.set_defaults(func=command_status)

    poll = subcommands.add_parser("poll")
    poll.add_argument("--run-id", required=True)
    poll.add_argument("--output")
    poll.set_defaults(func=command_poll)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
