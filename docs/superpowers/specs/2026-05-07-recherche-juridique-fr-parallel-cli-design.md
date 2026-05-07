# Design - Recherche Juridique FR Avancee avec Parallel CLI

Date: 2026-05-07  
Statut: design propose pour revue utilisateur  
Portee: ajouter une couche de recherche juridique francaise avancee a Legal-FR, basee sur Parallel CLI, sans renommer ni remplacer `jurisprudence-multilingue`.

## Objectif

Legal-FR dispose deja de 8 workflows cabinet-grade, de schemas, d'evals, de playbooks, d'OpenLegi et d'Exa. La prochaine brique doit ajouter une capacite de recherche juridique francaise profonde, orientee sources, veille et audit de citations.

Le nouveau composant cible uniquement le droit francais:

- droit positif francais;
- jurisprudence francaise;
- doctrine et commentaires francais accessibles publiquement;
- sources institutionnelles francaises;
- veille FR: AMF, CNIL, Cour de cassation, Conseil d'Etat, ministeres, autorites administratives, conventions collectives.

Il ne remplace pas `jurisprudence-multilingue`. Celui-ci reste responsable des usages multi-juridictions, CJUE, CEDH, decisions etrangeres, droit compare et traduction juridique.

## Positionnement

Nom recommande:

```text
recherche-juridique-fr-avancee
```

Role produit:

```text
Question juridique FR
  -> qualification du domaine
  -> recherche OpenLegi pour droit positif et sources officielles
  -> recherche Parallel CLI pour web juridique FR, doctrine, veille et sources complementaires
  -> extraction propre des sources utiles
  -> deep research si la question est complexe
  -> audit des sources et niveaux de confiance
  -> note DRAFT avec citations et points A VERIFIER
```

## Pourquoi Parallel CLI

Parallel CLI est adapte a ce role parce qu'il expose des commandes non interactives, toutes exploitables par agent avec `--json`. Les commandes utiles sont:

- `parallel-cli search`: recherche web naturelle ou par requete, avec filtres de domaine et dates;
- `parallel-cli extract`: extraction markdown propre depuis une URL publique;
- `parallel-cli research run`: recherche profonde multi-sources, synchrone ou async;
- `parallel-cli enrich run`: enrichissement de tableaux ou JSON;
- `parallel-cli findall run`: decouverte d'entites ou de listes;
- `parallel-cli monitor create`: surveillance continue de sources web.

References:

- `https://docs.parallel.ai/integrations/cli`
- `https://parallel.ai/blog/parallel-cli`
- `https://github.com/parallel-web/parallel-web-tools`

## Architecture

### Vertical Legal-FR

```text
plugins/vertical-plugins/legal-fr/
  skills/
    parallel-recherche-juridique-fr/
      SKILL.md
      references/
        source-policy-fr.md
        parallel-cli-patterns.md
        source-ranking.md
    source-audit-juridique-fr/
      SKILL.md
      references/
        typologie-sources-fr.md
        niveaux-confiance.md
    veille-juridique-fr/
      SKILL.md
      references/
        sources-veille-fr.md
        cadence-par-domaine.md
  commands/
    recherche/
      chercher.md
      extraire-source.md
      deep-research.md
      verifier-sources.md
      enrichir-dossier.md
      veille.md
```

### Agent Cowork

```text
plugins/agent-plugins/recherche-juridique-fr-avancee/
  .claude-plugin/
    plugin.json
  agents/
    recherche-juridique-fr-avancee.md
  skills/
    parallel-recherche-juridique-fr/
    source-audit-juridique-fr/
    veille-juridique-fr/
    openlegi-recherche/
    citation-juridique/
    quality-gates-juridiques/
    rapport-executif/
```

Le nouvel agent doit etre self-contained. Les skills sources restent dans `plugins/vertical-plugins/legal-fr/skills/`, puis sont copiees dans le plugin agent comme le reste de l'architecture actuelle.

## Repartition OpenLegi, Parallel CLI, Exa

### OpenLegi

Source prioritaire pour le droit positif francais:

