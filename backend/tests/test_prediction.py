"""
tests/test_prediction.py

Run with:  pytest

Requires models/house_price.pkl to be present (copied from your notebook).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

VALID_PAYLOAD = {
    "carpet_area_sqft": 1200,
    "floor_num": 3,
    "bathroom": 2,
    "balcony": 1,
    "location_grouped": "thane",
    "Furnishing": "Semi-Furnished",
    "Transaction": "Resale",
    "Ownership": "Freehold",
    "facing": "East",
}


@pytest.fixture(scope="module")
def client():
    # Using TestClient as a context manager is required so that the
    # FastAPI lifespan (which loads the model into app.state) actually runs.
    # A plain `TestClient(app)` assignment skips startup/shutdown events.
    with TestClient(app) as c:
        yield c


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_happy_path(client):
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert "predicted_price" in body
    assert isinstance(body["predicted_price"], float)
    assert body["predicted_price"] > 0


def test_predict_invalid_input_rejected(client):
    bad_payload = dict(VALID_PAYLOAD)
    bad_payload["Furnishing"] = "Not A Real Value"  # not in the allowed Literal
    response = client.post("/predict", json=bad_payload)
    assert response.status_code == 422


def test_predict_missing_field_rejected(client):
    bad_payload = dict(VALID_PAYLOAD)
    del bad_payload["carpet_area_sqft"]
    response = client.post("/predict", json=bad_payload)
    assert response.status_code == 422
