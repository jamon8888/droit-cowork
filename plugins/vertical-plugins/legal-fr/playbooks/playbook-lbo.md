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

- dette
- covenants
- suretes
- restrictions

## Regles de conformite

- `R-001`: Toute sortie issue du playbook reste marquee `DRAFT - Validation professionnelle requise` tant que `validated_by_human` n'est pas vrai.
- `R-002`: Chaque conclusion substantielle doit porter un `source_status` explicite: official, secondary, web, unverified ou not_found.
- `R-003`: Chaque extraction ou scoring doit inclure `confidence` entre 0 et 1 et signaler les hypotheses qui limitent la fiabilite.
- `R-LBO-001`: Identifier dette senior, dette mezzanine, maturite, tirages et remboursement.
- `R-LBO-002`: Verifier covenants financiers, testing dates, equity cure et reporting.
- `R-LBO-003`: Controler suretes, garanties, restrictions de distribution et dette additionnelle.

## Red flags automatiques

- `RF-001`: Source officielle introuvable ou `source_status` not_found pour une regle juridique determinante.
- `RF-002`: `validated_by_human` false alors que le livrable est presente comme final ou exploitable externe.
- `RF-003`: `confidence` inferieur a 0.5 sur une clause, date, montant ou obligation materielle.
- `RF-LBO-001`: Covenants absents, non chiffres ou sans methode de calcul.
- `RF-LBO-002`: Suretes ou rangs incompatibles avec la structure de dette.
- `RF-LBO-003`: Restrictions bloquant operations courantes ou distributions sans carve-out.
