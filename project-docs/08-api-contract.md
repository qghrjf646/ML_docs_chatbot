# 08 - API Contract

## Base path

- `/api/v1`

## Chat endpoint

- `POST /chat`
- Request:
  - `question: string`
- Response:
  - `answer: string`
  - `matched_documents: DocumentMatch[]`
  - `retrieval_mode: string`
  - `model_status: string`
  - `latency_ms: number`

## Evaluation endpoint

- `GET /evaluation/summary`
- Response:
  - `retrieval_recall_at_k: number`
  - `answer_faithfulness: number`
  - `answer_relevance: number`
  - `citation_precision: number`
  - `latency_p95_ms: number`
  - `total_interactions: number`
  - `status: string`

## Ingestion endpoint

- `POST /ingestion/arxiv?max_docs=<int>`
- Response:
  - `requested`
  - `ingested_documents`
  - `generated_chunks`
  - `topology_embeddings`
  - `status`
  - `message`

