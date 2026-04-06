from __future__ import annotations

import numpy as np

from app.domain.models import ArxivDocument


class TopologyAwareEncoder:
    """Lightweight GraphSAGE-style message passing encoder.

    This is a deterministic, training-free encoder for POC usage.
    It produces topology-aware vectors by combining each document feature vector
    with neighborhood information in a graph built from shared metadata.
    """

    def __init__(self, dim: int, layers: int = 2) -> None:
        self.dim = dim
        self.layers = layers
        self._rng = np.random.default_rng(42)

    def build_adjacency(self, docs: list[ArxivDocument]) -> np.ndarray:
        n = len(docs)
        adj = np.zeros((n, n), dtype=np.float32)

        for i in range(n):
            adj[i, i] = 1.0

        for i in range(n):
            d1 = docs[i]
            a1 = set(d1.authors)
            c1 = set(d1.categories)
            for j in range(i + 1, n):
                d2 = docs[j]
                a2 = set(d2.authors)
                c2 = set(d2.categories)

                shared_authors = len(a1.intersection(a2))
                shared_categories = len(c1.intersection(c2))
                weight = 0.0
                if shared_authors:
                    weight += 1.25 * shared_authors
                if shared_categories:
                    weight += 0.75 * shared_categories

                if weight > 0:
                    adj[i, j] = weight
                    adj[j, i] = weight

        return adj

    def encode(
        self,
        docs: list[ArxivDocument],
        base_vectors: dict[str, list[float]],
    ) -> dict[str, list[float]]:
        if not docs:
            return {}

        x = np.array([base_vectors[d.doc_id] for d in docs], dtype=np.float32)
        if x.shape[1] != self.dim:
            raise ValueError("base vector dimension does not match encoder dim")

        adj = self.build_adjacency(docs)
        degree = np.sum(adj, axis=1)
        degree[degree == 0] = 1.0
        d_inv_sqrt = np.diag(np.power(degree, -0.5))
        a_norm = d_inv_sqrt @ adj @ d_inv_sqrt

        w_self = self._rng.normal(0.0, 0.2, size=(self.dim, self.dim)).astype(np.float32)
        w_neigh = self._rng.normal(0.0, 0.2, size=(self.dim, self.dim)).astype(np.float32)

        h = x
        for _ in range(self.layers):
            h = np.tanh((h @ w_self) + ((a_norm @ h) @ w_neigh))

        # L2 normalization for stable cosine search.
        norms = np.linalg.norm(h, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        h = h / norms

        return {docs[idx].doc_id: h[idx].tolist() for idx in range(len(docs))}
