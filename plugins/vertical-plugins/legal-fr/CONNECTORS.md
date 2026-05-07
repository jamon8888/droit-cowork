# Connecteurs Legal-FR

## Exa MCP

Endpoint: `https://mcp.exa.ai/mcp`.

## OpenLegi MCP

Configuration MCP remote: `https://mcp.openlegi.fr/legifrance/mcp?token=${OPENLEGI_TOKEN}`.

OpenLegi donne acces aux codes, jurisprudences, conventions collectives, JORF, LODA, RNE et EUR-Lex selon les outils disponibles.

## Verification locale

Le script de verification est local/offline: il lit uniquement `plugins/vertical-plugins/legal-fr/.mcp.json` et ne contacte ni Exa ni OpenLegi.

Commande:

```bash
python scripts/check_legal_fr_connectors.py
```

Si `OPENLEGI_TOKEN` n'est pas configure dans l'environnement, la verification de configuration peut quand meme reussir avec l'avertissement attendu:

```text
WARN: OPENLEGI_TOKEN is not set; runtime OpenLegi calls will fail until configured.
Legal-FR connector config OK
```

Quand `OPENLEGI_TOKEN` est configure et que les entrees MCP sont valides, la sortie attendue est:

```text
Legal-FR connector config OK
```

## Parallel Agent Skills

Installation recommandee: `npx skills add parallel-web/parallel-agent-skills --all --global`.

## Parallel CLI

Parallel CLI is the local/Cowork execution layer for advanced French legal research.

Install options:

```bash
pipx install "parallel-web-tools[cli]"
```

or:

```bash
npm install -g parallel-web-cli
```

Verification:

```bash
python scripts/check_legal_fr_parallel_cli.py
```

Expected when the CLI is installed and local auth or `PARALLEL_API_KEY` is available:

```text
Legal-FR Parallel CLI config OK
```

If `PARALLEL_API_KEY` is not set, local login or device flow may still work. The checker prints:

```text
WARN: PARALLEL_API_KEY is not set; parallel-cli must be authenticated by local login or device flow.
Legal-FR Parallel CLI config OK
```
