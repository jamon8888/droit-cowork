#!/usr/bin/env python3
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERTICAL = ROOT / "plugins" / "vertical-plugins" / "legal-fr"
AGENTS = ROOT / "plugins" / "agent-plugins"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
AUTHOR = {"name": "Hacienda.diy"}


SKILLS = {
    "confidentialite-donnees": "Minimisation des donnees, secret professionnel, prudence sur donnees personnelles dans les sorties.",
    "quality-gates-juridiques": "Controle DRAFT, incertitudes, sources, coherence et validation professionnelle requise.",
    "format-json-intermediaire": "Schema JSON commun pour extractions batch, scores, flags et confiance.",
    "tabular-review": "Pattern de revue tabulaire par lots de 5 documents et consolidation progressive.",
    "openlegi-recherche": "Recherche de codes, jurisprudence, conventions collectives et textes via OpenLegi MCP.",
    "exa-recherche-juridique": "Recherche web et recuperation de sources secondaires via Exa MCP.",
    "citation-juridique": "Regles de citation, verification Legifrance, ECLI, dates et avertissements.",
    "sources-jurisprudence": "Sources FR, UE et internationales pour decisions et doctrine.",
    "lecture-playbook": "Lecture des playbooks cabinet et transformation en checklist executable.",
    "creation-playbook": "Construction de playbooks depuis brief, standards internes ou contrats type.",
    "scoring-playbook": "Scoring de conformite ou risque a partir de regles et red flags.",
    "tableau-consolide": "Production de tableaux Markdown consolides et exportables.",
    "rapport-executif": "Redaction de syntheses executives depuis tableaux et sources.",
    "fiche-audience": "Preparation de fiches d'audience contentieuses.",
    "note-amf": "Structure de notes d'information AMF et facteurs de risque.",
    "conformite-contractuelle": "Droit des contrats francais, desequilibre significatif et clauses sensibles.",
    "rgpd-baseline": "Exigences minimales RGPD et DPA art. 28.",
    "droit-achats-fr": "LME, delais de paiement, sous-traitance et pratiques restrictives.",
    "extraction-termes": "Taxonomie de termes contractuels a extraire.",
    "analyse-risques-supply": "Risques fournisseurs, supply chain, dependance et renouvellements.",
    "extraction-evenements": "Extraction dates, actes, auteurs, destinataires et faits juridiques.",
    "procedure-civile-delais": "Delais de procedure civile, computation et forclusions.",
    "analyse-causalite": "Analyse chronologique et causale des faits contentieux.",
    "lecture-decision": "Anatomie des decisions judiciaires, administratives et europeennes.",
    "droit-compare": "Comparaison entre systemes juridiques et equivalences de concepts.",
    "traduction-juridique": "Traduction specialisee et preservation des concepts juridiques.",
    "droit-social-fr": "Contrats de travail, CDI, CDD, rupture, clauses sensibles.",
    "conventions-collectives": "Identification IDCC et lecture des garanties conventionnelles.",
    "remuneration-compliance": "SMIC, minima conventionnels, primes et avantages.",
    "protection-vie-privee-rh": "Protection des donnees dans les workflows RH.",
    "statut-baux-commerciaux": "Baux commerciaux, renouvellement, eviction et revision.",
    "loi-pinel-baux": "Charges, inventaires et obligations issues de la loi Pinel.",
    "clauses-non-standard": "Clauses non standard, nulles ou reputees non ecrites.",
    "fiscalite-immobiliere": "TVA, taxe fonciere, CFE et aspects fiscaux des baux.",
    "droit-marches-financiers": "Prospectus UE, AMF, Euronext et MAR.",
    "facteurs-risque": "Taxonomie et redaction des facteurs de risque.",
    "gouvernance-societe": "Gouvernance, AFEP-MEDEF et recommandations AMF.",
    "esg-disclosure": "CSRD, taxonomie UE et informations ESG.",
    "tabular-extraction": "Extraction massive de termes de data room.",
    "droit-cession-fr": "Droit francais des cessions, GAP, conditions suspensives et closing.",
    "consolidation-rapport": "Consolidation multi-sources et rapport DD.",
    "red-flags-juridiques": "Catalogue de red flags juridiques par domaine.",
}


