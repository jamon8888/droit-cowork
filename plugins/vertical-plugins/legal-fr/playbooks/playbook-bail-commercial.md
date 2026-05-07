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

- duree
- charges
- indexation
- renouvellement
- eviction

## Regles de conformite

- `R-001`: Toute sortie issue du playbook reste marquee `DRAFT - Validation professionnelle requise` tant que `validated_by_human` n'est pas vrai.
- `R-002`: Chaque conclusion substantielle doit porter un `source_status` explicite: official, secondary, web, unverified ou not_found.
- `R-003`: Chaque extraction ou scoring doit inclure `confidence` entre 0 et 1 et signaler les hypotheses qui limitent la fiabilite.
- `R-BAI-001`: Extraire duree, prise d'effet, destination, renouvellement et conge.
- `R-BAI-002`: Verifier charges, travaux, taxes, depot de garantie et repartition Pinel.
- `R-BAI-003`: Controler indexation, revision, eviction et indemnite eventuelle.

## Red flags automatiques

- `RF-001`: Source officielle introuvable ou `source_status` not_found pour une regle juridique determinante.
- `RF-002`: `validated_by_human` false alors que le livrable est presente comme final ou exploitable externe.
- `RF-003`: `confidence` inferieur a 0.5 sur une clause, date, montant ou obligation materielle.
- `RF-BAI-001`: Charges non detaillees ou transfert au preneur potentiellement non conforme.
- `RF-BAI-002`: Indexation incoherente, indice absent ou clause d'echelle mobile asymetrique.
- `RF-BAI-003`: Renonciation ou restriction au renouvellement ou a l'eviction sans analyse.
