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

- non-concurrence
- remuneration
- periode essai
- CCN

## Regles de conformite

- `R-001`: Toute sortie issue du playbook reste marquee `DRAFT - Validation professionnelle requise` tant que `validated_by_human` n'est pas vrai.
- `R-002`: Chaque conclusion substantielle doit porter un `source_status` explicite: official, secondary, web, unverified ou not_found.
- `R-003`: Chaque extraction ou scoring doit inclure `confidence` entre 0 et 1 et signaler les hypotheses qui limitent la fiabilite.
- `R-TRA-001`: Identifier type de contrat, poste, classification, CCN et lieu d'execution.
- `R-TRA-002`: Verifier remuneration, avantages, temps de travail et minima applicables.
- `R-TRA-003`: Controler periode essai, non-concurrence, mobilite et clauses sensibles.

## Red flags automatiques

- `RF-001`: Source officielle introuvable ou `source_status` not_found pour une regle juridique determinante.
- `RF-002`: `validated_by_human` false alors que le livrable est presente comme final ou exploitable externe.
- `RF-003`: `confidence` inferieur a 0.5 sur une clause, date, montant ou obligation materielle.
- `RF-TRA-001`: Non-concurrence sans contrepartie, limitation temporelle ou zone definie.
- `RF-TRA-002`: CCN absente ou incoherente avec l'activite et la classification.
- `RF-TRA-003`: Periode essai ou renouvellement non source par le contrat ou la CCN.
