import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPrediction } from "../api/predictionClient";
import type {
  PredictionRequest,
  Furnishing,
  Transaction,
  Ownership,
  Facing,
} from "../types/prediction";
import locations from "../data/locations.json";

const FURNISHING_OPTIONS: Furnishing[] = ["Furnished", "Semi-Furnished", "Unfurnished"];
const TRANSACTION_OPTIONS: Transaction[] = ["New Property", "Other", "Rent/Lease", "Resale"];
const OWNERSHIP_OPTIONS: Ownership[] = [
  "Co-operative Society",
  "Freehold",
  "Leasehold",
  "Power Of Attorney",
];
const FACING_OPTIONS: Facing[] = [
  "East", "North", "North - East", "North - West",
  "South", "South - East", "South -West", "West",
];

export default function PredictionForm() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    carpet_area_sqft: "",
    floor_num: "",
    bathroom: "",
    balcony: "",
    location_grouped: locations[0] ?? "",
    Furnishing: FURNISHING_OPTIONS[0],
    Transaction: TRANSACTION_OPTIONS[0],
    Ownership: OWNERSHIP_OPTIONS[0],
    facing: FACING_OPTIONS[0],
  });

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    const area = Number(formData.carpet_area_sqft);
    if (!area || area <= 0) {
      setError("Carpet area must be a number greater than 0.");
      return;
    }

    const payload: PredictionRequest = {
      carpet_area_sqft: area,
      floor_num: Number(formData.floor_num) || 0,
      bathroom: Number(formData.bathroom) || 0,
      balcony: Number(formData.balcony) || 0,
      location_grouped: formData.location_grouped,
      Furnishing: formData.Furnishing,
      Transaction: formData.Transaction,
      Ownership: formData.Ownership,
      facing: formData.facing,
    };

    setLoading(true);
    try {
      const result = await getPrediction(payload);
      navigate("/result", { state: { predictedPrice: result.predicted_price } });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="card">
        <h1>House Price Prediction</h1>
        <form onSubmit={handleSubmit} className="form-grid">
          <label className="field">
            Location
            <select
              name="location_grouped"
              value={formData.location_grouped}
              onChange={handleChange}
            >
              {locations.map((loc: string) => (
                <option key={loc} value={loc}>
                  {loc}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            Carpet area (sqft)
            <input
              type="number"
              name="carpet_area_sqft"
              value={formData.carpet_area_sqft}
              onChange={handleChange}
              min="1"
              required
            />
          </label>

          <label className="field">
            Floor number
            <input
              type="number"
              name="floor_num"
              value={formData.floor_num}
              onChange={handleChange}
              required
            />
          </label>

          <label className="field">
            Bathrooms
            <input
              type="number"
              name="bathroom"
              value={formData.bathroom}
              onChange={handleChange}
              min="0"
              required
            />
          </label>

          <label className="field">
            Balconies
            <input
              type="number"
              name="balcony"
              value={formData.balcony}
              onChange={handleChange}
              min="0"
              required
            />
          </label>

          <label className="field">
            Furnishing
            <select name="Furnishing" value={formData.Furnishing} onChange={handleChange}>
              {FURNISHING_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            Transaction
            <select name="Transaction" value={formData.Transaction} onChange={handleChange}>
              {TRANSACTION_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            Ownership
            <select name="Ownership" value={formData.Ownership} onChange={handleChange}>
              {OWNERSHIP_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            Facing
            <select name="facing" value={formData.facing} onChange={handleChange}>
              {FACING_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          {error && <p className="error-message">{error}</p>}

          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? "Predicting..." : "Predict price"}
          </button>
        </form>
      </div>
    </div>
  );
}