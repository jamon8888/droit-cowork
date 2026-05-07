# Audit Legal-FR

Every production-grade Legal-FR workflow emits an `audit_trail` record for each material finding.

Required audit fields:
- `DRAFT - Validation professionnelle requise`
- `validated_by_human`
- `confidence`
- `source_status`
- `audit_trail`

The audit trail links extracted text, legal sources, reviewer identity, confidence scoring and human validation status. Outputs remain drafts until `validated_by_human` is true.
