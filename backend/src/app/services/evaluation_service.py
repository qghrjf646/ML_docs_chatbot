from __future__ import annotations

from dataclasses import dataclass
from statistics import quantiles

from app.domain.models import EvaluationSummaryPayload
from app.services.text_processing import jaccard_similarity, tokenize


@dataclass
class InteractionTrace:
    question: str
    answer: str
    matched_documents: int
    latency_ms: float


class EvaluationService:
    def __init__(self) -> None:
        self._traces: list[InteractionTrace] = []

    def record(self, question: str, answer: str, matched_documents: int, latency_ms: float) -> None:
        self._traces.append(
            InteractionTrace(
                question=question,
                answer=answer,
                matched_documents=matched_documents,
                latency_ms=latency_ms,
            )
        )

    def summary(self) -> EvaluationSummaryPayload:
        if not self._traces:
            return EvaluationSummaryPayload(
                retrieval_recall_at_k=0.0,
                answer_faithfulness=0.0,
                answer_relevance=0.0,
                citation_precision=0.0,
                latency_p95_ms=0.0,
                total_interactions=0,
                status="cold_start",
            )

        total = len(self._traces)
        retrieval_recall = sum(1 for t in self._traces if t.matched_documents > 0) / total

        relevance_scores: list[float] = []
        faithfulness_scores: list[float] = []
        citation_scores: list[float] = []
        latencies = [t.latency_ms for t in self._traces]

        for trace in self._traces:
            q_tokens = set(tokenize(trace.question))
            a_tokens = set(tokenize(trace.answer))
            relevance_scores.append(jaccard_similarity(q_tokens, a_tokens))

            if a_tokens:
                citation_scores.append(1.0 if "citation" in trace.answer.lower() else 0.0)
            else:
                citation_scores.append(0.0)

            if trace.matched_documents <= 0:
                faithfulness_scores.append(0.0)
            else:
                faithfulness_scores.append(min(1.0, 0.5 + (0.1 * trace.matched_documents)))

        if len(latencies) == 1:
            p95 = latencies[0]
        else:
            p95 = quantiles(latencies, n=100)[94]

        return EvaluationSummaryPayload(
            retrieval_recall_at_k=round(retrieval_recall, 4),
            answer_faithfulness=round(sum(faithfulness_scores) / total, 4),
            answer_relevance=round(sum(relevance_scores) / total, 4),
            citation_precision=round(sum(citation_scores) / total, 4),
            latency_p95_ms=round(float(p95), 2),
            total_interactions=total,
            status="active",
        )
