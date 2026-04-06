# ML_docs_chatbot

Proof of concept for a Graph RAG chatbot over a document collection, using Neo4j as the knowledge graph and a Hugging Face hosted LLM (Gemma 4 31B target model).

This repository now includes a functional baseline implementation.

## Current Scope

- Populate open-source corpus from arXiv (55 papers) with metadata and PDFs.
- Ingest metadata into Neo4j graph (Document, Chunk, Author, Category, Source).
- Compute topology-aware document embeddings with GraphSAGE-style propagation.
- Run hybrid retrieval and grounded answer generation.
- Return matched documents for each chatbot response.
- Expose evaluation metrics in API and frontend tabs.
- Include unit and e2e test suites.

## Repository Layout

- `docs/`: user-provided source documents for ingestion.
- `project-docs/`: architecture and engineering documentation.
- `backend/`: Python API skeleton (Graph RAG service layer placeholder).
- `frontend/`: React UI skeleton (chat + matched docs + evaluation tabs placeholders).
- `tests/`: unit and e2e test strategy, scenarios, and datasets skeleton.
- `scripts/`: placeholder entry points for ingestion and evaluation automation.

## Quick Start

1. Copy `.env.example` to `.env` and adjust secrets.
2. Run `docker compose up --build`.
3. Trigger ingestion once services are up:
	- `POST http://localhost:8000/api/v1/ingestion/arxiv?max_docs=55`
3. Access services:
	- Frontend: http://localhost:5173
	- Backend: http://localhost:8000/docs
	- Neo4j Browser: http://localhost:7474

## Important Notes

- Corpus content is in `docs/arxiv/` with JSON metadata, abstracts, and PDFs.
- For live LLM generation, set `HF_TOKEN` in `.env`.
- Without HF token, the backend switches to deterministic fallback answers while still returning matched documents.

## Network Troubleshooting

- Frontend API calls now use relative paths and Vite proxy, which avoids browser-side `localhost` resolution issues on remote environments.
- In GitHub Codespaces, use forwarded URLs without appending the port at the end if the hostname already includes it.
	- Correct style: `https://<workspace>-7474.app.github.dev/`
	- Incorrect style: `https://<workspace>-7474.app.github.dev:7474`
