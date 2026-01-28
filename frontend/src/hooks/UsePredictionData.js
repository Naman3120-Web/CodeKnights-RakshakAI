import { useState, useEffect, useMemo } from "react";
import {
  fetchPredictions,
  fetchZones,
  fetchPatrolSuggestions,
} from "../services/api";

const parseMonthString = (monthStr) => {
  if (!monthStr) return null;
  const [year, month] = monthStr.split("-").map(Number);
  if (!year || !month) return null;
  return new Date(year, month - 1, 1);
};

export default function usePredictionData(filters) {
  const [predictions, setPredictions] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [zonesById, setZonesById] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [predictionsRes, zonesRes, suggestionsRes] = await Promise.all([
          fetchPredictions({ limit: 500 }),
          fetchZones({ limit: 500 }),
          fetchPatrolSuggestions({ limit: 500 }),
        ]);

        const zoneMap = zonesRes.reduce((acc, zone) => {
          acc[zone.id] = zone;
          return acc;
        }, {});

        setZonesById(zoneMap);
        setSuggestions(suggestionsRes);

        const enrichedPredictions = predictionsRes
          .map((prediction) => {
            const zone = zoneMap[prediction.zone_id];
            if (!zone) return null;
            return {
              id: prediction.id,
              zoneId: prediction.zone_id,
              zoneName: zone.zone_name,
              lat: zone.center_lat,
              lng: zone.center_lng,
              radius: zone.radius,
              areaType: zone.area_type,
              predictedMonth: prediction.predicted_month,
              riskLevel: prediction.risk_level,
              riskScore: prediction.risk_score,
              expectedCrimes: prediction.expected_crimes,
              generatedAt: prediction.generated_at,
            };
          })
          .filter(Boolean);

        setPredictions(enrichedPredictions);
      } catch (err) {
        console.error("Failed to load prediction data", err);
        setError("Failed to load prediction data.");
        setPredictions([]);
        setSuggestions([]);
        setZonesById({});
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [filters]);

  const filteredPredictions = useMemo(() => {
    return predictions.filter((prediction) => {
      const riskMatch =
        filters.riskLevel === "All" ||
        prediction.riskLevel === filters.riskLevel;

      if (filters.timeRange && filters.timeRange !== "all") {
        const predictedDate = parseMonthString(prediction.predictedMonth);
        if (!predictedDate) return false;

        const now = new Date();
        const monthsDiff =
          (predictedDate.getFullYear() - now.getFullYear()) * 12 +
          (predictedDate.getMonth() - now.getMonth());

        if (filters.timeRange === "3m" && monthsDiff > 3) return false;
        if (filters.timeRange === "6m" && monthsDiff > 6) return false;
        if (filters.timeRange === "9m" && monthsDiff > 9) return false;
        if (filters.timeRange === "12m" && monthsDiff > 12) return false;
      }

      return riskMatch;
    });
  }, [predictions, filters]);

  return {
    predictions: filteredPredictions,
    suggestions,
    zonesById,
    loading,
    error,
  };
}
