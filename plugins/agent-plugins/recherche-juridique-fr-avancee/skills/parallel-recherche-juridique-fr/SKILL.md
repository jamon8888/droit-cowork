---
name: parallel-recherche-juridique-fr
description: Recherche juridique francaise avancee via Parallel CLI: search, extract, research, enrich, findall et monitor.
---

# parallel-recherche-juridique-fr

## Purpose

Recherche juridique francaise avancee via Parallel CLI: search, extract, research, enrich, findall et monitor.

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

## Installation Parallel CLI et Agent Skills

Sources officielles:

- https://docs.parallel.ai/integrations/cli
- https://docs.parallel.ai/integrations/agent-skills

Installation recommandee pour Cowork/Agent Skills:

```bash
pipx install "parallel-web-tools[cli]" && pipx ensurepath
```

Alternatives supportees:

```bash
uv tool install "parallel-web-tools[cli]"
npm install -g parallel-web-cli
```

Installer les Parallel Agent Skills lorsque le runtime local les supporte:

```bash
npx skills add parallel-web/parallel-agent-skills --all --global
```

## Parallel MCP

Documentation officielle: https://docs.parallel.ai/integrations/mcp/quickstart.

Parallel Search MCP:

- Endpoint: `https://search.parallel.ai/mcp`.
- Outils attendus: `web_search`, `web_fetch`.
- Usage Legal-FR: recherche web rapide et fetch URL depuis Claude Desktop/Cowork.
- Les resultats restent `secondary` ou `unverified` tant qu'OpenLegi ou une source officielle ne confirme pas le point de droit.

Parallel Task MCP:

- Endpoint: `https://task-mcp.parallel.ai/mcp`.
- Outils attendus: `createDeepResearch`, `createTaskGroup`, `getStatus`, `getResultMarkdown`.
- Authentification: OAuth ou `PARALLEL_API_KEY`; ne jamais hardcoder la cle.
- Usage Legal-FR: recherche longue interactive, task groups et enrichissement.
- Cette couche est optionnelle et distincte du CLI local et de la Task API backend.

Authentification:

```bash
parallel-cli login --device
parallel-cli auth --json
```

`PARALLEL_API_KEY` peut etre defini dans l'environnement utilisateur pour les executions non interactives. Ne jamais ecrire `PARALLEL_API_KEY` avec une valeur dans le repo, dans un playbook ou dans une sortie.

Regles d'usage Legal-FR:

- Utiliser `parallel-cli` seulement pour recherche web publique, extraction, enrichissement, veille ou recherche longue.
- Ajouter `--json` a toutes les commandes executees par un agent ou un script.
- Conserver OpenLegi comme source prioritaire pour le droit positif francais.
- Classer les resultats Parallel comme `secondary` ou `unverified` tant qu'une source officielle n'a pas confirme le point de droit.

## Output Contract

- Markdown pour les rapports et tableaux finaux.
- JSON pour les extractions intermediaires.
- `source`, `localisation`, `confiance` et `verification_humaine_requise` lorsque l'information est extraite d'un document.

## Red flags a surveiller

- source officielle absente.
- source secondaire presentee comme officielle.
- parallel-cli sans sortie JSON.
