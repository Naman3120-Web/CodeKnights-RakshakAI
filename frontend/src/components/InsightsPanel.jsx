import React from "react";
import { BarChart2, Zap, TrendingUp, AlertTriangle } from "lucide-react";
import { SEVERITY_COLORS } from "../utils/constants";

export default function InsightsPanel({ data, onGenerateReport }) {
  // --- Analysis Logic ---

  // 1. Total Incidents
  const total = data.length;

  // 2. Most Common Crime Type
  const getMostCommonType = () => {
    if (total === 0) return "N/A";

    const counts = data.reduce((acc, curr) => {
      acc[curr.type] = (acc[curr.type] || 0) + 1;
      return acc;
    }, {});

    return Object.keys(counts).reduce((a, b) =>
      counts[a] > counts[b] ? a : b,
    );
  };

  // 3. Peak Time Analysis (Simple Hour Extraction)
  const getPeakTime = () => {
    if (total === 0) return "N/A";

    const hourCounts = data.reduce((acc, curr) => {
      const hour = new Date(curr.date).getHours();
      acc[hour] = (acc[hour] || 0) + 1;
      return acc;
    }, {});

    const peakHour = Object.keys(hourCounts).reduce((a, b) =>
      hourCounts[a] > hourCounts[b] ? a : b,
    );

    // Format: "14:00 - 15:00"
    return `${peakHour}:00 - ${parseInt(peakHour) + 1}:00`;
  };

  const mostCommon = getMostCommonType();
  const peakTime = getPeakTime();

  return (
    <aside className="insights-panel">
      <div className="panel-header">
        <h3>
          <BarChart2 size={16} /> Analysis
        </h3>
      </div>

      {/* Metric 1: Total Volume */}
      <div className="stat-card">
        <span className="stat-label">Total Incidents</span>
        <span className="stat-value">{total}</span>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "6px",
            marginTop: "6px",
            fontSize: "0.75rem",
            color: "#10b981",
          }}
        ></div>
      </div>

      {/* Metric 2: Primary Threat */}
      <div
        className="stat-card"
        style={{
          borderColor: mostCommon !== "N/A" ? "var(--border)" : "var(--border)",
        }}
      >
        <span className="stat-label">Most Common Type</span>
        <span className="stat-value" style={{ color: "var(--primary)" }}>
          {mostCommon}
        </span>
        {mostCommon === "Assault" && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              marginTop: "6px",
              fontSize: "0.75rem",
              color: SEVERITY_COLORS.High,
            }}
          >
            <AlertTriangle size={12} /> High Priority
          </div>
        )}
      </div>

      {/* Metric 3: Time Pattern */}
      <div className="stat-card">
        <span className="stat-label">Peak Activity Time</span>
        <span className="stat-value">{peakTime}</span>
      </div>

      {/* AI Action Button */}
      <div className="sidebar-footer" style={{ marginTop: "auto" }}>
        <button
          className="btn-predict"
          style={{
            width: "100%",
            backgroundColor: "var(--primary)",
            color: "white",
            padding: "12px",
            border: "none",
            borderRadius: "6px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "8px",
            fontWeight: "600",
            cursor: "pointer",
          }}
          onClick={onGenerateReport}
        >
          <Zap size={16} fill="white" /> Generate Report
        </button>
      </div>
    </aside>
  );
}
