# Design - Legal-FR Production-Grade Cabinet

Date: 2026-05-07  
Statut: design valide pour revue utilisateur  
Portee: transformer le scaffold Legal-FR Legora en suite juridique exploitable en cabinet, avec les 8 workflows inclus.

## Objectif

La V1 Legal-FR cree une architecture propre: un vertical commun `legal-fr`, 8 agents Cowork, commands, skills, playbooks, MCP Exa/OpenLegi et tests structurels.

La V2 production-grade cabinet doit passer d'un scaffold a une chaine juridique controlee:

```text
document ou corpus
  -> intake
  -> extraction JSON stricte
  -> verification des sources
  -> scoring et red flags
  -> consolidation
  -> revue qualite juridique
  -> validation humaine
  -> livrable DRAFT trace
```

Le produit cible n'est pas seulement "8 plugins qui generent du Markdown". Il doit fournir des workflows metier fiables, auditables, sourcees et utilisables par des professionnels du droit francais.

## Inspiration Legora et Harvey

### Ce que l'on reprend de Legora

- revue tabulaire de corpus volumineux;
- extraction parallele par lots;
- playbooks codifies par cabinet;
- outputs comparables et exportables;
- logique cabinet-client: un livrable lisible par le client, mais controle par le cabinet;
- workflow "sources -> extraction -> tableau -> rapport".

### Ce que l'on reprend de Harvey

- profondeur analytique par domaine;
- agents specialises par tache juridique;
- raisonnement multi-etapes;
- revue contractuelle detaillee;
- red flags argumentes;
- synthese executive exploitable par associe, juriste senior ou client.

### Adaptation au contexte francais

La suite doit etre native droit francais, pas une simple traduction:

- sources officielles francaises via OpenLegi / Legifrance;
- jurisprudence et veille completees par Exa quand la source officielle ne suffit pas;
- references explicites aux textes, regimes, chambres, dates et numeros quand disponibles;
- limites deontologiques: livrables DRAFT, validation professionnelle obligatoire;
- usages cabinet: note interne, rapport client, tableau de revue, checklist de closing, fiche audience;
- contraintes donnees: minimisation, pas de secret ou donnee personnelle inutile dans les outputs.

## Non-objectifs

Cette V2 ne doit pas viser:

- remplacer la validation d'un avocat, notaire, juriste, DPO ou expert-comptable;
- produire des actes opposables automatiquement;
- donner une conclusion juridique definitive sans mention d'incertitude;
- resoudre toute la confidentialite par promesse textuelle uniquement;
- construire un SaaS complet avec comptes clients, facturation et monitoring cloud;
- integrer legacy anonymization MCP dans cette phase, sauf decision ulterieure.

## Architecture Cible

La V2 conserve l'architecture hybride:

```text
plugins/vertical-plugins/legal-fr/
  noyau commun
  commands
  skills
  playbooks
  schemas
  evals

plugins/agent-plugins/<workflow>/
  agent visible
  prompt orchestrateur
  skills bundlees
```

Elle ajoute une couche production-grade:

```text
plugins/vertical-plugins/legal-fr/
  schemas/
    common/
    workflows/
  evals/
    fixtures/
    expected/
    rubrics/
  audit/
    README.md
  quality-gates/
    README.md
```

## Noyau Commun Cabinet-Grade

Tous les workflows doivent utiliser le meme noyau, pour eviter 8 implementations faibles et divergentes.

### `intake-classifier`

Mission:
- identifier type de document, langue, domaine juridique, qualite OCR, presence de pieces jointes, urgence;
- separer document principal, annexes, pieces, correspondances et sources externes;
- produire un JSON d'inventaire.

Sortie minimale:

```json
{
  "document_id": "string",
  "filename": "string",
  "detected_type": "contract|case_law|email|pleading|lease|employment|financial|unknown",
  "language": "fr|en|de|other|mixed",
  "legal_domain": "contracts|social|baux|contentieux|capital_markets|due_diligence|unknown",
  "readability": {
    "status": "ok|ocr_weak|unreadable",
    "confidence": 0.0
  },
  "requires_human_triage": false
}
```

### `schema-extractor`

Mission:
- extraire les champs selon le schema du workflow;
- retourner du JSON strict;
- citer les passages documentaires utilises;
- ne pas produire de synthese narrative.

Regle:
- aucun tableau final ne doit etre construit directement depuis du texte libre;
- le tableau final vient toujours de JSON intermediaires.

### `source-verifier`

Mission:
- verifier textes, articles, regimes, dates, jurisprudences et citations;
- distinguer source officielle, source secondaire, source web et hypothese;
- signaler tout point de droit potentiellement obsolete.

