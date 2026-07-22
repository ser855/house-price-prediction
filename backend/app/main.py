"""
main.py

FastAPI app entrypoint.

Run locally with:
    uvicorn app.main:app --reload

Then open http://localhost:8000/docs to test /predict interactively.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.prediction import router as prediction_router
from app.core.config import settings
from app.services.inference import PredictionService
from app.utils.logging_config import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load the model ONCE, not on every request
    configure_logging()
    service = PredictionService(model_path=settings.model_path)
    service.load()
    app.state.prediction_service = service

    yield

    # Shutdown: nothing to clean up for now


app = FastAPI(title="House Price Prediction API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)
