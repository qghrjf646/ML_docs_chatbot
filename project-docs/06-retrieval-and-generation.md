# 06 - Retrieval and Generation Strategy (Implemented Baseline)

## Retrieval implementation

Current retrieval is a hybrid scorer over ingested graph documents:

1. Lexical score: Jaccard overlap between question tokens and document text tokens.
2. Semantic score: cosine similarity between question hash embedding and document topology embedding.
3. Graph signal: normalized document graph degree.

Final score:

$$
score = 0.55 \cdot lexical + 0.35 \cdot semantic + 0.10 \cdot centrality
$$

Top-k matched documents are returned with snippet, arXiv IDs, category metadata, and source links.

## Generation implementation

- Uses Hugging Face `InferenceClient` with target model `google/gemma-4-31b-it`.
- Prompt includes strict grounding instruction and context snippets from matched documents.
- Expected answer includes explicit citations.
- If HF token/model call is unavailable, deterministic fallback response is returned with matched references.

## API output

- `answer`
- `matched_documents[]`
- `retrieval_mode`
- `model_status`
- `latency_ms`

