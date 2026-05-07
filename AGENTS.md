# Legal-FR Suite - Agent Instructions

## Role

This repository is the Legal-FR plugin suite for French legal workflows. Agents assist legal professionals; they do not replace qualified professional review.

## Mandatory Legal Posture

- Every external-facing output must include `DRAFT - Validation professionnelle requise`.
- Human validation is mandatory before client, regulator, counterparty, filing, or external use.
- Do not present legal conclusions as final advice.
- Mark uncertain points as `A VERIFIER`.
- Cite legal sources for critical conclusions.

## Source Discipline

- Use OpenLegi before Parallel for French positive law.
- OpenLegi avant Parallel is the default research order for Legal-FR workflows.
- Use Exa and Parallel CLI for public web research, source discovery, secondary context, enrichment, and veille.
- Use `parallel-cli` only with `--json` in Legal-FR research commands.
- Treat Parallel Task API as a second backend layer, not a replacement for local Cowork CLI workflows.
- Keep `jurisprudence-multilingue` for multilingual, comparative, CJUE/CEDH, and translation workflows.

## Security And Secrets

- Never hardcode `OPENLEGI_TOKEN` or `PARALLEL_API_KEY`.
- Do not expose environment variables in generated reports.
- Do not reintroduce `legacy anonymization MCP`.
- Do not send raw confidential client data to public web research tools.

## Development Workflow

- Edit Legal-FR generation logic in `scripts/generate_legal_fr_scaffold.py` when changing generated plugin assets.
- Active marketplace entries live in `.claude-plugin/marketplace.json`.
- Project Claude settings live in `.claude/settings.json` and register `jamon8888/droit-cowork` as the Legal-FR marketplace source.
- Financial Services origin assets are archived under `archive/financial-services-origin/` and are not active plugin surface.

## Required Verification

Run before claiming completion:

```bash
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures tests.test_legal_fr_clean_repo -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
python scripts/check_legal_fr_parallel_task_api.py
```
