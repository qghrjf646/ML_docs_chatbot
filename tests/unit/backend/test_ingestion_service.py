from __future__ import annotations

from app.domain.models import ArxivDocument
from app.services.ingestion_service import IngestionService


class RepoCaptureStub:
    def __init__(self) -> None:
        self.schema_called = False
        self.upserts: list[tuple[str, int]] = []
        self.embedding_rows = 0

    def ensure_schema(self) -> None:
        self.schema_called = True

    def upsert_document(self, doc, chunks, base_embedding) -> None:
        _ = base_embedding
        self.upserts.append((doc.doc_id, len(chunks)))

    def set_topology_embeddings(self, embeddings: dict[str, list[float]]) -> int:
        self.embedding_rows = len(embeddings)
        return self.embedding_rows


class LoaderCaptureStub:
    def __init__(self, docs: list[ArxivDocument]) -> None:
        self.docs = docs

    def load_documents(self, max_docs: int | None = None) -> list[ArxivDocument]:
        if max_docs is None:
            return self.docs
        return self.docs[:max_docs]

    def load_abstract_text(self, arxiv_id: str) -> str:
        return f"Abstract for {arxiv_id}"


def _doc(arxiv_id: str) -> ArxivDocument:
    return ArxivDocument(
        arxiv_id=arxiv_id,
        title=f"Title {arxiv_id}",
        summary="summary text",
        published="2026-01-01T00:00:00Z",
        updated="2026-01-01T00:00:00Z",
        authors=["A", "B"],
        categories=["cs.AI", "cs.LG"],
        primary_category="cs.AI",
        pdf_url=f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        abs_url=f"https://arxiv.org/abs/{arxiv_id}",
    )


def test_ingestion_service_generates_report() -> None:
    docs = [_doc("1"), _doc("2")]
    repo = RepoCaptureStub()
    loader = LoaderCaptureStub(docs)
    service = IngestionService(repository=repo, loader=loader, embedding_dim=16)

    report = service.ingest_arxiv()

    assert repo.schema_called is True
    assert report.ingested_documents == 2
    assert report.topology_embeddings == 2
    assert report.generated_chunks >= 2
    assert len(repo.upserts) == 2
