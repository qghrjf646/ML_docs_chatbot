from __future__ import annotations

from app.domain.models import ArxivDocument
from app.services.retrieval_service import RetrievalService


class RepoStub:
    def __init__(self, docs: list[dict], should_fail: bool = False) -> None:
        self.docs = docs
        self.should_fail = should_fail

    def fetch_documents(self, limit: int = 500) -> list[dict]:
        _ = limit
        if self.should_fail:
            raise RuntimeError("neo4j unavailable")
        return self.docs


class LoaderStub:
    def __init__(self, docs: list[ArxivDocument]) -> None:
        self.docs = docs

    def load_documents(self, max_docs: int | None = None) -> list[ArxivDocument]:
        if max_docs is None:
            return self.docs
        return self.docs[:max_docs]


def _metadata(arxiv_id: str, title: str, summary: str) -> ArxivDocument:
    return ArxivDocument(
        arxiv_id=arxiv_id,
        title=title,
        summary=summary,
        published="2026-01-01T00:00:00Z",
        updated="2026-01-01T00:00:00Z",
        authors=["Alice"],
        categories=["cs.AI"],
        primary_category="cs.AI",
        pdf_url=f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        abs_url=f"https://arxiv.org/abs/{arxiv_id}",
    )


def test_retrieval_ranks_relevant_document_first() -> None:
    docs = [
        {
            "doc_id": "arxiv:1",
            "arxiv_id": "1",
            "title": "Graph retrieval with embeddings",
            "summary": "Hybrid retrieval for graph rag systems",
            "published": "2026",
            "categories": ["cs.AI"],
            "abs_url": "a",
            "pdf_url": "p",
            "chunks": [{"text": "graph retrieval and embedding ranking"}],
            "graph_degree": 5,
            "topology_embedding": [1.0, 0.0, 0.0, 0.0],
        },
        {
            "doc_id": "arxiv:2",
            "arxiv_id": "2",
            "title": "Medical imaging",
            "summary": "radiology segmentation",
            "published": "2026",
            "categories": ["eess.IV"],
            "abs_url": "a2",
            "pdf_url": "p2",
            "chunks": [{"text": "ct scan model"}],
            "graph_degree": 1,
            "topology_embedding": [0.0, 1.0, 0.0, 0.0],
        },
    ]

    service = RetrievalService(
        repository=RepoStub(docs),
        loader=LoaderStub([]),
        embedding_dim=4,
    )

    matches = service.retrieve("graph retrieval ranking", top_k=2)
    assert matches
    assert matches[0].arxiv_id == "1"


def test_retrieval_uses_loader_fallback_when_repo_fails() -> None:
    loader_docs = [_metadata("1111.00001v1", "Language model confidence", "confidence calibration")]
    service = RetrievalService(
        repository=RepoStub([], should_fail=True),
        loader=LoaderStub(loader_docs),
        embedding_dim=8,
    )

    matches = service.retrieve("confidence", top_k=3)
    assert len(matches) == 1
    assert matches[0].arxiv_id == "1111.00001v1"
