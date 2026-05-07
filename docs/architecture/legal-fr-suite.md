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
