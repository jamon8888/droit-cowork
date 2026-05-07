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

- sous-traitant
- finalites
- duree
- mesures securite
- sort donnees

## Regles de conformite

- `R-001`: Toute sortie issue du playbook reste marquee `DRAFT - Validation professionnelle requise` tant que `validated_by_human` n'est pas vrai.
- `R-002`: Chaque conclusion substantielle doit porter un `source_status` explicite: official, secondary, web, unverified ou not_found.
- `R-003`: Chaque extraction ou scoring doit inclure `confidence` entre 0 et 1 et signaler les hypotheses qui limitent la fiabilite.
- `R-DPA-001`: Identifier le sous-traitant, le responsable de traitement et les categories de donnees traitees.
- `R-DPA-002`: Verifier que les finalites, la duree et les instructions documentees sont explicites.
- `R-DPA-003`: Controler les mesures securite, l'assistance, l'audit et le sort donnees en fin de prestation.

## Red flags automatiques

- `RF-001`: Source officielle introuvable ou `source_status` not_found pour une regle juridique determinante.
- `RF-002`: `validated_by_human` false alors que le livrable est presente comme final ou exploitable externe.
- `RF-003`: `confidence` inferieur a 0.5 sur une clause, date, montant ou obligation materielle.
- `RF-DPA-001`: Sous-traitant ulterieur autorise sans encadrement ou information prealable.
- `RF-DPA-002`: Finalites ou duree absentes, ouvertes ou incompatibles avec le contrat principal.
- `RF-DPA-003`: Sort donnees non precise: restitution, suppression, conservation ou preuve d'effacement.
