
from fastapi import APIRouter, HTTPException
from backend.transport.schemas.request import PredictionRequest
from backend.transport.services.prediction_service import run_prediction_service



router = APIRouter()



@router.post("/predict")
async def predict(request: PredictionRequest):
    try:
        
        result = await run_prediction_service(request.user)

        
        return result

    except ValueError as e:
        
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
       
        raise HTTPException(status_code=500, detail=str(e))