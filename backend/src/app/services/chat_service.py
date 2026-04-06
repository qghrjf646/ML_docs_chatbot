from __future__ import annotations

import time

from app.domain.models import DocumentMatch
from app.services.evaluation_service import EvaluationService
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService


class ChatService:
    def __init__(
        self,
        retrieval: RetrievalService,
        llm: LLMService,
        evaluation: EvaluationService,
        top_k: int,
    ) -> None:
        self.retrieval = retrieval
        self.llm = llm
        self.evaluation = evaluation
        self.top_k = top_k

    def ask(self, question: str) -> tuple[str, list[DocumentMatch], str, float]:
        started_at = time.perf_counter()

        matches = self.retrieval.retrieve(question, top_k=self.top_k)
        answer, model_status = self.llm.generate_answer(question, matches)

        latency_ms = (time.perf_counter() - started_at) * 1000.0
        self.evaluation.record(
            question=question,
            answer=answer,
            matched_documents=len(matches),
            latency_ms=latency_ms,
        )
        return answer, matches, model_status, latency_ms
