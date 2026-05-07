# Legal-FR Clean Repository Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the active repository from Financial Services to a clean Legal-FR suite while archiving the original Financial Services codebase under `archive/financial-services-origin/`.

**Architecture:** Keep the active root focused on Legal-FR plugins, tests, scripts, docs, and marketplace entries. Move Financial Services assets into an archive directory and update validation scripts so archived material is preserved but not treated as active plugin surface. Root `README.md`, `AGENTS.md`, and `CLAUDE.md` become Legal-FR-specific.

**Tech Stack:** Python stdlib, unittest, JSON plugin manifests, Markdown docs, existing Cowork plugin layout, git-aware file moves.

---

## File Map

- Create: `tests/test_legal_fr_clean_repo.py` — RED tests proving the active repo is Legal-FR-only and Financial Services is archived.
- Modify: `scripts/check.py` — tolerate missing active Managed Agent cookbooks and validate only active plugin paths.
- Modify: `.claude-plugin/marketplace.json` — trim active marketplace to Legal-FR vertical and nine Legal-FR agent plugins.
- Modify: `README.md` — replace Financial Services identity with Legal-FR suite documentation.
- Create/modify: `AGENTS.md` — root Legal-FR agent instructions.
- Modify: `CLAUDE.md` — root Legal-FR runtime instructions.
- Create: `docs/architecture/legal-fr-suite.md` — active/archive architecture.
- Create: `docs/agents/legal-fr-agents.md` — nine-agent catalogue.
- Create: `docs/workflows/legora-harvey-fr-workflows.md` — production workflow mapping.
- Create: `archive/financial-services-origin/ARCHIVE.md` — archive inventory and rationale.
- Move: non-Legal-FR active assets into `archive/financial-services-origin/`.

## Active Legal-FR Plugin Slugs

Use this exact list wherever tests or scripts need the active plugin set:

```python
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
```

## Task 1: RED Tests For Clean Legal-FR Repository

**Files:**
- Create: `tests/test_legal_fr_clean_repo.py`

- [ ] **Step 1: Create the clean-repo test file**

Create `tests/test_legal_fr_clean_repo.py` with this complete content:

```python
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
```

- [ ] **Step 2: Run the RED test**

Run:

```bash
python -m unittest tests.test_legal_fr_clean_repo -v
```

Expected: failures because `archive/financial-services-origin/` does not exist yet and the marketplace still lists Financial Services plugins.

- [ ] **Step 3: Commit RED test**

Run:

```bash
git add tests/test_legal_fr_clean_repo.py
git commit -m "test: add legal fr clean repo expectations"
```

## Task 2: Archive Financial Services Origin Assets

**Files:**
- Create directory: `archive/financial-services-origin/`
- Move: non-Legal-FR plugin directories, Managed Agent cookbooks, Microsoft 365 install tooling, Financial Services scripts/tests.
- Create: `archive/financial-services-origin/ARCHIVE.md`

- [ ] **Step 1: Create archive directories**

Run:

```powershell
New-Item -ItemType Directory -Force archive/financial-services-origin | Out-Null
New-Item -ItemType Directory -Force archive/financial-services-origin/plugins | Out-Null
New-Item -ItemType Directory -Force archive/financial-services-origin/scripts | Out-Null
New-Item -ItemType Directory -Force archive/financial-services-origin/tests | Out-Null
```

- [ ] **Step 2: Archive the original README**

Run:

```powershell
git mv README.md archive/financial-services-origin/README.md
```

- [ ] **Step 3: Move Financial Services vertical plugins**

Run:

```powershell
$verticals = @(
  'financial-analysis',
  'investment-banking',
  'equity-research',
  'private-equity',
  'wealth-management',
  'fund-admin',
  'operations'
)
foreach ($slug in $verticals) {
  git mv "plugins/vertical-plugins/$slug" "archive/financial-services-origin/plugins/vertical-plugins/$slug"
}
```

- [ ] **Step 4: Move partner-built plugins**

Run:

```powershell
git mv plugins/partner-built archive/financial-services-origin/plugins/partner-built
```

- [ ] **Step 5: Move non-Legal-FR agent plugins**

Run:

