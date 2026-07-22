import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="page">
      <div className="card result-page">
        <h1>404 — Page not found</h1>
        <Link to="/">Back to home</Link>
      </div>
    </div>
  );
}