- codes;
- textes consolides;
- jurisprudence officielle disponible;
- conventions collectives;
- JORF, LODA, RNE, EUR-Lex quand expose par OpenLegi.

Regle: toute conclusion critique sur l'etat du droit francais doit chercher une source officielle OpenLegi avant toute source web secondaire.

### Parallel CLI

Moteur de recherche approfondie et d'exploitation web:

- doctrine publique;
- articles de cabinets;
- commentaires d'autorites;
- communiques;
- rapports publics;
- pages institutionnelles non couvertes par OpenLegi;
- veille web;
- extraction de contenu cible;
- recherche multi-sources longue.

Parallel ne remplace pas la source officielle. Il complete, contextualise et documente.

### Exa

Exa reste disponible comme MCP de recherche rapide et exploration web. Le nouvel agent peut l'utiliser pour une premiere recherche courte, mais la trajectoire production-grade pour recherche profonde doit passer par Parallel CLI quand `PARALLEL_API_KEY` et `parallel-cli` sont disponibles.

## Commandes

### `recherche:chercher`

Usage:

```text
[question juridique FR] [domaine optionnel] [sources/domaines optionnels]
```

Workflow:

1. Qualifier le domaine juridique.
2. Interroger OpenLegi si la question touche un texte, regime ou jurisprudence francaise.
3. Lancer `parallel-cli search "[question]" --json`.
4. Si necessaire, filtrer par domaines institutionnels: `legifrance.gouv.fr`, `courdecassation.fr`, `conseil-etat.fr`, `amf-france.org`, `cnil.fr`, `service-public.fr`, `travail-emploi.gouv.fr`.
5. Produire une liste de sources classees.

Sortie:

```json
{
  "query": "...",
  "domain": "droit_social",
  "official_sources": [],
  "secondary_sources": [],
  "source_gaps": [],
  "next_actions": []
}
```

### `recherche:extraire-source`

Usage:

```text
[url] [objectif extraction]
```

Workflow:

```bash
parallel-cli extract <url> --objective "<objectif>" --json
```

Sortie:

- markdown extrait;
- statut de source;
- passages cites;
- limites de confiance;
- recommandation: source utilisable, secondaire seulement, ou a ecarter.

### `recherche:deep-research`

Usage:

```text
[question juridique FR complexe] [processor: lite|base|core|pro|ultra]
```

Workflow:

```bash
parallel-cli research run "<question>" --processor pro --json
```

Pour les recherches longues:

```bash
parallel-cli research run "<question>" --processor pro --no-wait --json
parallel-cli research status <run_id> --json
parallel-cli research poll <run_id> --json
```

Sortie:

- synthese juridique;
- sources officielles;
- sources secondaires;
- points de divergence;
- points `A VERIFIER`;
- audit trail complet.

### `recherche:verifier-sources`

Usage:

```text
[fichier note ou tableau sources]
```

Workflow:

1. Lire les citations et URLs.
2. Classer chaque source.
3. Identifier les conclusions critiques sans source officielle.
4. Marquer les citations secondaires.
5. Produire un rapport de corrections.

### `recherche:enrichir-dossier`

Usage:

```text
[fichier JSON/CSV de societes, parties, textes ou decisions] [intent]
```

Workflow:

```bash
parallel-cli enrich run --source-type json --source <input> --target <output> --intent "<intent>"
```

Cas Legal-FR:

- enrichir une data room DD avec signaux publics FR;
- enrichir une liste de textes avec commentaires institutionnels;
- enrichir des societes avec publications publiques, sanctions ou procedures;
- enrichir une liste de decisions avec contexte doctrinal public.

### `recherche:veille`

Usage:

```text
[sujet] [cadence: daily|weekly|every_two_weeks] [domaines]
```

Workflow:

```bash
parallel-cli monitor create "<sujet>" --cadence weekly --json
```

Sortie:

- configuration de veille;
- sources surveillees;
- schema d'evenement attendu;
- mode de revue humaine.

## Skill `parallel-recherche-juridique-fr`

Responsibilities:

