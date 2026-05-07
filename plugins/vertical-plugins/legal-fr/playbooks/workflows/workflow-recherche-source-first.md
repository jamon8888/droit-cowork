---
schema_version: 2.0.0
playbook_id: workflow-recherche-source-first
name: workflow-recherche-source-first
version: 2.0.0
workflow_type: recherche
jurisdiction: FR
domain: recherche-juridique-fr
primary_agent: recherche-juridique-fr-avancee
status: draft
draft_notice: DRAFT - Validation professionnelle requise
---

# Workflow - Recherche Source-First FR

## Intake

| intake_id | Champ | Obligatoire | Blocage si absent |
| --- | --- | --- | --- |
| intake_id:workflow-recherche-source-first-scope | Question, objectif, position client et livrable attendu | oui | intake_remediation |
| intake_id:workflow-recherche-source-first-matter | Domaine, juridiction FR, periode et parties concernees | oui | intake_remediation |
| intake_id:workflow-recherche-source-first-risk | Niveau de risque, urgence, usage interne/externe | oui | intake_remediation |

## Documents Requis

| document_id | Document | Usage | Failure state |
| --- | --- | --- | --- |
| document_id:workflow-recherche-source-first-corpus | Corpus principal ou dossier client | extraction | missing_document |
| document_id:workflow-recherche-source-first-brief | Brief utilisateur, hypothese ou instruction cabinet | cadrage | missing_document |
| document_id:workflow-recherche-source-first-reference | Playbook ou standard cabinet applicable | controle | missing_document |

## Sources Autorisees

| source_rule_id | Ordre | Source | Usage | Failure state |
| --- | --- | --- | --- | --- |
| source_rule_id:workflow-recherche-source-first-official | 1 | OpenLegi / source officielle FR ou UE | droit positif et conclusion critique | official_source_not_found |
| source_rule_id:workflow-recherche-source-first-public | 2 | Exa / Parallel CLI public web avec JSON | contexte, recherche large, enrichment | low_confidence |
| source_rule_id:workflow-recherche-source-first-manual | 3 | Source fournie par le professionnel | dossier, doctrine, cabinet | human_review_required |

## Agents Et Skills

| assignment_id | Agent | Skills obligatoires | Sortie |
| --- | --- | --- | --- |
| assignment_id:workflow-recherche-source-first-orchestrator | recherche-juridique-fr-avancee | legal-fr-runtime, workflow-playbooks, source-ledger, review-queue | workflow_run |
| assignment_id:workflow-recherche-source-first-source | source-verifier | source-ledger, citation-juridique, openlegi-recherche | source_ledger |
| assignment_id:workflow-recherche-source-first-review | legal-qa-reviewer | review-queue, quality-gates-juridiques | review_queue |

## Etapes Workflow

| step_id | Etape | Entree | Sortie | quality_gate_id | Stop condition |
| --- | --- | --- | --- | --- | --- |
| step_id:workflow-recherche-source-first-01-intake | Intake strict et inventaire | brief + corpus | workflow_run.schema.json | quality_gate_id:workflow-recherche-source-first-intake | missing_document |
| step_id:workflow-recherche-source-first-02-extract | Extraction JSON schema-backed | corpus | extraction tables | quality_gate_id:workflow-recherche-source-first-schema | schema_invalid |
| step_id:workflow-recherche-source-first-03-source | Verification source-ledger | findings | source-ledger.schema.json | quality_gate_id:workflow-recherche-source-first-sources | official_source_not_found |
| step_id:workflow-recherche-source-first-04-risk | Red flags, scoring, priorite | findings + sources | review_queue.schema.json | quality_gate_id:workflow-recherche-source-first-risk | low_confidence |
| step_id:workflow-recherche-source-first-05-review | Validation humaine | review queue | decisions | quality_gate_id:workflow-recherche-source-first-human | human_review_rejected |
| step_id:workflow-recherche-source-first-06-export | Export livrables | decisions validees | deliverables.schema.json | quality_gate_id:workflow-recherche-source-first-export | blocked_until_validated |

