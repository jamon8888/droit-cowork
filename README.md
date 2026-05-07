# Legal-FR Suite

Legal-FR Suite is a production-grade French legal workflow codebase for Cowork/Codex plugins. It packages a Legal-FR vertical plugin, nine specialized Legal-FR agents, schemas, eval fixtures, source verification rules, OpenLegi/Exa MCP configuration, Parallel CLI research commands, and a Parallel Task API scaffold.

Every output is a draft for professional validation. Nothing in this repository constitutes legal advice, a binding legal opinion, a filing, or a client-ready deliverable without review by a qualified professional.

## Active Architecture

- `plugins/vertical-plugins/legal-fr`: source of commands, skills, playbooks, schemas, evals, and MCP configuration.
- `plugins/agent-plugins/*`: nine self-contained Legal-FR agent plugins with bundled skills.
- `scripts`: Legal-FR generation, validation, eval, connector, Parallel CLI, and Parallel Task API helpers.
- `tests`: Legal-FR structural, production-grade, clean-repo, and eval fixture tests.
- `docs`: architecture, agents, workflows, specs, and implementation plans.
- `archive/financial-services-origin`: preserved Financial Services origin material.

## Agents

| Agent | Purpose |
|---|---|
| `revue-conformite-interne` | Internal compliance review against cabinet playbooks. |
| `analyse-contrats-fournisseurs` | Supplier contract corpus review and risk scoring. |
| `chronologie-contentieux` | Litigation timeline construction and procedural checks. |
| `jurisprudence-multilingue` | Case law research, multilingual analysis, translation, and comparative law. |
| `revue-contrats-travail` | French employment contract and HR corpus review. |
| `red-flags-bail` | Commercial lease red flag review. |
| `note-information-amf` | AMF disclosure and risk factor drafting support. |
| `tabular-due-diligence` | Large-scale due diligence table extraction and reporting. |
| `recherche-juridique-fr-avancee` | French legal research with OpenLegi-first sourcing, Parallel CLI, source audit, veille, and Task API second layer. |

## Validation

Run:

```bash
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures tests.test_legal_fr_clean_repo -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
python scripts/check_legal_fr_parallel_task_api.py
```

Optional environment check:

```bash
python scripts/check_legal_fr_parallel_cli.py
```

If `parallel-cli` is not installed, this may return `ERROR: parallel-cli is not installed or not on PATH`.

## Archive

The original Financial Services repository material is preserved in `archive/financial-services-origin/`.
