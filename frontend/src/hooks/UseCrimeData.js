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

        // Transform backend data to frontend format
        const transformedData = result.map(transformCrimeData);

        setData(transformedData);
      } catch {
        setError("Failed to load crime data. Using mock data.");
        setData([]);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [filters]);

  // 2. Filter Data (Client Side Logic for additional filtering)
  const filteredData = useMemo(() => {
    return data.filter((crime) => {
      // Case-insensitive comparison for crime type
      const typeMatch =
        filters.crimeType === "All" ||
        crime.type.toLowerCase() === filters.crimeType.toLowerCase();

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
