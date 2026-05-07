# Legal-FR Parallel MCP Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add official Parallel Search MCP and optional Parallel Task MCP documentation/configuration to Legal-FR while preserving OpenLegi-first legal sourcing and existing Parallel CLI/Task API paths.

**Architecture:** The generated Legal-FR scaffold remains the source of truth. Tests define required MCP URLs, optional authentication behavior, and docs/skill language. The generator updates `.mcp.json`, `CONNECTORS.md`, and skill bundles; connector checks validate offline config and warn on missing optional secrets.

**Tech Stack:** Python unittest, JSON MCP config, Markdown plugin skills/docs, existing Legal-FR generator.

---

### Task 1: Add Failing Production-Grade Tests

**Files:**
- Modify: `tests/test_legal_fr_production_grade.py`

- [ ] **Step 1: Add tests for Parallel MCP config and docs**

Add assertions to `LegalFrProductionGradeTest`:

```python
def test_parallel_mcp_connectors_are_documented_and_optional(self) -> None:
    config = load_json(LEGAL_FR / ".mcp.json")
    servers = config["mcpServers"]
    self.assertEqual(servers["parallel-search"]["url"], "https://search.parallel.ai/mcp")
    self.assertEqual(servers["parallel-search"]["type"], "http")
    self.assertEqual(servers["parallel-task"]["url"], "https://task-mcp.parallel.ai/mcp")
    self.assertEqual(servers["parallel-task"]["type"], "http")
    self.assertTrue(servers["parallel-task"]["optional"])
    self.assertIn("${PARALLEL_API_KEY}", json.dumps(servers["parallel-task"]))

    connectors = (LEGAL_FR / "CONNECTORS.md").read_text(encoding="utf-8")
    skill = (LEGAL_FR / "skills" / "parallel-recherche-juridique-fr" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    combined = connectors + "\n" + skill
    for required in [
        "https://docs.parallel.ai/integrations/mcp/quickstart",
        "https://search.parallel.ai/mcp",
        "https://task-mcp.parallel.ai/mcp",
        "web_search",
        "web_fetch",
        "createDeepResearch",
        "createTaskGroup",
        "getStatus",
        "getResultMarkdown",
        "Parallel Search MCP",
        "Parallel Task MCP",
    ]:
        self.assertIn(required, combined)
```

- [ ] **Step 2: Add tests for checker constants and secret policy**

Extend `test_parallel_cli_checker_exists_and_documents_no_secret_policy` or add:

```python
def test_connector_checker_knows_parallel_mcp_urls_without_secret_values(self) -> None:
    checker = (ROOT / "scripts" / "check_legal_fr_connectors.py").read_text(encoding="utf-8")
    self.assertIn("PARALLEL_SEARCH_ENDPOINT", checker)
    self.assertIn("PARALLEL_TASK_ENDPOINT", checker)
    self.assertIn("https://search.parallel.ai/mcp", checker)
    self.assertIn("https://task-mcp.parallel.ai/mcp", checker)
    self.assertIn("PARALLEL_API_KEY", checker)
    self.assertNotIn("PARALLEL_API_KEY=", checker)
```

- [ ] **Step 3: Run tests to verify RED**

Run:

```bash
python -m unittest tests.test_legal_fr_production_grade.LegalFrProductionGradeTest.test_parallel_mcp_connectors_are_documented_and_optional tests.test_legal_fr_production_grade.LegalFrProductionGradeTest.test_connector_checker_knows_parallel_mcp_urls_without_secret_values -v
```

Expected: FAIL because `.mcp.json`, docs, skill text and checker do not include Parallel MCP yet.

### Task 2: Update Generator and Connector Checker

**Files:**
- Modify: `scripts/generate_legal_fr_scaffold.py`
- Modify: `scripts/check_legal_fr_connectors.py`

- [ ] **Step 1: Update generated `.mcp.json`**

In `vertical_docs()`, extend `mcpServers`:

```python
"parallel-search": {
    "type": "http",
    "url": "https://search.parallel.ai/mcp",
},
"parallel-task": {
    "type": "http",
    "url": "https://task-mcp.parallel.ai/mcp",
    "headers": {
        "Authorization": "Bearer ${PARALLEL_API_KEY}",
    },
    "optional": True,
},
```

- [ ] **Step 2: Update connector checker constants and validation**

Add constants:

```python
PARALLEL_SEARCH_ENDPOINT = "https://search.parallel.ai/mcp"
PARALLEL_TASK_ENDPOINT = "https://task-mcp.parallel.ai/mcp"
PARALLEL_API_KEY_REF = "${PARALLEL_API_KEY}"
PARALLEL_TOKEN_WARN = (
    "WARN: PARALLEL_API_KEY is not set; Parallel Task MCP will require OAuth or env auth before runtime use."
)
```

