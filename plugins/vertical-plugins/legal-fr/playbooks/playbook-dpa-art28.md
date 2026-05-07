# Playbook DPA Art. 28 RGPD

## Metadata

- playbook_id: `playbook-dpa-art28`
- domain: accord de sous-traitance RGPD article 28
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
| sous-traitant | Terme specifique domaine | string | A EXTRAIRE |
| finalites | Terme specifique domaine | string | A EXTRAIRE |
| duree | Terme specifique domaine | string | A EXTRAIRE |
| mesures securite | Terme specifique domaine | string | A EXTRAIRE |
| sort donnees | Terme specifique domaine | string | A EXTRAIRE |

## Regles de conformite

| ID | Regle | Severite | Controle | Action |
| --- | --- | --- | --- | --- |
| R-001 | Toute conclusion critique cite une source ou reste A VERIFIER | blocking | audit trail | Bloquer le livrable |
| R-002 | Toute sortie externe porte la mention DRAFT | blocking | quality gate | Ajouter la mention |
| R-003 | Toute observation a un score de confiance | major | risk score | Ajouter confidence |
| R-DPA-001 | Identifier le sous-traitant, le responsable de traitement et les categories de donnees traitees. | major | playbook domaine | Revoir avec juriste |
| R-DPA-002 | Verifier que les finalites, la duree et les instructions documentees sont explicites. | major | playbook domaine | Revoir avec juriste |
| R-DPA-003 | Controler les mesures securite, l'assistance, l'audit et le sort donnees en fin de prestation. | major | playbook domaine | Revoir avec juriste |

## Red flags automatiques

| ID | Red flag | Severite | Action |
| --- | --- | --- | --- |
| RF-001 | Source absente sur conclusion majeure | blocking | Marquer A VERIFIER |
| RF-002 | Document illisible ignore | blocking | Ajouter a coverage |
| RF-003 | validated_by_human absent | major | Ajouter human validation |
| RF-DPA-001 | Sous-traitant ulterieur autorise sans encadrement ou information prealable. | major | Revue juridique ciblee |
| RF-DPA-002 | Finalites ou duree absentes, ouvertes ou incompatibles avec le contrat principal. | major | Revue juridique ciblee |
| RF-DPA-003 | Sort donnees non precise: restitution, suppression, conservation ou preuve d'effacement. | major | Revue juridique ciblee |
