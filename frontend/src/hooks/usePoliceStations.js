import { useState, useEffect } from "react";
import { fetchPoliceStations, transformPoliceStationData } from "../services/api";

export default function usePoliceStations() {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadStations = async () => {
      setLoading(true);
      setError(null);
      try {
        const result = await fetchPoliceStations();
        const transformedData = result.map(transformPoliceStationData);
        setStations(transformedData);
      } catch (err) {
        console.error("Failed to load police stations", err);
        setError("Failed to load police stations.");
        setStations([]);
      } finally {
        setLoading(false);
      }
    };
    loadStations();
  }, []);

  return { stations, loading, error };
}