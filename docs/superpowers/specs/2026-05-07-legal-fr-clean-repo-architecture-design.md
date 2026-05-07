# Legal-FR Clean Repository Architecture Design

## Goal

Transform the current `financial-services` repository into a clean, documented Legal-FR codebase while preserving the original Financial Services material in an archive directory.

The active repository root must become focused on the French legal plugin suite:

- Legal-FR vertical plugin.
- Nine Legal-FR agent plugins.
- Legal-FR generation, validation, connector, eval, and Parallel integration scripts.
- Legal-FR tests and eval fixtures.
- Legal-FR documentation, runtime instructions, and agent instructions.

Everything that belongs to the original Financial Services distribution must remain accessible under `archive/financial-services-origin/`.

## Non-Goals

- Do not delete the original Financial Services assets permanently.
- Do not reintroduce `legacy anonymization MCP`.
- Do not change Legal-FR workflow behavior beyond paths, docs, marketplace scope, and repository structure.
- Do not install or call paid external services during restructuring.
- Do not require `parallel-cli` to be installed for deterministic CI checks.

## Current State

The repository currently mixes two identities:

- Original Financial Services assets: financial-analysis, investment-banking, equity-research, private-equity, wealth-management, fund-admin, operations, partner-built connectors, Microsoft 365 install tooling, and Managed Agent cookbooks.
- New Legal-FR assets: `plugins/vertical-plugins/legal-fr`, nine Legal-FR agent plugins, Legal-FR tests, Legal-FR evals, OpenLegi/Exa connectors, Parallel CLI checker, and Parallel Task API scaffold.

`main` also contains local generated instruction files from GitNexus (`AGENTS.md`, `CLAUDE.md`, `.claude/`, `.gitignore` edits). The cleanup should integrate new Legal-FR `AGENTS.md` and `CLAUDE.md` intentionally, not preserve accidental generated blocks as repository architecture.

## Target Repository Layout

```text
/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── LICENSE
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── vertical-plugins/
│   │   └── legal-fr/
│   └── agent-plugins/
│       ├── revue-conformite-interne/
│       ├── analyse-contrats-fournisseurs/
│       ├── chronologie-contentieux/
│       ├── jurisprudence-multilingue/
│       ├── revue-contrats-travail/
│       ├── red-flags-bail/
│       ├── note-information-amf/
│       ├── tabular-due-diligence/
│       └── recherche-juridique-fr-avancee/
├── scripts/
│   ├── generate_legal_fr_scaffold.py
│   ├── run_legal_fr_evals.py
│   ├── check_legal_fr_connectors.py
│   ├── check_legal_fr_parallel_cli.py
│   ├── check_legal_fr_parallel_task_api.py
│   └── legal_fr_parallel_task.py
├── tests/
│   ├── test_legal_fr_scaffold.py
│   ├── test_legal_fr_production_grade.py
│   └── test_legal_fr_eval_fixtures.py
├── docs/
│   ├── architecture/
│   │   └── legal-fr-suite.md
│   ├── agents/
│   │   └── legal-fr-agents.md
│   ├── workflows/
│   │   └── legora-harvey-fr-workflows.md
│   └── superpowers/
│       ├── specs/
│       └── plans/
└── archive/
    └── financial-services-origin/
        ├── README.md
        ├── plugins/
        ├── managed-agent-cookbooks/
        ├── claude-for-msft-365-install/
        ├── scripts/
        ├── tests/
        └── ARCHIVE.md
```

## Archive Rules

Move Financial Services origin material into `archive/financial-services-origin/`:

- `plugins/vertical-plugins/financial-analysis`
- `plugins/vertical-plugins/investment-banking`
- `plugins/vertical-plugins/equity-research`
- `plugins/vertical-plugins/private-equity`
- `plugins/vertical-plugins/wealth-management`
- `plugins/vertical-plugins/fund-admin`
- `plugins/vertical-plugins/operations`
- `plugins/partner-built`
- all non-Legal-FR agent plugins
- `managed-agent-cookbooks`
- `claude-for-msft-365-install`
- Financial Services-specific scripts and tests
- original root README content as archive documentation

Keep active at root:

- Legal-FR vertical plugin.
- Legal-FR agent plugins.
- Legal-FR generator/check/eval scripts.
- Legal-FR tests.
- Legal-FR docs and superpowers specs/plans.
- `.claude-plugin/marketplace.json` trimmed to Legal-FR only.