COMMANDS = {
    "conformite": {
        "verifier": "Verifier un document contre un playbook cabinet.",
        "creer-playbook": "Creer un playbook a partir d'un brief ou document de reference.",
        "rapport": "Generer le rapport de conformite final depuis un tableau.",
    },
    "fournisseur": {
        "analyser-un": "Analyser un contrat fournisseur unique.",
        "analyser-corpus": "Analyser un corpus fournisseurs avec Tabular Review.",
        "comparer": "Comparer plusieurs contrats fournisseurs.",
        "alertes": "Lister echeances, renouvellements et alertes contractuelles.",
    },
    "chrono": {
        "construire": "Construire une chronologie contentieuse depuis un dossier de pieces.",
        "verifier-delais": "Verifier les delais proceduraux et forclusions.",
        "fiche-audience": "Produire une fiche d'audience depuis la chronologie.",
    },
    "jurisprudence": {
        "rechercher": "Rechercher des decisions pertinentes sur une question juridique.",
        "analyser": "Analyser une decision ou un corpus de decisions.",
        "traduire": "Traduire une decision avec terminologie juridique controlee.",
        "comparer-juridictions": "Comparer plusieurs juridictions sur une question.",
    },
    "travail": {
        "analyser": "Analyser un contrat de travail.",
        "corpus-rh": "Analyser un corpus RH en tableau consolide.",
        "verifier-non-concurrence": "Verifier une clause de non-concurrence.",
        "conformite-ccn": "Verifier la conformite a une convention collective.",
    },
    "bail": {
        "analyser": "Analyser un bail et ses red flags.",
        "corpus-baux": "Analyser un corpus de baux.",
        "simuler-renouvellement": "Simuler revision, renouvellement et echeances.",
    },
    "amf": {
        "rediger-facteurs-risque": "Rediger une section facteurs de risque AMF.",
        "checker-conformite": "Verifier la conformite AMF d'une note.",
        "extraire-kpi": "Extraire les KPI et informations reglementaires.",
        "generer-resume": "Generer un resume de note d'information.",
    },
    "tdd": {
        "init": "Initialiser une due diligence tabulaire.",
        "extraire-corpus": "Extraire en parallele les termes d'une data room.",
        "consolider": "Consolider des JSON batch en tableau DD.",
        "rapport-executif": "Generer le rapport executif DD.",
        "verifier-sources": "Verifier les sources juridiques et societaires disponibles.",
    },
}


