from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_ingestion_service
from app.domain.models import IngestionReport
from app.services.ingestion_service import IngestionService


router = APIRouter(prefix="/ingestion", tags=["ingestion"])


@router.post("/arxiv", response_model=IngestionReport)
def ingest_arxiv_corpus(
    max_docs: int | None = Query(default=None, ge=1, le=500),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
) -> IngestionReport:
    return ingestion_service.ingest_arxiv(max_docs=max_docs)
