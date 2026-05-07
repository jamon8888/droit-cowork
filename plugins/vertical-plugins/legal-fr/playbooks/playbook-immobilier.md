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

- titres
- baux
- charges
- urbanisme

## Regles de conformite

- `R-001`: Toute sortie issue du playbook reste marquee `DRAFT - Validation professionnelle requise` tant que `validated_by_human` n'est pas vrai.
- `R-002`: Chaque conclusion substantielle doit porter un `source_status` explicite: official, secondary, web, unverified ou not_found.
- `R-003`: Chaque extraction ou scoring doit inclure `confidence` entre 0 et 1 et signaler les hypotheses qui limitent la fiabilite.
- `R-IMM-001`: Verifier titres, origine de propriete, servitudes et droits de tiers.
- `R-IMM-002`: Extraire baux, charges, travaux, assurances et fiscalite recurrente.
- `R-IMM-003`: Controler urbanisme, autorisations, conformite, environnement et contentieux.

## Red flags automatiques

- `RF-001`: Source officielle introuvable ou `source_status` not_found pour une regle juridique determinante.
- `RF-002`: `validated_by_human` false alors que le livrable est presente comme final ou exploitable externe.
- `RF-003`: `confidence` inferieur a 0.5 sur une clause, date, montant ou obligation materielle.
- `RF-IMM-001`: Titre ou servitude determinant absent de la data room.
- `RF-IMM-002`: Charges ou travaux significatifs non attribues a une partie.
- `RF-IMM-003`: Urbanisme non verifie ou autorisation essentielle manquante.
