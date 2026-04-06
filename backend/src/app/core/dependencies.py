from __future__ import annotations

from functools import lru_cache

from app.core.config import settings
from app.infrastructure.neo4j_repository import Neo4jRepository
from app.services.arxiv_loader import ArxivCorpusLoader
from app.services.chat_service import ChatService
from app.services.evaluation_service import EvaluationService
from app.services.ingestion_service import IngestionService
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService


@lru_cache(maxsize=1)
def get_repository() -> Neo4jRepository:
    return Neo4jRepository(settings)


@lru_cache(maxsize=1)
def get_loader() -> ArxivCorpusLoader:
    return ArxivCorpusLoader(
        metadata_dir=settings.arxiv_metadata_dir,
        abstracts_dir=settings.arxiv_abstracts_dir,
    )


@lru_cache(maxsize=1)
def get_evaluation_service() -> EvaluationService:
    return EvaluationService()


@lru_cache(maxsize=1)
def get_ingestion_service() -> IngestionService:
    return IngestionService(
        repository=get_repository(),
        loader=get_loader(),
        embedding_dim=settings.embedding_dim,
    )


@lru_cache(maxsize=1)
def get_retrieval_service() -> RetrievalService:
    return RetrievalService(
        repository=get_repository(),
        loader=get_loader(),
        embedding_dim=settings.embedding_dim,
    )


@lru_cache(maxsize=1)
def get_llm_service() -> LLMService:
    return LLMService(model_id=settings.hf_model_id, token=settings.hf_token)


@lru_cache(maxsize=1)
def get_chat_service() -> ChatService:
    return ChatService(
        retrieval=get_retrieval_service(),
        llm=get_llm_service(),
        evaluation=get_evaluation_service(),
        top_k=settings.retrieval_top_k,
    )
