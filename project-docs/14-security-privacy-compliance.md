# 14 - Security, Privacy, Compliance

## Security baseline

- Store credentials in environment variables and secret managers.
- Avoid logging sensitive document content in plain text.
- Enforce strict API input validation.

## Privacy controls

- Track document origin and access scope metadata.
- Support redaction rules during ingestion.
- Define retention and deletion policies.

## LLM usage controls

- Restrict outbound payloads to required evidence only.
- Add prompt guardrails to limit data leakage.
- Record model request metadata without storing sensitive prompts.

## Compliance readiness (future)

- Audit trail for ingestion and query processing.
- Reproducible benchmark and decision logs.
