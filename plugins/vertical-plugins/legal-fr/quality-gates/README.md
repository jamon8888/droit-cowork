# Quality Gates Legal-FR

Legal-FR quality gates block final delivery when source verification, confidence scoring or professional validation is incomplete.

Required quality signals:
- `DRAFT - Validation professionnelle requise`
- `validated_by_human`
- `confidence`
- `source_status`
- `audit_trail`

Quality gates must preserve the draft notice, review `source_status`, inspect every `confidence` value and require human validation before any external reliance.
