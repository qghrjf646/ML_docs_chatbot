# 11 - Unit Test Catalog

## Backend critical units

- Chunking engine
  - empty files
  - tiny files
  - overlap boundary behavior
  - multilingual and malformed text

- Graph mapping
  - duplicate entities
  - orphan chunks
  - cyclic entity relations
  - idempotent upsert behavior

- Retrieval ranking
  - tie scores
  - missing embedding vector
  - conflicting graph proximity and semantic similarity
  - deterministic ordering under equal weights

- Prompt and citation composer
  - max token budget truncation
  - missing evidence fallback
  - invalid metadata sanitization

## Frontend critical units

- Tab navigation state.
- Evidence list rendering from empty and large payloads.
- Metric card formatting for null and outlier values.
- Error and loading indicators.
