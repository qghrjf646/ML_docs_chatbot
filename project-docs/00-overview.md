# 00 - Project Overview

## Mission

Build a professional Graph RAG chatbot that:

- uses Neo4j to model document knowledge as a graph,
- uses Hugging Face Inference Client with Gemma 4 31B as the LLM,
- returns both answers and matched source documents,
- exposes measurable quality and reliability via evaluation dashboards.

## Scope of This Phase

This phase delivers:

- arXiv corpus population (55 docs + metadata + PDFs),
- Neo4j ingestion and graph population baseline,
- hybrid retrieval + HF generation integration,
- topology-aware embedding baseline,
- documentation-first engineering artifacts.

This phase provides a functional baseline and remains a POC (not production hardened).

## Non-Functional Targets (Future Implementation)

- Reliability: resilient retrieval and graceful degradation.
- Explainability: explicit evidence links for every answer.
- Testability: high unit coverage and BDD scenario traceability.
- Observability: latency, quality, and error telemetry.
