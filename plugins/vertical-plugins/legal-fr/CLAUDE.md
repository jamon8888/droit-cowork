# Legal-FR Repository Notes

This file is a repository-readable mirror. Claude plugin runtime does not load plugin-root `CLAUDE.md`; production rules live in the `legal-fr-runtime` skill and in command/agent instructions.

## Required Output Posture

- Treat all external deliverables as drafts. Every report, memo, table, note, or client-facing artifact must include: `DRAFT - Validation professionnelle requise`.
- Human validation by a qualified legal professional is mandatory before client, regulator, counterparty, or other external use.
- Do not present a legal conclusion as final when source coverage, current-law status, document completeness, or interpretation remains uncertain.

## Source Order and Citations

- For French positive law, use OpenLegi before Exa.
- Use Exa for broader research, secondary materials, comparative checks, source discovery, and non-positive-law context.
- Cite an official source for every critical legal conclusion whenever an official source exists.
- If the governing rule, current-law position, or source status is uncertain, mark the point as `A VERIFIER`.
- No connector beyond OpenLegi and Exa is required for now.

## Recherche juridique FR avancee

- Utiliser OpenLegi avant Parallel pour toute question de droit positif francais.
- Utiliser Parallel CLI seulement avec `--json`.
- Ne jamais exposer `PARALLEL_API_KEY`.
- Classer chaque source: officielle, institutionnelle, doctrine, presse, inconnue.
- La couche Parallel Task API est une deuxieme couche backend; elle ne remplace pas le CLI pour Cowork local.
- Marquer `A VERIFIER` si une conclusion critique ne dispose pas de source officielle.

## Structured Extraction First

- Extract structured JSON before writing Markdown.
- Validate the JSON against the applicable Legal-FR schema where available.
- Use the JSON as the source of truth for the Markdown report, tables, findings, risk scores, citations, and validation metadata.
- Do not hide extraction gaps in prose. Surface missing documents, unreadable sections, incomplete citations, and uncertain legal bases.

## Audit Trail

Maintain an audit trail for every material finding:

- Source excerpt.
- Source status, such as official, unverified, secondary, or not_found.
- Confidence.
- Reviewer note for the human validator.

The audit trail must stay consistent with the finding, citation, risk score, and human validation fields.

## Quality Gates

Apply the Legal-FR quality gates before final output:

- Draft notice is present.
- Required schema fields are populated.
- Critical legal conclusions have cited sources.
- French positive-law research used OpenLegi before Exa.
- Uncertain or current-law-sensitive points are marked `A VERIFIER`.
- Source status and confidence are explicit.
- Audit trail entries exist for material findings.
- Human validation metadata states that validation is required and not yet completed unless a qualified reviewer has actually validated it.

If a gate fails, stop and return the blocking issues instead of producing a polished external deliverable.