Priorite des sources:

1. OpenLegi / Legifrance / source officielle equivalente.
2. EUR-Lex, Curia, CEDH, AMF, CNIL, ACPR, INPI, BODACC si disponible.
3. Exa pour decouverte, comparaison, doctrine ou source non officielle.
4. Memoire interne seulement comme piste, jamais comme source finale suffisante.

### `risk-scorer`

Mission:
- scorer les risques avec une methode stable;
- separer gravite juridique, impact operationnel, probabilite, urgence et confiance.

Score recommande:

```json
{
  "severity": "blocking|major|minor|info",
  "legal_impact": 0,
  "business_impact": 0,
  "probability": 0,
  "urgency": 0,
  "confidence": 0.0,
  "global_score": 0.0,
  "rationale": "string"
}
```

### `legal-qa-reviewer`

Mission:
- verifier coherence, citations, sources, incertitudes, absence de conclusion definitive;
- controler que le livrable est marque DRAFT;
- signaler les hallucinations possibles;
- refuser un livrable si les sources critiques sont absentes.

Critere bloquant:
- une recommandation juridique majeure sans source ou extrait documentaire doit rester en `A VERIFIER`.

### `human-validation-gate`

Mission:
- rendre visible ce qui doit etre valide par un professionnel;
- produire une checklist de validation;
- distinguer livrable interne et livrable externe.

Regle:
- tous les outputs externes portent `DRAFT - Validation professionnelle requise`;
- les conclusions critiques doivent avoir un champ `validated_by_human: false` par defaut.

### `audit-trail`

Mission:
- relier chaque conclusion a:
  - document source;
  - extrait cite;
  - regle ou source juridique;
  - agent ou worker ayant produit l'observation;
  - niveau de confiance;
  - statut de validation.

Sortie cible:

```json
{
  "finding_id": "RF-001",
  "workflow": "red-flags-bail",
  "document_id": "bail-001",
  "source_excerpt": "string",
  "legal_source": {
    "type": "official|case_law|secondary|none",
    "citation": "string",
    "url": "string"
  },
  "agent": "document-extractor",
  "reviewer": "legal-qa-reviewer",
  "confidence": 0.82,
  "validated_by_human": false
}
```

## Les 8 Workflows en Production-Grade

Chaque workflow doit avoir:

- un schema JSON d'extraction;
- un playbook metier enrichi;
- une matrice de risques;
- une fixture de test synthetique;
- un expected output;
- une grille d'evaluation;
- un quality gate final.

### 1. `revue-conformite-interne`

Objectif cabinet:
- transformer les standards internes en playbooks executables;
- verifier un contrat entrant contre ces standards.

Production-grade:
- playbooks versionnes;
- regles avec base legale ou base cabinet;
- matrice conforme / non conforme / incertain;
- detection des clauses bloquantes;
- rapport de conformite trace.

Livrables:
- `RAPPORT-CONFORMITE-*.md`
- `AUDIT-CONFORMITE-*.json`
- playbook enrichi si creation demandee.

### 2. `analyse-contrats-fournisseurs`

Objectif cabinet:
- analyser un portefeuille de contrats fournisseurs;
- comparer termes, delais, renouvellements, penalites, juridiction et dependance.

Production-grade:
- extraction batch par JSON;
- tableau consolide;
- alertes echeances;
- controle LME / delais de paiement / sous-traitance;
- scoring par fournisseur.

Livrables:
- `TABLEAU-FOURNISSEURS-*.md`
- `ALERTES-CONTRATS-*.md`
- `AUDIT-FOURNISSEURS-*.json`

### 3. `chronologie-contentieux`

Objectif cabinet:
- reconstruire la chronologie factuelle et procedurale d'un dossier.

Production-grade:
- extraction dates, actes, auteurs, destinataires, pieces;
- deduplication des evenements;
- verification des delais;
- detection incoherences et pieces manquantes;
- fiche audience.

Livrables:
- `CHRONOLOGIE-*.md`
- `VERIFICATION-DELAIS-*.md`
- `FICHE-AUDIENCE-*.md`
- `AUDIT-CHRONOLOGIE-*.json`

### 4. `jurisprudence-multilingue`

Objectif cabinet:
- rechercher, analyser, comparer et traduire des decisions.

Production-grade:
- requetes separees sources officielles / Exa;
- fiches de decision structurees;
- traduction avec glossaire;
- statut source officielle / secondaire;
- comparaison inter-juridictions.