## Marketplace Scope

The active `.claude-plugin/marketplace.json` must only register:

- `legal-fr`
- `revue-conformite-interne`
- `analyse-contrats-fournisseurs`
- `chronologie-contentieux`
- `jurisprudence-multilingue`
- `revue-contrats-travail`
- `red-flags-bail`
- `note-information-amf`
- `tabular-due-diligence`
- `recherche-juridique-fr-avancee`

The archived Financial Services marketplace may be kept inside the archive for reference, but active validation should ignore archived plugin manifests.

## Root Documentation

### README.md

Replace the Financial Services README with a Legal-FR suite README covering:

- repository purpose;
- active architecture;
- plugin catalogue;
- agent catalogue;
- MCP connectors: OpenLegi, Exa;
- Parallel CLI local layer;
- Parallel Task API second layer;
- validation commands;
- archive location.

### AGENTS.md

Create a root Legal-FR `AGENTS.md` with:

- production-grade legal assistant posture;
- French law scope;
- OpenLegi-first sourcing;
- Exa/Parallel use boundaries;
- human validation gates;
- no secret leakage;
- no `legacy anonymization MCP`;
- development workflow and verification commands.

### CLAUDE.md

Create a root Legal-FR `CLAUDE.md` with:

- concise runtime instructions for Claude/Cowork/Codex;
- Legal-FR quality gates;
- source/citation rules;
- Parallel CLI and Task API rules;
- archive boundaries.

## Active Scripts

Keep or create only Legal-FR active scripts at root:

- `scripts/generate_legal_fr_scaffold.py`
- `scripts/run_legal_fr_evals.py`
- `scripts/check_legal_fr_connectors.py`
- `scripts/check_legal_fr_parallel_cli.py`
- `scripts/check_legal_fr_parallel_task_api.py`
- `scripts/legal_fr_parallel_task.py`

Financial Services scripts move to the archive.

## Active Tests

Keep only:

- `tests/test_legal_fr_scaffold.py`
- `tests/test_legal_fr_production_grade.py`
- `tests/test_legal_fr_eval_fixtures.py`

Update path-based tests as needed so archived manifests are not treated as active plugin manifests.

## Legal-FR Documentation

Add focused docs:

- `docs/architecture/legal-fr-suite.md`: repository architecture, generation model, active/archive boundaries.
- `docs/agents/legal-fr-agents.md`: one page listing the nine agents, their skills, commands, and intended users.
- `docs/workflows/legora-harvey-fr-workflows.md`: mapping of Legora/Harvey-inspired workflows to French legal production use.

These docs should be concise and operational, not marketing copy.

## Validation Commands

Required deterministic checks after implementation:

```bash
python scripts/check.py
python -m unittest tests.test_legal_fr_scaffold tests.test_legal_fr_production_grade tests.test_legal_fr_eval_fixtures -v
python scripts/run_legal_fr_evals.py
python scripts/check_legal_fr_connectors.py
python scripts/check_legal_fr_parallel_task_api.py
```

Conditional environment check:

```bash
python scripts/check_legal_fr_parallel_cli.py
```

Acceptable local failure if `parallel-cli` is not installed:

```text
ERROR: parallel-cli is not installed or not on PATH
```

## Acceptance Criteria

- Active repository root presents as Legal-FR, not Financial Services.
- Original Financial Services content exists under `archive/financial-services-origin/`.
- Active marketplace lists only Legal-FR plugins.
- `scripts/check.py` succeeds on active plugins and does not fail on archived content.
- Legal-FR tests pass.
- Legal-FR eval runner reports 45 expected outputs checked.
- Root `README.md`, `AGENTS.md`, and `CLAUDE.md` are Legal-FR-specific and intentional.
- No active artifact requires `legacy anonymization MCP`.
- No active artifact hardcodes `OPENLEGI_TOKEN assignment` or `PARALLEL_API_KEY assignment`.
- Git status is clean except for intentionally ignored local GitNexus index data.

## Implementation Notes

Use an isolated worktree because the current main workspace contains local generated instruction files. Move files with git-aware operations where possible so history remains readable. Do not delete user-local generated files from the main workspace during the design/plan phase.
