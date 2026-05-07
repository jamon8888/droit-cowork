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

Marketplace catalog and project registration live in `.claude-plugin/marketplace.json` and `.claude/settings.json`.

Original Financial Services assets live in `archive/financial-services-origin/` and should not be treated as active plugin surface.
