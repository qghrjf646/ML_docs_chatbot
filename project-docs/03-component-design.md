# 03 - Component Design

## Backend modules (target)

- API layer: request validation and response formatting.
- Ingestion service: parsing, chunking, entity extraction, graph writes.
- Retrieval service: hybrid graph traversal + embedding search.
- Generation service: prompt composition and LLM call.
- Evaluation service: benchmark execution and metric aggregation.
- Infrastructure adapters: Neo4j, Hugging Face, persistence.

## Frontend modules (target)

- Chat panel: question input and answer rendering.
- Matched docs panel: evidence list with provenance metadata.
- Evaluation panel: metric tabs and trend cards.
- Diagnostics panel (future): trace IDs, debug metadata.

## Component principles

- Strict boundaries between domain, application, and infrastructure.
- Explicit contracts with typed schemas.
- Pure business logic where possible for easy unit testing.
