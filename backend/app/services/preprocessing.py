"""
services/preprocessing.py

Turns a validated PredictionRequest into a one-row pandas DataFrame with
exactly the column names + order the model's pipeline was trained on
(see notebook cell 26: numeric_features + categorical_features).

No manual encoding happens here — the exported pipeline (house_price.pkl)
already bundles imputation, scaling, and one-hot encoding internally.
This function's only job is to match column names exactly.
"""

import pandas as pd

from app.schemas.prediction import PredictionRequest

# Must match notebook cell 26 exactly, in this exact order
NUMERIC_FEATURES = ["carpet_area_sqft", "floor_num", "bathroom", "balcony"]
CATEGORICAL_FEATURES = ["location_grouped", "Furnishing", "Transaction", "Ownership", "facing"]
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def request_to_dataframe(request: PredictionRequest) -> pd.DataFrame:
    """Build the one-row input DataFrame the pipeline expects."""
    row = {
        "carpet_area_sqft": request.carpet_area_sqft,
        "floor_num": request.floor_num,
        "bathroom": request.bathroom,
        "balcony": request.balcony,
        "location_grouped": request.location_grouped,
        "Furnishing": request.Furnishing,
        "Transaction": request.Transaction,
        "Ownership": request.Ownership,
        "facing": request.facing,
    }
    df = pd.DataFrame([row])
    # Enforce exact column order the pipeline was trained on
    return df[ALL_FEATURES]
