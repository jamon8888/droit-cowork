# Design — Vertical Legal-FR Legora

Date: 2026-05-07  
Statut: implementation V1 planifiee  
Objectif: creer une verticale juridique francaise inspiree des workflows Legora, avec un socle commun reutilisable et des agents Cowork metier.

## Decision d'architecture

L'architecture retenue est un modele hybride:

1. `plugins/vertical-plugins/legal-fr/` porte le socle juridique commun.
2. `plugins/agent-plugins/<workflow>/` porte les 8 agents Cowork autonomes.
3. Les agents bundlent les skills utiles depuis `legal-fr`, comme les agents financiers existants bundlent leurs skills depuis les verticals.
4. Les cookbooks Managed Agent sont prevus en extension, mais non crees dans la premiere passe sauf demande explicite.

Cette option evite la duplication entre les 8 workflows tout en exploitant les agents pour les livrables de bout en bout.

## Perimetre initial

Le vertical `legal-fr` doit couvrir les 8 workflows Legora-FR suivants:

| Workflow | Agent plugin | Command family |
|---|---|---|
| Revue conformite interne | `revue-conformite-interne` | `conformite:*` |
| Analyse contrats fournisseurs | `analyse-contrats-fournisseurs` | `fournisseur:*` |
| Chronologie contentieux | `chronologie-contentieux` | `chrono:*` |
| Jurisprudence multilingue | `jurisprudence-multilingue` | `jurisprudence:*` |
| Revue contrats travail | `revue-contrats-travail` | `travail:*` |
| Red flags bail | `red-flags-bail` | `bail:*` |
| Note information AMF | `note-information-amf` | `amf:*` |
| Tabular due diligence | `tabular-due-diligence` | `tdd:*` |

## Vertical commun

Structure cible:

```text
plugins/vertical-plugins/legal-fr/
  .claude-plugin/plugin.json
  .mcp.json
  README.md
  CHANGELOG.md
  CLAUDE.md
  CONNECTORS.md
  commands/
    conformite/*.md
    fournisseur/*.md
    chrono/*.md
    jurisprudence/*.md
    travail/*.md
    bail/*.md
    amf/*.md
    tdd/*.md
  playbooks/
    README.md
    format-playbook.md
    playbook-cgv-standard.md
    playbook-dpa-art28.md
    playbook-contrats-fournisseurs.md
    playbook-contrats-travail.md
    playbook-bail-commercial.md
    playbook-cession-pme.md
    playbook-lbo.md
    playbook-immobilier.md
    playbook-dette.md
  skills/
    confidentialite-donnees/
    tabular-review/
    lecture-playbook/
    conformite-contractuelle/
    rgpd-baseline/
    droit-achats-fr/
    extraction-termes/
    analyse-risques-supply/
    extraction-evenements/
    procedure-civile-delais/
    analyse-causalite/
    sources-jurisprudence/
    lecture-decision/
    droit-compare/
    traduction-juridique/
    droit-social-fr/
    conventions-collectives/
    remuneration-compliance/
    protection-vie-privee-rh/
    statut-baux-commerciaux/
    loi-pinel-baux/
    clauses-non-standard/
    fiscalite-immobiliere/
    droit-marches-financiers/
    facteurs-risque/
    gouvernance-societe/
    esg-disclosure/
    tabular-extraction/
    droit-cession-fr/
    consolidation-rapport/
    red-flags-juridiques/
```

Les skills `confidentialite-donnees`, `tabular-review` et `lecture-playbook` sont transverses. Les autres skills sont regroupees par domaine, mais restent dans un seul vertical pour permettre la reutilisation par plusieurs agents.

## Agents Cowork

Chaque agent plugin suit la structure existante:

```text
plugins/agent-plugins/<agent-slug>/
  .claude-plugin/plugin.json
  agents/<agent-slug>.md
  skills/<skill>/...
```

Chaque prompt agent doit inclure:

- role professionnel et profil cible;
- livrables attendus;
- workflow et points de controle humain;
- regles de confidentialite et minimisation des donnees dans les sorties;
- skills utilisees;
- limites deontologiques: draft, validation professionnelle, pas d'action irreversible.

