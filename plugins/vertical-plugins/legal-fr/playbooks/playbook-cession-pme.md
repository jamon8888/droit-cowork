# Playbook Cession PME

## Metadata

- playbook_id: `playbook-cession-pme`
- domain: cession de PME
- source_status: `unverified`
- validated_by_human: `false`
- confidence: `0.0`
- draft_notice: `DRAFT - Validation professionnelle requise`
- validation_required: `true`

## Termes a extraire

- GAP
- conditions suspensives
- cession
- changement controle

## Regles de conformite

- `R-001`: Toute sortie issue du playbook reste marquee `DRAFT - Validation professionnelle requise` tant que `validated_by_human` n'est pas vrai.
- `R-002`: Chaque conclusion substantielle doit porter un `source_status` explicite: official, secondary, web, unverified ou not_found.
- `R-003`: Chaque extraction ou scoring doit inclure `confidence` entre 0 et 1 et signaler les hypotheses qui limitent la fiabilite.
- `R-CES-001`: Identifier perimetre de cession, prix, ajustement et calendrier closing.
- `R-CES-002`: Verifier GAP, plafonds, franchises, durees et procedures de reclamation.
- `R-CES-003`: Controler conditions suspensives, cession des contrats et changement controle.

## Red flags automatiques

- `RF-001`: Source officielle introuvable ou `source_status` not_found pour une regle juridique determinante.
- `RF-002`: `validated_by_human` false alors que le livrable est presente comme final ou exploitable externe.
- `RF-003`: `confidence` inferieur a 0.5 sur une clause, date, montant ou obligation materielle.
- `RF-CES-001`: Condition suspensive non purgee ou preuve de levee absente.
- `RF-CES-002`: GAP sans plafond, duree ou procedure de notification claire.
- `RF-CES-003`: Changement controle declenchant consentement tiers non obtenu.
