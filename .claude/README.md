# Claude Project Settings

This directory contains project-scope Claude Code settings for the Legal-FR marketplace.

## Marketplace Target

The official marketplace catalog is:

- `.claude-plugin/marketplace.json`

The project settings register that catalog from GitHub:

- `jamon8888/droit-cowork`

After this repository is pushed, users can add the marketplace manually with:

```bash
claude plugin marketplace add jamon8888/droit-cowork
```

or from inside Claude Code:

```text
/plugin marketplace add jamon8888/droit-cowork
```

`.claude/settings.json` also enables the Legal-FR vertical and all Legal-FR agent plugins by default for project users who trust the repository.

## Notes

- Do not put secrets in `.claude/settings.json`.
- Keep API keys such as `OPENLEGI_TOKEN` and `PARALLEL_API_KEY` in the local environment.
- Keep marketplace plugin sources relative to the repository root.
