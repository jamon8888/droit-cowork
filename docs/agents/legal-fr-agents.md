# Legal-FR Agents

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

Each agent plugin is self-contained: its `agents/<slug>.md` prompt and bundled `skills/` directory can be installed independently from the full vertical.
