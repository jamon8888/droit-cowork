import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERTICAL = ROOT / "plugins" / "vertical-plugins" / "legal-fr"
AGENTS = ROOT / "plugins" / "agent-plugins"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CLAUDE_SETTINGS = ROOT / ".claude" / "settings.json"
CLAUDE_README = ROOT / ".claude" / "README.md"

EXPECTED_COMMANDS = {
    "conformite": ["verifier", "creer-playbook", "rapport"],
    "fournisseur": ["analyser-un", "analyser-corpus", "comparer", "alertes"],
    "chrono": ["construire", "verifier-delais", "fiche-audience"],
    "jurisprudence": ["rechercher", "analyser", "traduire", "comparer-juridictions"],
    "travail": ["analyser", "corpus-rh", "verifier-non-concurrence", "conformite-ccn"],
    "bail": ["analyser", "corpus-baux", "simuler-renouvellement"],
    "amf": ["rediger-facteurs-risque", "checker-conformite", "extraire-kpi", "generer-resume"],
    "tdd": ["init", "extraire-corpus", "consolider", "rapport-executif", "verifier-sources"],
    "recherche": [
        "chercher",
        "extraire-source",
        "deep-research",
        "verifier-sources",
        "enrichir-dossier",
        "veille",
        "task-run",
        "task-status",
        "task-poll",
    ],
    "workflow": ["init", "run", "review", "export", "eval"],
}

EXPECTED_PLAYBOOKS = [
    "README.md",
    "format-playbook.md",
    "playbook-cgv-standard.md",
    "playbook-dpa-art28.md",
    "playbook-contrats-fournisseurs.md",
    "playbook-contrats-travail.md",
    "playbook-bail-commercial.md",
    "playbook-cession-pme.md",
    "playbook-lbo.md",
    "playbook-immobilier.md",
    "playbook-dette.md",
    "workflows/workflow-dd-ma.md",
    "workflows/workflow-audit-rh.md",
    "workflows/workflow-preparation-audience.md",
    "workflows/workflow-audit-baux.md",
    "workflows/workflow-conformite-fournisseurs.md",
    "workflows/workflow-recherche-source-first.md",
]

EXPECTED_SKILLS = [
    "legal-fr-runtime",
    "workflow-playbooks",
    "source-ledger",
    "review-queue",
    "confidentialite-donnees",
    "quality-gates-juridiques",
    "format-json-intermediaire",
    "tabular-review",
    "openlegi-recherche",
    "exa-recherche-juridique",
    "citation-juridique",
    "sources-jurisprudence",
    "lecture-playbook",
    "creation-playbook",
    "scoring-playbook",
    "tableau-consolide",
    "rapport-executif",
    "fiche-audience",
    "note-amf",
    "conformite-contractuelle",
    "rgpd-baseline",
    "droit-achats-fr",
    "extraction-termes",
    "analyse-risques-supply",
    "extraction-evenements",
    "procedure-civile-delais",
    "analyse-causalite",
    "lecture-decision",
    "droit-compare",
    "traduction-juridique",
    "droit-social-fr",
    "conventions-collectives",
    "remuneration-compliance",
    "protection-vie-privee-rh",
    "statut-baux-commerciaux",
    "loi-pinel-baux",
    "clauses-non-standard",
    "fiscalite-immobiliere",
    "droit-marches-financiers",
    "facteurs-risque",
    "gouvernance-societe",
    "esg-disclosure",
    "tabular-extraction",
    "droit-cession-fr",
    "consolidation-rapport",
    "red-flags-juridiques",
    "parallel-recherche-juridique-fr",
    "source-audit-juridique-fr",
    "veille-juridique-fr",
    "parallel-task-api-juridique-fr",
]

