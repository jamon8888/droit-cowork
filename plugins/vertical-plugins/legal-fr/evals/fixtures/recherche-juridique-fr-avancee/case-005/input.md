# Eval fixture case-005: recherche-juridique-fr-avancee

DRAFT - Validation professionnelle requise

## Workflow

`recherche-juridique-fr-avancee`

## Case type

`source_not_found`

## Risk level

`medium`

## Cas eval recherche-juridique-fr-avancee

Deep research async avec run_id et interaction_id.

Question: verifier l'etat du droit francais applicable.
Contrainte: OpenLegi doit etre interroge avant Parallel.
Source attendue: officielle si conclusion critique.

## Cabinet scenario

Affirmation juridique plausible mais source officielle introuvable dans le dossier.

## Expected handling

Marquer la source comme introuvable et interdire toute conclusion finale.

## Source package

- Document reference: `recherche-juridique-fr-avancee-case-005-document`
- Source status to test: `not_found`
- Human validation remains mandatory before reliance.