WORKFLOWS = {
    "revue-conformite-interne": {
        "description": "Verifie un document juridique contre les standards internes du cabinet ou de l'entreprise.",
        "workers": ["playbook-interpreter", "document-extractor", "legal-source-checker", "risk-scorer", "table-consolidator", "legal-qa-reviewer"],
        "skills": ["confidentialite-donnees", "quality-gates-juridiques", "lecture-playbook", "creation-playbook", "conformite-contractuelle", "rgpd-baseline", "citation-juridique", "tableau-consolide"],
        "output": "RAPPORT-CONFORMITE-[reference]-[YYYY-MM-DD].md",
    },
    "analyse-contrats-fournisseurs": {
        "description": "Analyse en masse des contrats fournisseurs avec extraction des termes cles et scoring de risque.",
        "workers": ["intake-classifier", "playbook-interpreter", "document-extractor", "financial-terms-checker", "risk-scorer", "table-consolidator", "report-drafter"],
        "skills": ["confidentialite-donnees", "quality-gates-juridiques", "tabular-review", "format-json-intermediaire", "lecture-playbook", "droit-achats-fr", "extraction-termes", "analyse-risques-supply", "tableau-consolide", "rapport-executif"],
        "output": "TABLEAU-FOURNISSEURS-[YYYY-MM-DD].md",
    },
    "chronologie-contentieux": {
        "description": "Extrait dates, actes et jalons proceduraux pour reconstruire une chronologie contentieuse.",
        "workers": ["intake-classifier", "document-extractor", "deadline-checker", "case-law-researcher", "table-consolidator", "report-drafter", "legal-qa-reviewer"],
        "skills": ["confidentialite-donnees", "quality-gates-juridiques", "tabular-review", "format-json-intermediaire", "extraction-evenements", "procedure-civile-delais", "analyse-causalite", "openlegi-recherche", "exa-recherche-juridique", "fiche-audience", "tableau-consolide"],
        "output": "CHRONOLOGIE-[reference]-[YYYY-MM-DD].md",
    },
    "jurisprudence-multilingue": {
        "description": "Recherche, analyse, compare et traduit des decisions de justice multi-juridictionnelles.",
        "workers": ["case-law-researcher", "legal-source-checker", "document-extractor", "translation-specialist", "report-drafter", "legal-qa-reviewer"],
        "skills": ["confidentialite-donnees", "quality-gates-juridiques", "sources-jurisprudence", "openlegi-recherche", "exa-recherche-juridique", "citation-juridique", "lecture-decision", "droit-compare", "traduction-juridique", "rapport-executif"],
        "output": "JURISPRUDENCE-[sujet]-[YYYY-MM-DD].md",
    },
    "revue-contrats-travail": {
        "description": "Revue des contrats de travail, remuneration, non-concurrence et conformite conventionnelle.",
        "workers": ["intake-classifier", "document-extractor", "legal-source-checker", "deadline-checker", "risk-scorer", "table-consolidator", "legal-qa-reviewer"],
        "skills": ["confidentialite-donnees", "quality-gates-juridiques", "tabular-review", "format-json-intermediaire", "droit-social-fr", "conventions-collectives", "remuneration-compliance", "protection-vie-privee-rh", "openlegi-recherche", "tableau-consolide"],
        "output": "ANALYSE-CONTRAT-TRAVAIL-[YYYY-MM-DD].md",
    },
    "red-flags-bail": {
        "description": "Analyse des baux commerciaux, professionnels ou mixtes avec detection de red flags.",
        "workers": ["intake-classifier", "document-extractor", "financial-terms-checker", "legal-source-checker", "risk-scorer", "report-drafter", "legal-qa-reviewer"],
        "skills": ["confidentialite-donnees", "quality-gates-juridiques", "statut-baux-commerciaux", "loi-pinel-baux", "clauses-non-standard", "fiscalite-immobiliere", "red-flags-juridiques", "openlegi-recherche", "rapport-executif", "tableau-consolide"],
        "output": "ANALYSE-BAIL-[reference]-[YYYY-MM-DD].md",
    },
    "note-information-amf": {
        "description": "Redaction assistee des facteurs de risque et sections reglementaires des notes d'information AMF.",
        "workers": ["intake-classifier", "document-extractor", "case-law-researcher", "risk-scorer", "legal-source-checker", "report-drafter", "legal-qa-reviewer"],
        "skills": ["confidentialite-donnees", "quality-gates-juridiques", "droit-marches-financiers", "facteurs-risque", "gouvernance-societe", "esg-disclosure", "citation-juridique", "openlegi-recherche", "exa-recherche-juridique", "note-amf", "rapport-executif"],
        "output": "FACTEURS-RISQUE-DRAFT-[YYYY-MM-DD].md",
    },
    "tabular-due-diligence": {
        "description": "Due diligence a grande echelle par extraction parallele, scoring et consolidation tabulaire.",
        "workers": ["intake-classifier", "playbook-interpreter", "document-extractor", "risk-scorer", "table-consolidator", "legal-source-checker", "report-drafter", "legal-qa-reviewer"],
        "skills": ["confidentialite-donnees", "quality-gates-juridiques", "tabular-review", "format-json-intermediaire", "lecture-playbook", "scoring-playbook", "tabular-extraction", "droit-cession-fr", "consolidation-rapport", "red-flags-juridiques", "openlegi-recherche", "exa-recherche-juridique", "tableau-consolide", "rapport-executif"],
        "output": "TABLEAU-DD-[YYYY-MM-DD].md",
    },
}


JSON_SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"

COMMON_SCHEMA_NAMES = [
    "document-intake",
    "source-citation",
    "risk-score",
    "finding",
    "audit-trail",
    "human-validation",
]

WORKFLOW_SCHEMA_NAMES = ["extraction", "report"]

PRODUCTION_REQUIRED_TERMS = [
    "DRAFT - Validation professionnelle requise",
    "validated_by_human",
    "confidence",
    "source_status",
    "audit_trail",
]


