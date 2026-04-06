# 02 - System Context

## External dependencies

- Neo4j service (internal container).
- Hugging Face Inference API (external managed service).
- Source documents manually provided in `docs/`.

## Internal boundaries

- Frontend: presentation and interaction only.
- Backend API: orchestration, retrieval, generation, evaluation.
- Graph store: knowledge model and graph traversal.
- Evaluation subsystem: score computation and trend tracking.

## Interface contracts

- Frontend to backend: REST endpoints.
- Backend to Neo4j: Cypher and graph driver.
- Backend to Hugging Face: inference client request/response contract.

## Operational assumptions

- Internet access is required for Hugging Face inference.
- Neo4j credentials are managed through environment variables.
- Corpus quality directly impacts retrieval quality.
