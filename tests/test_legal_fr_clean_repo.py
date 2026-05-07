import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "financial-services-origin"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS = ROOT / "plugins"

LEGAL_FR_PLUGINS = [
    "legal-fr",
    "revue-conformite-interne",
    "analyse-contrats-fournisseurs",
    "chronologie-contentieux",
    "jurisprudence-multilingue",
    "revue-contrats-travail",
    "red-flags-bail",
    "note-information-amf",
    "tabular-due-diligence",
    "recherche-juridique-fr-avancee",
]

ARCHIVED_VERTICALS = [
    "financial-analysis",
    "investment-banking",
    "equity-research",
    "private-equity",
    "wealth-management",
    "fund-admin",
    "operations",
]


class LegalFrCleanRepoTest(unittest.TestCase):
    def test_active_marketplace_only_lists_legal_fr_plugins(self) -> None:
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        entries = {entry["name"]: entry["source"] for entry in marketplace["plugins"]}
        self.assertEqual(list(entries), LEGAL_FR_PLUGINS)
        self.assertEqual(entries["legal-fr"], "./plugins/vertical-plugins/legal-fr")
        for slug in LEGAL_FR_PLUGINS[1:]:
            self.assertEqual(entries[slug], f"./plugins/agent-plugins/{slug}")

    def test_financial_services_assets_are_archived_not_active(self) -> None:
        self.assertTrue((ARCHIVE / "ARCHIVE.md").is_file())
        self.assertTrue((ARCHIVE / "README.md").is_file())
        self.assertTrue((ARCHIVE / "plugins").is_dir())
        self.assertTrue((ARCHIVE / "managed-agent-cookbooks").is_dir())
        self.assertTrue((ARCHIVE / "claude-for-msft-365-install").is_dir())
        for slug in ARCHIVED_VERTICALS:
            self.assertFalse((PLUGINS / "vertical-plugins" / slug).exists(), slug)
            self.assertTrue((ARCHIVE / "plugins" / "vertical-plugins" / slug).is_dir(), slug)
        self.assertFalse((PLUGINS / "partner-built").exists())
        self.assertTrue((ARCHIVE / "plugins" / "partner-built").is_dir())

    def test_active_plugins_contain_only_legal_fr_surface(self) -> None:
        active_verticals = sorted(path.name for path in (PLUGINS / "vertical-plugins").iterdir() if path.is_dir())
        active_agents = sorted(path.name for path in (PLUGINS / "agent-plugins").iterdir() if path.is_dir())
        self.assertEqual(active_verticals, ["legal-fr"])
        self.assertEqual(active_agents, sorted(LEGAL_FR_PLUGINS[1:]))

    def test_root_docs_are_legal_fr_specific(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("Legal-FR", readme)
        self.assertIn("recherche-juridique-fr-avancee", readme)
        self.assertIn("OpenLegi avant Parallel", agents)
        self.assertIn("DRAFT - Validation professionnelle requise", agents)
        self.assertIn("Parallel Task API", claude)
        self.assertNotIn("Pitch Agent", readme)
        self.assertNotIn("investment recommendations", readme.lower())

    def test_clean_repo_docs_exist(self) -> None:
        expected_docs = [
            ROOT / "docs" / "architecture" / "legal-fr-suite.md",
            ROOT / "docs" / "agents" / "legal-fr-agents.md",
            ROOT / "docs" / "workflows" / "legora-harvey-fr-workflows.md",
        ]
        for path in expected_docs:
            with self.subTest(path=path):
                self.assertTrue(path.is_file())
                text = path.read_text(encoding="utf-8")
                self.assertIn("Legal-FR", text)


if __name__ == "__main__":
    unittest.main()
