# E2E Runbook (Skeleton)

## Goal

Validate that end users receive accurate, grounded answers with explicit evidence and transparent quality metrics.

## Planned tooling

- Playwright for UI-driven E2E tests.
- API-level checks for deterministic setup and teardown.

## Validation workflow

1. Prepare controlled corpus in `tests/data/synthetic_corpus/`.
2. Run ingestion pipeline to populate graph.
3. Execute chatbot scenarios and collect traces.
4. Assert answer grounding and citation validity.
5. Assert metric availability in evaluation UI tabs.
