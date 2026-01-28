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

      // Add time range filtering based on months
      if (filters.timeRange && filters.timeRange !== "all") {
        const crimeDate = new Date(crime.date);
        const now = new Date();
        const monthsDiff =
          (now.getFullYear() - crimeDate.getFullYear()) * 12 +
          (now.getMonth() - crimeDate.getMonth());

        if (filters.timeRange === "3m" && monthsDiff > 3) return false;
        if (filters.timeRange === "6m" && monthsDiff > 6) return false;
        if (filters.timeRange === "9m" && monthsDiff > 9) return false;
        if (filters.timeRange === "12m" && monthsDiff > 12) return false;
      }

      return typeMatch;
    });
  }, [data, filters]);

  return { crimes: filteredData, loading, error };
}
