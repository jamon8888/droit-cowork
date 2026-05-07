#!/usr/bin/env python3
"""Validate Legal-FR MCP connector config without making network calls."""

from __future__ import annotations

import json
import os
import argparse
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
MCP_CONFIG = ROOT / "plugins" / "vertical-plugins" / "legal-fr" / ".mcp.json"
EXA_ENDPOINT = "https://mcp.exa.ai/mcp"
OPENLEGI_DOCS_URL = "https://www.openlegi.fr/documentation/"
OPENLEGI_HEALTH_URL = "https://mcp.openlegi.fr/health"
OPENLEGI_MCP_ENDPOINT = "https://mcp.openlegi.fr/legifrance/mcp?token=${OPENLEGI_TOKEN}"
OPENLEGI_TOKEN_REF = "${OPENLEGI_TOKEN}"
OPENLEGI_TOKEN_WARN = (
    "WARN: OPENLEGI_TOKEN is not set; runtime OpenLegi calls will fail until configured."
)
OK_MESSAGE = "Legal-FR connector config OK"
OPENLEGI_HEALTH_OK = "OpenLegi health OK"


def error(message: str) -> str:
    return f"ERROR: {message}"


def load_config(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.is_file():
        return None, [error(f"{path.relative_to(ROOT)} is missing")]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [error(f"{path.relative_to(ROOT)} is malformed JSON: {exc}")]
    if not isinstance(data, dict):
        return None, [error(f"{path.relative_to(ROOT)} must contain a JSON object")]
    return data, []


def get_servers(config: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    servers = config.get("mcpServers")
    if not isinstance(servers, dict):
        return None, [error("plugins/vertical-plugins/legal-fr/.mcp.json must define mcpServers")]
    return servers, []


def server_named(servers: dict[str, Any], name: str) -> dict[str, Any] | None:
    for key, value in servers.items():
        if key.lower() == name and isinstance(value, dict):
            return value
    return None


def contains_token_ref(value: Any) -> bool:
    if isinstance(value, str):
        return OPENLEGI_TOKEN_REF in value
    if isinstance(value, list):
        return any(contains_token_ref(item) for item in value)
    if isinstance(value, dict):
        return any(contains_token_ref(item) for item in value.values())
    return False


def validate(config: dict[str, Any]) -> list[str]:
    servers, errors = get_servers(config)
    if servers is None:
        return errors

    exa = server_named(servers, "exa")
    if exa is None:
        errors.append(error("Exa MCP entry is missing"))
    else:
        endpoint = exa.get("url", exa.get("endpoint"))
        if endpoint != EXA_ENDPOINT:
            errors.append(error(f"Exa MCP endpoint must be exactly {EXA_ENDPOINT}"))

    openlegi = server_named(servers, "openlegi")
    if openlegi is None:
        errors.append(error("OpenLegi MCP entry is missing"))
    elif not contains_token_ref(openlegi):
        errors.append(error(f"OpenLegi MCP config must contain {OPENLEGI_TOKEN_REF}"))

    return errors


def validate_openlegi_health() -> list[str]:
    try:
        with urlopen(OPENLEGI_HEALTH_URL, timeout=20) as response:
            raw = response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as exc:
        return [error(f"OpenLegi health check failed: {exc}")]

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [error(f"OpenLegi health response is not JSON: {exc}")]

    services = payload.get("services")
    if payload.get("status") != "ok":
        return [error(f"OpenLegi health status is not ok: {payload.get('status')}")]
    if not isinstance(services, dict) or services.get("legifrance") is not True:
        return [error("OpenLegi health does not report legifrance=true")]
    return []


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Legal-FR MCP connector config. Offline by default; use --online for OpenLegi health."
    )
    parser.add_argument(
        "--online",
        action="store_true",
        help=f"Call {OPENLEGI_HEALTH_URL}; does not use OPENLEGI_TOKEN and should not consume MCP quota.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    config, errors = load_config(MCP_CONFIG)
    if config is not None:
        errors.extend(validate(config))
    if args.online:
        errors.extend(validate_openlegi_health())

    if errors:
        for message in errors:
            print(message)
        return 1

    if "OPENLEGI_TOKEN" not in os.environ:
        print(OPENLEGI_TOKEN_WARN)
    if args.online:
        print(OPENLEGI_HEALTH_OK)
    print(OK_MESSAGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
