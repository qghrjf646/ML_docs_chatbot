from fastapi import APIRouter, Depends

from app.core.dependencies import get_evaluation_service
from app.domain.models import EvaluationSummaryPayload
from app.services.evaluation_service import EvaluationService


router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.get("/summary", response_model=EvaluationSummaryPayload)
def get_evaluation_summary(
    evaluation_service: EvaluationService = Depends(get_evaluation_service),
) -> EvaluationSummaryPayload:
    return evaluation_service.summary()
