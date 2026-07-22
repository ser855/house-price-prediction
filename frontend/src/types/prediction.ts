// Types mirroring the backend's PredictionRequest / PredictionResponse schema
// (backend/app/schemas/prediction.py)

export type Furnishing = "Furnished" | "Semi-Furnished" | "Unfurnished";

export type Transaction = "New Property" | "Other" | "Rent/Lease" | "Resale";

export type Ownership =
  | "Co-operative Society"
  | "Freehold"
  | "Leasehold"
  | "Power Of Attorney";

export type Facing =
  | "East"
  | "North"
  | "North - East"
  | "North - West"
  | "South"
  | "South - East"
  | "South -West"
  | "West";

export interface PredictionRequest {
  carpet_area_sqft: number;
  floor_num: number;
  bathroom: number;
  balcony: number;
  location_grouped: string;
  Furnishing: Furnishing;
  Transaction: Transaction;
  Ownership: Ownership;
  facing: Facing;
}

export interface PredictionResponse {
  predicted_price: number;
}