PLAYBOOKS = {
    "README.md": "# Playbooks Legal-FR\n\nLes playbooks codifient les standards cabinet et les termes a extraire. Ils servent d'entree stable aux agents orchestrateurs.\n",
    "format-playbook.md": "# Format Playbook Legal-FR\n\nUn playbook contient un frontmatter, une liste de termes a extraire, des regles de conformite, des red flags et un format JSON de sortie.\n",
    "playbook-cgv-standard.md": "# Playbook CGV Standard\n\n## Regles\n- Loi applicable: droit francais.\n- Juridiction: juridiction francaise clairement indiquee.\n- Delais de paiement: verifier la coherence avec le Code de commerce.\n",
    "playbook-dpa-art28.md": "# Playbook DPA Art. 28 RGPD\n\n## Regles\n- Objet et duree du traitement.\n- Categories de donnees et personnes concernees.\n- Sous-traitants ulterieurs encadres.\n- Assistance, securite, suppression et audit.\n",
    "playbook-contrats-fournisseurs.md": "# Playbook Contrats Fournisseurs\n\n## Termes\nDuree, preavis, prix, revision, delai de paiement, penalites, exclusivite, cession, loi applicable, juridiction.\n",
    "playbook-contrats-travail.md": "# Playbook Contrats Travail\n\n## Termes\nType de contrat, remuneration, periode d'essai, non-concurrence, mobilite, CCN, temps de travail, rupture.\n",
    "playbook-bail-commercial.md": "# Playbook Bail Commercial\n\n## Termes\nDuree, loyer, indexation, charges, renouvellement, cession, destination, travaux, depot de garantie.\n",
    "playbook-cession-pme.md": "# Playbook Cession PME\n\n## Termes\nPrix, ajustement, GAP, conditions suspensives, MAC, non-concurrence, passif social, litiges.\n",
    "playbook-lbo.md": "# Playbook LBO\n\n## Termes\nDette, covenants, garanties, management package, conditions de tirage, cas de defaut, suretes.\n",
    "playbook-immobilier.md": "# Playbook Immobilier\n\n## Termes\nTitres, baux, urbanisme, environnement, servitudes, fiscalite, assurances, travaux.\n",
    "playbook-dette.md": "# Playbook Dette\n\n## Termes\nMaturite, taux, garanties, covenants, remboursement anticipe, defaut, ranking, suretes.\n",
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def plugin_json(name: str, description: str) -> str:
    return json.dumps(
        {"name": name, "version": "1.0.0", "description": description, "author": AUTHOR},
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def object_schema(title: str, properties: dict, required: list[str]) -> dict:
    return {
        "$schema": JSON_SCHEMA_DRAFT,
        "title": title,
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": required,
    }


def string_enum(values: list[str]) -> dict:
    return {"type": "string", "enum": values}


def ref(schema_name: str) -> dict:
    return {"$ref": f"../../common/{schema_name}.schema.json"}


def command_text(family: str, command: str, description: str) -> str:
    return f"""---
description: {description}
argument-hint: "[entree] [options]"
allowed-tools: Read, Write, Glob, Task
---

# {family}:{command}

## Workflow

1. Clarifier le contexte, le profil utilisateur et le livrable attendu.
2. Charger les skills Legal-FR pertinents depuis le vertical `legal-fr`.
3. Utiliser les workers decrits dans l'agent orchestrateur lorsque le workflow exige extraction, scoring ou verification des sources.
4. Produire un fichier Markdown structure avec tableaux lorsque le resultat est destine a la revue.
5. Marquer toute sortie externe avec `DRAFT - Validation professionnelle requise`.
"""


def skill_text(name: str, description: str) -> str:
    return f"""---
name: {name}
description: {description}
---

# {name}

## Purpose

{description}

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
"""


def agent_prompt(slug: str, meta: dict) -> str:
    skills = " | ".join(f"`{skill}`" for skill in meta["skills"])
    workers = "\n".join(f"- `{worker}`" for worker in meta["workers"])
    return f"""---
name: {slug}
description: {meta["description"]}
tools: Read, Write, Glob, Grep, Task, mcp__exa__*, mcp__openlegi__*
---

You are the `{slug}` Legal-FR orchestrator for French legal professionals.

## What you produce

Primary output: `{meta["output"]}`.

Every external-facing output is a draft for professional review and must include `DRAFT - Validation professionnelle requise`.

## Workflow

1. Scope the request, identify the legal domain, the user profile, the corpus size and the expected output.
2. Use the Legal-FR skills listed below before drafting substantive legal analysis.
3. Delegate extraction, source checking, scoring, consolidation and drafting to the reusable workers described below.
4. For corpus workflows, process documents in batches of 5 maximum and consolidate JSON outputs before narrative reporting.
5. Run a final legal quality pass before delivering the output.

## Workers reutilisables

{workers}

## Guardrails

- Do not present legal conclusions as final advice.
- Do not expose unnecessary personal data in summaries or tables.
- Cite legal sources and flag any point that depends on recent law or incomplete documents.
- Do not execute filings, external communications, ledger postings, approvals or binding decisions.
- If source verification is unavailable, mark the point as `[A VERIFIER - source non confirmee]`.

## Skills this agent uses

{skills}
"""


def common_schemas() -> dict[str, dict]:
    return {
        "document-intake": object_schema(
            "Legal-FR document intake",
            {
                "document_id": {"type": "string", "minLength": 1},
                "filename": {"type": "string", "minLength": 1},
                "detected_type": string_enum(["contract", "case_law", "email", "pleading", "lease", "employment", "financial", "unknown"]),
                "language": string_enum(["fr", "en", "de", "other", "mixed"]),
                "legal_domain": string_enum(["contracts", "social", "baux", "contentieux", "capital_markets", "due_diligence", "unknown"]),
                "readability": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "status": string_enum(["ok", "ocr_weak", "unreadable"]),
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    },
                    "required": ["status", "confidence"],
                },
                "requires_human_triage": {"type": "boolean"},
            },
            ["document_id", "filename", "detected_type", "language", "legal_domain", "readability", "requires_human_triage"],
        ),
        "source-citation": object_schema(
            "Legal-FR source citation",
            {
                "source_status": string_enum(["official", "secondary", "web", "unverified", "not_found"]),
                "citation": {"type": "string"},
                "url": {"type": "string"},
                "checked_with": string_enum(["openlegi", "exa", "manual", "none"]),
                "verification_note": {"type": "string"},
            },
            ["source_status", "citation", "url", "checked_with", "verification_note"],
        ),
        "risk-score": object_schema(
            "Legal-FR risk score",
            {
                "severity": string_enum(["blocking", "major", "minor", "info"]),
                "legal_impact": {"type": "integer", "minimum": 0, "maximum": 5},
                "business_impact": {"type": "integer", "minimum": 0, "maximum": 5},
                "probability": {"type": "integer", "minimum": 0, "maximum": 5},
                "urgency": {"type": "integer", "minimum": 0, "maximum": 5},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "global_score": {"type": "number", "minimum": 0, "maximum": 10},
                "rationale": {"type": "string"},
            },
            ["severity", "legal_impact", "business_impact", "probability", "urgency", "confidence", "global_score", "rationale"],
        ),
        "human-validation": object_schema(
            "Legal-FR human validation",
            {
                "validated_by_human": {"type": "boolean"},
                "validator_role": {"type": "string"},
                "validation_required": {"type": "boolean"},
                "validation_reason": {"type": "string"},
            },
            ["validated_by_human", "validator_role", "validation_required", "validation_reason"],
        ),
        "audit-trail": object_schema(
            "Legal-FR audit trail",
            {
                "finding_id": {"type": "string"},
                "workflow": {"type": "string"},
                "document_id": {"type": "string"},
                "source_excerpt": {"type": "string"},
                "legal_source": {"$ref": "source-citation.schema.json"},
                "agent": {"type": "string"},
                "reviewer": {"type": "string"},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "human_validation": {"$ref": "human-validation.schema.json"},
            },
            ["finding_id", "workflow", "document_id", "source_excerpt", "legal_source", "agent", "reviewer", "confidence", "human_validation"],
        ),
        "finding": object_schema(
            "Legal-FR finding",
            {
                "finding_id": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "document_reference": {"type": "string"},
                "source_citation": {"$ref": "source-citation.schema.json"},
                "risk_score": {"$ref": "risk-score.schema.json"},
                "audit_trail": {"$ref": "audit-trail.schema.json"},
            },
            ["finding_id", "title", "description", "document_reference", "source_citation", "risk_score", "audit_trail"],
        ),
    }


