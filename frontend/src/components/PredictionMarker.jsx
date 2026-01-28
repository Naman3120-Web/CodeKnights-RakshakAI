import React from "react";
import { CircleMarker, Popup } from "react-leaflet";

const getRiskColor = (riskLevel) => {
  switch (riskLevel) {
    case "High":
      return "#ef4444";
    case "Medium":
      return "#f59e0b";
    case "Low":
      return "#22c55e";
    default:
      return "#3b82f6";
  }
};

export default function PredictionMarker({ prediction }) {
  const color = getRiskColor(prediction.riskLevel);

  return (
    <CircleMarker
      center={[prediction.lat, prediction.lng]}
      radius={8}
      pathOptions={{
        color,
        fillColor: color,
        fillOpacity: 0.7,
        weight: 2,
      }}
    >
      <Popup>
        <div style={{ minWidth: "220px" }}>
          <h4 style={{ margin: "0 0 6px 0", fontSize: "14px" }}>
            🧠 Predicted Risk Zone
          </h4>
          <div style={{ fontSize: "12px", marginBottom: "6px" }}>
            📍 {prediction.zoneName}
          </div>
          <div style={{ fontSize: "12px", marginBottom: "6px" }}>
            📅 {prediction.predictedMonth}
          </div>
          <div style={{ fontSize: "12px", marginBottom: "6px" }}>
            ⚠️ Risk Level: <strong>{prediction.riskLevel}</strong>
          </div>
          <div style={{ fontSize: "12px", marginBottom: "6px" }}>
            🔢 Expected Crimes: <strong>{prediction.expectedCrimes}</strong>
          </div>
          <div style={{ fontSize: "12px" }}>
            📊 Risk Score: <strong>{prediction.riskScore}</strong>
          </div>
        </div>
      </Popup>
    </CircleMarker>
  );
}
