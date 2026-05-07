# Legal-FR

Legal-FR is a vertical juridique francais for Legora-FR workflows, enriched by Harvey-FR patterns and adapted to cabinet practice. It packages reusable commands, skills, schemas, eval fixtures, source-checking conventions, and MCP connector definitions for French legal drafting and review workflows.

Every external deliverable produced from this vertical is a draft for professional review, not a final legal opinion or client-ready work product.

## Cabinet-Grade Assets

- Schemas: common and workflow-specific JSON schemas define intake, source citations, findings, risk scores, audit trails, human validation, extraction outputs, and report outputs.
- Evals: fixture inputs, expected JSON outputs, rubrics, and a local runner cover compliant cases, blocking red flags, current-law uncertainty, incomplete documents, and missing sources.
- Audit trail: each material finding should preserve the source excerpt, source status, confidence, and reviewer note needed for cabinet review.
- Quality gates: outputs must pass legal quality checks before delivery, including source coverage, structured fields, confidence handling, draft status, and human validation metadata.
- Connector verification: OpenLegi is required for French positive law and Exa is required for broader research; `scripts/check_legal_fr_connectors.py` validates the connector configuration without network calls.
- Human validation gates: outputs remain blocked for client or external use until a qualified professional validates them.

## Workflows

| Workflow slug | Purpose |
|---|---|
| `revue-conformite-interne` | Build and apply internal compliance playbooks, then produce findings and remediation notes. |
| `analyse-contrats-fournisseurs` | Review supplier contracts across a corpus, extract non-standard terms, compare positions, and flag purchasing/legal risks. |
| `chronologie-contentieux` | Build litigation chronologies, verify procedural deadlines, assess causality, and prepare hearing-oriented summaries. |
| `jurisprudence-multilingue` | Research, read, compare, translate, and cite case law across French and broader legal sources. |
| `revue-contrats-travail` | Review employment contracts and HR corpora against French labor law, collective bargaining rules, remuneration, and privacy constraints. |
| `red-flags-bail` | Identify red flags in commercial leases, including lease status, Pinel-law points, non-standard clauses, renewal scenarios, and real-estate tax issues. |
| `note-information-amf` | Draft and check AMF-oriented disclosure sections, including risk factors, governance, ESG, KPIs, and regulatory citations. |
| `tabular-due-diligence` | Run tabular due diligence over transaction corpora, extract structured terms, score findings, and consolidate executive reports. |
| `recherche-juridique-fr-avancee` | Research French legal questions with OpenLegi-first source discipline, Parallel CLI deep research, source audit, veille, and Task API second-layer scaffolding. |

## Parallel Task API Layer

Parallel CLI is the default local/Cowork execution path for advanced French legal research. Parallel Task API is the deuxieme couche for backend production, long-running research, batch enrichment, polling, webhooks, and schema-backed outputs.

## Workflow Runner

The local workflow runner materializes Playbook V2 execution without network calls:

```bash
python scripts/legal_fr_workflow.py init --playbook workflow-dd-ma --matter "Acquisition PME" --objective "Audit acheteur" --document data-room/index.md --workdir .legal-fr-runs
python scripts/legal_fr_workflow.py run --run-dir .legal-fr-runs/<run-id>
python scripts/legal_fr_workflow.py run --run-dir .legal-fr-runs/<run-id> --full
python scripts/legal_fr_workflow.py review --run-dir .legal-fr-runs/<run-id> --validate
python scripts/legal_fr_workflow.py export --run-dir .legal-fr-runs/<run-id>
python scripts/legal_fr_workflow.py eval
```

Each run directory contains:

- `workflow-run.json`
- `source-ledger.json`
- `review-queue.json`
- `audit-trail.json`
- `deliverables.json` after validated export

The default `run` command advances exactly one stage. `--full` is explicit and still stops on missing documents, source gaps, failed quality gates or pending human validation. The runner validates each state file against local schemas before transitions, so corrupted `workflow-run.json`, `source-ledger.json`, `review-queue.json` or `audit-trail.json` files fail closed.

Local scaffold verification:

```bash
python scripts/check_legal_fr_parallel_task_api.py
```

Expected output:

```text
Legal-FR Parallel Task API scaffold OK
```

## Verification

Run these commands from the repository root before committing Legal-FR changes:

```bash
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
```

The connector check warns if `OPENLEGI_TOKEN` is not configured locally; that warning is expected in a development environment as long as the config itself is valid.

## Operating Notes

- Extract and validate structured JSON before writing any Markdown report. Markdown is a presentation layer over the schema-backed extraction, not the source of truth.
- Use official legal sources for critical legal conclusions. For French positive law, query OpenLegi first; use Exa and Parallel CLI for broader public research, secondary context, comparative checks, enrichment, or source discovery.
- Mark uncertain current-law points as `A VERIFIER` and do not convert uncertainty into a firm conclusion.
- Every external report must display `DRAFT - Validation professionnelle requise`.
- Maintain an audit trail for material findings: source excerpt, source status, confidence, and reviewer note.
- Apply the Legal-FR quality gates before final output, especially source status, confidence bands, schema completeness, draft notice, and human validation metadata.
- Human validation by a qualified legal professional is mandatory before any client, regulator, counterparty, or other external use.
- Only OpenLegi and Exa are required MCP connectors for now; Parallel CLI and Parallel Task API are execution layers for advanced research, not replacements for source validation.
