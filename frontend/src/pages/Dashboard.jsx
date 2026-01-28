import React, { useState } from "react";
import TopBar from "../components/TopBar";
import Sidebar from "../components/Sidebar";
import MapView from "../components/MapView";
import InsightsPanel from "../components/InsightsPanel";
import useCrimeData from "../hooks/UseCrimedata";
import usePoliceStations from "../hooks/usePoliceStations";
import "../styles/layout.css";

export default function Dashboard() {
  // 1. Shared State
  const [filters, setFilters] = useState({
    crimeType: "All",
    timeRange: "all",
  });

  const [toggles, setToggles] = useState({
    showHeatmap: false,
    showHotspots: true,
    showPoliceStations: true, // Add this
  });

  // 2. Fetch data from backend using custom hooks
  const { crimes, loading: crimesLoading, error: crimesError } = useCrimeData(filters);
  const { stations: policeStations, loading: stationsLoading } = usePoliceStations();

  const loading = crimesLoading || stationsLoading;
  const error = crimesError;

  // 3. Handlers
  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleToggleChange = (key) => {
    setToggles((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleReset = () => {
    setFilters({ crimeType: "All", timeRange: "all" });
    setToggles({ showHeatmap: false, showHotspots: true, showPoliceStations: true });
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
            Loading data...
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
              policeStations={policeStations}
              showHeatmap={toggles.showHeatmap}
              showHotspots={toggles.showHotspots}
              showPoliceStations={toggles.showPoliceStations}
            />

            <InsightsPanel data={crimes} />
          </>
        )}
      </div>
    </div>
  );
}
