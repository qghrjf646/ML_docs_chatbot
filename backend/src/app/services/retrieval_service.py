from __future__ import annotations

from app.domain.models import DocumentMatch
from app.infrastructure.neo4j_repository import Neo4jRepository
from app.services.arxiv_loader import ArxivCorpusLoader
from app.services.text_processing import (
    cosine_similarity,
    hash_embedding,
    jaccard_similarity,
    tokenize,
)


class RetrievalService:
    def __init__(
        self,
        repository: Neo4jRepository,
        loader: ArxivCorpusLoader,
        embedding_dim: int,
    ) -> None:
        self.repository = repository
        self.loader = loader
        self.embedding_dim = embedding_dim

    def retrieve(self, question: str, top_k: int) -> list[DocumentMatch]:
        try:
            docs = self.repository.fetch_documents(limit=500)
        except Exception:
            docs = []

        if not docs:
            docs = self._fallback_documents()

        q_tokens = set(tokenize(question))
        q_vec = hash_embedding(question, dim=self.embedding_dim)
        max_degree = max((doc.get("graph_degree", 0) for doc in docs), default=1)
        if max_degree <= 0:
            max_degree = 1

        scored: list[DocumentMatch] = []
        for doc in docs:
            text_parts = [doc.get("title", ""), doc.get("summary", "")]
            chunks = doc.get("chunks", [])
            chunk_text = " ".join(chunk.get("text", "") for chunk in chunks)
            text_parts.append(chunk_text)

            doc_text = " ".join(part for part in text_parts if part)
            d_tokens = set(tokenize(doc_text))
            lexical = jaccard_similarity(q_tokens, d_tokens)

            embedding = doc.get("topology_embedding") or doc.get("base_embedding") or []
            semantic = cosine_similarity(q_vec, embedding) if embedding else 0.0
            centrality = float(doc.get("graph_degree", 0)) / float(max_degree)

            score = (0.55 * lexical) + (0.35 * semantic) + (0.10 * centrality)
            if score <= 0:
                continue

            snippet = chunks[0].get("text", "") if chunks else doc.get("summary", "")
            snippet = snippet[:320]

            scored.append(
                DocumentMatch(
                    doc_id=doc.get("doc_id", ""),
                    arxiv_id=doc.get("arxiv_id", ""),
                    title=doc.get("title", ""),
                    score=round(score, 6),
                    published=doc.get("published", ""),
                    categories=doc.get("categories", []),
                    abs_url=doc.get("abs_url", ""),
                    pdf_url=doc.get("pdf_url", ""),
                    snippet=snippet,
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]

    def _fallback_documents(self) -> list[dict]:
        documents = self.loader.load_documents(max_docs=200)
        items: list[dict] = []
        for doc in documents:
            items.append(
                {
                    "doc_id": doc.doc_id,
                    "arxiv_id": doc.arxiv_id,
                    "title": doc.title,
                    "summary": doc.summary,
                    "published": doc.published,
                    "categories": doc.categories,
                    "abs_url": doc.abs_url,
                    "pdf_url": doc.pdf_url,
                    "chunks": [{"text": doc.summary}],
                    "graph_degree": 1,
                    "base_embedding": hash_embedding(doc.summary, self.embedding_dim),
                }
            )
        return items
