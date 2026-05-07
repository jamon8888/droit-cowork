---
description: Construire une chronologie contentieuse depuis un dossier de pieces.
argument-hint: "[entree] [options]"
allowed-tools: Read, Write, Glob, Task
---

# chrono:construire

## Workflow

1. Clarifier le contexte, le profil utilisateur et le livrable attendu.
2. Charger les skills Legal-FR pertinents depuis le vertical `legal-fr`.
3. Utiliser les workers decrits dans l'agent orchestrateur lorsque le workflow exige extraction, scoring ou verification des sources.
4. Produire un fichier Markdown structure avec tableaux lorsque le resultat est destine a la revue.
5. Marquer toute sortie externe avec `DRAFT - Validation professionnelle requise`.
