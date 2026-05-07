# Connecteurs Legal-FR

## Exa MCP

Endpoint: `https://mcp.exa.ai/mcp`.

## OpenLegi MCP

Documentation officielle: https://www.openlegi.fr/documentation/.

Configuration MCP remote officielle pour Claude Desktop/Cowork:

```json
{
  "mcpServers": {
    "openlegi": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://mcp.openlegi.fr/legifrance/mcp?token=${OPENLEGI_TOKEN}"
      ]
    }
  }
}
```

OpenLegi donne acces aux codes, jurisprudences, conventions collectives, JORF, LODA, RNE et EUR-Lex selon les outils disponibles.

Ne jamais hardcoder `OPENLEGI_TOKEN`. La documentation OpenLegi decrit aussi le header `Authorization: Bearer <token>` pour les clients MCP avances. Le transport MCP utilise SSE; les clients HTTP bas niveau doivent envoyer `Accept: application/json, text/event-stream` et parser la reponse SSE au lieu d'appeler `response.json()` directement.

## Verification locale

Le script de verification est local/offline par defaut: il lit uniquement `plugins/vertical-plugins/legal-fr/.mcp.json` et ne contacte ni Exa ni OpenLegi.

Commande:

```bash
python scripts/check_legal_fr_connectors.py
```

Verification online OpenLegi, sans token et sans consommer de quota MCP:

```bash
curl https://mcp.openlegi.fr/health
python scripts/check_legal_fr_connectors.py --online
```

Le health check doit retourner `status: ok` et `services.legifrance: true`.

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

Documentation officielle: https://docs.parallel.ai/integrations/cli.

Installation recommandee pour un outil agent disponible dans le PATH:

```bash
pipx install "parallel-web-tools[cli]" && pipx ensurepath
```

Alternatives supportees:

```bash
uv tool install "parallel-web-tools[cli]"
npm install -g parallel-web-cli
```

Authentification:

```bash
parallel-cli login --device
parallel-cli auth --json
```

`PARALLEL_API_KEY` peut remplacer le login local pour les executions non interactives. Ne jamais stocker sa valeur dans le repo.

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
