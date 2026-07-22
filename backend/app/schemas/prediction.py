"""
schemas/prediction.py

Request/response schema for the house price prediction API.
Field names match the exact columns the model was trained on
(see notebook cell 26: numeric_features + categorical_features).

Categorical values and numeric bounds below were confirmed directly
from the notebook's df[col].unique() and df[...].describe() outputs
on the cleaned training data (not guessed).
"""

from typing import Literal

from pydantic import BaseModel, Field

# --- confirmed categorical values ---
FurnishingType = Literal["Furnished", "Semi-Furnished", "Unfurnished"]
TransactionType = Literal["New Property", "Other", "Rent/Lease", "Resale"]
OwnershipType = Literal["Co-operative Society", "Freehold", "Leasehold", "Power Of Attorney"]
FacingType = Literal[
    "East", "North", "North - East", "North - West",
    "South", "South - East", "South -West", "West",
]
LocationType = Literal[
    "agra", "ahmedabad", "aurangabad", "badlapur", "bangalore", "bhiwadi",
    "bhubaneswar", "chandigarh", "chennai", "coimbatore", "dehradun",
    "faridabad", "ghaziabad", "goa", "greater-noida", "guntur", "gurgaon",
    "guwahati", "hyderabad", "jaipur", "jamshedpur", "kalyan", "kanpur",
    "kochi", "kolkata", "lucknow", "mangalore", "mohali", "mumbai",
    "nagpur", "nashik", "navi-mumbai", "new-delhi", "noida", "other",
    "palghar", "panchkula", "patna", "pune", "raipur", "ranchi",
    "siliguri", "sonipat", "surat", "thane", "thrissur", "vadodara",
    "varanasi", "vijayawada", "visakhapatnam", "zirakpur",
]


class PredictionRequest(BaseModel):
    # --- numeric_features ---
    # Bounds taken from df.describe() on the cleaned training data:
    #   carpet_area_sqft: min 5, max 40000 (typical range ~855-1576, 25th-75th pct)
    #   floor_num: min -1 (basement), max 200 (typical range 2-6)
    #   bathroom: min 1, max 10 (typical range 2-3)
    #   balcony: min 1, max 10 (typical range 1-2)
    carpet_area_sqft: float = Field(..., gt=0, le=40000, description="Carpet area in square feet")
    floor_num: int = Field(..., ge=-1, le=200, description="0 = Ground floor, -1 = Basement")
    bathroom: int = Field(..., ge=0, le=10)
    balcony: int = Field(..., ge=0, le=10)

    # --- categorical_features ---
    location_grouped: LocationType
    Furnishing: FurnishingType
    Transaction: TransactionType
    Ownership: OwnershipType
    facing: FacingType


class PredictionResponse(BaseModel):
    predicted_price: float