Livrables:
- `JURISPRUDENCE-*.md`
- `TRADUCTION-DECISION-*.md`
- `COMPARAISON-JURIDICTIONS-*.md`
- `AUDIT-SOURCES-*.json`

### 5. `revue-contrats-travail`

Objectif cabinet:
- auditer contrats de travail, clauses sensibles, remuneration et convention collective.

Production-grade:
- schema CDI / CDD / avenant / rupture;
- controle clause de non-concurrence;
- controle periode d'essai;
- minima legaux et conventionnels avec source;
- statut CCN explicite: detectee, fournie, absente, a verifier.

Livrables:
- `ANALYSE-CONTRAT-TRAVAIL-*.md`
- `TABLEAU-RH-*.md`
- `AUDIT-SOCIAL-*.json`

### 6. `red-flags-bail`

Objectif cabinet:
- detecter risques dans baux commerciaux, professionnels, derogatoires et mixtes.

Production-grade:
- qualification du bail;
- controle statut baux commerciaux;
- charges Pinel;
- indexation et renouvellement;
- simulation financiere documentee;
- red flags par position preneur / bailleur.

Livrables:
- `ANALYSE-BAIL-*.md`
- `TABLEAU-BAUX-*.md`
- `SIMULATION-RENOUVELLEMENT-*.md`
- `AUDIT-BAIL-*.json`

### 7. `note-information-amf`

Objectif cabinet:
- assister la redaction et le controle des facteurs de risque et sections AMF.

Production-grade:
- classification risques par categorie;
- materialite et probabilite;
- coherence avec documents entreprise;
- controle genericite des facteurs de risque;
- checklist pre-depot;
- sources AMF / Prospectus / MAR / ESG quand pertinentes.

Livrables:
- `FACTEURS-RISQUE-DRAFT-*.md`
- `CHECK-AMF-*.md`
- `RESUME-NOTE-*.md`
- `AUDIT-AMF-*.json`

### 8. `tabular-due-diligence`

Objectif cabinet:
- analyser une data room massive avec extraction parallele, scoring et rapport executif.

Production-grade:
- inventaire corpus;
- batch de 5 documents maximum;
- JSONL intermediaires;
- consolidation par categorie;
- coverage explicite;
- tableau final avant rapport narratif;
- go / no-go / go conditionnel documente.

Livrables:
- `TABLEAU-DD-*.md`
- `RAPPORT-EXECUTIF-DD-*.md`
- `BATCH-*.jsonl`
- `AUDIT-DD-*.json`

## Schemas JSON

Chaque workflow doit avoir deux schemas:

1. `extraction.schema.json`: format des observations brutes.
2. `report.schema.json`: format minimal attendu avant generation Markdown.

Les schemas communs sont:

```text
schemas/common/
  document-intake.schema.json
  source-citation.schema.json
  risk-score.schema.json
  finding.schema.json
  audit-trail.schema.json
  human-validation.schema.json
```

Les schemas workflow sont:

```text
schemas/workflows/
  revue-conformite-interne/
  analyse-contrats-fournisseurs/
  chronologie-contentieux/
  jurisprudence-multilingue/
  revue-contrats-travail/
  red-flags-bail/
  note-information-amf/
  tabular-due-diligence/
```

## Evals Cabinet-Grade

Les tests structurels actuels valident l'existence des fichiers. La V2 doit ajouter des evals metier.

Structure cible:

```text
evals/
  fixtures/
    <workflow>/
      case-001/
        input.md
        playbook.md
        metadata.json
  expected/
    <workflow>/
      case-001.expected.json
  rubrics/
    <workflow>.rubric.md
```

Types de cas requis:

- cas conforme;
- cas avec red flag bloquant;
- cas avec incertitude juridique;
- cas document illisible ou incomplet;
- cas source introuvable;
- cas corpus multi-documents pour les workflows tabulaires.

Critere de succes:

- pas de faux negatif sur les red flags bloquants connus;
- les sources critiques sont citees ou marquees `A VERIFIER`;
- aucune conclusion definitive sans validation humaine;
- le JSON respecte le schema;
- les erreurs sont explicites, pas masquees.

## Quality Gates

Un livrable ne passe pas en sortie finale si:

- il manque la mention `DRAFT - Validation professionnelle requise`;
- une citation critique n'a pas de source;
- un document illisible est ignore au lieu d'etre marque;
- une conclusion juridique est formulee comme certaine alors que la source est absente;
- le score de confiance global est inferieur a 0.7 sans alerte;
- le tableau de corpus n'indique pas la coverage;
- le schema JSON intermediaire est invalide.

## Confidentialite et Donnees

