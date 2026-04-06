# 17 - Open Questions

## Recently resolved

- Corpus source chosen: arXiv metadata + abstracts + PDFs.
- Graph schema adapted to concrete metadata fields (`Author`, `Category`, `Source`, `Document`, `Chunk`).
- Initial topology-aware embeddings implemented with GraphSAGE-style propagation.

## Graph modeling

- Which entity extraction method should be first (rules, LLM, hybrid)?
- Should we model section hierarchy as explicit nodes?

## Inference and cost

- What latency and cost targets are acceptable for Gemma 4 31B inference?
- Do we need fallback models for degraded mode?

## GNN scope

- Which objective gives best retrieval lift for this corpus?
- What retraining frequency is acceptable?

## Evaluation governance

- Who curates gold datasets and approves metric thresholds?
- How do we handle disagreements between automatic and human scores?
