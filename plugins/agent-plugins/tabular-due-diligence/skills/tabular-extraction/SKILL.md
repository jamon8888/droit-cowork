---
name: tabular-extraction
description: Extraction massive de termes de data room.
---

# tabular-extraction

## Purpose

Extraction massive de termes de data room.

## Workflow

1. Identifier le contexte juridique, le type de document et la question traitee.
2. Produire des resultats structures avec sources, incertitudes et champs non trouves.
3. Pour toute extraction de corpus, retourner un JSON stable avant toute synthese narrative.
4. Pour toute affirmation de droit positif, verifier via OpenLegi ou signaler l'incertitude.
5. Conserver la mention `DRAFT - Validation professionnelle requise` pour les livrables externes.

## Output Contract

- Markdown pour les rapports et tableaux finaux.
- JSON pour les extractions intermediaires.
- `source`, `localisation`, `confiance` et `verification_humaine_requise` lorsque l'information est extraite d'un document.
