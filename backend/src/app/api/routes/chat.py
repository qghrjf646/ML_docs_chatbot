from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_chat_service
from app.domain.models import DocumentMatch
from app.services.chat_service import ChatService


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")


class ChatResponse(BaseModel):
    answer: str
    matched_documents: list[DocumentMatch]
    retrieval_mode: str
    model_status: str
    latency_ms: float


@router.post("", response_model=ChatResponse)
def ask_chatbot(
    payload: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    answer, matches, model_status, latency_ms = chat_service.ask(payload.question)
    return ChatResponse(
        answer=answer,
        matched_documents=matches,
        retrieval_mode="graph_rag_hybrid",
        model_status=model_status,
        latency_ms=round(latency_ms, 2),
    )