- choisir entre `search`, `extract`, `research`, `enrich`, `findall`, `monitor`;
- imposer `--json`;
- gerer les exit codes CLI;
- preferer les commandes non interactives;
- utiliser `--no-wait` pour travaux longs;
- conserver `run_id` et `interaction_id` dans l'audit trail;
- ne jamais exposer `PARALLEL_API_KEY`.

Pattern de decision:

| Besoin | Commande |
|---|---|
| Trouver des sources | `parallel-cli search ... --json` |
| Lire une URL | `parallel-cli extract ... --json` |
| Question complexe | `parallel-cli research run ... --json` |
| Gros travail long | `research run --no-wait`, puis `status/poll` |
| Enrichir un tableau | `parallel-cli enrich run ...` |
| Trouver une liste d'entites | `parallel-cli findall run ... --json` |
| Veille continue | `parallel-cli monitor create ... --json` |

## Skill `source-audit-juridique-fr`

Typologie des sources:

| Rang | Type | Exemples | Usage |
|---|---|---|---|
| 1 | officielle | Legifrance, OpenLegi, Cour de cassation, Conseil d'Etat, JORF | peut soutenir une conclusion critique |
| 2 | autorite/institution | AMF, CNIL, ACPR, ministeres, URSSAF, Service Public | forte valeur, a croiser si normatif |
| 3 | doctrine professionnelle | cabinets, revues, commentaires praticiens | contexte, pas source finale seule |
| 4 | presse / blog / agregateur | presse, newsletters, sites non officiels | signal faible, jamais source critique seule |
| 5 | inconnu / instable | pages sans auteur, contenu non date | a ecarter ou marquer faible confiance |

Champs obligatoires:

```json
{
  "source_url": "...",
  "source_type": "official|institutional|doctrine|press|unknown",
  "source_status": "verified|secondary|stale|conflicting|unverified",
  "excerpt": "...",
  "legal_point_supported": "...",
  "confidence": 0.0,
  "reviewer_note": "..."
}
```

## Skill `veille-juridique-fr`

Sources prioritaires:

- AMF;
- CNIL;
- Cour de cassation;
- Conseil d'Etat;
- Legifrance / JORF;
- ministere du Travail;
- economie.gouv.fr;
- impots.gouv.fr;
- service-public.fr;
- URSSAF;
- ACPR / Banque de France;
- EUR-Lex uniquement si impact direct FR.

Cadences recommandees:

| Domaine | Cadence |
|---|---|
| AMF / capital markets | daily ou weekly |
| RGPD / CNIL | weekly |
| droit social | weekly |
| baux / immobilier | every_two_weeks |
| contentieux / procedure | weekly |
| contrats / distribution | every_two_weeks |

## Agent `recherche-juridique-fr-avancee`

Frontmatter attendu:

```yaml
---
name: recherche-juridique-fr-avancee
description: Recherche juridique francaise avancee avec OpenLegi, Parallel CLI et audit des sources.
tools: Read, Write, Glob, Grep, Bash(parallel-cli:*), Bash(python:*), mcp__openlegi__*, mcp__exa__*
---
```

Guardrails:

- DRAFT obligatoire;
- OpenLegi avant Parallel pour droit positif FR;
- Parallel en `--json` uniquement;
- pas de conclusion critique sans source officielle ou mention `A VERIFIER`;
- pas de secret dans les outputs;
- pas de conseil juridique definitif;
- citations courtes et auditables;
- validation humaine obligatoire.

## Integration dans les 8 workflows existants

| Workflow | Integration |
|---|---|
| `revue-conformite-interne` | verifier sources des playbooks cabinet et textes cites |
| `analyse-contrats-fournisseurs` | enrichir corpus avec actualites fournisseur, sanctions publiques, doctrine achats |
| `chronologie-contentieux` | trouver contexte public, communiques, decision publiee, source procedurale |
| `jurisprudence-multilingue` | reste multi-juridiction; peut appeler la skill FR pour la partie francaise uniquement |
| `revue-contrats-travail` | veille conventions collectives, droit social, URSSAF, ministere du Travail |
| `red-flags-bail` | veille baux commerciaux, Pinel, indices, doctrine immobiliere publique |
| `note-information-amf` | veille AMF, documents emetteurs, communiques, doctrine et sanctions |
| `tabular-due-diligence` | enrichir data room avec sources publiques FR et signaux faibles |

