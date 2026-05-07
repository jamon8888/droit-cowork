# Playbook Cession PME

## Metadata

- playbook_id: `playbook-cession-pme`
- domain: cession de PME
- source_status: `unverified`
- validated_by_human: `false`
- confidence: `0.0`
- draft_notice: `DRAFT - Validation professionnelle requise`
- validation_required: `true`

## Termes a extraire

| Terme | Description | Type | Valeur par defaut |
| --- | --- | --- | --- |
| document_id | Identifiant stable du document | string | nom fichier |
| source_excerpt | Extrait qui justifie l'observation | string | A VERIFIER |
| source_status | official, secondary, web, unverified, not_found | enum | unverified |
| confidence | Confiance 0-1 | number | 0.5 |
| GAP | Terme specifique domaine | string | A EXTRAIRE |
| conditions suspensives | Terme specifique domaine | string | A EXTRAIRE |
| cession | Terme specifique domaine | string | A EXTRAIRE |
| changement controle | Terme specifique domaine | string | A EXTRAIRE |

## Regles de conformite

| ID | Regle | Severite | Controle | Action |
| --- | --- | --- | --- | --- |
| R-001 | Toute conclusion critique cite une source ou reste A VERIFIER | blocking | audit trail | Bloquer le livrable |
| R-002 | Toute sortie externe porte la mention DRAFT | blocking | quality gate | Ajouter la mention |
| R-003 | Toute observation a un score de confiance | major | risk score | Ajouter confidence |
| R-CES-001 | Identifier perimetre de cession, prix, ajustement et calendrier closing. | major | playbook domaine | Revoir avec juriste |
| R-CES-002 | Verifier GAP, plafonds, franchises, durees et procedures de reclamation. | major | playbook domaine | Revoir avec juriste |
| R-CES-003 | Controler conditions suspensives, cession des contrats et changement controle. | major | playbook domaine | Revoir avec juriste |

## Red flags automatiques

| ID | Red flag | Severite | Action |
| --- | --- | --- | --- |
| RF-001 | Source absente sur conclusion majeure | blocking | Marquer A VERIFIER |
| RF-002 | Document illisible ignore | blocking | Ajouter a coverage |
| RF-003 | validated_by_human absent | major | Ajouter human validation |
| RF-CES-001 | Condition suspensive non purgee ou preuve de levee absente. | major | Revue juridique ciblee |
| RF-CES-002 | GAP sans plafond, duree ou procedure de notification claire. | major | Revue juridique ciblee |
| RF-CES-003 | Changement controle declenchant consentement tiers non obtenu. | major | Revue juridique ciblee |
