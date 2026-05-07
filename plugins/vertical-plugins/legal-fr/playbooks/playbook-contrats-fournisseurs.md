# Playbook Contrats Fournisseurs

## Metadata

- playbook_id: `playbook-contrats-fournisseurs`
- domain: contrats fournisseurs et achats
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
| preavis | Terme specifique domaine | string | A EXTRAIRE |
| prix | Terme specifique domaine | string | A EXTRAIRE |
| revision | Terme specifique domaine | string | A EXTRAIRE |
| penalites | Terme specifique domaine | string | A EXTRAIRE |
| exclusivite | Terme specifique domaine | string | A EXTRAIRE |

## Regles de conformite

| ID | Regle | Severite | Controle | Action |
| --- | --- | --- | --- | --- |
| R-001 | Toute conclusion critique cite une source ou reste A VERIFIER | blocking | audit trail | Bloquer le livrable |
| R-002 | Toute sortie externe porte la mention DRAFT | blocking | quality gate | Ajouter la mention |
| R-003 | Toute observation a un score de confiance | major | risk score | Ajouter confidence |
| R-FOU-001 | Extraire duree, renouvellement, preavis et conditions de sortie. | major | playbook domaine | Revoir avec juriste |
| R-FOU-002 | Verifier prix, revision, indexation et penalites operationnelles ou financieres. | major | playbook domaine | Revoir avec juriste |
| R-FOU-003 | Qualifier les clauses d'exclusivite, dependance, cession et changement de controle. | major | playbook domaine | Revoir avec juriste |

## Red flags automatiques

| ID | Red flag | Severite | Action |
| --- | --- | --- | --- |
| RF-001 | Source absente sur conclusion majeure | blocking | Marquer A VERIFIER |
| RF-002 | Document illisible ignore | blocking | Ajouter a coverage |
| RF-003 | validated_by_human absent | major | Ajouter human validation |
| RF-FOU-001 | Renouvellement automatique sans preavis exploitable ou calendrier d'alerte. | major | Revue juridique ciblee |
| RF-FOU-002 | Revision de prix unilaterale ou penalites disproportionnees. | major | Revue juridique ciblee |
| RF-FOU-003 | Exclusivite ou dependance fournisseur sans mecanisme de sortie. | major | Revue juridique ciblee |
