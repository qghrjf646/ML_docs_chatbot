from __future__ import annotations

from pydantic import BaseModel, Field


class ChunkPayload(BaseModel):
    chunk_id: str
    text: str
    position: int
    token_count: int


class ArxivDocument(BaseModel):
    arxiv_id: str
    title: str
    summary: str
    published: str
    updated: str
    authors: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    primary_category: str = ""
    pdf_url: str
    abs_url: str
    doi: str | None = None
    journal_ref: str | None = None
    comment: str | None = None

    @property
    def doc_id(self) -> str:
        return f"arxiv:{self.arxiv_id}"


class DocumentMatch(BaseModel):
    doc_id: str
    arxiv_id: str
    title: str
    score: float
    published: str
    categories: list[str]
    abs_url: str
    pdf_url: str
    snippet: str


class IngestionReport(BaseModel):
    requested: int
    ingested_documents: int
    generated_chunks: int
    topology_embeddings: int
    status: str
    message: str


class EvaluationSummaryPayload(BaseModel):
    retrieval_recall_at_k: float
    answer_faithfulness: float
    answer_relevance: float
    citation_precision: float
    latency_p95_ms: float
    total_interactions: int
    status: str
