from __future__ import annotations

from app.domain.models import ChunkPayload, IngestionReport
from app.infrastructure.neo4j_repository import Neo4jRepository
from app.services.arxiv_loader import ArxivCorpusLoader
from app.services.gnn_embeddings import TopologyAwareEncoder
from app.services.text_processing import hash_embedding, split_into_chunks


class IngestionService:
    def __init__(
        self,
        repository: Neo4jRepository,
        loader: ArxivCorpusLoader,
        embedding_dim: int,
    ) -> None:
        self.repository = repository
        self.loader = loader
        self.embedding_dim = embedding_dim
        self.encoder = TopologyAwareEncoder(dim=embedding_dim, layers=2)

    def ingest_arxiv(self, max_docs: int | None = None) -> IngestionReport:
        documents = self.loader.load_documents(max_docs=max_docs)
        if not documents:
            return IngestionReport(
                requested=max_docs or 0,
                ingested_documents=0,
                generated_chunks=0,
                topology_embeddings=0,
                status="empty",
                message="No metadata files found in corpus.",
            )

        self.repository.ensure_schema()

        total_chunks = 0
        base_vectors: dict[str, list[float]] = {}
        for doc in documents:
            abstract_markdown = self.loader.load_abstract_text(doc.arxiv_id)
            source_text = f"{doc.title}\n\n{doc.summary}\n\n{abstract_markdown}".strip()

            chunk_texts = split_into_chunks(source_text, chunk_size=120, overlap=20)
            if not chunk_texts:
                chunk_texts = [source_text]

            chunks = [
                ChunkPayload(
                    chunk_id=f"{doc.doc_id}:chunk:{idx}",
                    text=text,
                    position=idx,
                    token_count=len(text.split()),
                )
                for idx, text in enumerate(chunk_texts)
            ]

            base_vector = hash_embedding(source_text, dim=self.embedding_dim)
            base_vectors[doc.doc_id] = base_vector

            self.repository.upsert_document(doc, chunks, base_vector)
            total_chunks += len(chunks)

        topology = self.encoder.encode(documents, base_vectors)
        topo_count = self.repository.set_topology_embeddings(topology)

        return IngestionReport(
            requested=max_docs or len(documents),
            ingested_documents=len(documents),
            generated_chunks=total_chunks,
            topology_embeddings=topo_count,
            status="ok",
            message="ArXiv corpus ingested into Neo4j with topology-aware embeddings.",
        )