Le bundling des skills se fera par copie depuis `plugins/vertical-plugins/legal-fr/skills/`, puis `scripts/check.py` devra verifier qu'aucune skill referencee par un agent n'est absente de son bundle.

## Taxonomie agentique

La verticale juridique ne doit pas etre pensee comme 8 agents monolithiques. Elle doit separer les agents orchestrateurs visibles par l'utilisateur, les workers reutilisables et les skills de methode.

### Agents orchestrateurs

Les orchestrateurs correspondent aux 8 plugins Cowork. Ils possedent le livrable final, l'ordre des etapes, les points de validation humaine et les decisions de routing entre workers.

| Agent orchestrateur | Mission | Livrable principal |
|---|---|---|
| `revue-conformite-interne` | Verifier un document contre un playbook cabinet ou entreprise. | Tableau de conformite + recommandations |
| `analyse-contrats-fournisseurs` | Extraire et comparer les conditions fournisseurs sur un corpus. | Tableau fournisseurs consolide |
| `chronologie-contentieux` | Reconstruire la chronologie factuelle et procedurale d'un dossier. | Chronologie + verification des delais |
| `jurisprudence-multilingue` | Rechercher, analyser, comparer et traduire des decisions. | Note jurisprudentielle sourcee |
| `revue-contrats-travail` | Auditer contrats RH et clauses sensibles en droit social FR. | Analyse contrat ou tableau RH |
| `red-flags-bail` | Detecter les risques dans les baux et simuler les effets financiers. | Red flag report bail |
| `note-information-amf` | Rediger et verifier les facteurs de risque et sections AMF. | Draft facteurs de risque |
| `tabular-due-diligence` | Extraire massivement les termes d'une data room et scorer les risques. | Tableau DD + rapport executif |

### Workers reutilisables

Ces workers ne sont pas necessairement exposes comme plugins Cowork. En V1, ils sont decrits dans les prompts orchestrateurs. En V2, ils pourront devenir des subagents dans `managed-agent-cookbooks/<agent>/subagents/*.yaml`.

| Worker | Role | Sortie attendue | Utilise par |
|---|---|---|---|
| `intake-classifier` | Identifier type de document, domaine juridique, langue, qualite OCR, priorite. | JSON d'inventaire documentaire | fournisseurs, contentieux, travail, baux, AMF, DD |
| `playbook-interpreter` | Lire un playbook et produire une checklist executable. | JSON `rules[]`, `terms[]`, `red_flags[]` | conformite, fournisseurs, travail, baux, DD |
| `document-extractor` | Extraire champs, clauses, dates et citations depuis un document. | JSON conforme au schema du workflow | fournisseurs, contentieux, travail, baux, AMF, DD |
| `legal-source-checker` | Verifier textes, articles, regimes et citations via OpenLegi. | Liste de sources verifiees + alertes d'incertitude | tous |
| `case-law-researcher` | Rechercher jurisprudence et doctrine via OpenLegi et Exa. | Decisions classees par pertinence | jurisprudence, contentieux, travail, baux, AMF |
| `risk-scorer` | Transformer observations et red flags en score structure. | Score 0-10 + gravite + justification | fournisseurs, travail, baux, AMF, DD |
| `table-consolidator` | Fusionner JSON batch en tableau Markdown/exportable. | Tableau consolide avec coverage | fournisseurs, contentieux, travail, baux, DD |
| `report-drafter` | Rediger une synthese narrative depuis le tableau et les sources. | Rapport Markdown final | tous |
| `legal-qa-reviewer` | Controler citations, incertitudes, coherences, mentions DRAFT. | Liste d'issues + version corrigee si possible | tous |
| `deadline-checker` | Calculer delais, echeances, forclusions et alertes. | Tableau d'echeances | contentieux, travail, baux |
| `financial-terms-checker` | Verifier loyers, indexations, penalites, seuils financiers. | JSON calculs + alertes | fournisseurs, baux, AMF, DD |
| `translation-specialist` | Traduire en preservant concepts juridiques et faux amis. | Traduction + glossaire | jurisprudence |

