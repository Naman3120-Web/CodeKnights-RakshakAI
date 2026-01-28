import React from "react";
import {
  Filter,
  RotateCcw,
  AlertTriangle,
  Sparkles,
  Brain,
} from "lucide-react";
import "../styles/components.css";

const RISK_LEVELS = {
  All: "All Risk Levels",
  Low: "Low Risk",
  Medium: "Medium Risk",
  High: "High Risk",
};

export default function PredictionSidebar({
  filters,
  onFilterChange,
  onReset,
  onGeneratePredictions,
  generating,
  hasPredictions,
}) {
  return (
    <aside className="sidebar">
      {/* Generate AI Predictions Button */}
      <div className="sidebar-section">
        <h3>
          <Brain size={16} /> AI Analysis
        </h3>
        <button
          className={`btn-generate-ai ${generating ? "generating" : ""}`}
          onClick={onGeneratePredictions}
          disabled={generating}
        >
          <Sparkles size={16} />
          {generating
            ? "Generating..."
            : hasPredictions
              ? "Regenerate Predictions"
              : "Generate AI Predictions"}
        </button>
        <p className="ai-description">
          Uses Gemini AI to analyze crime patterns and generate patrol
          suggestions for each zone.
        </p>
      </div>

      <div className="sidebar-separator" />

      <div className="sidebar-section">
        <h3>
          <Filter size={16} /> Filters
        </h3>

        <div className="control-group">
          <label>Risk Level</label>
          <select
            value={filters.riskLevel}
            onChange={(e) => onFilterChange("riskLevel", e.target.value)}
            className="crime-type-select"
          >
            {Object.entries(RISK_LEVELS).map(([key, label]) => (
              <option key={key} value={key}>
                {key === "All" ? label : `⚠️ ${label}`}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="sidebar-separator" />

      <div className="sidebar-section">
        <h3>
          <AlertTriangle size={16} /> AI Insights
        </h3>
        <p style={{ fontSize: "12px", color: "#64748b", marginTop: "6px" }}>
          {hasPredictions
            ? "AI predictions generated. Markers show predicted crime locations."
            : "Click 'Generate AI Predictions' to analyze zones with AI."}
        </p>
      </div>

      <div className="sidebar-footer">
        <button className="btn-reset" onClick={onReset}>
          <RotateCcw size={14} /> Reset
        </button>
      </div>
    </aside>
  );
}