## Tableau Principal

| column_id | Colonne | Source | Regle |
| --- | --- | --- | --- |
| column_id:workflow-recherche-source-first-document | Document / piece / question | document_id | Toujours renseigne |
| column_id:workflow-recherche-source-first-finding | Finding ou terme extrait | extraction JSON | Ne pas deduire si absent |
| column_id:workflow-recherche-source-first-source | Source et source_status | source-ledger | Official si conclusion critique |
| column_id:workflow-recherche-source-first-risk | Risque, criticite, action | risk-score | Score justifie |
| column_id:workflow-recherche-source-first-review | Validation humaine | review-queue | Bloquant avant usage externe |

## Red Flags

| rule_id | Red flag | Niveau | Action |
| --- | --- | --- | --- |
| rule_id:workflow-recherche-source-first-rf-001 | Source officielle absente pour conclusion critique | blocking | stop et chercher source officielle |
| rule_id:workflow-recherche-source-first-rf-002 | Confiance inferieure a 0.70 | major | review_queue obligatoire |
| rule_id:workflow-recherche-source-first-rf-003 | Document manquant ou illisible | major | remediation documentaire |
| rule_id:workflow-recherche-source-first-rf-004 | Sortie externe sans validation humaine | blocking | bloquer export |

## Quality Gates

| quality_gate_id | Controle | Critere de passage | Failure state |
| --- | --- | --- | --- |
| quality_gate_id:workflow-recherche-source-first-intake | Intake complet | Tous les intake_id requis remplis | intake_remediation |
| quality_gate_id:workflow-recherche-source-first-schema | Schema valide | workflow-run, source-ledger, review-queue valides | schema_invalid |
| quality_gate_id:workflow-recherche-source-first-sources | Sources citees | source_status explicite, official si critique | official_source_not_found |
| quality_gate_id:workflow-recherche-source-first-risk | Risques controles | score, confiance, action et owner presents | low_confidence |
| quality_gate_id:workflow-recherche-source-first-human | Validation humaine | decision validee ou rejet motive | human_review_rejected |
| quality_gate_id:workflow-recherche-source-first-export | Export autorise | DRAFT present et validation professionnelle documentee | blocked_until_validated |

## Livrables

| deliverable_id | Livrable | Format | Etat initial |
| --- | --- | --- | --- |
| deliverable_id:workflow-recherche-source-first-deliv-01 | NOTE-RECHERCHE | Markdown + JSON | blocked_until_validated |
| deliverable_id:workflow-recherche-source-first-deliv-02 | SOURCE-LEDGER | Markdown + JSON | blocked_until_validated |
| deliverable_id:workflow-recherche-source-first-deliv-03 | REVIEW-QUEUE | Markdown + JSON | blocked_until_validated |
| deliverable_id:workflow-recherche-source-first-deliv-04 | BIBLIOGRAPHIE | Markdown + JSON | blocked_until_validated |

## Validation Humaine

- Toute sortie reste `DRAFT - Validation professionnelle requise`.
- Le full-run ne doit jamais contourner `review-queue`.
- Une decision `human_review_rejected` renvoie vers l'etape corrigee, pas vers l'export.
- Le tableau principal est la source de verite operationnelle; le rapport narratif est derive du JSON et du source-ledger.

## Failure States

| Etat | Signification | Remediation |
| --- | --- | --- |
| missing_document | Piece ou brief absent | Demander document_id manquant |
| official_source_not_found | Source officielle introuvable | Marquer A VERIFIER et bloquer conclusion critique |
| low_confidence | Confiance insuffisante | Ajouter item review_queue |
| schema_invalid | JSON non conforme | Reprendre l'etape schema |
| quality_gate_failed | Gate non passe | Stop, lister les blocages |
| human_review_rejected | Reviewer refuse | Corriger puis reprendre l'etape concernee |
