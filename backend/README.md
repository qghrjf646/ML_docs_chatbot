# Backend

Python FastAPI backend skeleton for Graph RAG orchestration.

Current state:

- ArXiv metadata ingestion into Neo4j.
- Chunk generation and graph upsert.
- Topology-aware embedding generation via GraphSAGE-style message passing.
- Hybrid retrieval (lexical + embedding + graph centrality).
- Hugging Face generation path with robust fallback mode.
- Runtime evaluation metrics endpoint.

Planned modules:

- `api/`: HTTP routes.
- `services/`: ingestion, retrieval, generation, evaluation orchestration.
- `infrastructure/`: Neo4j, Hugging Face, and storage adapters.
- `domain/`: entities and value objects.
- `core/`: settings and shared utilities.
