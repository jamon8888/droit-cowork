---
schema_version: 2.0.0
playbook_id: workflow-audit-baux
name: workflow-audit-baux
version: 2.0.0
workflow_type: immobilier
jurisdiction: FR
domain: immobilier
primary_agent: red-flags-bail
status: draft
draft_notice: DRAFT - Validation professionnelle requise
---

# Workflow - Audit Baux FR

## Intake

| intake_id | Champ | Obligatoire | Blocage si absent |
| --- | --- | --- | --- |
| intake_id:workflow-audit-baux-scope | Question, objectif, position client et livrable attendu | oui | intake_remediation |
| intake_id:workflow-audit-baux-matter | Domaine, juridiction FR, periode et parties concernees | oui | intake_remediation |
| intake_id:workflow-audit-baux-risk | Niveau de risque, urgence, usage interne/externe | oui | intake_remediation |

## Documents Requis

| document_id | Document | Usage | Failure state |
| --- | --- | --- | --- |
| document_id:workflow-audit-baux-corpus | Corpus principal ou dossier client | extraction | missing_document |
| document_id:workflow-audit-baux-brief | Brief utilisateur, hypothese ou instruction cabinet | cadrage | missing_document |
| document_id:workflow-audit-baux-reference | Playbook ou standard cabinet applicable | controle | missing_document |

## Sources Autorisees

| source_rule_id | Ordre | Source | Usage | Failure state |
| --- | --- | --- | --- | --- |
| source_rule_id:workflow-audit-baux-official | 1 | OpenLegi / source officielle FR ou UE | droit positif et conclusion critique | official_source_not_found |
| source_rule_id:workflow-audit-baux-public | 2 | Exa / Parallel CLI public web avec JSON | contexte, recherche large, enrichment | low_confidence |
| source_rule_id:workflow-audit-baux-manual | 3 | Source fournie par le professionnel | dossier, doctrine, cabinet | human_review_required |

## Agents Et Skills

| assignment_id | Agent | Skills obligatoires | Sortie |
| --- | --- | --- | --- |
| assignment_id:workflow-audit-baux-orchestrator | red-flags-bail | legal-fr-runtime, workflow-playbooks, source-ledger, review-queue | workflow_run |
| assignment_id:workflow-audit-baux-source | source-verifier | source-ledger, citation-juridique, openlegi-recherche | source_ledger |
| assignment_id:workflow-audit-baux-review | legal-qa-reviewer | review-queue, quality-gates-juridiques | review_queue |

## Etapes Workflow

| step_id | Etape | Entree | Sortie | quality_gate_id | Stop condition |
| --- | --- | --- | --- | --- | --- |
| step_id:workflow-audit-baux-01-intake | Intake strict et inventaire | brief + corpus | workflow_run.schema.json | quality_gate_id:workflow-audit-baux-intake | missing_document |
| step_id:workflow-audit-baux-02-extract | Extraction JSON schema-backed | corpus | extraction tables | quality_gate_id:workflow-audit-baux-schema | schema_invalid |
| step_id:workflow-audit-baux-03-source | Verification source-ledger | findings | source-ledger.schema.json | quality_gate_id:workflow-audit-baux-sources | official_source_not_found |
| step_id:workflow-audit-baux-04-risk | Red flags, scoring, priorite | findings + sources | review_queue.schema.json | quality_gate_id:workflow-audit-baux-risk | low_confidence |
| step_id:workflow-audit-baux-05-review | Validation humaine | review queue | decisions | quality_gate_id:workflow-audit-baux-human | human_review_rejected |
| step_id:workflow-audit-baux-06-export | Export livrables | decisions validees | deliverables.schema.json | quality_gate_id:workflow-audit-baux-export | blocked_until_validated |

## Tableau Principal

| column_id | Colonne | Source | Regle |
| --- | --- | --- | --- |
| column_id:workflow-audit-baux-document | Document / piece / question | document_id | Toujours renseigne |
| column_id:workflow-audit-baux-finding | Finding ou terme extrait | extraction JSON | Ne pas deduire si absent |
| column_id:workflow-audit-baux-source | Source et source_status | source-ledger | Official si conclusion critique |
| column_id:workflow-audit-baux-risk | Risque, criticite, action | risk-score | Score justifie |
| column_id:workflow-audit-baux-review | Validation humaine | review-queue | Bloquant avant usage externe |

## Red Flags

| rule_id | Red flag | Niveau | Action |
| --- | --- | --- | --- |
| rule_id:workflow-audit-baux-rf-001 | Source officielle absente pour conclusion critique | blocking | stop et chercher source officielle |
| rule_id:workflow-audit-baux-rf-002 | Confiance inferieure a 0.70 | major | review_queue obligatoire |
| rule_id:workflow-audit-baux-rf-003 | Document manquant ou illisible | major | remediation documentaire |
| rule_id:workflow-audit-baux-rf-004 | Sortie externe sans validation humaine | blocking | bloquer export |

## Quality Gates

| quality_gate_id | Controle | Critere de passage | Failure state |
| --- | --- | --- | --- |
| quality_gate_id:workflow-audit-baux-intake | Intake complet | Tous les intake_id requis remplis | intake_remediation |
| quality_gate_id:workflow-audit-baux-schema | Schema valide | workflow-run, source-ledger, review-queue valides | schema_invalid |
| quality_gate_id:workflow-audit-baux-sources | Sources citees | source_status explicite, official si critique | official_source_not_found |
| quality_gate_id:workflow-audit-baux-risk | Risques controles | score, confiance, action et owner presents | low_confidence |
| quality_gate_id:workflow-audit-baux-human | Validation humaine | decision validee ou rejet motive | human_review_rejected |
| quality_gate_id:workflow-audit-baux-export | Export autorise | DRAFT present et validation professionnelle documentee | blocked_until_validated |

## Livrables

| deliverable_id | Livrable | Format | Etat initial |
| --- | --- | --- | --- |
| deliverable_id:workflow-audit-baux-deliv-01 | TABLEAU-BAUX | Markdown + JSON | blocked_until_validated |
| deliverable_id:workflow-audit-baux-deliv-02 | RAPPORT-RED-FLAGS-BAUX | Markdown + JSON | blocked_until_validated |
| deliverable_id:workflow-audit-baux-deliv-03 | REVIEW-QUEUE | Markdown + JSON | blocked_until_validated |
| deliverable_id:workflow-audit-baux-deliv-04 | SOURCE-LEDGER | Markdown + JSON | blocked_until_validated |

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
