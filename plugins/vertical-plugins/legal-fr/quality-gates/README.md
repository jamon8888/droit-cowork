# Quality Gates Legal-FR

Legal-FR quality gates are cabinet policy checks applied manually by the `legal-qa-reviewer` and workflow instructions until automated enforcement is added through tests, eval scripts or prompt-level gates.

Required quality signals:
- `DRAFT - Validation professionnelle requise`
- `validated_by_human`
- `confidence`
- `source_status`
- `audit_trail`

The manual gate requires reviewers to preserve the draft notice, review `source_status`, inspect every `confidence` value and require human validation before any external reliance.