### Regles de delegation

- L'orchestrateur ne fait pas l'extraction brute si un worker peut produire un JSON plus stable.
- Les workers d'extraction retournent du JSON, jamais du Markdown narratif.
- Les workers de recherche doivent distinguer source officielle, source secondaire et hypothese.
- Le `legal-qa-reviewer` est appele avant toute sortie externe ou quasi-finale.
- Les workflows de corpus utilisent des batches de 5 documents maximum et consolident progressivement.

## Matrice workflows, agents, skills et outputs

| Workflow | Orchestrateur | Workers principaux | Skills critiques | Commands | Outputs |
|---|---|---|---|---|---|
| Revue conformite interne | `revue-conformite-interne` | `playbook-interpreter`, `document-extractor`, `legal-source-checker`, `risk-scorer`, `table-consolidator`, `legal-qa-reviewer` | `lecture-playbook`, `creation-playbook`, `conformite-contractuelle`, `rgpd-baseline`, `citation-juridique`, `quality-gates-juridiques` | `conformite/verifier.md`, `conformite/creer-playbook.md`, `conformite/rapport.md` | `RAPPORT-CONFORMITE-*.md`, `playbooks/*.md` |
| Analyse contrats fournisseurs | `analyse-contrats-fournisseurs` | `intake-classifier`, `playbook-interpreter`, `document-extractor`, `financial-terms-checker`, `risk-scorer`, `table-consolidator`, `report-drafter` | `droit-achats-fr`, `extraction-termes`, `analyse-risques-supply`, `tabular-review`, `tableau-consolide` | `fournisseur/analyser-un.md`, `fournisseur/analyser-corpus.md`, `fournisseur/comparer.md`, `fournisseur/alertes.md` | `TABLEAU-FOURNISSEURS-*.md`, `ALERTES-CONTRATS-*.md` |
| Chronologie contentieux | `chronologie-contentieux` | `intake-classifier`, `document-extractor`, `deadline-checker`, `case-law-researcher`, `table-consolidator`, `report-drafter`, `legal-qa-reviewer` | `extraction-evenements`, `procedure-civile-delais`, `analyse-causalite`, `openlegi-recherche`, `fiche-audience` | `chrono/construire.md`, `chrono/verifier-delais.md`, `chrono/fiche-audience.md` | `CHRONOLOGIE-*.md`, `VERIFICATION-DELAIS-*.md`, `FICHE-AUDIENCE-*.md` |
| Jurisprudence multilingue | `jurisprudence-multilingue` | `case-law-researcher`, `legal-source-checker`, `document-extractor`, `translation-specialist`, `report-drafter`, `legal-qa-reviewer` | `sources-jurisprudence`, `lecture-decision`, `droit-compare`, `traduction-juridique`, `exa-recherche-juridique`, `openlegi-recherche` | `jurisprudence/rechercher.md`, `jurisprudence/analyser.md`, `jurisprudence/traduire.md`, `jurisprudence/comparer-juridictions.md` | `JURISPRUDENCE-*.md`, `TRADUCTION-DECISION-*.md`, `COMPARAISON-JURIDICTIONS-*.md` |
| Revue contrats travail | `revue-contrats-travail` | `intake-classifier`, `document-extractor`, `legal-source-checker`, `deadline-checker`, `risk-scorer`, `table-consolidator`, `legal-qa-reviewer` | `droit-social-fr`, `conventions-collectives`, `remuneration-compliance`, `protection-vie-privee-rh`, `tabular-review` | `travail/analyser.md`, `travail/corpus-rh.md`, `travail/verifier-non-concurrence.md`, `travail/conformite-ccn.md` | `ANALYSE-CONTRAT-TRAVAIL-*.md`, `TABLEAU-RH-*.md` |
| Red flags bail | `red-flags-bail` | `intake-classifier`, `document-extractor`, `financial-terms-checker`, `legal-source-checker`, `risk-scorer`, `report-drafter`, `legal-qa-reviewer` | `statut-baux-commerciaux`, `loi-pinel-baux`, `clauses-non-standard`, `fiscalite-immobiliere`, `red-flags-juridiques` | `bail/analyser.md`, `bail/corpus-baux.md`, `bail/simuler-renouvellement.md` | `ANALYSE-BAIL-*.md`, `TABLEAU-BAUX-*.md`, `SIMULATION-RENOUVELLEMENT-*.md` |
| Note information AMF | `note-information-amf` | `intake-classifier`, `document-extractor`, `case-law-researcher`, `risk-scorer`, `legal-source-checker`, `report-drafter`, `legal-qa-reviewer` | `droit-marches-financiers`, `facteurs-risque`, `gouvernance-societe`, `esg-disclosure`, `citation-juridique` | `amf/rediger-facteurs-risque.md`, `amf/checker-conformite.md`, `amf/extraire-kpi.md`, `amf/generer-resume.md` | `FACTEURS-RISQUE-DRAFT-*.md`, `CHECK-AMF-*.md`, `RESUME-NOTE-*.md` |
| Tabular due diligence | `tabular-due-diligence` | `intake-classifier`, `playbook-interpreter`, `document-extractor`, `risk-scorer`, `table-consolidator`, `legal-source-checker`, `report-drafter`, `legal-qa-reviewer` | `tabular-extraction`, `droit-cession-fr`, `consolidation-rapport`, `red-flags-juridiques`, `tabular-review`, `format-json-intermediaire` | `tdd/init.md`, `tdd/extraire-corpus.md`, `tdd/consolider.md`, `tdd/rapport-executif.md`, `tdd/verifier-sources.md` | `TABLEAU-DD-*.md`, `RAPPORT-EXECUTIF-DD-*.md`, `JSONL batches` |