```powershell
$legalAgents = @(
  'revue-conformite-interne',
  'analyse-contrats-fournisseurs',
  'chronologie-contentieux',
  'jurisprudence-multilingue',
  'revue-contrats-travail',
  'red-flags-bail',
  'note-information-amf',
  'tabular-due-diligence',
  'recherche-juridique-fr-avancee'
)
New-Item -ItemType Directory -Force archive/financial-services-origin/plugins/agent-plugins | Out-Null
Get-ChildItem plugins/agent-plugins -Directory | Where-Object { $legalAgents -notcontains $_.Name } | ForEach-Object {
  git mv $_.FullName "archive/financial-services-origin/plugins/agent-plugins/$($_.Name)"
}
```

- [ ] **Step 6: Move Managed Agent cookbooks and Microsoft 365 install tooling**

Run:

```powershell
git mv managed-agent-cookbooks archive/financial-services-origin/managed-agent-cookbooks
git mv claude-for-msft-365-install archive/financial-services-origin/claude-for-msft-365-install
```

- [ ] **Step 7: Move Financial Services scripts**

Run:

```powershell
$activeLegalScripts = @(
  'check.py',
  'generate_legal_fr_scaffold.py',
  'run_legal_fr_evals.py',
  'check_legal_fr_connectors.py',
  'check_legal_fr_parallel_cli.py',
  'check_legal_fr_parallel_task_api.py',
  'legal_fr_parallel_task.py'
)
Get-ChildItem scripts -File | Where-Object { $activeLegalScripts -notcontains $_.Name } | ForEach-Object {
  git mv $_.FullName "archive/financial-services-origin/scripts/$($_.Name)"
}
```

- [ ] **Step 8: Move Financial Services tests**

Run:

```powershell
Get-ChildItem tests -File | Where-Object { $_.Name -notlike 'test_legal_fr_*' } | ForEach-Object {
  git mv $_.FullName "archive/financial-services-origin/tests/$($_.Name)"
}
```

- [ ] **Step 9: Add archive inventory**

Create `archive/financial-services-origin/ARCHIVE.md` with this content:

```markdown
# Financial Services Origin Archive

This directory preserves the original Financial Services repository material after the active root was converted into the Legal-FR suite.

## Archived Material

- Original Financial Services README.
- Original Financial Services vertical plugins.
- Original Financial Services agent plugins.
- Partner-built plugins.
- Managed Agent cookbooks.
- Claude for Microsoft 365 install tooling.
- Financial Services scripts and tests.

## Active Repository Boundary

The active repository root now serves the Legal-FR plugin suite only. Archived files are retained for reference and migration history, but active marketplace validation and Legal-FR tests should not treat this archive as installable plugin surface.

## Restoration

To restore a Financial Services asset, copy or move the relevant archived directory back into the active tree and update `.claude-plugin/marketplace.json`, tests, and documentation intentionally.
```

- [ ] **Step 10: Run the clean-repo test**

Run:

```bash
python -m unittest tests.test_legal_fr_clean_repo -v
```

Expected: some failures remain for marketplace and root docs, but archive presence assertions should now pass.

- [ ] **Step 11: Commit archive move**

Run:

```bash
git add archive plugins scripts tests README.md
git commit -m "refactor: archive financial services origin assets"
```

## Task 3: Adapt Active Validation To Legal-FR-Only Root

**Files:**
- Modify: `scripts/check.py`

- [ ] **Step 1: Replace top-level constants in `scripts/check.py`**

Replace:

```python
PLUGINS = ROOT / "plugins"
MANAGED = ROOT / "managed-agent-cookbooks"
errors: list[str] = []
checked = 0
```

with:

```python
PLUGINS = ROOT / "plugins"
MANAGED = ROOT / "managed-agent-cookbooks"
ARCHIVE = ROOT / "archive"
errors: list[str] = []
checked = 0
```

- [ ] **Step 2: Add helper functions after `rel()`**

Add:

```python
def active_glob(pattern: str) -> list[Path]:
    return [path for path in ROOT.glob(pattern) if ARCHIVE not in path.parents]


def managed_yaml_files() -> list[Path]:
    if not MANAGED.is_dir():
        return []
    return sorted(MANAGED.rglob("*.yaml"))
```

