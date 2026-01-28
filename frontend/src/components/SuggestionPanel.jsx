import React from "react";
import { Lightbulb, MapPin, Clock } from "lucide-react";
import "../styles/components.css";

const riskBadgeColor = (risk) => {
  switch (risk) {
    case "High":
      return "#fee2e2";
    case "Medium":
      return "#fef3c7";
    case "Low":
      return "#dcfce7";
    default:
      return "#e2e8f0";
  }
};

export default function SuggestionPanel({ suggestions }) {
  // Group suggestions by risk level for better organization
  const groupedSuggestions = suggestions.reduce((acc, item) => {
    if (!acc[item.riskLevel]) acc[item.riskLevel] = [];
    acc[item.riskLevel].push(item);
    return acc;
  }, {});

  const riskLevels = ["High", "Medium", "Low"];

  return (
    <div className="suggestion-panel">
      <div className="suggestion-header">
        <div className="suggestion-title">
          <Lightbulb size={16} /> AI Patrol Suggestions
        </div>
        <div className="suggestion-count">
          {suggestions.length} zones analyzed
        </div>
      </div>

      {suggestions.length === 0 ? (
        <div className="suggestion-empty">
          No AI suggestions yet. Click "Generate AI Predictions" to analyze
          zones.
        </div>
      ) : (
        <div className="suggestion-list">
          {riskLevels.map((riskLevel) => {
            const items = groupedSuggestions[riskLevel] || [];
            if (items.length === 0) return null;

            return (
              <div key={riskLevel} className="suggestion-group">
                <div className="suggestion-group-header">
                  <span
                    className="suggestion-badge"
                    style={{ background: riskBadgeColor(riskLevel) }}
                  >
                    {riskLevel} Risk
                  </span>
                  <span className="suggestion-group-count">
                    {items.length} zones
                  </span>
                </div>
                {items.map((item) => (
                  <div className="suggestion-card" key={item.id}>
                    <div className="suggestion-card-top">
                      <div className="suggestion-zone">
                        <MapPin size={14} /> {item.zoneName}
                      </div>
                      <span
                        className="suggestion-badge"
                        style={{ background: riskBadgeColor(item.riskLevel) }}
                      >
                        {item.riskLevel}
                      </span>
                    </div>
                    {item.timeWindow && (
                      <div className="suggestion-time">
                        <Clock size={12} /> Expected: {item.timeWindow}
                      </div>
                    )}
                    {item.predictedLat && item.predictedLng && (
                      <div className="suggestion-coords">
                        📍 Predicted location: {item.predictedLat.toFixed(4)},{" "}
                        {item.predictedLng.toFixed(4)}
                      </div>
                    )}
                    <div className="suggestion-text">
                      {item.suggestionText.split("\n").map((line, idx) => (
                        <div key={idx} className="suggestion-item">
                          {line.startsWith("•") ? line : `• ${line}`}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