## Configuration et verification

Nouveaux checks proposes:

```text
scripts/check_legal_fr_parallel_cli.py
```

Checks locaux:

- `parallel-cli --version` executable;
- `parallel-cli auth --json` retourne JSON parseable;
- `PARALLEL_API_KEY` absent: warning, pas erreur si auth locale existe;
- aucune valeur de token hardcodee;
- les commands Legal-FR referencent `--json`;
- la doc mentionne les exit codes.

Sorties attendues:

```text
WARN: PARALLEL_API_KEY is not set; parallel-cli must be authenticated by local login or device flow.
Legal-FR Parallel CLI config OK
```

ou:

```text
Legal-FR Parallel CLI config OK
```

## Evals

Ajouter des fixtures dediees:

```text
plugins/vertical-plugins/legal-fr/evals/fixtures/recherche-juridique-fr-avancee/
  case-001-question-simple/
  case-002-source-officielle-manquante/
  case-003-doctrine-secondaire/
  case-004-veille-amf/
  case-005-deep-research-async/
```

Expected outputs:

- toutes les sorties sont `DRAFT - Validation professionnelle requise`;
- `source_type` present;
- au moins une source officielle requise pour conclusion critique;
- `A VERIFIER` si aucune source officielle;
- `parallel_run_id` ou `parallel_interaction_id` present pour deep research;
- pas de token ni secret.

## Non-objectifs

- Ne pas remplacer `jurisprudence-multilingue`.
- Ne pas etendre a la finance ou a la recherche marche.
- Ne pas appeler Parallel automatiquement si la question peut etre resolue par OpenLegi seul.
- Ne pas stocker les resultats dans un service externe.
- Ne pas cacher les limites de confiance.
- Ne pas hardcoder `PARALLEL_API_KEY`.

## Risques

| Risque | Mitigation |
|---|---|
| cout ou latence Parallel pour deep research | utiliser `search`/`extract` par defaut, `research` seulement si necessaire |
| source secondaire confondue avec source officielle | typologie source obligatoire et quality gate |
| output trop confiant | `A VERIFIER`, confidence, human validation |
| secrets dans logs | checker anti-token et interdiction de print env |
| dependance CLI absente | checker dedie et degradation vers OpenLegi/Exa |
| derive hors FR | prompts et tests limitent le perimetre au droit francais |

## Plan d'implementation propose

1. Ajouter tests RED pour structure agent/skills/commands/checker/evals.
2. Ajouter `scripts/check_legal_fr_parallel_cli.py`.
3. Ajouter skills `parallel-recherche-juridique-fr`, `source-audit-juridique-fr`, `veille-juridique-fr`.
4. Ajouter commands `recherche/*`.
5. Ajouter agent plugin `recherche-juridique-fr-avancee`.
6. Synchroniser skills dans l'agent plugin.
7. Ajouter eval fixtures et expected outputs.
8. Mettre a jour README/CONNECTORS/CLAUDE Legal-FR.
9. Etendre `scripts/check.py` si necessaire.
10. Verifier: `scripts/check.py`, tests Legal-FR, eval runner, connector checker, nouveau checker Parallel.

## Criteres d'acceptation

- `recherche-juridique-fr-avancee` est installe comme agent plugin autonome.
- Les 3 skills sources existent dans `legal-fr`.
- Les 6 commands `recherche/*` existent.
- Le checker Parallel CLI detecte CLI manquant, auth manquante et config OK.
- Les commands utilisent `Bash(parallel-cli:*)` et imposent `--json`.
- Les outputs distinguent sources officielles et secondaires.
- `jurisprudence-multilingue` reste present et non renomme.
- Les tests et evals passent.
- Aucun secret hardcode.
- Aucun livrable externe sans `DRAFT - Validation professionnelle requise`.