## Cartographie des skills

La liste de skills doit etre factorisee par famille pour eviter une verticale plate difficile a maintenir.

```text
skills/
  core/
    confidentialite-donnees/
    quality-gates-juridiques/
    format-json-intermediaire/
    tabular-review/
  sources/
    openlegi-recherche/
    exa-recherche-juridique/
    citation-juridique/
    sources-jurisprudence/
  playbooks/
    lecture-playbook/
    creation-playbook/
    scoring-playbook/
  outputs/
    tableau-consolide/
    rapport-executif/
    fiche-audience/
    note-amf/
  domaines/
    contrats/
    achats/
    social/
    contentieux/
    baux/
    capital-markets/
    due-diligence/
```

Le depot existant utilise `skills/<skill>/SKILL.md` sans sous-familles. Pour rester compatible avec `scripts/check.py`, l'implementation V1 peut garder des dossiers plats, mais les README du vertical doivent documenter cette cartographie logique.

## Pattern Tabular Review

Le pattern commun est:

```text
Corpus documents
  -> inventaire et classification
  -> verification de lisibilite et classification documentaire
  -> batches de 5 documents maximum
  -> extraction parallele par agent specialise
  -> JSON intermediaires
  -> scoring risque
  -> consolidation tabulaire Markdown
  -> rapport narratif optionnel
```

Regles:

- batch maximum: 5 documents;
- sortie intermediaire: JSON structure, pas Markdown;
- consolidation separee de l'extraction;
- tableau final produit avant tout rapport narratif;
- documents illisibles marques `ILLISIBLE`, pas ignores;
- confiance inferieure a `0.7` signalee par `[VERIFICATION HUMAINE REQUISE]`.

## Connecteurs et dependances

### Exa MCP

Statut: requis pour recherche web, veille, jurisprudence et sources institutionnelles non disponibles localement.  
Source verifiee: <https://github.com/exa-labs/exa-mcp-server>  
Configuration cible:

```json
{
  "mcpServers": {
    "exa": {
      "type": "http",
      "url": "https://mcp.exa.ai/mcp"
    }
  }
}
```

Exa expose notamment `web_search_exa` et `web_fetch_exa`; les outils avances peuvent etre actives par parametre `tools` si necessaire.

### OpenLegi MCP

