from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.dependencies import (
    get_chat_service,
    get_evaluation_service,
    get_ingestion_service,
)
from app.domain.models import DocumentMatch, EvaluationSummaryPayload, IngestionReport
from app.main import app


class ChatServiceStub:
    def ask(self, question: str):
        answer = f"answer for: {question}\n\nCitations: 2604.00001v1"
        matches = [
            DocumentMatch(
                doc_id="arxiv:2604.00001v1",
                arxiv_id="2604.00001v1",
                title="Example paper",
                score=0.88,
                published="2026-04-01",
                categories=["cs.AI"],
                abs_url="https://arxiv.org/abs/2604.00001v1",
                pdf_url="https://arxiv.org/pdf/2604.00001v1.pdf",
                snippet="example snippet",
            )
        ]
        return answer, matches, "hf_text_generation", 123.4


class EvalServiceStub:
    def summary(self) -> EvaluationSummaryPayload:
        return EvaluationSummaryPayload(
            retrieval_recall_at_k=1.0,
            answer_faithfulness=0.9,
            answer_relevance=0.85,
            citation_precision=1.0,
            latency_p95_ms=210.0,
            total_interactions=12,
            status="active",
        )


class IngestionServiceStub:
    def ingest_arxiv(self, max_docs: int | None = None) -> IngestionReport:
        requested = max_docs or 50
        return IngestionReport(
            requested=requested,
            ingested_documents=requested,
            generated_chunks=requested * 2,
            topology_embeddings=requested,
            status="ok",
            message="stub ingestion complete",
        )


def _client() -> TestClient:
    app.dependency_overrides[get_chat_service] = lambda: ChatServiceStub()
    app.dependency_overrides[get_evaluation_service] = lambda: EvalServiceStub()
    app.dependency_overrides[get_ingestion_service] = lambda: IngestionServiceStub()
    return TestClient(app)


def test_chat_endpoint_returns_documents() -> None:
    client = _client()
    response = client.post("/api/v1/chat", json={"question": "what is graph rag"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["matched_documents"]
    assert payload["retrieval_mode"] == "graph_rag_hybrid"


def test_ingestion_endpoint_accepts_limit() -> None:
    client = _client()
    response = client.post("/api/v1/ingestion/arxiv?max_docs=55")
    assert response.status_code == 200
    payload = response.json()
    assert payload["ingested_documents"] == 55


def test_evaluation_summary_endpoint() -> None:
    client = _client()
    response = client.get("/api/v1/evaluation/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "active"
    assert payload["retrieval_recall_at_k"] == 1.0
