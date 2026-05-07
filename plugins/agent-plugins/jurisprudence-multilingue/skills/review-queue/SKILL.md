---
name: review-queue
description: File de validation humaine pour bloquer, corriger, rejeter ou approuver les findings et livrables juridiques.
---

# review-queue

## Purpose

File de validation humaine pour bloquer, corriger, rejeter ou approuver les findings et livrables juridiques.

## Workflow

1. Lire l'etat `workflow-run` et le playbook V2 avant d'agir.
2. Ne jamais avancer un workflow sans schema, audit trail, source-ledger et review-queue coherents.
3. Appliquer les quality gates avant chaque transition de stage.
4. Maintenir `DRAFT - Validation professionnelle requise` dans tout livrable.
5. Retourner les blocages au lieu de produire une synthese externe lorsque la validation humaine ou les sources manquent.

## Specialization

- Creer une entree pour chaque gate echoue, source manquante, confidence basse, document illisible ou decision humaine attendue.
- Distinguer `open`, `blocked`, `validated` et `rejected`.
- Interdire l'export valide tant que des items bloquants restent ouverts.
- Renvoyer les rejets humains vers l'etape de remediation concernee.

## Output Contract

- JSON stable pour etat machine.
- Markdown uniquement comme vue lisible derivee du JSON.
- `audit_trail`, `source_status`, `confidence`, `quality_gate_id` et `validated_by_human` visibles dans les sorties de controle.
