# ADR 0004 - Topology-Aware Embeddings with GNN

## Status

Proposed

## Decision

Introduce GNN-derived embeddings to complement text embeddings for graph-aware retrieval quality.

## Rationale

- Captures neighborhood and relation structure beyond text-only semantics.
- Expected to improve cross-document retrieval where relationships matter.

## Risks

- Increased complexity in training and inference pipelines.
- Requires robust benchmark evidence before default activation.
