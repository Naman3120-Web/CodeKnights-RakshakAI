import React from "react";
import { Filter, Map, RotateCcw, Hand, AlertTriangle, Zap } from "lucide-react";
import "../styles/components.css";

const CRIME_TYPES = {
  All: "All Categories",
  theft: "Theft",
  assault: "Assault",
  accident: "Accident",
};

const TIME_RANGES = [
  { value: "all", label: "All Time" },
  { value: "3m", label: "Last 3 Months" },
  { value: "6m", label: "Last 6 Months" },
  { value: "9m", label: "Last 9 Months" },
  { value: "12m", label: "Last 12 Months" },
];

// const getCrimeIcon = (type) => {
//   switch (type) {
//     case "theft":
//       return <Hand size={14} style={{ marginRight: "6px" }} />;
//     case "assault":
//       return <AlertTriangle size={14} style={{ marginRight: "6px" }} />;
//     case "accident":
//       return <Zap size={14} style={{ marginRight: "6px" }} />;
//     default:
//       return null;
//   }
// };

export default function Sidebar({
  filters,
  toggles,
  onFilterChange,
  onToggleChange,
  onReset,
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-section">
        <h3>
          <Filter size={16} /> Filters
        </h3>

        <div className="control-group">
          <label>Crime Type</label>
          <select
            value={filters.crimeType}
            onChange={(e) => onFilterChange("crimeType", e.target.value)}
            className="crime-type-select"
          >
            {Object.entries(CRIME_TYPES).map(([key, label]) => (
              <option key={key} value={key}>
                {key === "All" ? label : `🔴 ${label}`}
              </option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label>Time Range</label>
          <select
            value={filters.timeRange}
            onChange={(e) => onFilterChange("timeRange", e.target.value)}
            className="time-range-select"
          >
            {TIME_RANGES.map((range) => (
              <option key={range.value} value={range.value}>
                {range.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="sidebar-separator" />

      <div className="sidebar-section">
        <h3>
          <Map size={16} /> Layers
        </h3>
        <div className="toggle-row">
          <label>🔥 Heatmap</label>
          <input
            type="checkbox"
            checked={toggles.showHeatmap}
            onChange={() => onToggleChange("showHeatmap")}
            className="toggle-checkbox"
          />
        </div>
        <div className="toggle-row">
          <label>🎯 Hotspots</label>
          <input
            type="checkbox"
            checked={toggles.showHotspots}
            onChange={() => onToggleChange("showHotspots")}
            className="toggle-checkbox"
          />
        </div>
        <div className="toggle-row">
          <label>🚔 Police Stations</label>
          <input
            type="checkbox"
            checked={toggles.showPoliceStations}
            onChange={() => onToggleChange("showPoliceStations")}
            className="toggle-checkbox"
          />
        </div>
      </div>

      <div className="sidebar-footer">
        <button className="btn-reset" onClick={onReset}>
          <RotateCcw size={14} /> Reset
        </button>
      </div>
    </aside>
  );
}