EXPECTED_AGENTS = {
    "revue-conformite-interne": [
        "legal-fr-runtime",
        "workflow-playbooks",
        "source-ledger",
        "review-queue",
        "confidentialite-donnees",
        "quality-gates-juridiques",
        "lecture-playbook",
        "creation-playbook",
        "conformite-contractuelle",
        "rgpd-baseline",
        "citation-juridique",
        "tableau-consolide",
    ],
    "analyse-contrats-fournisseurs": [
        "legal-fr-runtime",
        "workflow-playbooks",
        "source-ledger",
        "review-queue",
        "confidentialite-donnees",
        "quality-gates-juridiques",
        "tabular-review",
        "format-json-intermediaire",
        "lecture-playbook",
        "droit-achats-fr",
        "extraction-termes",
        "analyse-risques-supply",
        "tableau-consolide",
        "rapport-executif",
    ],
    "chronologie-contentieux": [
        "legal-fr-runtime",
        "workflow-playbooks",
        "source-ledger",
        "review-queue",
        "confidentialite-donnees",
        "quality-gates-juridiques",
        "tabular-review",
        "format-json-intermediaire",
        "extraction-evenements",
        "procedure-civile-delais",
        "analyse-causalite",
        "openlegi-recherche",
        "exa-recherche-juridique",
        "fiche-audience",
        "tableau-consolide",
    ],
    "jurisprudence-multilingue": [
        "legal-fr-runtime",
        "workflow-playbooks",
        "source-ledger",
        "review-queue",
        "confidentialite-donnees",
        "quality-gates-juridiques",
        "sources-jurisprudence",
        "openlegi-recherche",
        "exa-recherche-juridique",
        "citation-juridique",
        "lecture-decision",
        "droit-compare",
        "traduction-juridique",
        "rapport-executif",
    ],
    "revue-contrats-travail": [
        "legal-fr-runtime",
        "workflow-playbooks",
        "source-ledger",
        "review-queue",
        "confidentialite-donnees",
        "quality-gates-juridiques",
        "tabular-review",
        "format-json-intermediaire",
        "droit-social-fr",
        "conventions-collectives",
        "remuneration-compliance",
        "protection-vie-privee-rh",
        "openlegi-recherche",
        "tableau-consolide",
    ],
    "red-flags-bail": [
        "legal-fr-runtime",
        "workflow-playbooks",
        "source-ledger",
        "review-queue",
        "confidentialite-donnees",
        "quality-gates-juridiques",
        "statut-baux-commerciaux",
        "loi-pinel-baux",
        "clauses-non-standard",
        "fiscalite-immobiliere",
        "red-flags-juridiques",
        "openlegi-recherche",
        "rapport-executif",
        "tableau-consolide",
    ],
    "note-information-amf": [
        "legal-fr-runtime",
        "workflow-playbooks",
        "source-ledger",
        "review-queue",
        "confidentialite-donnees",
        "quality-gates-juridiques",
        "droit-marches-financiers",
        "facteurs-risque",
        "gouvernance-societe",
        "esg-disclosure",
        "citation-juridique",
        "openlegi-recherche",
        "exa-recherche-juridique",
        "note-amf",
        "rapport-executif",
    ],
    "tabular-due-diligence": [
        "legal-fr-runtime",
        "workflow-playbooks",
        "source-ledger",
        "review-queue",
        "confidentialite-donnees",
        "quality-gates-juridiques",
        "tabular-review",
        "format-json-intermediaire",
        "lecture-playbook",
        "scoring-playbook",
        "tabular-extraction",
        "droit-cession-fr",
        "consolidation-rapport",
        "red-flags-juridiques",
        "openlegi-recherche",
        "exa-recherche-juridique",
        "tableau-consolide",
        "rapport-executif",
    ],
    "recherche-juridique-fr-avancee": [
        "legal-fr-runtime",
        "workflow-playbooks",
        "source-ledger",
        "review-queue",
        "confidentialite-donnees",
        "quality-gates-juridiques",
        "openlegi-recherche",
        "exa-recherche-juridique",
        "citation-juridique",
        "rapport-executif",
        "parallel-recherche-juridique-fr",
        "source-audit-juridique-fr",
        "veille-juridique-fr",
        "parallel-task-api-juridique-fr",
    ],
}


