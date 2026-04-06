# 10 - Testing Strategy (TDD + BDD)

## TDD policy

- Write failing unit tests first for each service module.
- Implement minimal logic to pass tests.
- Refactor with coverage and mutation checks.

## BDD policy

- Capture user-visible behavior in Gherkin scenarios.
- Map each scenario to automated e2e checks.
- Keep scenarios tied to acceptance criteria.

## Quality gates (target)

- Unit coverage target: >= 90% lines and branches for critical modules.
- Mandatory tests for retrieval ranking and citation grounding.
- E2E smoke suite required on every main branch change.

## Test levels

- Unit: pure functions, adapters, serializers.
- Integration: Neo4j and inference adapter contracts.
- E2E: real user journeys through frontend and backend.
