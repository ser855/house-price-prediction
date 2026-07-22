// api/predictionClient.ts
// Wraps the fetch call to the backend's /predict endpoint.

import type { PredictionRequest, PredictionResponse } from "../types/prediction";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getPrediction(
  payload: PredictionRequest
): Promise<PredictionResponse> {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    // FastAPI's validation errors (422) come back with a `detail` field
    const errorBody = await response.json().catch(() => null);
    const message =
      errorBody?.detail?.[0]?.msg ??
      errorBody?.detail ??
      `Request failed with status ${response.status}`;
    throw new Error(typeof message === "string" ? message : "Prediction request failed");
  }

  return response.json();
}