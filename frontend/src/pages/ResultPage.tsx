import { useLocation, Link } from "react-router-dom";

function formatIndianCurrency(amount: number): string {
  if (amount >= 1e7) {
    return `₹${(amount / 1e7).toFixed(2)} Cr`;
  }
  if (amount >= 1e5) {
    return `₹${(amount / 1e5).toFixed(2)} Lac`;
  }
  return `₹${amount.toLocaleString("en-IN")}`;
}

export default function ResultPage() {
  const location = useLocation();
  const predictedPrice = location.state?.predictedPrice as number | undefined;

  if (predictedPrice === undefined) {
    return (
      <div className="page">
        <div className="card result-page">
          <p>No prediction found. Please submit the form first.</p>
          <Link to="/">Back to form</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="card result-page">
        <h1>Predicted Price</h1>
        <p className="predicted-amount">{formatIndianCurrency(predictedPrice)}</p>
        <p className="predicted-exact">
          ({predictedPrice.toLocaleString("en-IN")} exact)
        </p>
        <Link to="/">Predict another</Link>
      </div>
    </div>
  );
}