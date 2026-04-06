from __future__ import annotations

from app.services.evaluation_service import EvaluationService


def test_evaluation_summary_cold_start() -> None:
    service = EvaluationService()
    summary = service.summary()

    assert summary.status == "cold_start"
    assert summary.total_interactions == 0
    assert summary.retrieval_recall_at_k == 0.0


def test_evaluation_summary_updates_with_interactions() -> None:
    service = EvaluationService()
    service.record(
        question="what is graph rag",
        answer="Graph RAG uses retrieval. Citations: 2601.00001v1",
        matched_documents=3,
        latency_ms=110.0,
    )
    service.record(
        question="how to calibrate confidence",
        answer="Need additional context. Citations: none",
        matched_documents=1,
        latency_ms=240.0,
    )

    summary = service.summary()
    assert summary.status == "active"
    assert summary.total_interactions == 2
    assert summary.retrieval_recall_at_k > 0.0
    assert summary.latency_p95_ms >= 110.0
