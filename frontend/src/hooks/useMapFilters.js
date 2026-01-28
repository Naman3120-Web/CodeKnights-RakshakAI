import { useState } from "react";

export default function useMapFilters() {
  const [filters, setFilters] = useState({
    crimeType: "All",
    timeRange: "24h",
  });

  const [toggles, setToggles] = useState({
    showHeatmap: false,
    showHotspots: true,
  });

  const updateFilter = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const updateToggle = (key) => {
    setToggles((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const resetFilters = () => {
    setFilters({ crimeType: "All", timeRange: "24h" });
    setToggles({ showHeatmap: false, showHotspots: true });
  };

  return { filters, toggles, updateFilter, updateToggle, resetFilters };
}
