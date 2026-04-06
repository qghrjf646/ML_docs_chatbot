# Corpus Documents Folder

This folder now contains a populated open-source corpus from arXiv.

Current structure:

- `arxiv/pdfs/`: 55 downloaded paper PDFs.
- `arxiv/metadata/`: one JSON metadata file per document.
- `arxiv/abstracts/`: one Markdown abstract document per paper.
- `arxiv/arxiv_index.json`: global index and fetch manifest.

Why both PDF and metadata:

- Metadata is used to build the knowledge graph (authors, categories, publication info).
- Abstract text and document snippets are used for retrieval and grounding.
- PDF paths are kept for traceability and future full-text extraction.

Fetch script:

- `scripts/ingest/fetch_arxiv_corpus.py`

