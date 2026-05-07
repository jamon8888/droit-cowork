# Playbook Bail Commercial

## Metadata

- playbook_id: `playbook-bail-commercial`
- domain: baux commerciaux
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
| duree | Terme specifique domaine | string | A EXTRAIRE |
| charges | Terme specifique domaine | string | A EXTRAIRE |
| indexation | Terme specifique domaine | string | A EXTRAIRE |
| renouvellement | Terme specifique domaine | string | A EXTRAIRE |
| eviction | Terme specifique domaine | string | A EXTRAIRE |

## Regles de conformite

| ID | Regle | Severite | Controle | Action |
| --- | --- | --- | --- | --- |
| R-001 | Toute conclusion critique cite une source ou reste A VERIFIER | blocking | audit trail | Bloquer le livrable |
| R-002 | Toute sortie externe porte la mention DRAFT | blocking | quality gate | Ajouter la mention |
| R-003 | Toute observation a un score de confiance | major | risk score | Ajouter confidence |
| R-BAI-001 | Extraire duree, prise d'effet, destination, renouvellement et conge. | major | playbook domaine | Revoir avec juriste |
| R-BAI-002 | Verifier charges, travaux, taxes, depot de garantie et repartition Pinel. | major | playbook domaine | Revoir avec juriste |
| R-BAI-003 | Controler indexation, revision, eviction et indemnite eventuelle. | major | playbook domaine | Revoir avec juriste |

## Red flags automatiques

| ID | Red flag | Severite | Action |
| --- | --- | --- | --- |
| RF-001 | Source absente sur conclusion majeure | blocking | Marquer A VERIFIER |
| RF-002 | Document illisible ignore | blocking | Ajouter a coverage |
| RF-003 | validated_by_human absent | major | Ajouter human validation |
| RF-BAI-001 | Charges non detaillees ou transfert au preneur potentiellement non conforme. | major | Revue juridique ciblee |
| RF-BAI-002 | Indexation incoherente, indice absent ou clause d'echelle mobile asymetrique. | major | Revue juridique ciblee |
| RF-BAI-003 | Renonciation ou restriction au renouvellement ou a l'eviction sans analyse. | major | Revue juridique ciblee |
