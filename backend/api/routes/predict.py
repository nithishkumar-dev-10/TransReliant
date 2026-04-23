from fastapi import APIRouter, HTTPException
from backend.transport.schemas.request import PredictionRequest
from backend.transport.services.prediction_service import run_prediction_service

router = APIRouter()

@router.post("/predict")
async def predict(request: PredictionRequest):
    try:
        result = await run_prediction_service(request.ticket_input, request.delay_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))