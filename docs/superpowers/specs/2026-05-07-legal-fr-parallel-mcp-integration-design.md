# Legal-FR Parallel MCP Integration Design

## Context

Legal-FR already has three web/research layers:

- `OpenLegi MCP` for official French legal sources.
- `Parallel CLI` for local Cowork execution, JSON-first searches, extraction, enrichment and monitoring.
- `Parallel Task API` as a backend second layer for long-running batch research.

The official Parallel MCP documentation adds a missing fourth integration surface:

- Parallel MCP Quickstart: https://docs.parallel.ai/integrations/mcp/quickstart
- Parallel Search MCP: https://docs.parallel.ai/integrations/mcp/search-mcp
- Parallel Task MCP: https://docs.parallel.ai/integrations/mcp/task-mcp

## Decision

Add Parallel MCP to Legal-FR as an optional connector layer, without replacing the existing CLI or Task API paths.

The connector hierarchy becomes:

1. `OpenLegi MCP`: first source for French positive law.
2. `Parallel Search MCP`: fast web search and URL fetch inside Claude Desktop/Cowork.
3. `Parallel CLI`: deterministic local/scriptable path with `--json`, used by commands and evals.
4. `Parallel Task MCP`: optional authenticated chat-client layer for deep research and task groups.
5. `Parallel Task API`: backend automation layer for production batch workflows.

## MCP Servers

Legal-FR should add two Parallel MCP entries:

```json
{
  "mcpServers": {
    "parallel-search": {
      "type": "http",
      "url": "https://search.parallel.ai/mcp"
    },
    "parallel-task": {
      "type": "http",
      "url": "https://task-mcp.parallel.ai/mcp",
      "headers": {
        "Authorization": "Bearer ${PARALLEL_API_KEY}"
      },
      "optional": true
    }
  }
}
```

`parallel-search` is safe as a default optional research aid because the Search MCP is documented as free anonymous for light use. `parallel-task` must remain authenticated and optional because the Task MCP always requires OAuth or a Parallel API key.

## Legal-FR Usage Rules

- OpenLegi remains mandatory before Parallel for French positive-law conclusions.
- Parallel Search MCP can discover web sources and fetch URLs, but its findings are `secondary` or `unverified` until confirmed by an official source.
- Parallel Task MCP is for longer research or data enrichment in interactive clients; it does not replace the CLI path used by scripts and tests.
- No API key value may be written into the repo, docs, generated skills, command outputs or eval fixtures.
- If `PARALLEL_API_KEY` is absent, connector validation should pass with a warning for optional `parallel-task`, not fail the whole Legal-FR scaffold.

## Documentation Updates

Update:

- `plugins/vertical-plugins/legal-fr/.mcp.json`
- `plugins/vertical-plugins/legal-fr/CONNECTORS.md`
- `plugins/vertical-plugins/legal-fr/skills/parallel-recherche-juridique-fr/SKILL.md`
- `plugins/agent-plugins/recherche-juridique-fr-avancee/skills/parallel-recherche-juridique-fr/SKILL.md`
- `scripts/generate_legal_fr_scaffold.py`
- `scripts/check_legal_fr_connectors.py`
- `tests/test_legal_fr_production_grade.py`

## Validation

Required local checks:

- `python scripts/check.py`
- `python -m unittest tests.test_legal_fr_production_grade -v`
- `python scripts/check_legal_fr_connectors.py`
- `python scripts/check_legal_fr_connectors.py --online`
- `python scripts/run_legal_fr_evals.py`

Expected warnings:

- Missing `OPENLEGI_TOKEN` warns but does not fail offline connector validation.
- Missing `PARALLEL_API_KEY` warns for optional `parallel-task` but does not fail connector validation.

## Self-Review

- The document is complete and contains no unresolved markers.
- The design does not replace the existing CLI or Task API layers.
- The source hierarchy keeps OpenLegi first for French legal conclusions.
- The optional authenticated Task MCP path avoids hardcoded secrets.
