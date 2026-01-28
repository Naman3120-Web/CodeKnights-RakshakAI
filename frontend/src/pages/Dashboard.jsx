import React, { useState } from "react";
import TopBar from "../components/TopBar";
import Sidebar from "../components/Sidebar";
import MapView from "../components/MapView";
import InsightsPanel from "../components/InsightsPanel";
import useCrimeData from "../hooks/UseCrimedata";
import "../styles/layout.css";

export default function Dashboard() {
  // 1. Shared State
  const [filters, setFilters] = useState({
    crimeType: "All",
    timeRange: "all", // all, 3m, 6m, 9m, 12m
  });

  const [toggles, setToggles] = useState({
    showHeatmap: false,
    showHotspots: true,
  });

  // 2. Fetch data from backend using custom hook
  const { crimes, loading, error } = useCrimeData(filters);

  // 3. Handlers
  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleToggleChange = (key) => {
    setToggles((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleReset = () => {
    setFilters({ crimeType: "All", timeRange: "all" });
    setToggles({ showHeatmap: false, showHotspots: true });
  };

  return (
    <div className="dashboard-layout">
      <TopBar />

      <div className="main-content">
        <Sidebar
          filters={filters}
          toggles={toggles}
          onFilterChange={handleFilterChange}
          onToggleChange={handleToggleChange}
          onReset={handleReset}
        />

        {loading ? (
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              flex: 1,
              fontSize: "1.2rem",
              color: "#666",
            }}
          >
            Loading crime data...
          </div>
        ) : error ? (
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              flex: 1,
              fontSize: "1.2rem",
              color: "#d32f2f",
            }}
          >
            {error}
          </div>
        ) : (
          <>
            <MapView
              crimes={crimes}
              showHeatmap={toggles.showHeatmap}
              showHotspots={toggles.showHotspots}
            />

            <InsightsPanel data={crimes} />
          </>
        )}
      </div>
    </div>
  );
}
