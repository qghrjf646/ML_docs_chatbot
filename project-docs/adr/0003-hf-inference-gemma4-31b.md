# ADR 0003 - Hugging Face Inference Client with Gemma 4 31B

## Status

Accepted

## Decision

Use Hugging Face Inference Client as the LLM integration path with Gemma 4 31B as the target model.

## Rationale

- Managed inference endpoint reduces operational burden.
- Flexible model management and integration options.

## Consequences

- Requires API token and external network availability.
- Latency and cost must be monitored and benchmarked.