- [ ] **Step 3: Replace Managed Agent YAML loops**

Replace both occurrences of:

```python
for yml in sorted(MANAGED.rglob("*.yaml")):
```

with:

```python
for yml in managed_yaml_files():
```

- [ ] **Step 4: Replace JSON glob loop**

Replace:

```python
for pat in json_globs:
    for jf in sorted(ROOT.glob(pat)):
```

with:

```python
for pat in json_globs:
    for jf in sorted(active_glob(pat)):
```

- [ ] **Step 5: Guard required Managed Agent files**

Replace:

```python
for d in sorted(MANAGED.iterdir()):
    if not d.is_dir():
        continue
    for req in ("agent.yaml", "README.md", "steering-examples.json"):
        if not (d / req).is_file():
            err(f"missing: {rel(d)}/{req}")
```

with:

```python
if MANAGED.is_dir():
    for d in sorted(MANAGED.iterdir()):
        if not d.is_dir():
            continue
        for req in ("agent.yaml", "README.md", "steering-examples.json"):
            if not (d / req).is_file():
                err(f"missing: {rel(d)}/{req}")
```

- [ ] **Step 6: Run validation script**

Run:

```bash
python scripts/check.py
```

Expected: may still fail until marketplace is trimmed and docs are written. It must not crash because `managed-agent-cookbooks` is absent.

- [ ] **Step 7: Commit validation update**

Run:

```bash
git add scripts/check.py
git commit -m "refactor: scope validation to active legal fr plugins"
```

## Task 4: Trim Marketplace To Legal-FR Plugins

**Files:**
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Replace marketplace content**

Replace `.claude-plugin/marketplace.json` with:

```json
{
  "name": "legal-fr-suite",
  "owner": {
    "name": "Hacienda.diy"
  },
  "plugins": [
    {
      "name": "legal-fr",
      "source": "./plugins/vertical-plugins/legal-fr",
      "description": "Socle juridique francais: playbooks, Tabular Review, OpenLegi, Exa, Parallel CLI et skills metier."
    },
    {
      "name": "revue-conformite-interne",
      "source": "./plugins/agent-plugins/revue-conformite-interne",
      "description": "Verifie un document juridique contre les standards internes du cabinet ou de l'entreprise."
    },
    {
      "name": "analyse-contrats-fournisseurs",
      "source": "./plugins/agent-plugins/analyse-contrats-fournisseurs",
      "description": "Analyse en masse des contrats fournisseurs avec extraction des termes cles et scoring de risque."
    },
    {
      "name": "chronologie-contentieux",
      "source": "./plugins/agent-plugins/chronologie-contentieux",
      "description": "Extrait dates, actes et jalons proceduraux pour reconstruire une chronologie contentieuse."
    },
    {
      "name": "jurisprudence-multilingue",
      "source": "./plugins/agent-plugins/jurisprudence-multilingue",
      "description": "Recherche, analyse, compare et traduit des decisions de justice multi-juridictionnelles."
    },
    {
      "name": "revue-contrats-travail",
      "source": "./plugins/agent-plugins/revue-contrats-travail",
      "description": "Revue des contrats de travail, remuneration, non-concurrence et conformite conventionnelle."
    },
    {
      "name": "red-flags-bail",
      "source": "./plugins/agent-plugins/red-flags-bail",
      "description": "Analyse des baux commerciaux, professionnels ou mixtes avec detection de red flags."
    },
    {
      "name": "note-information-amf",
      "source": "./plugins/agent-plugins/note-information-amf",
      "description": "Redaction assistee des facteurs de risque et sections reglementaires des notes d'information AMF."
    },
    {
      "name": "tabular-due-diligence",
      "source": "./plugins/agent-plugins/tabular-due-diligence",
      "description": "Due diligence a grande echelle par extraction parallele, scoring et consolidation tabulaire."
    },
    {
      "name": "recherche-juridique-fr-avancee",
      "source": "./plugins/agent-plugins/recherche-juridique-fr-avancee",
      "description": "Recherche juridique francaise avancee avec OpenLegi, Parallel CLI, audit des sources et couche Task API."
    }
  ]
}
```

- [ ] **Step 2: Run marketplace tests**

