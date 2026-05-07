---
name: workflow-playbooks
description: Execution des playbooks workflow V2 avec identifiants stables, reprises stage-by-stage, gates et livrables.
---

# workflow-playbooks

## Purpose

Execution des playbooks workflow V2 avec identifiants stables, reprises stage-by-stage, gates et livrables.

## Workflow

1. Lire l'etat `workflow-run` et le playbook V2 avant d'agir.
2. Ne jamais avancer un workflow sans schema, audit trail, source-ledger et review-queue coherents.
3. Appliquer les quality gates avant chaque transition de stage.
4. Maintenir `DRAFT - Validation professionnelle requise` dans tout livrable.
5. Retourner les blocages au lieu de produire une synthese externe lorsque la validation humaine ou les sources manquent.

## Specialization

- Lire uniquement des playbooks `schema_version: 2.0.0`.
- Verifier les identifiants stables: `playbook_id`, `intake_id`, `document_id`, `source_rule_id`, `assignment_id`, `step_id`, `rule_id`, `quality_gate_id`, `deliverable_id`.
- Executer stage-by-stage par defaut; un full-run exige un argument explicite `--full`.
- Stopper sur intake incomplet, source officielle introuvable, confidence basse, schema invalide, gate echoue ou validation humaine rejetee.

## Output Contract

- JSON stable pour etat machine.
- Markdown uniquement comme vue lisible derivee du JSON.
- `audit_trail`, `source_status`, `confidence`, `quality_gate_id` et `validated_by_human` visibles dans les sorties de controle.