class LegalFrScaffoldTest(unittest.TestCase):
    def test_vertical_manifest_and_mcp_are_present(self):
        manifest = VERTICAL / ".claude-plugin" / "plugin.json"
        self.assertTrue(manifest.is_file())
        data = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "legal-fr")
        self.assertEqual(data["version"], "1.0.0")
        self.assertEqual(data["author"]["name"], "Hacienda.diy")

        mcp = json.loads((VERTICAL / ".mcp.json").read_text(encoding="utf-8"))
        servers = mcp["mcpServers"]
        self.assertIn("exa", servers)
        self.assertEqual(servers["exa"]["url"], "https://mcp.exa.ai/mcp")
        self.assertIn("openlegi", servers)
        self.assertIn("mcp-remote", " ".join(servers["openlegi"]["args"]))
        self.assertNotIn("piighost", servers)

    def test_vertical_commands_playbooks_and_skills_exist(self):
        for family, command_names in EXPECTED_COMMANDS.items():
            for command_name in command_names:
                command = VERTICAL / "commands" / family / f"{command_name}.md"
                self.assertTrue(command.is_file(), str(command))
                text = command.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"), str(command))
                self.assertIn("allowed-tools:", text)

        for playbook in EXPECTED_PLAYBOOKS:
            self.assertTrue((VERTICAL / "playbooks" / playbook).is_file(), playbook)

        for skill in EXPECTED_SKILLS:
            skill_file = VERTICAL / "skills" / skill / "SKILL.md"
            self.assertTrue(skill_file.is_file(), str(skill_file))
            text = skill_file.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), str(skill_file))
            self.assertIn("## Workflow", text)

    def test_agent_plugins_are_self_contained(self):
        for agent, skills in EXPECTED_AGENTS.items():
            root = AGENTS / agent
            self.assertTrue((root / ".claude-plugin" / "plugin.json").is_file(), agent)
            prompt = root / "agents" / f"{agent}.md"
            self.assertTrue(prompt.is_file(), str(prompt))
            prompt_text = prompt.read_text(encoding="utf-8")
            self.assertTrue(prompt_text.startswith("---\n"), str(prompt))
            self.assertIn("## Workers reutilisables", prompt_text)
            self.assertIn("## Guardrails", prompt_text)
            self.assertNotIn("piighost", prompt_text.lower())
            for skill in skills:
                bundled = root / "skills" / skill / "SKILL.md"
                self.assertTrue(bundled.is_file(), str(bundled))

    def test_marketplace_registers_vertical_and_agents(self):
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        self.assertIn("workflows juridiques francais", marketplace["description"])
        entries = {entry["name"]: entry["source"] for entry in marketplace["plugins"]}
        self.assertEqual(entries["legal-fr"], "./plugins/vertical-plugins/legal-fr")
        for agent in EXPECTED_AGENTS:
            self.assertEqual(entries[agent], f"./plugins/agent-plugins/{agent}")

    def test_claude_project_settings_register_github_marketplace(self):
        self.assertTrue(CLAUDE_SETTINGS.is_file())
        self.assertTrue(CLAUDE_README.is_file())
        settings = json.loads(CLAUDE_SETTINGS.read_text(encoding="utf-8"))
        source = settings["extraKnownMarketplaces"]["legal-fr-suite"]["source"]
        self.assertEqual(source["source"], "github")
        self.assertEqual(source["repo"], "jamon8888/droit-cowork")

        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        for plugin in marketplace["plugins"]:
            self.assertIs(settings["enabledPlugins"][f"{plugin['name']}@legal-fr-suite"], True)

        readme = CLAUDE_README.read_text(encoding="utf-8")
        self.assertIn(".claude-plugin/marketplace.json", readme)
        self.assertIn("jamon8888/droit-cowork", readme)


if __name__ == "__main__":
    unittest.main()
