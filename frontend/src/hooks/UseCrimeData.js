import { useState, useEffect, useMemo } from "react";
import { fetchCrimes, transformCrimeData } from "../services/api";

export default function useCrimeData(filters) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 1. Fetch Data from Backend
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);
      try {
        const result = await fetchCrimes(filters);
        console.log("Fetched raw data:", result);

        // Transform backend data to frontend format
        const transformedData = result.map(transformCrimeData);
        console.log("Transformed data:", transformedData);

        setData(transformedData);
      } catch (err) {
        console.error("Failed to load crime data", err);
        setError("Failed to load crime data. Using mock data.");
        // Fallback to empty array on error
        setData([]);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [filters]); // Re-fetch when filters change

  // 2. Filter Data (Client Side Logic for additional filtering)
  const filteredData = useMemo(() => {
    return data.filter((crime) => {
      const typeMatch =
        filters.crimeType === "All" || crime.type === filters.crimeType;

      // Add time range filtering if needed
      if (filters.timeRange && filters.timeRange !== "all") {
        const crimeDate = new Date(crime.date);
        const now = new Date();
        const hoursDiff = (now - crimeDate) / (1000 * 60 * 60);

        if (filters.timeRange === "24h" && hoursDiff > 24) return false;
        if (filters.timeRange === "7d" && hoursDiff > 168) return false;
        if (filters.timeRange === "30d" && hoursDiff > 720) return false;
      }

      return typeMatch;
    });
  }, [data, filters]);

  return { crimes: filteredData, loading, error };
}
