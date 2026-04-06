# 13 - Evaluation Framework

## Evaluation dimensions

1. Retrieval quality
2. Generation quality
3. End-to-end user experience

## Retrieval metrics

- Recall@K
- MRR
- nDCG
- evidence hit rate

## Generation metrics

- Faithfulness (grounding to evidence)
- Relevance to question
- Completeness against reference answer
- Citation precision and citation recall

## End-to-end metrics

- Latency p50 and p95
- failure rate
- timeout rate

## Methods

- Offline benchmark datasets in `tests/data/evaluation_sets/`
- Scenario-driven BDD validation
- Periodic regression snapshots to detect quality drift

## Frontend tab mapping

- Overview: rollup scorecards
- Retrieval: rank and evidence metrics
- Generation: faithfulness and relevance scores
- End-to-End: latency and reliability trends