Statut: requis pour sources juridiques francaises officielles.  
Source verifiee: <https://auth.openlegi.fr/documentation/legal/>  
Usage: acces aux sources juridiques officielles francaises via API PISTE de Legifrance.

La configuration exacte dependra du mode d'authentification OpenLegi retenu. Le vertical doit donc documenter OpenLegi dans `CONNECTORS.md` et placer une entree `.mcp.json` explicite avec variables d'environnement, sans hardcoder de secret.

### Parallel Agent Skills

Statut: dependance CLI, pas MCP.  
Source verifiee: <https://docs.parallel.ai/integrations/agent-skills> et <https://github.com/parallel-web/parallel-agent-skills>  
Usage: enrichir les agents avec recherche, extraction web, deep research et data enrichment via Agent Skills CLI.

Installation cible documentee:

```bash
npx skills add parallel-web/parallel-agent-skills --all --global
```

Ou installation ciblee:

```bash
npx skills add parallel-web/parallel-agent-skills --skill parallel-web-search
```

Le repo ne doit pas vendor ces skills externes dans `legal-fr`; il doit seulement documenter leur installation et les considerer comme prerequis optionnels pour les workflows de recherche lourde.

### bodacc-mcp

Statut: differe.  
Usage potentiel: verification BODACC, evenements societaires, procedures collectives pour `note-information-amf` et `tabular-due-diligence`.

La premiere implementation ne l'ajoute pas a `.mcp.json`, car les MCP demandes explicitement pour cette version sont Exa et OpenLegi. `bodacc-mcp` reste documente comme extension future.

## Marketplace

La premiere implementation doit ajouter dans `.claude-plugin/marketplace.json`:

- `legal-fr` comme vertical plugin;
- les 8 agents Cowork si leurs dossiers sont crees dans la meme passe.

Chaque `plugin.json` individuel reste conforme au schema actuel du depot:

```json
{
  "name": "<slug>",
  "version": "1.0.0",
  "description": "...",
  "author": {
    "name": "Hacienda.diy"
  }
}
```

## Validation

Commandes de verification minimales:

```bash
python scripts/check.py
npx gitnexus analyze --embeddings
```

`scripts/check.py` est obligatoire apres scaffolding. GitNexus est recommande apres creation de nombreux fichiers pour garder l'index coherent.

## Decisions d'implementation initiales

- Les 8 agents Cowork sont crees des la premiere passe.
- Les cookbooks Managed Agent ne sont pas crees dans cette passe.
- Les commandes utilisent le format en dossiers, par exemple `commands/conformite/verifier.md`, conforme a la spec fournie.
- `.mcp.json` inclut `exa` et `openlegi`. `parallel-agent-skills` est documente dans `CONNECTORS.md`, pas declare comme MCP.
- L'anonymisation locale est exclue de cette premiere version. Les fichiers mentionnent seulement qu'elle pourra etre ajoutee ulterieurement.
- `bodacc-mcp` est differe et seulement mentionne comme extension possible.

## Scope de la premiere implementation

La premiere implementation doit creer les fichiers de structure et les contenus de base utilisables:

- manifests;
- README et CONNECTORS;
- CLAUDE.md commun;
- commands avec frontmatter et workflow;
- skills avec instructions operationnelles initiales;
- playbooks standards;
- prompts des 8 agents;
- marketplace.

Elle ne doit pas encore creer les cookbooks Managed Agent, sauf si le perimetre est explicitement etendu.

## Risques et garde-fous

- Risque de conseil juridique non valide: tous les outputs externes portent `DRAFT — Validation professionnelle requise`.
- Risque donnees personnelles: pas de blocage technique dans cette version; les prompts doivent rappeler de ne pas exposer de donnees personnelles dans les sorties et de privilegier les references anonymisees quand le corpus le permet.
- Risque de sources obsoletes: OpenLegi et Exa doivent etre utilises pour les questions de droit positif ou jurisprudence recente.
- Risque de duplication: les skills communes restent dans `legal-fr`; les agents ne gardent que des copies synchronisees.
- Risque de corpus massif: Tabular Review impose des JSON intermediaires et batches de 5 documents.
