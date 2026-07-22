"""
services/inference.py

Loads the exported scikit-learn Pipeline (house_price.pkl) and runs
predictions. The model is meant to be loaded ONCE at app startup
(see main.py lifespan), not on every request.
"""

import logging
from pathlib import Path

import joblib
import pandas as pd

logger = logging.getLogger(__name__)


class PredictionService:
    def __init__(self, model_path: str):
        self._model_path = model_path
        self._model = None

    def load(self) -> None:
        path = Path(self._model_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Model file not found at '{path}'. "
                "Copy house_price.pkl from your notebook into backend/models/."
            )
        logger.info("Loading model from %s", path)
        self._model = joblib.load(path)
        logger.info("Model loaded successfully")

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def predict(self, df: pd.DataFrame) -> float:
        if self._model is None:
            raise RuntimeError("Model is not loaded yet. Call load() first.")
        prediction = self._model.predict(df)
        return float(prediction[0])

