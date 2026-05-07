# Playbook CGV Standard

## Metadata

- playbook_id: `playbook-cgv-standard`
- domain: conditions generales de vente B2B/B2C
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
| delai paiement | Terme specifique domaine | string | A EXTRAIRE |
| penalites | Terme specifique domaine | string | A EXTRAIRE |
| juridiction | Terme specifique domaine | string | A EXTRAIRE |
| limitation responsabilite | Terme specifique domaine | string | A EXTRAIRE |

## Regles de conformite

| ID | Regle | Severite | Controle | Action |
| --- | --- | --- | --- | --- |
| R-001 | Toute conclusion critique cite une source ou reste A VERIFIER | blocking | audit trail | Bloquer le livrable |
| R-002 | Toute sortie externe porte la mention DRAFT | blocking | quality gate | Ajouter la mention |
| R-003 | Toute observation a un score de confiance | major | risk score | Ajouter confidence |
| R-CGV-001 | Verifier que les delais de paiement sont identifies et compatibles avec le cadre applicable. | major | playbook domaine | Revoir avec juriste |
| R-CGV-002 | Qualifier les penalites, indemnites et interets applicables en cas de retard. | major | playbook domaine | Revoir avec juriste |
| R-CGV-003 | Controler la coherence entre loi applicable, juridiction et limitation de responsabilite. | major | playbook domaine | Revoir avec juriste |

## Red flags automatiques

| ID | Red flag | Severite | Action |
| --- | --- | --- | --- |
| RF-001 | Source absente sur conclusion majeure | blocking | Marquer A VERIFIER |
| RF-002 | Document illisible ignore | blocking | Ajouter a coverage |
| RF-003 | validated_by_human absent | major | Ajouter human validation |
| RF-CGV-001 | Delai paiement absent, excessif ou contradictoire entre plusieurs clauses. | major | Revue juridique ciblee |
| RF-CGV-002 | Penalites absentes ou incompatibles avec le regime commercial vise. | major | Revue juridique ciblee |
| RF-CGV-003 | Limitation responsabilite illisible, illimitee sans justification ou potentiellement desequilibree. | major | Revue juridique ciblee |
