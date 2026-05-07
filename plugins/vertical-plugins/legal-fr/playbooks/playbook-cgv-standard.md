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

- delai paiement
- penalites
- juridiction
- limitation responsabilite

## Regles de conformite

- `R-001`: Toute sortie issue du playbook reste marquee `DRAFT - Validation professionnelle requise` tant que `validated_by_human` n'est pas vrai.
- `R-002`: Chaque conclusion substantielle doit porter un `source_status` explicite: official, secondary, web, unverified ou not_found.
- `R-003`: Chaque extraction ou scoring doit inclure `confidence` entre 0 et 1 et signaler les hypotheses qui limitent la fiabilite.
- `R-CGV-001`: Verifier que les delais de paiement sont identifies et compatibles avec le cadre applicable.
- `R-CGV-002`: Qualifier les penalites, indemnites et interets applicables en cas de retard.
- `R-CGV-003`: Controler la coherence entre loi applicable, juridiction et limitation de responsabilite.

## Red flags automatiques

- `RF-001`: Source officielle introuvable ou `source_status` not_found pour une regle juridique determinante.
- `RF-002`: `validated_by_human` false alors que le livrable est presente comme final ou exploitable externe.
- `RF-003`: `confidence` inferieur a 0.5 sur une clause, date, montant ou obligation materielle.
- `RF-CGV-001`: Delai paiement absent, excessif ou contradictoire entre plusieurs clauses.
- `RF-CGV-002`: Penalites absentes ou incompatibles avec le regime commercial vise.
- `RF-CGV-003`: Limitation responsabilite illisible, illimitee sans justification ou potentiellement desequilibree.
