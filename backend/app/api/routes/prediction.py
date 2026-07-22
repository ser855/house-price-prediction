"""
api/routes/prediction.py

GET  /health   -> simple liveness check
POST /predict  -> run the model on a validated request
"""

from fastapi import APIRouter, HTTPException, Request

from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.preprocessing import request_to_dataframe

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest, http_request: Request) -> PredictionResponse:
    service = http_request.app.state.prediction_service

    if not service.is_loaded:
        # Should never happen in practice since the model loads at startup,
        # but fail loudly and clearly if it somehow does.
        raise HTTPException(status_code=503, detail="Model is not loaded")

    df = request_to_dataframe(request)

    try:
        predicted_price = service.predict(df)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    return PredictionResponse(predicted_price=predicted_price)