Run:

```bash
python -m unittest tests.test_legal_fr_scaffold.LegalFrScaffoldTest.test_marketplace_registers_vertical_and_agents tests.test_legal_fr_clean_repo.LegalFrCleanRepoTest.test_active_marketplace_only_lists_legal_fr_plugins -v
```

Expected: pass once active plugin paths exist and only Legal-FR entries remain.

- [ ] **Step 3: Commit marketplace trim**

Run:

```bash
git add .claude-plugin/marketplace.json
git commit -m "refactor: trim marketplace to legal fr suite"
```

## Task 5: Replace Root Legal-FR Documentation

**Files:**
- Create: `README.md`
- Create/modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Create: `docs/architecture/legal-fr-suite.md`
- Create: `docs/agents/legal-fr-agents.md`
- Create: `docs/workflows/legora-harvey-fr-workflows.md`

- [ ] **Step 1: Create root README**

Create `README.md` with this structure and content:

```markdown
# Legal-FR Suite

Legal-FR Suite is a production-grade French legal workflow codebase for Cowork/Codex plugins. It packages a Legal-FR vertical plugin, nine specialized Legal-FR agents, schemas, eval fixtures, source verification rules, OpenLegi/Exa MCP configuration, Parallel CLI research commands, and a Parallel Task API scaffold.

Every output is a draft for professional validation. Nothing in this repository constitutes legal advice, a binding legal opinion, a filing, or a client-ready deliverable without review by a qualified professional.

## Active Architecture

- `plugins/vertical-plugins/legal-fr`: source of commands, skills, playbooks, schemas, evals, and MCP configuration.
- `plugins/agent-plugins/*`: nine self-contained Legal-FR agent plugins with bundled skills.
- `scripts`: Legal-FR generation, validation, eval, connector, Parallel CLI, and Parallel Task API helpers.
- `tests`: Legal-FR structural, production-grade, clean-repo, and eval fixture tests.
- `docs`: architecture, agents, workflows, specs, and implementation plans.
- `archive/financial-services-origin`: preserved Financial Services origin material.

## Agents

| Agent | Purpose |
|---|---|
| `revue-conformite-interne` | Internal compliance review against cabinet playbooks. |
| `analyse-contrats-fournisseurs` | Supplier contract corpus review and risk scoring. |
| `chronologie-contentieux` | Litigation timeline construction and procedural checks. |
| `jurisprudence-multilingue` | Case law research, multilingual analysis, translation, and comparative law. |
| `revue-contrats-travail` | French employment contract and HR corpus review. |
| `red-flags-bail` | Commercial lease red flag review. |
| `note-information-amf` | AMF disclosure and risk factor drafting support. |
| `tabular-due-diligence` | Large-scale due diligence table extraction and reporting. |
| `recherche-juridique-fr-avancee` | French legal research with OpenLegi-first sourcing, Parallel CLI, source audit, veille, and Task API second layer. |

## Validation

Run:

```bash
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures tests.test_legal_fr_clean_repo -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
python scripts/check_legal_fr_parallel_task_api.py
```

Optional environment check:

```bash
python scripts/check_legal_fr_parallel_cli.py
```

If `parallel-cli` is not installed, this may return `ERROR: parallel-cli is not installed or not on PATH`.

## Archive

The original Financial Services repository material is preserved in `archive/financial-services-origin/`.
```

- [ ] **Step 2: Create root AGENTS.md**

Create `AGENTS.md` with:

```markdown
# Legal-FR Suite — Agent Instructions

## Role

This repository is the Legal-FR plugin suite for French legal workflows. Agents assist legal professionals; they do not replace qualified professional review.

## Mandatory Legal Posture

- Every external-facing output must include `DRAFT - Validation professionnelle requise`.
- Human validation is mandatory before client, regulator, counterparty, filing, or external use.
- Do not present legal conclusions as final advice.
- Mark uncertain points as `A VERIFIER`.
- Cite legal sources for critical conclusions.

## Source Discipline

- Use OpenLegi before Parallel for French positive law.
- Use Exa and Parallel CLI for public web research, source discovery, secondary context, enrichment, and veille.
- Use `parallel-cli` only with `--json` in Legal-FR research commands.
- Treat Parallel Task API as a second backend layer, not a replacement for local Cowork CLI workflows.
- Keep `jurisprudence-multilingue` for multilingual, comparative, CJUE/CEDH, and translation workflows.

## Security And Secrets

- Never hardcode `OPENLEGI_TOKEN` or `PARALLEL_API_KEY`.
- Do not expose environment variables in generated reports.
- Do not reintroduce `piighost`.
- Do not send raw confidential client data to public web research tools.

## Development Workflow

- Edit Legal-FR generation logic in `scripts/generate_legal_fr_scaffold.py` when changing generated plugin assets.
- Active marketplace entries live in `.claude-plugin/marketplace.json`.
- Financial Services origin assets are archived under `archive/financial-services-origin/` and are not active plugin surface.

## Required Verification

Run before claiming completion:

```bash
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures tests.test_legal_fr_clean_repo -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
python scripts/check_legal_fr_parallel_task_api.py
```
```

- [ ] **Step 3: Create root CLAUDE.md**

Create `CLAUDE.md` with:

```markdown
# Legal-FR Runtime Instructions

Use this repository as the active Legal-FR suite.

## Output Rules

- Preserve `DRAFT - Validation professionnelle requise` on every external deliverable.
- Require human validation before reliance.
- Surface incomplete documents, missing sources, uncertainty, and low confidence.

## Research Rules

- OpenLegi avant Parallel for French positive law.
- Exa and Parallel CLI are support layers for broader public source discovery and enrichment.
- Parallel CLI commands must use JSON output.
- Parallel Task API is a backend second layer for async or batch research.
- `jurisprudence-multilingue` remains the workflow for multilingual/comparative case law and translation.

## Active Repository Boundary

Active Legal-FR assets live in `plugins/vertical-plugins/legal-fr`, `plugins/agent-plugins`, `scripts`, `tests`, and `docs`.

Original Financial Services assets live in `archive/financial-services-origin/` and should not be treated as active plugin surface.
```

- [ ] **Step 4: Add architecture docs**

Create `docs/architecture/legal-fr-suite.md` with:

```markdown
# Legal-FR Suite Architecture

Legal-FR Suite is organized around one vertical plugin and nine self-contained agent plugins.

## Source Of Truth

- Vertical source: `plugins/vertical-plugins/legal-fr`
- Generated or bundled agent copies: `plugins/agent-plugins/<agent>/skills`
- Generator: `scripts/generate_legal_fr_scaffold.py`
- Active marketplace: `.claude-plugin/marketplace.json`

## Active vs Archived

The active root contains only Legal-FR plugin surface. Original Financial Services material is preserved under `archive/financial-services-origin/` for reference.

## Validation

`scripts/check.py` validates active plugin manifests, marketplace paths, agent frontmatter, bundled skills, and Legal-FR structure. Legal-FR-specific tests validate schemas, commands, eval fixtures, source discipline, and clean-repo boundaries.
```

- [ ] **Step 5: Add agents doc**

Create `docs/agents/legal-fr-agents.md` with the same nine-agent table from the README plus this sentence:

```markdown
Each agent plugin is self-contained: its `agents/<slug>.md` prompt and bundled `skills/` directory can be installed independently from the full vertical.
```

- [ ] **Step 6: Add workflows doc**

Create `docs/workflows/legora-harvey-fr-workflows.md` with:

```markdown
# Legora and Harvey Inspired French Legal Workflows

Legal-FR combines Legora-style tabular review and playbook workflows with Harvey-style legal reasoning patterns adapted to French law.

## Production Workflow Families

- Internal compliance review: playbook-driven checks against cabinet standards.
- Supplier agreement analysis: corpus extraction, table consolidation, and risk scoring.
- Litigation chronology: fact/date extraction, procedural checks, and hearing preparation.
- Jurisprudence multilingue: case law research, translation, and comparative analysis.
- Employment contract review: French labor law and collective bargaining checks.
- Lease red flags: commercial lease analysis and statutory risk review.
- AMF disclosure support: risk factors and regulated disclosure drafting.
- Tabular due diligence: data room extraction, scoring, and executive reporting.
- Advanced French legal research: OpenLegi-first source discipline with Parallel CLI and Task API layers.

## Quality Gates

All workflows require source status, confidence, audit trail, draft notice, and human validation metadata.
```

- [ ] **Step 7: Run doc tests**

Run:

```bash
python -m unittest tests.test_legal_fr_clean_repo.LegalFrCleanRepoTest.test_root_docs_are_legal_fr_specific tests.test_legal_fr_clean_repo.LegalFrCleanRepoTest.test_clean_repo_docs_exist -v
```

Expected: pass.

- [ ] **Step 8: Commit docs**

Run:

```bash
git add README.md AGENTS.md CLAUDE.md docs/architecture docs/agents docs/workflows
git commit -m "docs: replace root docs with legal fr suite guidance"
```

## Task 6: Full Validation And Cleanup

**Files:**
- Modify if needed: tests or docs only when validation exposes a real mismatch.

- [ ] **Step 1: Run full deterministic validation**

Run:

```bash
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures tests.test_legal_fr_clean_repo -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
python scripts/check_legal_fr_parallel_task_api.py
```

Expected:

- `scripts/check.py`: `OK`
- unittest: all tests pass
- eval runner: `Legal-FR evals passed: 45 expected outputs checked`
- connector checker: `Legal-FR connector config OK`, with acceptable `OPENLEGI_TOKEN` warning if unset
- Task API checker: `Legal-FR Parallel Task API scaffold OK`

- [ ] **Step 2: Run conditional Parallel CLI checker**

Run:

```bash
python scripts/check_legal_fr_parallel_cli.py
```

Expected acceptable outcomes:

- `Legal-FR Parallel CLI config OK` when CLI is installed and auth shape is valid.
- `ERROR: parallel-cli is not installed or not on PATH` when local CLI is absent.

- [ ] **Step 3: Scan active surface for forbidden strings**

Run:

```powershell
Get-ChildItem -Path plugins, scripts, tests, docs, .claude-plugin, README.md, AGENTS.md, CLAUDE.md -Recurse -File -Include *.md,*.json,*.py |
  Where-Object { $_.FullName -notmatch '\\archive\\financial-services-origin\\' } |
  Select-String -Pattern 'PARALLEL_API_KEY=|OPENLEGI_TOKEN=|piighost' -CaseSensitive:$false
```

Expected: no matches except negative assertions in tests if `tests` are included. If matches are only test assertions such as `assertNotIn("PARALLEL_API_KEY=", ...)`, record them as acceptable. If any active docs, scripts, commands, skills, or schemas contain assignments or `piighost`, fix them.

- [ ] **Step 4: Check git status**

Run:

```bash
git status --short --branch
```

Expected: clean worktree on `codex/legal-fr-clean-repo-architecture`.

- [ ] **Step 5: Refresh GitNexus**

Run:

```bash
npx gitnexus analyze --embeddings
npx gitnexus status
```

Expected: indexed commit equals current commit.

- [ ] **Step 6: Commit any final validation fixes**

If validation required fixes, commit with:

```bash
git add <changed-files>
git commit -m "fix: finalize legal fr clean repository validation"
```

If no fixes were required, do not create an empty commit.

## Task 7: Merge Back To Main

**Files:**
- No planned edits.

- [ ] **Step 1: Verify branch status**

Run:

```bash
git status --short --branch
git log --oneline main..HEAD
```

Expected: clean feature branch with implementation commits ahead of `main`.

- [ ] **Step 2: Merge from main workspace after user approval**

From `C:\Users\NMarchitecte\financial-services`, run:

```bash
git merge --no-ff codex/legal-fr-clean-repo-architecture
```

Expected: merge succeeds. If main still has dirty local GitNexus files, confirm they do not overlap with tracked files being merged or clean only generated local artifacts after inspection.

- [ ] **Step 3: Re-run validation on main**

Run the same commands from Task 6 Step 1 on the main workspace.

- [ ] **Step 4: Remove worktree and branch**

Run:

```bash
git worktree remove C:\Users\NMarchitecte\.config\superpowers\worktrees\financial-services\legal-fr-clean-repo
git branch -d codex/legal-fr-clean-repo-architecture
```

Expected: worktree and branch removed after successful merge.
