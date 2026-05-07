---
name: source-ledger
description: Registre de sources pour tracer source officielle, secondaire, web, not_found, extrait, outil et confiance.
---

# source-ledger

## Purpose

Registre de sources pour tracer source officielle, secondaire, web, not_found, extrait, outil et confiance.

## Workflow

1. Lire l'etat `workflow-run` et le playbook V2 avant d'agir.
2. Ne jamais avancer un workflow sans schema, audit trail, source-ledger et review-queue coherents.
3. Appliquer les quality gates avant chaque transition de stage.
4. Maintenir `DRAFT - Validation professionnelle requise` dans tout livrable.
5. Retourner les blocages au lieu de produire une synthese externe lorsque la validation humaine ou les sources manquent.

## Specialization

- Maintenir une ligne par source exploitee ou manquante.
- Distinguer `official`, `secondary`, `web`, `unverified` et `not_found`.
- Conserver extrait, outil utilise, date de verification, confiance et finding lie.
- Bloquer les conclusions critiques quand aucune source officielle disponible n'est documentee.

## Output Contract

- JSON stable pour etat machine.
- Markdown uniquement comme vue lisible derivee du JSON.
- `audit_trail`, `source_status`, `confidence`, `quality_gate_id` et `validated_by_human` visibles dans les sorties de controle.
