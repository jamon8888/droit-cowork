# Playbook Dette

## Metadata

- playbook_id: `playbook-dette`
- domain: contrats de dette
- source_status: `unverified`
- validated_by_human: `false`
- confidence: `0.0`
- draft_notice: `DRAFT - Validation professionnelle requise`
- validation_required: `true`

## Termes a extraire

- maturite
- taux
- covenants
- defaut

## Regles de conformite

- `R-001`: Toute sortie issue du playbook reste marquee `DRAFT - Validation professionnelle requise` tant que `validated_by_human` n'est pas vrai.
- `R-002`: Chaque conclusion substantielle doit porter un `source_status` explicite: official, secondary, web, unverified ou not_found.
- `R-003`: Chaque extraction ou scoring doit inclure `confidence` entre 0 et 1 et signaler les hypotheses qui limitent la fiabilite.
- `R-DET-001`: Identifier maturite, amortissement, taux, marges, commissions et prepayment.
- `R-DET-002`: Verifier covenants, representations, undertakings et obligations de reporting.
- `R-DET-003`: Controler cas de defaut, cross-default, grace periods, suretes et acceleration.

## Red flags automatiques

- `RF-001`: Source officielle introuvable ou `source_status` not_found pour une regle juridique determinante.
- `RF-002`: `validated_by_human` false alors que le livrable est presente comme final ou exploitable externe.
- `RF-003`: `confidence` inferieur a 0.5 sur une clause, date, montant ou obligation materielle.
- `RF-DET-001`: Maturite ou taux absent, variable non indexe ou formule incomplete.
- `RF-DET-002`: Covenants sans seuil, periodicite ou consequence de breach.
- `RF-DET-003`: Defaut automatique ou acceleration sans cure period identifiable.
