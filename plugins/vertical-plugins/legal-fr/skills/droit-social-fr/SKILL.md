---
name: droit-social-fr
description: Contrats de travail, CDI, CDD, rupture, clauses sensibles.
---

# droit-social-fr

## Purpose

Contrats de travail, CDI, CDD, rupture, clauses sensibles.

## Workflow

1. Identifier le contexte juridique, le type de document et la question traitee.
2. Produire des resultats structures avec sources, incertitudes et champs non trouves.
3. Pour toute extraction de corpus, retourner un JSON stable avant toute synthese narrative.
4. Pour toute affirmation de droit positif, verifier via OpenLegi ou signaler l'incertitude.
5. Conserver la mention `DRAFT - Validation professionnelle requise` pour les livrables externes.

## Cabinet-grade requirements

- Produire uniquement des livrables marques `DRAFT - Validation professionnelle requise` tant que `validated_by_human: false`.
- Exposer les incertitudes en francais clair avec la mention `A VERIFIER` lorsqu'une source, une date, une qualification ou une piece manque.
- Refuser toute conclusion definitive sans validation professionnelle et sans lien entre le finding, la source et le reviewer.
- Garder un `audit_trail` exploitable pour chaque finding: document, extrait, source juridique, controle effectue, horodatage et reviewer attendu.

## JSON discipline

- Structurer les extractions avec `source_status`, `confidence`, `validated_by_human: false` et `audit_trail`.
- Utiliser `source_status` pour distinguer `official`, `secondary`, `not_found` et `unverified`; ne jamais masquer une source introuvable.
- Encadrer `confidence` entre 0 et 1 et baisser le score lorsqu'une piece est illisible, absente ou contradictoire.
- Conserver un JSON valide et stable avant toute synthese narrative, avec champs non trouves explicitement renseignes.

## French legal sourcing

- Verifier les affirmations de droit positif avec une source officielle francaise ou europeenne, en priorite OpenLegi/Legifrance lorsque disponible.
- Citer les references utiles: code, article, juridiction, date, numero, ECLI ou source AMF selon le domaine.
- Marquer `A VERIFIER` et `source_status: unverified` si la source officielle n'est pas disponible dans le dossier ou via connecteur.
- Ne pas transformer une recherche web ou une source secondaire en conclusion juridique sans validation humaine.

## Output Contract

- Markdown pour les rapports et tableaux finaux.
- JSON pour les extractions intermediaires.
- `source`, `localisation`, `confiance` et `verification_humaine_requise` lorsque l'information est extraite d'un document.

## Red flags a surveiller

- non-concurrence sans contrepartie.
- periode essai non sourcee.
- CCN absente.
