# Playbook Immobilier

## Metadata

- playbook_id: `playbook-immobilier`
- domain: due diligence immobiliere
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
| titres | Terme specifique domaine | string | A EXTRAIRE |
| baux | Terme specifique domaine | string | A EXTRAIRE |
| charges | Terme specifique domaine | string | A EXTRAIRE |
| urbanisme | Terme specifique domaine | string | A EXTRAIRE |

## Regles de conformite

| ID | Regle | Severite | Controle | Action |
| --- | --- | --- | --- | --- |
| R-001 | Toute conclusion critique cite une source ou reste A VERIFIER | blocking | audit trail | Bloquer le livrable |
| R-002 | Toute sortie externe porte la mention DRAFT | blocking | quality gate | Ajouter la mention |
| R-003 | Toute observation a un score de confiance | major | risk score | Ajouter confidence |
| R-IMM-001 | Verifier titres, origine de propriete, servitudes et droits de tiers. | major | playbook domaine | Revoir avec juriste |
| R-IMM-002 | Extraire baux, charges, travaux, assurances et fiscalite recurrente. | major | playbook domaine | Revoir avec juriste |
| R-IMM-003 | Controler urbanisme, autorisations, conformite, environnement et contentieux. | major | playbook domaine | Revoir avec juriste |

## Red flags automatiques

| ID | Red flag | Severite | Action |
| --- | --- | --- | --- |
| RF-001 | Source absente sur conclusion majeure | blocking | Marquer A VERIFIER |
| RF-002 | Document illisible ignore | blocking | Ajouter a coverage |
| RF-003 | validated_by_human absent | major | Ajouter human validation |
| RF-IMM-001 | Titre ou servitude determinant absent de la data room. | major | Revue juridique ciblee |
| RF-IMM-002 | Charges ou travaux significatifs non attribues a une partie. | major | Revue juridique ciblee |
| RF-IMM-003 | Urbanisme non verifie ou autorisation essentielle manquante. | major | Revue juridique ciblee |
