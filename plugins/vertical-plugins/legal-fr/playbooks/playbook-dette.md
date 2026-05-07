# Playbook Dette

## Metadata

- playbook_id: `playbook-dette`
- domain: contrats de dette
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
| maturite | Terme specifique domaine | string | A EXTRAIRE |
| taux | Terme specifique domaine | string | A EXTRAIRE |
| covenants | Terme specifique domaine | string | A EXTRAIRE |
| defaut | Terme specifique domaine | string | A EXTRAIRE |

## Regles de conformite

| ID | Regle | Severite | Controle | Action |
| --- | --- | --- | --- | --- |
| R-001 | Toute conclusion critique cite une source ou reste A VERIFIER | blocking | audit trail | Bloquer le livrable |
| R-002 | Toute sortie externe porte la mention DRAFT | blocking | quality gate | Ajouter la mention |
| R-003 | Toute observation a un score de confiance | major | risk score | Ajouter confidence |
| R-DET-001 | Identifier maturite, amortissement, taux, marges, commissions et prepayment. | major | playbook domaine | Revoir avec juriste |
| R-DET-002 | Verifier covenants, representations, undertakings et obligations de reporting. | major | playbook domaine | Revoir avec juriste |
| R-DET-003 | Controler cas de defaut, cross-default, grace periods, suretes et acceleration. | major | playbook domaine | Revoir avec juriste |

## Red flags automatiques

| ID | Red flag | Severite | Action |
| --- | --- | --- | --- |
| RF-001 | Source absente sur conclusion majeure | blocking | Marquer A VERIFIER |
| RF-002 | Document illisible ignore | blocking | Ajouter a coverage |
| RF-003 | validated_by_human absent | major | Ajouter human validation |
| RF-DET-001 | Maturite ou taux absent, variable non indexe ou formule incomplete. | major | Revue juridique ciblee |
| RF-DET-002 | Covenants sans seuil, periodicite ou consequence de breach. | major | Revue juridique ciblee |
| RF-DET-003 | Defaut automatique ou acceleration sans cure period identifiable. | major | Revue juridique ciblee |