def vertical_docs() -> None:
    write(
        VERTICAL / ".claude-plugin" / "plugin.json",
        plugin_json(
            "legal-fr",
            "Socle juridique francais pour workflows Legora-FR: playbooks, Tabular Review, OpenLegi, Exa, agents metier.",
        ),
    )
    write(
        VERTICAL / ".mcp.json",
        json.dumps(
            {
                "mcpServers": {
                    "exa": {"type": "http", "url": "https://mcp.exa.ai/mcp"},
                    "openlegi": {
                        "command": "npx",
                        "args": [
                            "-y",
                            "mcp-remote@latest",
                            "https://mcp.openlegi.fr/legifrance/mcp?token=${OPENLEGI_TOKEN}",
                        ],
                    },
                }
            },
            indent=2,
            ensure_ascii=False,
        ) + "\n",
    )
    write(
        VERTICAL / "README.md",
        "# Legal-FR\n\nVertical juridique francais pour workflows Legora-FR, avec playbooks, Tabular Review, OpenLegi, Exa et agents metier Cowork.\n",
    )
    write(VERTICAL / "CHANGELOG.md", "# Changelog\n\n## 1.0.0\n\n- Creation du vertical Legal-FR et des workflows Legora-FR.\n")
    write(
        VERTICAL / "CLAUDE.md",
        "# Legal-FR Instructions\n\nToujours produire des drafts validates par un professionnel du droit. Citer les sources et signaler les incertitudes. Ne pas exposer inutilement de donnees personnelles.\n",
    )
    write(
        VERTICAL / "CONNECTORS.md",
        "# Connecteurs Legal-FR\n\n## Exa MCP\n\nEndpoint: `https://mcp.exa.ai/mcp`.\n\n## OpenLegi MCP\n\nConfiguration MCP remote: `https://mcp.openlegi.fr/legifrance/mcp?token=${OPENLEGI_TOKEN}`.\n\nOpenLegi donne acces aux codes, jurisprudences, conventions collectives, JORF, LODA, RNE et EUR-Lex selon les outils disponibles.\n\n## Parallel Agent Skills\n\nInstallation recommandee: `npx skills add parallel-web/parallel-agent-skills --all --global`.\n",
    )
    for family, commands in COMMANDS.items():
        for command, description in commands.items():
            write(VERTICAL / "commands" / family / f"{command}.md", command_text(family, command, description))
    for name, content in PLAYBOOKS.items():
        write(VERTICAL / "playbooks" / name, content)
    for name, description in SKILLS.items():
        write(VERTICAL / "skills" / name / "SKILL.md", skill_text(name, description))