In `validate()`, require `parallel-search.url == PARALLEL_SEARCH_ENDPOINT`. Require `parallel-task.url == PARALLEL_TASK_ENDPOINT`, `optional is True`, and token reference present in the task server. Do not require the actual env var.

In `main()`, print `PARALLEL_TOKEN_WARN` when `PARALLEL_API_KEY` is absent.

- [ ] **Step 3: Update generated docs and skill text**

In `CONNECTORS.md`, add sections:

```markdown
## Parallel Search MCP

Documentation officielle: https://docs.parallel.ai/integrations/mcp/quickstart.
Endpoint: `https://search.parallel.ai/mcp`.
Outils attendus: `web_search`, `web_fetch`.
Usage Legal-FR: recherche web rapide et fetch URL; les resultats restent `secondary` ou `unverified` tant qu'OpenLegi ou une source officielle ne confirme pas le point de droit.

## Parallel Task MCP

Endpoint: `https://task-mcp.parallel.ai/mcp`.
Outils attendus: `createDeepResearch`, `createTaskGroup`, `getStatus`, `getResultMarkdown`.
Authentification: OAuth ou `PARALLEL_API_KEY`; ne jamais hardcoder la cle.
Usage Legal-FR: recherche longue interactive, task groups et enrichissement; optionnel et distinct du CLI et de la Task API backend.
```

In `skill_integration_section("parallel-recherche-juridique-fr")`, add the same MCP hierarchy and usage rules.

- [ ] **Step 4: Regenerate scaffold**

Run:

```bash
python scripts/generate_legal_fr_scaffold.py
```

Expected output:

```text
generated legal-fr vertical, production-grade layer and 9 Legal-FR agent plugins
```

### Task 3: Verify and Commit

**Files:**
- Commit all files touched by Task 1 and Task 2.
- Do not stage unrelated `.gitignore` or `.claude/` changes.

- [ ] **Step 1: Run targeted GREEN tests**

Run:

```bash
python -m unittest tests.test_legal_fr_production_grade.LegalFrProductionGradeTest.test_parallel_mcp_connectors_are_documented_and_optional tests.test_legal_fr_production_grade.LegalFrProductionGradeTest.test_connector_checker_knows_parallel_mcp_urls_without_secret_values -v
```

Expected: OK.

- [ ] **Step 2: Run full Legal-FR verification**

Run:

```bash
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures tests.test_legal_fr_clean_repo tests.test_legal_fr_workflow_design_spec tests.test_legal_fr_workflow_runner -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
python scripts/check_legal_fr_connectors.py --online
python -m py_compile scripts/generate_legal_fr_scaffold.py scripts/check_legal_fr_connectors.py
git diff --check
```

Expected:

- `check.py`: OK.
- unittest suite: OK.
- evals: 45 expected outputs checked.
- connector checker: OK with warnings if `OPENLEGI_TOKEN` or `PARALLEL_API_KEY` are absent.
- online checker: `OpenLegi health OK`.
- py_compile: no output.
- diff check: no output.

- [ ] **Step 3: Stage scoped changes**

Run `git status --short`, then stage only Legal-FR files changed by this plan:

```bash
git add docs/superpowers/specs/2026-05-07-legal-fr-parallel-mcp-integration-design.md docs/superpowers/plans/2026-05-07-legal-fr-parallel-mcp-integration.md tests/test_legal_fr_production_grade.py scripts/generate_legal_fr_scaffold.py scripts/check_legal_fr_connectors.py plugins/vertical-plugins/legal-fr/.mcp.json plugins/vertical-plugins/legal-fr/CONNECTORS.md plugins/vertical-plugins/legal-fr/skills/parallel-recherche-juridique-fr/SKILL.md plugins/agent-plugins/recherche-juridique-fr-avancee/skills/parallel-recherche-juridique-fr/SKILL.md
```

If regenerating copies `openlegi-recherche` or unrelated skills without substantive MCP changes, inspect before staging and exclude mechanical whitespace churn.

- [ ] **Step 4: Commit**

Run:

```bash
git diff --cached --check
git commit -m "docs: add legal fr parallel mcp layer"
```

Expected: commit succeeds.

## Self-Review

- Spec coverage: all decisions in the design are implemented by Task 1 and Task 2.
- Completion scan: no unresolved marker text remains.
- Type consistency: server names are `parallel-search` and `parallel-task`; endpoint constants match the official URLs.
- Scope: this plan does not install the MCP into user-level Codex/Claude config. It updates the Legal-FR plugin scaffold and verification only.
