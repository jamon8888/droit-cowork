---
name: openlegi-recherche
description: Recherche de codes, jurisprudence, conventions collectives et textes via OpenLegi MCP.
---

# openlegi-recherche

## Purpose

Recherche de codes, jurisprudence, conventions collectives et textes via OpenLegi MCP.

## Workflow

1. Identifier le contexte juridique, le type de document et la question traitee.
2. Produire des resultats structures avec sources, incertitudes et champs non trouves.
3. Pour toute extraction de corpus, retourner un JSON stable avant toute synthese narrative.
4. Pour toute affirmation de droit positif, verifier via OpenLegi ou signaler l'incertitude.
5. Conserver la mention `DRAFT - Validation professionnelle requise` pour les livrables externes.

## Cabinet-grade requirements

- Produire uniquement des livrables marques `DRAFT - Validation professionnelle requise` tant que `validated_by_human: false`.
- Exposer les incertitudes en francais clair avec la mention `A VERIFIER` lorsqu'une source, une date, une qualification ou une piece manque.
- Refuser toute conclusion definitive sans validation professionnelle et sans lien entre le finding, la source et le reviewer.
- Garder un `audit_trail` exploitable pour chaque finding: document, extrait, source juridique, controle effectue, horodatage et reviewer attendu.

## JSON discipline

- Structurer les extractions avec `source_status`, `confidence`, `validated_by_human: false` et `audit_trail`.
- Utiliser `source_status` pour distinguer `official`, `secondary`, `not_found` et `unverified`; ne jamais masquer une source introuvable.
- Encadrer `confidence` entre 0 et 1 et baisser le score lorsqu'une piece est illisible, absente ou contradictoire.
- Conserver un JSON valide et stable avant toute synthese narrative, avec champs non trouves explicitement renseignes.

## French legal sourcing

- Verifier les affirmations de droit positif avec une source officielle francaise ou europeenne, en priorite OpenLegi/Legifrance lorsque disponible.
- Citer les references utiles: code, article, juridiction, date, numero, ECLI ou source AMF selon le domaine.
- Marquer `A VERIFIER` et `source_status: unverified` si la source officielle n'est pas disponible dans le dossier ou via connecteur.
- Ne pas transformer une recherche web ou une source secondaire en conclusion juridique sans validation humaine.

## Installation et validation OpenLegi MCP

Source officielle:

- https://www.openlegi.fr/documentation/

Configuration Claude Desktop/Cowork recommandee via MCP remote:

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

Verifier la disponibilite sans consommer de quota MCP:

```bash
curl https://mcp.openlegi.fr/health
python scripts/check_legal_fr_connectors.py --online
```

Le health check doit retourner `status: ok` et `services.legifrance: true`.

Authentification et protocole:

- Utiliser `OPENLEGI_TOKEN` comme variable d'environnement utilisateur, jamais comme secret hardcode.
- La documentation OpenLegi accepte aussi le header `Authorization: Bearer <token>` pour les clients MCP avances.
- Le transport MCP utilise SSE; les clients HTTP bas niveau doivent envoyer `Accept: application/json, text/event-stream`.
- Ne pas traiter `https://mcp.openlegi.fr/legifrance/mcp` comme une API REST JSON simple; utiliser Claude Desktop, `mcp-remote@latest`, un SDK MCP ou un parser SSE.

## Output Contract

- Markdown pour les rapports et tableaux finaux.
- JSON pour les extractions intermediaires.
- `source`, `localisation`, `confiance` et `verification_humaine_requise` lorsque l'information est extraite d'un document.