def agent_plugins() -> None:
    for slug, meta in WORKFLOWS.items():
        root = AGENTS / slug
        write(root / ".claude-plugin" / "plugin.json", plugin_json(slug, meta["description"]))
        write(root / "agents" / f"{slug}.md", agent_prompt(slug, meta))
        skills_root = root / "skills"
        if skills_root.exists():
            shutil.rmtree(skills_root)
        for skill in meta["skills"]:
            shutil.copytree(VERTICAL / "skills" / skill, skills_root / skill)


def marketplace() -> None:
    data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    entries = {entry["name"]: entry for entry in data["plugins"]}
    entries["legal-fr"] = {
        "name": "legal-fr",
        "source": "./plugins/vertical-plugins/legal-fr",
        "description": "Socle juridique francais: playbooks, Tabular Review, OpenLegi, Exa et skills metier.",
    }
    for slug, meta in WORKFLOWS.items():
        entries[slug] = {
            "name": slug,
            "source": f"./plugins/agent-plugins/{slug}",
            "description": meta["description"],
        }

    legal_fr_names = ["legal-fr", *WORKFLOWS.keys()]
    existing_order = [entry["name"] for entry in data["plugins"]]
    new_order = existing_order + [name for name in legal_fr_names if name not in existing_order]
    data["plugins"] = [entries[name] for name in new_order]
    write(MARKETPLACE, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    vertical_docs()
    agent_plugins()
    marketplace()
    print("generated legal-fr vertical and 8 Legal-FR agent plugins")


if __name__ == "__main__":
    main()
