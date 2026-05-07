---
name: recherche:chercher
description: Rechercher des sources juridiques francaises avec OpenLegi et Parallel CLI.
argument-hint: "[question|url|fichier] [options]"
allowed-tools: Read, Write, Glob, Task, Bash(parallel-cli:*), Bash(python:*)
---

# recherche:chercher

## Regles

- Skill runtime obligatoire: `legal-fr-runtime`.
- DRAFT - Validation professionnelle requise.
- Perimetre: droit francais uniquement.
- OpenLegi avant Parallel pour droit positif francais.
- Toute commande Parallel CLI doit produire du JSON avec `--json`.
- Ne jamais afficher `PARALLEL_API_KEY`.
- Marquer `A VERIFIER` si aucune source officielle ne soutient une conclusion critique.

## Invocation technique

Outil principal: `parallel-cli`.

## Schema et audit trail

- Produire une extraction JSON schema-backed avant tout Markdown.
- Relier chaque conclusion a une source officielle, institutionnelle, doctrinale ou web dans un audit trail.
- Appliquer un quality gate: source officielle pour conclusion critique, `confidence`, `source_status`, `human_validation`, absence de secret.

## Sortie attendue

```json
{
  "workflow": "recherche-juridique-fr-avancee",
  "draft_notice": "DRAFT - Validation professionnelle requise",
  "official_sources": [],
  "secondary_sources": [],
  "source_gaps": [],
  "audit_trail": [],
  "human_validation": {"required": true, "status": "pending"}
}
```
