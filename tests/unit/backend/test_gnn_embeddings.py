from __future__ import annotations

import numpy as np

from app.domain.models import ArxivDocument
from app.services.gnn_embeddings import TopologyAwareEncoder


def _doc(arxiv_id: str, authors: list[str], categories: list[str]) -> ArxivDocument:
    return ArxivDocument(
        arxiv_id=arxiv_id,
        title=f"Title {arxiv_id}",
        summary=f"Summary {arxiv_id}",
        published="2026-01-01T00:00:00Z",
        updated="2026-01-01T00:00:00Z",
        authors=authors,
        categories=categories,
        primary_category=categories[0],
        pdf_url=f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        abs_url=f"https://arxiv.org/abs/{arxiv_id}",
    )


def test_adjacency_uses_shared_metadata() -> None:
    encoder = TopologyAwareEncoder(dim=8)
    docs = [
        _doc("1", ["Alice"], ["cs.AI"]),
        _doc("2", ["Alice"], ["cs.LG"]),
        _doc("3", ["Charlie"], ["math.ST"]),
    ]
    adj = encoder.build_adjacency(docs)

    assert adj.shape == (3, 3)
    assert adj[0, 1] > 0
    assert adj[0, 2] == 0


def test_encoder_returns_normalized_vectors() -> None:
    encoder = TopologyAwareEncoder(dim=8)
    docs = [
        _doc("1", ["A"], ["cs.AI"]),
        _doc("2", ["B"], ["cs.AI"]),
    ]
    base = {
        docs[0].doc_id: [1.0, 0, 0, 0, 0, 0, 0, 0],
        docs[1].doc_id: [0, 1.0, 0, 0, 0, 0, 0, 0],
    }

    out = encoder.encode(docs, base)
    assert len(out) == 2
    for vec in out.values():
        norm = np.linalg.norm(np.array(vec, dtype=np.float32))
        assert np.isclose(norm, 1.0, atol=1e-5)
