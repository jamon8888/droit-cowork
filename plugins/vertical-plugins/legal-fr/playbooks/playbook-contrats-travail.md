# Playbook Contrats Travail

## Metadata

- playbook_id: `playbook-contrats-travail`
- domain: contrats de travail francais
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
| non-concurrence | Terme specifique domaine | string | A EXTRAIRE |
| remuneration | Terme specifique domaine | string | A EXTRAIRE |
| periode essai | Terme specifique domaine | string | A EXTRAIRE |
| CCN | Terme specifique domaine | string | A EXTRAIRE |

## Regles de conformite

| ID | Regle | Severite | Controle | Action |
| --- | --- | --- | --- | --- |
| R-001 | Toute conclusion critique cite une source ou reste A VERIFIER | blocking | audit trail | Bloquer le livrable |
| R-002 | Toute sortie externe porte la mention DRAFT | blocking | quality gate | Ajouter la mention |
| R-003 | Toute observation a un score de confiance | major | risk score | Ajouter confidence |
| R-TRA-001 | Identifier type de contrat, poste, classification, CCN et lieu d'execution. | major | playbook domaine | Revoir avec juriste |
| R-TRA-002 | Verifier remuneration, avantages, temps de travail et minima applicables. | major | playbook domaine | Revoir avec juriste |
| R-TRA-003 | Controler periode essai, non-concurrence, mobilite et clauses sensibles. | major | playbook domaine | Revoir avec juriste |

## Red flags automatiques

| ID | Red flag | Severite | Action |
| --- | --- | --- | --- |
| RF-001 | Source absente sur conclusion majeure | blocking | Marquer A VERIFIER |
| RF-002 | Document illisible ignore | blocking | Ajouter a coverage |
| RF-003 | validated_by_human absent | major | Ajouter human validation |
| RF-TRA-001 | Non-concurrence sans contrepartie, limitation temporelle ou zone definie. | major | Revue juridique ciblee |
| RF-TRA-002 | CCN absente ou incoherente avec l'activite et la classification. | major | Revue juridique ciblee |
| RF-TRA-003 | Periode essai ou renouvellement non source par le contrat ou la CCN. | major | Revue juridique ciblee |
