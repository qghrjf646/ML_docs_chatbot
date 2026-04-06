# 07 - Topology-Aware Embeddings with GNN

## Implemented baseline

The current system implements a lightweight GraphSAGE-style message passing encoder:

- Graph nodes: `Document`
- Edges weighted by shared authors and shared categories
- Initial features: normalized hash embeddings from document text
- Propagation layers: 2
- Activation: `tanh`
- Output: L2-normalized document embeddings stored in Neo4j

## Message passing formulation

At each layer $l$:

$$
H^{(l+1)} = tanh\left(H^{(l)}W_{self} + \hat{A}H^{(l)}W_{neigh}\right)
$$

where $\hat{A}$ is normalized adjacency from metadata-based graph links.

## Current role in retrieval

- Used as semantic component in hybrid retrieval scoring.
- Improves cross-document context transfer when lexical overlap is weak.

## Next improvements

- Supervised/contrastive training objective.
- Heterogeneous node support beyond document-level graph.
- Periodic embedding quality benchmarks.

