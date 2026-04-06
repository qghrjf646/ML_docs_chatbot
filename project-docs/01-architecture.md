# 01 - High-Level Architecture

## Core building blocks

1. Document corpus in `docs/`.
2. Backend orchestration API (FastAPI functional baseline).
3. Neo4j graph database for entities, chunks, and relationships.
4. Embedding layer with topology-aware enrichment (GraphSAGE-style baseline).
5. LLM generation via Hugging Face Inference Client (Gemma 4 31B target).
6. React frontend with chat, evidence, and evaluation tabs.

## Runtime flow (target)

1. User question enters frontend chat.
2. Backend performs graph-aware retrieval over Neo4j and vector signals.
3. Candidate chunks and graph paths are ranked.
4. Prompt is assembled with grounded evidence.
5. Hugging Face inference is called for answer generation.
6. Backend returns answer + matched documents + metadata.
7. Frontend renders answer and evidence.

## Evaluation flow (target)

1. Benchmark questions are executed automatically.
2. Retrieval and generation metrics are computed.
3. Aggregates are persisted for dashboard visualization.
