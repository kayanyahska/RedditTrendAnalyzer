import React from 'react';

function RegressionCard({ regression }) {
  if (!regression || !regression.coef || !regression.features) return null;

  return (
    <div className="card">
      <h3>📈 Regression Analysis</h3>
      <p><strong>R² score:</strong> {regression.r2?.toFixed(3)}</p>
      <p><strong>Intercept:</strong> {regression.intercept?.toFixed(3)}</p>
      <p><strong>Top Influential Features:</strong></p>
      <ul>
        {regression.features.map((feature, idx) => (
          <li key={idx}>
            {feature}: {regression.coef[idx].toFixed(3)}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RegressionCard;
