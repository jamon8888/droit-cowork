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
