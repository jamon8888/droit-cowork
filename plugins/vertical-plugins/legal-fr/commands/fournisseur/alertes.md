---
description: Lister echeances, renouvellements et alertes contractuelles.
argument-hint: "[entree] [options]"
allowed-tools: Read, Write, Glob, Task
---

# fournisseur:alertes

## Cabinet-grade workflow

Workflow cible: `analyse-contrats-fournisseurs`.

Skill runtime obligatoire: `legal-fr-runtime`.

Schemas requis:
- `plugins/vertical-plugins/legal-fr/schemas/common/document-intake.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/source-citation.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/risk-score.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/finding.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/audit-trail.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/common/human-validation.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/workflows/analyse-contrats-fournisseurs/extraction.schema.json`
- `plugins/vertical-plugins/legal-fr/schemas/workflows/analyse-contrats-fournisseurs/report.schema.json`

1. Classer l'entree, le domaine juridique, le profil utilisateur et le livrable attendu avant toute analyse.
2. Extraire les faits et termes dans le schema JSON du workflow, avec `confidence`, `source_status` et champs non trouves.
3. Construire un audit trail reliant chaque finding au document, a l'extrait source, a la verification juridique et au reviewer.
4. Appliquer un quality gate: sources citees, scores de risque, coherence du schema, incertitudes visibles et validation humaine requise.
5. Produire uniquement un livrable marque `DRAFT - Validation professionnelle requise` tant que `validated_by_human` n'est pas vrai.
