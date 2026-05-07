# Legal-FR eval rubric: revue-contrats-travail

## Required sections

The answer must include workflow, draft_notice, findings, audit_trail and human_validation.

## Case coverage

- `case-001`: `compliant` risk `low`
- `case-002`: `blocking_red_flag` risk `high`
- `case-003`: `legal_uncertainty` risk `medium`
- `case-004`: `unreadable_or_incomplete` risk `unknown`
- `case-005`: `source_not_found` risk `medium`

## Source and confidence checks

Each finding must include source_citation.source_status and risk_score.confidence. The source status must distinguish official, unverified and not_found cases.

## Human validation gate

Every case remains `DRAFT - Validation professionnelle requise`, with validated_by_human false and validation_required true.

## Audit trail requirements

Each top-level audit_trail item and each finding.audit_trail must link finding_id, workflow, document_id, legal_source, reviewer, confidence and human_validation.
