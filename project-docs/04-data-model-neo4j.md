# 04 - Neo4j Data Model (ArXiv Corpus)

## Node types (implemented)

- `Document`: one arXiv paper.
- `Chunk`: chunked text blocks from title/summary/abstract markdown.
- `Author`: normalized author name.
- `Category`: arXiv category code (for example `cs.LG`, `cs.CL`).
- `Source`: source registry node (`arxiv`).

## Relationship types (implemented)

- `(:Document)-[:HAS_CHUNK]->(:Chunk)`
- `(:Chunk)-[:NEXT]->(:Chunk)`
- `(:Document)-[:AUTHORED_BY]->(:Author)`
- `(:Document)-[:IN_CATEGORY]->(:Category)`
- `(:Document)-[:FROM_SOURCE]->(:Source)`

## Key properties

- Document:
	- `doc_id` (`arxiv:<id>`)
	- `arxiv_id`, `title`, `summary`
	- `published`, `updated`
	- `primary_category`, `categories[]`
	- `abs_url`, `pdf_url`, `doi`, `journal_ref`, `comment`
	- `base_embedding[]`, `topology_embedding[]`
- Chunk:
	- `chunk_id`, `text`, `position`, `token_count`
- Author:
	- `name`
- Category:
	- `code`

## Constraints

- Unique on `Document.doc_id`
- Unique on `Chunk.chunk_id`
- Unique on `Author.name`
- Unique on `Category.code`
- Unique on `Source.source_id`

## Topology-aware embedding model

- Initial document vectors: hashed text embeddings from document content.
- Graph edges for message passing: shared authors and shared categories.
- Encoder: deterministic GraphSAGE-style message passing over metadata graph.
- Output stored on each document as `topology_embedding[]`.

