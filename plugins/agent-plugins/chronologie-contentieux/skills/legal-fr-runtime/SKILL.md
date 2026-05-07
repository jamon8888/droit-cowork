---
name: legal-fr-runtime
description: Regles runtime obligatoires Legal-FR pour sorties draft, sources, Parallel CLI, JSON, audit trail et quality gates.
---

# legal-fr-runtime

## Purpose

Regles runtime obligatoires pour les plugins Legal-FR dans Claude Desktop/Cowork. Ce skill duplique les instructions critiques qui ne doivent pas rester seulement dans un `CLAUDE.md` de plugin.

## Workflow

1. Classer la demande, le domaine juridique, le profil utilisateur, le corpus et le livrable attendu.
2. Produire une extraction JSON schema-backed avant tout Markdown lorsque le workflow dispose d'un schema.
3. Appliquer l'ordre des sources: OpenLegi avant Exa pour le droit positif francais, puis Exa pour contexte secondaire et recherche large.
4. Pour la recherche avancee, utiliser OpenLegi avant Parallel; utiliser Parallel CLI uniquement avec sortie JSON (`--json`).
5. Construire un `audit_trail` pour chaque finding materiel avec source, extrait, statut, confiance et validation humaine.
6. Appliquer le quality gate avant sortie externe. Si un gate echoue, stop et retourner les blocages au lieu de produire un livrable poli.

## Output posture

- Tout rapport, memo, tableau, note, email ou livrable client contient `DRAFT - Validation professionnelle requise`.
- La validation par un avocat, juriste senior ou professionnel qualifie reste obligatoire avant tout usage externe.
- Ne jamais presenter une conclusion juridique comme definitive si la source, la date, la qualification ou le dossier complet manque.
- Les incertitudes critiques sont marquees `A VERIFIER`.

## Source order

- OpenLegi avant Exa pour toute affirmation de droit positif francais.
- OpenLegi avant Parallel pour toute recherche juridique FR avancee.
- Exa sert au contexte secondaire, a la decouverte de sources et aux verifications larges.
- Parallel CLI sert aux recherches web publiques, extractions, enrichissements et veilles; toujours ajouter `--json`.
- Ne jamais afficher, journaliser ou reconstituer `PARALLEL_API_KEY`.

## JSON and audit trail

- Valider les champs contre le schema Legal-FR applicable quand il existe.
- Le JSON est la source de verite; le Markdown est seulement la presentation.
- Ne pas masquer les pages illisibles, documents manquants, citations incompletes ou sources introuvables.
- Chaque finding materiel conserve `source_status`, `confidence`, `audit_trail` et `validated_by_human: false` tant que la validation n'est pas effective.

## Quality gate

Bloquer la sortie externe si l'un de ces points manque:

- mention `DRAFT - Validation professionnelle requise`;
- schema requis ou champs obligatoires;
- source officielle pour une conclusion critique quand elle existe;
- mention `A VERIFIER` pour point incertain;
- `source_status`, `confidence` et `audit_trail`;
- metadata de validation humaine.

## Output Contract

- Markdown pour les rapports et tableaux finaux.
- JSON pour les extractions intermediaires et la consolidation.
- Blocage explicite avec liste des gates echoues quand les conditions de livraison ne sont pas remplies.
