# Playbook LBO

## Metadata

- playbook_id: `playbook-lbo`
- domain: financement LBO
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
| dette | Terme specifique domaine | string | A EXTRAIRE |
| covenants | Terme specifique domaine | string | A EXTRAIRE |
| suretes | Terme specifique domaine | string | A EXTRAIRE |
| restrictions | Terme specifique domaine | string | A EXTRAIRE |

## Regles de conformite

| ID | Regle | Severite | Controle | Action |
| --- | --- | --- | --- | --- |
| R-001 | Toute conclusion critique cite une source ou reste A VERIFIER | blocking | audit trail | Bloquer le livrable |
| R-002 | Toute sortie externe porte la mention DRAFT | blocking | quality gate | Ajouter la mention |
| R-003 | Toute observation a un score de confiance | major | risk score | Ajouter confidence |
| R-LBO-001 | Identifier dette senior, dette mezzanine, maturite, tirages et remboursement. | major | playbook domaine | Revoir avec juriste |
| R-LBO-002 | Verifier covenants financiers, testing dates, equity cure et reporting. | major | playbook domaine | Revoir avec juriste |
| R-LBO-003 | Controler suretes, garanties, restrictions de distribution et dette additionnelle. | major | playbook domaine | Revoir avec juriste |

## Red flags automatiques

| ID | Red flag | Severite | Action |
| --- | --- | --- | --- |
| RF-001 | Source absente sur conclusion majeure | blocking | Marquer A VERIFIER |
| RF-002 | Document illisible ignore | blocking | Ajouter a coverage |
| RF-003 | validated_by_human absent | major | Ajouter human validation |
| RF-LBO-001 | Covenants absents, non chiffres ou sans methode de calcul. | major | Revue juridique ciblee |
| RF-LBO-002 | Suretes ou rangs incompatibles avec la structure de dette. | major | Revue juridique ciblee |
| RF-LBO-003 | Restrictions bloquant operations courantes ou distributions sans carve-out. | major | Revue juridique ciblee |
