# House Price Prediction — End-to-End ML Web App

An end-to-end machine learning product that predicts Indian property prices from listing details. Raw data is cleaned and modeled in a Jupyter notebook, served through a FastAPI backend, and consumed by a React + TypeScript frontend.

**Note**: 

## Overview

The user fills in property details (location, carpet area, floor, furnishing, etc.) in a web form. The frontend sends this to a FastAPI backend, which runs it through a trained scikit-learn pipeline and returns a predicted price.

notebooks/   -> data cleaning, EDA, model training, exports house_price.pkl
backend/     -> FastAPI service that loads the model and serves /predict
frontend/    -> React form that calls the backend and displays the result

## Architecture



1. User submits the form on the frontend.
2. Frontend sends a JSON request to POST /predict.
3. Backend validates the request, builds a one-row DataFrame matching the model's training columns, and runs it through the pipeline.
4. Pipeline (bundled preprocessing + model) returns a predicted price.
5. Backend returns {"predicted_price": <float>}, frontend displays it.

## Tech stack

Layer         | 	Technology
Modeling      | 	Python, pandas, scikit-learn, Jupyter
Backend       |     FastAPI, Pydantic, Uvicorn
Frontend      | 	React, TypeScript, Vite, React Router
Model export  | 	joblib (pickled Pipeline)

## Project structure


## Dataset

House Price by Juhi Bhojani — https://www.kaggle.com/datasets/juhibhojani/house-price

Real property listings from India (~187K rows). The raw CSV is not committed to this repo, To get it:
`
pip install kaggle
kaggle datasets download -d juhibhojani/house-price -p notebooks/data --unzip
`

## Setup

1. Notebook (regenerates the model)

**The trained model file (house_price.pkl) is not committed to this repo — You must regenerate it by running the notebook once:**

`
cd notebooks
python -m venv .venv
.venv\Scripts\activate
pip install jupyter pandas numpy scikit-learn matplotlib seaborn joblib
jupyter notebook house_price_model.ipynb
`

Run all cells (Kernel -> Restart & Run All)

**This produces house_price.pkl and locations.json inside notebooks/. Copy both into place:**

`
copy house_price.pkl ..\backend\models\house_price.pkl
copy locations.json ..\backend\locations.json
copy locations.json ..\frontend\src\data\locations.json
`

2. Backend

`
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
`
Runs at http://localhost:8000. Interactive docs at http://localhost:8000/docs.

**Environment variables (backend/.env):**

Variable     |	Default                 |	Description
MODEL_PATH   |	models/house_price.pkl  |	Path to the pickled pipeline
CORS_ORIGINS |	http://localhost:5173   |    Allowed frontend origin(s), comma-separated

Run tests:
`
pytest
`

3. Frontend

bash
cd frontend
npm install
copy .env.example .env

npm run dev

Runs at http://localhost:5173.

Environment variables (frontend/.env):

Variable	Default	Description
VITE_API_BASE_URL	http://localhost:8000	Base URL of the backend API

4. Try it

With both servers running, open http://localhost:5173, fill in the form, and submit — you'll get a real predicted price from the trained model.

## API reference

`GET /health`
Liveness check:

curl http://localhost:8000/health

{"status": "ok"}

``POST /predict``

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "carpet_area_sqft": 1200,
    "floor_num": 3,
    "bathroom": 2,
    "balcony": 1,
    "location_grouped": "thane",
    "Furnishing": "Semi-Furnished",
    "Transaction": "Resale",
    "Ownership": "Freehold",
    "facing": "East"
  }'

{"predicted_price": 16424062.5}

Invalid input (e.g. an unrecognized Furnishing value) returns 422 with validation details.

## Model

Two models were trained and compared on a held-out test set (20% split):

Model                     |    	MAE (₹)	    |    RMSE (₹)  |  	  R²
Linear Regression         |    4,540,134	  |   8,459,519	 |     0.617
Random Forest (200 trees) |	   1,021,595	  |   5,391,627	 |     0.844

Random Forest was selected as the final model — it captures non-linear relationships between features (location, area, furnishing) that a linear model misses, roughly quadrupling R² and cutting MAE by more than 4x.

Features used: carpet_area_sqft, floor_num, bathroom, balcony (numeric), location_grouped, Furnishing, Transaction, Ownership, facing (categorical). All preprocessing (imputation, scaling, one-hot encoding) is bundled inside the exported Pipeline, so the backend needs no manual encoding logic.

## Screenshots

https://github.com/ser855/house-price-prediction/blob/main/screenshot_%231_predicted_price.png

https://github.com/ser855/house-price-prediction/blob/main/screenshot_%232_parameters.png


Notes
- scikit-learn version is pinned in backend/requirements.txt to match the version the notebook was run with — a pickle trained on one version can fail to load on another.

- The model is loaded once at backend startup, not on every request
