# 05 - Ingestion Pipeline (Implemented Baseline)

## Input corpus

- `docs/arxiv/metadata/*.json`
- `docs/arxiv/abstracts/*.md`
- `docs/arxiv/pdfs/*.pdf` (traceability, not yet parsed in runtime pipeline)

## Fetch stage

Script: `scripts/ingest/fetch_arxiv_corpus.py`

- Queries arXiv API.
- Downloads at least 50 records.
- Stores one JSON metadata file per paper.
- Stores one abstract markdown file per paper.
- Downloads PDF files for each record.

## Graph ingestion stage

Endpoint: `POST /api/v1/ingestion/arxiv`

1. Load metadata JSON records.
2. Build document text from title + summary + abstract markdown.
3. Chunk text with overlap.
4. Upsert nodes and relationships in Neo4j.
5. Compute base embeddings from text.
6. Compute topology-aware embeddings via GraphSAGE-style propagation.
7. Persist embeddings on `Document` nodes.

## Idempotency and updates

- Document merge key: `doc_id` (`arxiv:<id>`).
- Chunk sets are refreshed per document on reingestion.
- Author and category nodes use merge semantics.

