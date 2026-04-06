# Ingestion Scripts

Planned responsibilities:

- Parse files from `docs/`
- chunk and enrich metadata
- create graph nodes and relationships in Neo4j
- trigger embedding generation and indexing

Implemented script:

- `fetch_arxiv_corpus.py`: fetches papers from arXiv and writes
	- `docs/arxiv/metadata/*.json`
	- `docs/arxiv/abstracts/*.md`
	- `docs/arxiv/pdfs/*.pdf`
	- `docs/arxiv/arxiv_index.json`
