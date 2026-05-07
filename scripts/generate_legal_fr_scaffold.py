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


SKILL_RED_FLAGS = {
    "conformite-contractuelle": [
        "clause non sourcee",
        "desequilibre significatif",
        "juridiction incoherente",
    ],
    "droit-achats-fr": [
        "delai de paiement excessif",
        "penalites absentes",
        "dependance fournisseur",
    ],
    "procedure-civile-delais": [
        "forclusion potentielle",
        "date procedurale incertaine",
        "piece manquante",
    ],
    "droit-social-fr": [
        "non-concurrence sans contrepartie",
        "periode essai non sourcee",
        "CCN absente",
    ],
    "statut-baux-commerciaux": [
        "renonciation droit imperatif",
        "charges Pinel non detaillees",
        "indexation incoherente",
    ],
    "droit-marches-financiers": [
        "facteur de risque generique",
        "materialite absente",
        "source AMF manquante",
    ],
    "tabular-extraction": [
        "coverage incomplete",
        "JSON batch invalide",
        "score sans audit trail",
    ],
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

WORKFLOW_INTAKE_METADATA = {
    "revue-conformite-interne": {
        "detected_type": "policy_or_contract",
        "legal_domain": "compliance",
    },
    "analyse-contrats-fournisseurs": {
        "detected_type": "supplier_agreement",
        "legal_domain": "contracts_supply",
    },
    "chronologie-contentieux": {
        "detected_type": "litigation_file",
        "legal_domain": "litigation",
    },
    "jurisprudence-multilingue": {
        "detected_type": "court_decision",
        "legal_domain": "case_law",
    },
    "revue-contrats-travail": {
        "detected_type": "employment_agreement",
        "legal_domain": "employment",
    },
    "red-flags-bail": {
        "detected_type": "lease_agreement",
        "legal_domain": "real_estate",
    },
    "note-information-amf": {
        "detected_type": "amf_disclosure_file",
        "legal_domain": "capital_markets",
    },
    "tabular-due-diligence": {
        "detected_type": "data_room_document",
        "legal_domain": "due_diligence",
    },
}

PRODUCTION_REQUIRED_TERMS = [
    "DRAFT - Validation professionnelle requise",
    "validated_by_human",
    "confidence",
    "source_status",
    "audit_trail",
]

EVAL_CASES = [
    ("case-001", "compliant", "low"),
    ("case-002", "blocking_red_flag", "high"),
    ("case-003", "legal_uncertainty", "medium"),
    ("case-004", "unreadable_or_incomplete", "unknown"),
    ("case-005", "source_not_found", "medium"),
]

EVAL_CASE_DETAILS = {
    "compliant": {
        "source_status": "official",
        "checked_with": "openlegi",
        "confidence": 0.9,
        "severity": "minor",
        "confidence_band": "high",
        "input_note": "Document lisible, source officielle disponible, aucun red flag bloquant apparent.",
        "expected_behavior": "Confirmer la conformite apparente tout en maintenant le statut draft.",
    },
    "blocking_red_flag": {
        "source_status": "official",
        "checked_with": "openlegi",
        "confidence": 0.86,
        "severity": "blocking",
        "confidence_band": "high",
        "input_note": "Clause manifestement sensible et source officielle disponible pour qualifier le risque.",
        "expected_behavior": "Identifier un red flag bloquant et exiger revue avocat avant usage externe.",
    },
    "legal_uncertainty": {
        "source_status": "unverified",
        "checked_with": "manual",
        "confidence": 0.48,
        "severity": "major",
        "confidence_band": "medium",
        "input_note": "Point juridique dependant d'informations recentes ou d'un contexte absent.",
        "expected_behavior": "Signaler l'incertitude juridique et demander validation humaine ciblee.",
    },
    "unreadable_or_incomplete": {
        "source_status": "unverified",
        "checked_with": "none",
        "confidence": 0.0,
        "severity": "info",
        "confidence_band": "unknown",
        "input_note": "Pieces OCR partielles ou pages manquantes empechant une analyse fiable.",
        "expected_behavior": "Bloquer la conclusion substantielle et demander une piece lisible complete.",
    },
    "source_not_found": {
        "source_status": "not_found",
        "checked_with": "openlegi",
        "confidence": 0.34,
        "severity": "major",
        "confidence_band": "low",
        "input_note": "Affirmation juridique plausible mais source officielle introuvable dans le dossier.",
        "expected_behavior": "Marquer la source comme introuvable et interdire toute conclusion finale.",
    },
}


CORE_PLAYBOOK_RULES = [
    ("R-001", "Toute conclusion critique cite une source ou reste A VERIFIER", "blocking", "audit trail", "Bloquer le livrable"),
    ("R-002", "Toute sortie externe porte la mention DRAFT", "blocking", "quality gate", "Ajouter la mention"),
    ("R-003", "Toute observation a un score de confiance", "major", "risk score", "Ajouter confidence"),
]

CORE_PLAYBOOK_RED_FLAGS = [
    ("RF-001", "Source absente sur conclusion majeure", "blocking", "Marquer A VERIFIER"),
    ("RF-002", "Document illisible ignore", "blocking", "Ajouter a coverage"),
    ("RF-003", "validated_by_human absent", "major", "Ajouter human validation"),
]

COMMON_EXTRACTION_TERMS = [
    ("document_id", "Identifiant stable du document", "string", "nom fichier"),
    ("source_excerpt", "Extrait qui justifie l'observation", "string", "A VERIFIER"),
    ("source_status", "official, secondary, web, unverified, not_found", "enum", "unverified"),
    ("confidence", "Confiance 0-1", "number", "0.5"),
]

PLAYBOOK_DEFINITIONS = {
    "playbook-cgv-standard.md": {
        "title": "Playbook CGV Standard",
        "domain": "conditions generales de vente B2B/B2C",
        "terms": ["delai paiement", "penalites", "juridiction", "limitation responsabilite"],
        "rules": [
            ("R-CGV-001", "Verifier que les delais de paiement sont identifies et compatibles avec le cadre applicable."),
            ("R-CGV-002", "Qualifier les penalites, indemnites et interets applicables en cas de retard."),
            ("R-CGV-003", "Controler la coherence entre loi applicable, juridiction et limitation de responsabilite."),
        ],
        "red_flags": [
            ("RF-CGV-001", "Delai paiement absent, excessif ou contradictoire entre plusieurs clauses."),
            ("RF-CGV-002", "Penalites absentes ou incompatibles avec le regime commercial vise."),
            ("RF-CGV-003", "Limitation responsabilite illisible, illimitee sans justification ou potentiellement desequilibree."),
        ],
    },
    "playbook-dpa-art28.md": {
        "title": "Playbook DPA Art. 28 RGPD",
        "domain": "accord de sous-traitance RGPD article 28",
        "terms": ["sous-traitant", "finalites", "duree", "mesures securite", "sort donnees"],
        "rules": [
            ("R-DPA-001", "Identifier le sous-traitant, le responsable de traitement et les categories de donnees traitees."),
            ("R-DPA-002", "Verifier que les finalites, la duree et les instructions documentees sont explicites."),
            ("R-DPA-003", "Controler les mesures securite, l'assistance, l'audit et le sort donnees en fin de prestation."),
        ],
        "red_flags": [
            ("RF-DPA-001", "Sous-traitant ulterieur autorise sans encadrement ou information prealable."),
            ("RF-DPA-002", "Finalites ou duree absentes, ouvertes ou incompatibles avec le contrat principal."),
            ("RF-DPA-003", "Sort donnees non precise: restitution, suppression, conservation ou preuve d'effacement."),
        ],
    },
    "playbook-contrats-fournisseurs.md": {
        "title": "Playbook Contrats Fournisseurs",
        "domain": "contrats fournisseurs et achats",
        "terms": ["duree", "preavis", "prix", "revision", "penalites", "exclusivite"],
        "rules": [
            ("R-FOU-001", "Extraire duree, renouvellement, preavis et conditions de sortie."),
            ("R-FOU-002", "Verifier prix, revision, indexation et penalites operationnelles ou financieres."),
            ("R-FOU-003", "Qualifier les clauses d'exclusivite, dependance, cession et changement de controle."),
        ],
        "red_flags": [
            ("RF-FOU-001", "Renouvellement automatique sans preavis exploitable ou calendrier d'alerte."),
            ("RF-FOU-002", "Revision de prix unilaterale ou penalites disproportionnees."),
            ("RF-FOU-003", "Exclusivite ou dependance fournisseur sans mecanisme de sortie."),
        ],
    },
    "playbook-contrats-travail.md": {
        "title": "Playbook Contrats Travail",
        "domain": "contrats de travail francais",
        "terms": ["non-concurrence", "remuneration", "periode essai", "CCN"],
        "rules": [
            ("R-TRA-001", "Identifier type de contrat, poste, classification, CCN et lieu d'execution."),
            ("R-TRA-002", "Verifier remuneration, avantages, temps de travail et minima applicables."),
            ("R-TRA-003", "Controler periode essai, non-concurrence, mobilite et clauses sensibles."),
        ],
        "red_flags": [
            ("RF-TRA-001", "Non-concurrence sans contrepartie, limitation temporelle ou zone definie."),
            ("RF-TRA-002", "CCN absente ou incoherente avec l'activite et la classification."),
            ("RF-TRA-003", "Periode essai ou renouvellement non source par le contrat ou la CCN."),
        ],
    },
    "playbook-bail-commercial.md": {
        "title": "Playbook Bail Commercial",
        "domain": "baux commerciaux",
        "terms": ["duree", "charges", "indexation", "renouvellement", "eviction"],
        "rules": [
            ("R-BAI-001", "Extraire duree, prise d'effet, destination, renouvellement et conge."),
            ("R-BAI-002", "Verifier charges, travaux, taxes, depot de garantie et repartition Pinel."),
            ("R-BAI-003", "Controler indexation, revision, eviction et indemnite eventuelle."),
        ],
        "red_flags": [
            ("RF-BAI-001", "Charges non detaillees ou transfert au preneur potentiellement non conforme."),
            ("RF-BAI-002", "Indexation incoherente, indice absent ou clause d'echelle mobile asymetrique."),
            ("RF-BAI-003", "Renonciation ou restriction au renouvellement ou a l'eviction sans analyse."),
        ],
    },
    "playbook-cession-pme.md": {
        "title": "Playbook Cession PME",
        "domain": "cession de PME",
        "terms": ["GAP", "conditions suspensives", "cession", "changement controle"],
        "rules": [
            ("R-CES-001", "Identifier perimetre de cession, prix, ajustement et calendrier closing."),
            ("R-CES-002", "Verifier GAP, plafonds, franchises, durees et procedures de reclamation."),
            ("R-CES-003", "Controler conditions suspensives, cession des contrats et changement controle."),
        ],
        "red_flags": [
            ("RF-CES-001", "Condition suspensive non purgee ou preuve de levee absente."),
            ("RF-CES-002", "GAP sans plafond, duree ou procedure de notification claire."),
            ("RF-CES-003", "Changement controle declenchant consentement tiers non obtenu."),
        ],
    },
    "playbook-lbo.md": {
        "title": "Playbook LBO",
        "domain": "financement LBO",
        "terms": ["dette", "covenants", "suretes", "restrictions"],
        "rules": [
            ("R-LBO-001", "Identifier dette senior, dette mezzanine, maturite, tirages et remboursement."),
            ("R-LBO-002", "Verifier covenants financiers, testing dates, equity cure et reporting."),
            ("R-LBO-003", "Controler suretes, garanties, restrictions de distribution et dette additionnelle."),
        ],
        "red_flags": [
            ("RF-LBO-001", "Covenants absents, non chiffres ou sans methode de calcul."),
            ("RF-LBO-002", "Suretes ou rangs incompatibles avec la structure de dette."),
            ("RF-LBO-003", "Restrictions bloquant operations courantes ou distributions sans carve-out."),
        ],
    },
    "playbook-immobilier.md": {
        "title": "Playbook Immobilier",
        "domain": "due diligence immobiliere",
        "terms": ["titres", "baux", "charges", "urbanisme"],
        "rules": [
            ("R-IMM-001", "Verifier titres, origine de propriete, servitudes et droits de tiers."),
            ("R-IMM-002", "Extraire baux, charges, travaux, assurances et fiscalite recurrente."),
            ("R-IMM-003", "Controler urbanisme, autorisations, conformite, environnement et contentieux."),
        ],
        "red_flags": [
            ("RF-IMM-001", "Titre ou servitude determinant absent de la data room."),
            ("RF-IMM-002", "Charges ou travaux significatifs non attribues a une partie."),
            ("RF-IMM-003", "Urbanisme non verifie ou autorisation essentielle manquante."),
        ],
    },
    "playbook-dette.md": {
        "title": "Playbook Dette",
        "domain": "contrats de dette",
        "terms": ["maturite", "taux", "covenants", "defaut"],
        "rules": [
            ("R-DET-001", "Identifier maturite, amortissement, taux, marges, commissions et prepayment."),
            ("R-DET-002", "Verifier covenants, representations, undertakings et obligations de reporting."),
            ("R-DET-003", "Controler cas de defaut, cross-default, grace periods, suretes et acceleration."),
        ],
        "red_flags": [
            ("RF-DET-001", "Maturite ou taux absent, variable non indexe ou formule incomplete."),
            ("RF-DET-002", "Covenants sans seuil, periodicite ou consequence de breach."),
            ("RF-DET-003", "Defaut automatique ou acceleration sans cure period identifiable."),
        ],
    },
}


def term_table(domain_terms: list[str]) -> str:
    rows = [
        "| Terme | Description | Type | Valeur par defaut |",
        "| --- | --- | --- | --- |",
    ]
    rows.extend(f"| {term} | {description} | {kind} | {default} |" for term, description, kind, default in COMMON_EXTRACTION_TERMS)
    rows.extend(f"| {term} | Terme specifique domaine | string | A EXTRAIRE |" for term in domain_terms)
    return "\n".join(rows)


def coded_bullets(items: list[tuple[str, str]]) -> str:
    return "\n".join(f"- `{code}`: {description}" for code, description in items)


def rule_table(core_rules: list[tuple[str, str, str, str, str]], domain_rules: list[tuple[str, str]]) -> str:
    rows = [
        "| ID | Regle | Severite | Controle | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    rows.extend(f"| {code} | {rule} | {severity} | {control} | {action} |" for code, rule, severity, control, action in core_rules)
    rows.extend(f"| {code} | {rule} | major | playbook domaine | Revoir avec juriste |" for code, rule in domain_rules)
    return "\n".join(rows)


def red_flag_table(core_red_flags: list[tuple[str, str, str, str]], domain_red_flags: list[tuple[str, str]]) -> str:
    rows = [
        "| ID | Red flag | Severite | Action |",
        "| --- | --- | --- | --- |",
    ]
    rows.extend(f"| {code} | {red_flag} | {severity} | {action} |" for code, red_flag, severity, action in core_red_flags)
    rows.extend(f"| {code} | {red_flag} | major | Revue juridique ciblee |" for code, red_flag in domain_red_flags)
    return "\n".join(rows)


def playbook_text(filename: str, definition: dict) -> str:
    title = definition["title"]
    terms = definition["terms"]
    return f"""# {title}

## Metadata

- playbook_id: `{filename.removesuffix(".md")}`
- domain: {definition["domain"]}
- source_status: `unverified`
- validated_by_human: `false`
- confidence: `0.0`
- draft_notice: `DRAFT - Validation professionnelle requise`
- validation_required: `true`

## Termes a extraire

{term_table(terms)}

## Regles de conformite

{rule_table(CORE_PLAYBOOK_RULES, definition["rules"])}

## Red flags automatiques

{red_flag_table(CORE_PLAYBOOK_RED_FLAGS, definition["red_flags"])}
"""


PLAYBOOKS = {
    "README.md": """# Playbooks Legal-FR

Les playbooks codifient les standards cabinet et les termes a extraire. Ils servent d'entree stable aux agents orchestrateurs.

Signaux obligatoires dans les playbooks operationnels:
- `source_status`
- `validated_by_human`
- `confidence`
- `DRAFT - Validation professionnelle requise`
""",
    "format-playbook.md": """# Format Playbook Legal-FR

Un playbook operationnel contient les sections `## Metadata`, `## Termes a extraire`, `## Regles de conformite` et `## Red flags automatiques`.

Les champs obligatoires sont `source_status`, `validated_by_human`, `confidence` et `DRAFT - Validation professionnelle requise`.
""",
    **{filename: playbook_text(filename, definition) for filename, definition in PLAYBOOK_DEFINITIONS.items()},
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


COMMAND_FAMILY_TO_WORKFLOW = {
    "conformite": "revue-conformite-interne",
    "fournisseur": "analyse-contrats-fournisseurs",
    "chrono": "chronologie-contentieux",
    "jurisprudence": "jurisprudence-multilingue",
    "travail": "revue-contrats-travail",
    "bail": "red-flags-bail",
    "amf": "note-information-amf",
    "tdd": "tabular-due-diligence",
}


def workflow_for_family(family: str) -> str:
    return COMMAND_FAMILY_TO_WORKFLOW[family]


def command_text(family: str, command: str, description: str) -> str:
    workflow = workflow_for_family(family)
    return f"""---
description: {description}
argument-hint: "[entree] [options]"
allowed-tools: Read, Write, Glob, Task
---

# {family}:{command}

## Cabinet-grade workflow

Workflow cible: `{workflow}`.

Schemas requis:
- `plugins/vertical-plugins/legal-fr/schemas/common/document-intake.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/source-citation.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/risk-score.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/finding.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/audit-trail.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/human-validation.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/workflows/{workflow}/extraction.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/workflows/{workflow}/report.schema.json`

1. Classer l'entree, le domaine juridique, le profil utilisateur et le livrable attendu avant toute analyse.
2. Extraire les faits et termes dans le schema JSON du workflow, avec `confidence`, `source_status` et champs non trouves.
3. Construire un audit trail reliant chaque finding au document, a l'extrait source, a la verification juridique et au reviewer.
4. Appliquer un quality gate: sources citees, scores de risque, coherence du schema, incertitudes visibles et validation humaine requise.
5. Produire uniquement un livrable marque `DRAFT - Validation professionnelle requise` tant que `validated_by_human` n'est pas vrai.
"""


def skill_text(name: str, description: str) -> str:
    red_flags = SKILL_RED_FLAGS.get(name, [])
    red_flags_section = ""
    if red_flags:
        red_flags_section = "\n## Red flags a surveiller\n\n" + "\n".join(f"- {flag}." for flag in red_flags) + "\n"

    content = f"""---
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
{red_flags_section}
"""
    return content.rstrip() + "\n"


def agent_prompt(slug: str, meta: dict) -> str:
    skills = " | ".join(f"`{skill}`" for skill in meta["skills"])
    core_workers = [
        "intake-classifier",
        "source-verifier",
        "schema-extractor",
        "risk-scorer",
        "legal-qa-reviewer",
        "human-validation-gate",
        "audit-trail",
    ]
    all_workers = list(dict.fromkeys([*core_workers, *meta["workers"]]))
    workers = "\n".join(f"- `{worker}`" for worker in all_workers)
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


def workflow_schema(workflow: str, schema_kind: str) -> dict:
    return object_schema(
        f"Legal-FR {workflow} {schema_kind}",
        {
            "workflow": {"const": workflow},
            "document_intake": ref("document-intake"),
            "findings": {
                "type": "array",
                "items": ref("finding"),
            },
            "audit_trail": {
                "type": "array",
                "items": ref("audit-trail"),
            },
            "human_validation": ref("human-validation"),
            "draft_notice": {"const": "DRAFT - Validation professionnelle requise"},
            "coverage": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "documents_seen": {"type": "integer", "minimum": 0},
                    "documents_processed": {"type": "integer", "minimum": 0},
                    "documents_unreadable": {"type": "integer", "minimum": 0},
                },
                "required": ["documents_seen", "documents_processed", "documents_unreadable"],
            },
        },
        ["workflow", "document_intake", "findings", "audit_trail", "human_validation", "draft_notice", "coverage"],
    )


def audit_readme() -> str:
    return """# Audit Legal-FR

Every production-grade Legal-FR workflow emits an `audit_trail` record for each material finding.

Required audit fields:
- `DRAFT - Validation professionnelle requise`
- `validated_by_human`
- `confidence`
- `source_status`
- `audit_trail`

The audit trail links extracted text, legal sources, reviewer identity, confidence scoring and human validation status. Outputs remain drafts until `validated_by_human` is true.
"""


def quality_gates_readme() -> str:
    return """# Quality Gates Legal-FR

Legal-FR quality gates are cabinet policy checks applied manually by the `legal-qa-reviewer` and workflow instructions until automated enforcement is added through tests, eval scripts or prompt-level gates.

Required quality signals:
- `DRAFT - Validation professionnelle requise`
- `validated_by_human`
- `confidence`
- `source_status`
- `audit_trail`

The manual gate requires reviewers to preserve the draft notice, review `source_status`, inspect every `confidence` value and require human validation before any external reliance.
"""


def eval_input(workflow: str, case_id: str, case_type: str, risk_level: str) -> str:
    details = EVAL_CASE_DETAILS[case_type]
    return f"""# Eval fixture {case_id}: {workflow}

DRAFT - Validation professionnelle requise

## Workflow

`{workflow}`

## Case type

`{case_type}`

## Risk level

`{risk_level}`

## Cabinet scenario

{details["input_note"]}

## Expected handling

{details["expected_behavior"]}

## Source package

- Document reference: `{workflow}-{case_id}-document`
- Source status to test: `{details["source_status"]}`
- Human validation remains mandatory before reliance.
"""


def eval_metadata(workflow: str, case_id: str, case_type: str, risk_level: str) -> dict:
    details = EVAL_CASE_DETAILS[case_type]
    return {
        "workflow": workflow,
        "case_id": case_id,
        "case_type": case_type,
        "expected_risk": risk_level,
        "expected_source_status": details["source_status"],
        "expected_confidence_band": details["confidence_band"],
        "requires_human_validation": True,
        "expected_behavior": details["expected_behavior"],
    }


def expected_eval_output(workflow: str, case_id: str, case_type: str, risk_level: str) -> dict:
    details = EVAL_CASE_DETAILS[case_type]
    intake_metadata = WORKFLOW_INTAKE_METADATA[workflow]
    finding_id = f"{workflow}-{case_id}-finding-001"
    document_id = f"{workflow}-{case_id}-document"
    unreadable = case_type == "unreadable_or_incomplete"
    document_intake = {
        "document_id": document_id,
        "filename": f"{workflow}-{case_id}.md",
        "detected_type": intake_metadata["detected_type"],
        "language": "fr",
        "legal_domain": intake_metadata["legal_domain"],
        "readability": {
            "status": "unreadable" if unreadable else "ok",
            "confidence": 0.0 if unreadable else details["confidence"],
        },
        "requires_human_triage": True,
    }
    coverage = {
        "documents_seen": 1,
        "documents_processed": 0 if unreadable else 1,
        "documents_unreadable": 1 if unreadable else 0,
    }
    human_validation = {
        "validated_by_human": False,
        "validator_role": "avocat ou juriste senior",
        "validation_required": True,
        "validation_reason": "Eval fixture only; external reliance requires professional validation.",
    }
    source_citation = {
        "source_status": details["source_status"],
        "citation": f"Fixture source for {workflow} {case_id}",
        "url": "",
        "checked_with": details["checked_with"],
        "verification_note": details["expected_behavior"],
    }
    audit_trail = {
        "finding_id": finding_id,
        "workflow": workflow,
        "document_id": document_id,
        "source_excerpt": details["input_note"],
        "legal_source": source_citation,
        "agent": workflow,
        "reviewer": "legal-qa-reviewer",
        "confidence": details["confidence"],
        "human_validation": human_validation,
    }
    finding = {
        "finding_id": finding_id,
        "title": f"{case_type} eval finding",
        "description": details["expected_behavior"],
        "document_reference": document_id,
        "source_citation": source_citation,
        "risk_score": {
            "severity": details["severity"],
            "legal_impact": 5 if risk_level == "high" else 3 if risk_level == "medium" else 1,
            "business_impact": 4 if risk_level == "high" else 2 if risk_level == "medium" else 1,
            "probability": 4 if risk_level == "high" else 2 if risk_level == "medium" else 0,
            "urgency": 5 if risk_level == "high" else 3 if risk_level == "medium" else 0,
            "confidence": details["confidence"],
            "global_score": 8.5 if risk_level == "high" else 5.0 if risk_level == "medium" else 1.5,
            "rationale": f"Fixture case {case_type} with {details['source_status']} source status.",
        },
        "audit_trail": audit_trail,
    }
    return {
        "workflow": workflow,
        "document_intake": document_intake,
        "draft_notice": "DRAFT - Validation professionnelle requise",
        "findings": [finding],
        "audit_trail": [audit_trail],
        "human_validation": human_validation,
        "coverage": coverage,
    }


def rubric_text(workflow: str) -> str:
    cases = "\n".join(f"- `{case_id}`: `{case_type}` risk `{risk_level}`" for case_id, case_type, risk_level in EVAL_CASES)
    return f"""# Legal-FR eval rubric: {workflow}

## Required sections

The schema JSON section must include workflow, document_intake, draft_notice, findings, audit_trail, human_validation and coverage.

## Case coverage

{cases}

## Source and confidence checks

Each finding must include source_citation.source_status and risk_score.confidence. The source status must distinguish official, unverified and not_found cases.

## Human validation gate

Every case remains `DRAFT - Validation professionnelle requise`, with validated_by_human false and validation_required true.

## Audit trail requirements

Each top-level audit_trail item and each finding.audit_trail must link finding_id, workflow, document_id, legal_source, reviewer, confidence and human_validation.
"""


def production_grade_files() -> None:
    for name, schema in common_schemas().items():
        write(
            VERTICAL / "schemas" / "common" / f"{name}.schema.json",
            json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
        )

    for workflow in WORKFLOWS:
        for schema_kind in WORKFLOW_SCHEMA_NAMES:
            write(
                VERTICAL / "schemas" / "workflows" / workflow / f"{schema_kind}.schema.json",
                json.dumps(workflow_schema(workflow, schema_kind), indent=2, ensure_ascii=False) + "\n",
            )

    write(VERTICAL / "audit" / "README.md", audit_readme())
    write(VERTICAL / "quality-gates" / "README.md", quality_gates_readme())

    for workflow in WORKFLOWS:
        write(VERTICAL / "evals" / "rubrics" / f"{workflow}.rubric.md", rubric_text(workflow))
        for case_id, case_type, risk_level in EVAL_CASES:
            write(
                VERTICAL / "evals" / "fixtures" / workflow / case_id / "input.md",
                eval_input(workflow, case_id, case_type, risk_level),
            )
            write(
                VERTICAL / "evals" / "fixtures" / workflow / case_id / "metadata.json",
                json.dumps(eval_metadata(workflow, case_id, case_type, risk_level), indent=2, ensure_ascii=False) + "\n",
            )
            write(
                VERTICAL / "evals" / "expected" / workflow / f"{case_id}.expected.json",
                json.dumps(expected_eval_output(workflow, case_id, case_type, risk_level), indent=2, ensure_ascii=False) + "\n",
            )


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
    production_grade_files()
    agent_plugins()
    marketplace()
    print("generated legal-fr vertical, production-grade layer and 8 Legal-FR agent plugins")


if __name__ == "__main__":
    main()