legacy anonymization MCP est volontairement hors scope pour cette phase, mais la V2 doit deja imposer:

- minimisation des donnees dans les sorties;
- pas de noms, adresses, IBAN, NIR ou informations sensibles dans les exemples;
- possibilite de referencer les parties par `PARTIE-A`, `PARTIE-B`, `SALARIE-001`, `FOURNISSEUR-001`;
- aucun secret dans `.mcp.json`;
- `OPENLEGI_TOKEN` uniquement via variable d'environnement;
- avertissement si un document contient des donnees personnelles manifestes.

Cette couche ne remplace pas une vraie anonymisation. Elle prepare seulement le retour futur d'un module dedie.

## Connecteurs

### OpenLegi

Role:
- verification des textes et sources officielles francaises;
- support principal pour droit positif.

Exigence:
- aucun token hardcode;
- erreur claire si `OPENLEGI_TOKEN` absent;
- statut de source conserve dans l'audit trail.

### Exa

Role:
- recherche web, doctrine, veille, decisions ou contexte non directement disponible via OpenLegi;
- comparaison de sources;
- enrichissement pour jurisprudence multilingue et capital markets.

Exigence:
- distinguer resultat Exa et source officielle;
- ne jamais traiter Exa comme autorite juridique finale sans verification.

### Parallel Agent Skills

Role:
- accelerer recherche, extraction web et deep research via CLI;
- rester optionnel et documente.

Exigence:
- ne pas vendor les skills externes dans `legal-fr`;
- documenter installation et usage;
- prevoir fallback Exa/OpenLegi si Parallel n'est pas installe.

## Agents et Workers

La suite doit distinguer:

- agents orchestrateurs visibles: les 8 workflows;
- workers internes reutilisables: extraction, source checking, scoring, QA;
- skills: savoir-faire et references metier;
- playbooks: standards cabinet versionnes;
- schemas: contrat technique entre workers.

Regle:
- l'orchestrateur coordonne;
- le worker extrait ou verifie;
- le schema controle;
- le QA reviewer bloque si la qualite est insuffisante;
- l'humain valide.

## Definition of Done V2

Pour considerer un workflow production-grade cabinet:

- schema JSON present et valide;
- au moins 5 fixtures metier;
- au moins 1 cas corpus si workflow tabulaire;
- playbook enrichi;
- sources critiques verifiees via OpenLegi ou marquees `A VERIFIER`;
- quality gate applique;
- audit trail produit;
- output Markdown final genere depuis JSON;
- tests structurels et evals passent;
- documentation d'usage cabinet presente.

Pour considerer la suite complete production-grade cabinet:

- les 8 workflows respectent la definition ci-dessus;
- le noyau commun est partage, pas copie-colle divergent;
- `scripts/check.py` passe;
- les evals passent;
- GitNexus est a jour;
- les limites de confidentialite sont explicites;
- aucune dependance externe ne requiert un secret hardcode.

## Roadmap Recommandee

### Phase 1 - Noyau commun

- ajouter `schemas/common`;
- enrichir skills `quality-gates-juridiques`, `format-json-intermediaire`, `citation-juridique`;
- definir audit trail et human validation gate;
- documenter erreurs standard.

### Phase 2 - Contrats techniques des 8 workflows

- ajouter `schemas/workflows/<workflow>`;
- definir outputs JSON et Markdown;
- connecter chaque command a son schema attendu;
- ajouter tests de validation schema.

### Phase 3 - Playbooks et skills metier

- enrichir les 8 playbooks;
- ajouter sources juridiques de base;
- separer standards cabinet et bases legales;
- ajouter red flags par workflow.

### Phase 4 - Evals metier

- creer fixtures synthetiques;
- ajouter expected outputs;
- ajouter rubrics;
- tester detection des faux negatifs critiques.

### Phase 5 - Runtime sources

- valider OpenLegi avec token;
- valider Exa MCP;
- documenter fallback si connecteur indisponible;
- ajouter rapport d'incertitude quand source externe echoue.

### Phase 6 - Packaging cabinet

- README par workflow;
- guide d'installation MCP;
- guide validation humaine;
- exemples de livrables;
- checklist de deploiement cabinet.

## Decision

La direction retenue est:

```text
Approche C etendue aux 8 workflows:
  construire tous les workflows en production-grade,
  mais uniquement via un noyau commun cabinet-grade obligatoire.
```

Cette approche maximise la coherence produit et evite de produire 8 workflows superficiels. Elle garde l'ambition de suite complete tout en imposant une discipline de qualite juridique, source checking, audit trail et validation humaine.
