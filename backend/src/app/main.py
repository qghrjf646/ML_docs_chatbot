from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.routes.evaluation import router as evaluation_router
from app.api.routes.ingestion import router as ingestion_router
from app.core.config import settings
from app.core.dependencies import get_repository


app = FastAPI(
    title="Graph RAG Chatbot API",
    version="0.1.0",
    description="Graph RAG API with Neo4j ingestion, retrieval, and Hugging Face generation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1")
app.include_router(evaluation_router, prefix="/api/v1")
app.include_router(ingestion_router, prefix="/api/v1")


@app.get("/health")
def health() -> dict:
    repository = get_repository()
    graph_ok = repository.ping()
    graph_counts = {}
    if graph_ok:
        try:
            graph_counts = repository.graph_stats()
        except Exception:
            graph_counts = {}

    return {
        "status": "ok",
        "mode": "runtime",
        "environment": settings.app_env,
        "neo4j_uri": settings.neo4j_uri,
        "hf_model_id": settings.hf_model_id,
        "neo4j_available": graph_ok,
        "graph_counts": graph_counts,
    }
