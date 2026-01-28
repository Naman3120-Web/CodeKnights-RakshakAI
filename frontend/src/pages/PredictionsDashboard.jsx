import React, { useMemo, useState, useEffect, useCallback } from "react";
import TopBar from "../components/TopBar";
import PredictionSidebar from "../components/PredictionSidebar";
import PredictionMapView from "../components/PredictionMapView";
import SuggestionPanel from "../components/SuggestionPanel";
import {
  fetchZones,
  getAIPatrolSuggestions,
  trainAIModels,
} from "../services/api";
import "../styles/layout.css";

export default function PredictionsDashboard({ onNavigate, activePage }) {
  const [filters, setFilters] = useState({
    riskLevel: "All",
  });

  const [zones, setZones] = useState([]);
  const [aiPredictions, setAiPredictions] = useState([]);
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState(null);

  // Fetch zones on mount
  useEffect(() => {
    const loadZones = async () => {
      try {
        const zonesData = await fetchZones({ limit: 500 });
        setZones(zonesData);
        setLoading(false);
      } catch (err) {
        console.error("Failed to load zones:", err);
        setError("Failed to load zone data");
        setLoading(false);
      }
    };
    loadZones();
  }, []);

  // Generate AI predictions for all zones
  const generateAIPredictions = useCallback(async () => {
    if (zones.length === 0) return;

    setGenerating(true);
    setError(null);

    try {
      // First train the AI models
      await trainAIModels();

      const predictions = [];
      const suggestions = [];
      const crimeTypes = ["theft", "assault", "accident"];

      // Generate predictions for each zone using Gemini AI
      for (const zone of zones) {
        try {
          const crimeType =
            crimeTypes[Math.floor(Math.random() * crimeTypes.length)];

          const aiResponse = await getAIPatrolSuggestions(
            zone.center_lat,
            zone.center_lng,
            zone.zone_name,
            crimeType,
          );

          // Create prediction from AI response
          const prediction = {
            id: zone.id,
            zoneId: zone.id,
            zoneName: zone.zone_name,
            lat: aiResponse.latitude || zone.center_lat,
            lng: aiResponse.longitude || zone.center_lng,
            radius: zone.radius,
            riskLevel: aiResponse.risk_level || "High",
            expectedTimeWindow:
              aiResponse.expected_crime_time_window || "Next 24 hours",
            crimeType: crimeType,
          };
          predictions.push(prediction);

          // Create suggestions from AI response
          if (aiResponse.suggestions && Array.isArray(aiResponse.suggestions)) {
            aiResponse.suggestions.forEach((suggestionText, idx) => {
              suggestions.push({
                id: `${zone.id}-${idx}`,
                zoneName: zone.zone_name,
                zoneId: zone.id,
                riskLevel: aiResponse.risk_level || "High",
                suggestionText: suggestionText,
                predictedLat: aiResponse.latitude,
                predictedLng: aiResponse.longitude,
                timeWindow: aiResponse.expected_crime_time_window,
              });
            });
          } else if (aiResponse.raw_response) {
            // Handle raw response from API
            suggestions.push({
              id: `${zone.id}-0`,
              zoneName: zone.zone_name,
              zoneId: zone.id,
              riskLevel: "High",
              suggestionText: aiResponse.raw_response,
            });
          }
        } catch (zoneErr) {
          console.error(
            `Error getting AI prediction for ${zone.zone_name}:`,
            zoneErr,
          );
        }
      }

      setAiPredictions(predictions);
      setAiSuggestions(suggestions);
    } catch (err) {
      console.error("Error generating AI predictions:", err);
      setError(
        "Failed to generate AI predictions. Check if Gemini API is configured.",
      );
    } finally {
      setGenerating(false);
    }
  }, [zones]);

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleReset = () => {
    setFilters({ riskLevel: "All" });
  };

  // Group suggestions by zone (deduplicate)
  const filteredSuggestions = useMemo(() => {
    if (!aiSuggestions.length) return [];

    // Group by zone, then flatten
    const groupedByZone = {};
    aiSuggestions.forEach((s) => {
      if (!groupedByZone[s.zoneId]) {
        groupedByZone[s.zoneId] = {
          id: s.id,
          zoneName: s.zoneName,
          zoneId: s.zoneId,
          riskLevel: s.riskLevel,
          suggestions: [],
          predictedLat: s.predictedLat,
          predictedLng: s.predictedLng,
          timeWindow: s.timeWindow,
        };
      }
      groupedByZone[s.zoneId].suggestions.push(s.suggestionText);
    });

    return Object.values(groupedByZone)
      .map((group) => ({
        ...group,
        suggestionText: group.suggestions.join("\n• "),
      }))
      .filter((s) => {
        if (filters.riskLevel !== "All" && s.riskLevel !== filters.riskLevel) {
          return false;
        }
        return true;
      })
      .sort((a, b) => {
        const riskPriority = { High: 3, Medium: 2, Low: 1 };
        return (
          (riskPriority[b.riskLevel] || 0) - (riskPriority[a.riskLevel] || 0)
        );
      });
  }, [aiSuggestions, filters.riskLevel]);

  // Filter predictions by risk level
  const filteredPredictions = useMemo(() => {
    return aiPredictions.filter((p) => {
      if (filters.riskLevel !== "All" && p.riskLevel !== filters.riskLevel) {
        return false;
      }
      return true;
    });
  }, [aiPredictions, filters.riskLevel]);

  return (
    <div className="dashboard-layout">
      <TopBar onNavigate={onNavigate} activePage={activePage} />

      <div className="main-content">
        <PredictionSidebar
          filters={filters}
          onFilterChange={handleFilterChange}
          onReset={handleReset}
          onGeneratePredictions={generateAIPredictions}
          generating={generating}
          hasPredictions={aiPredictions.length > 0}
        />

        {loading ? (
          <div className="prediction-loading">Loading zones...</div>
        ) : error ? (
          <div className="prediction-error">{error}</div>
        ) : generating ? (
          <div className="prediction-center">
            <div className="prediction-generating">
              <div className="generating-spinner"></div>
              <p>🤖 Generating AI predictions with Gemini...</p>
              <p className="generating-sub">
                Analyzing crime patterns and generating patrol suggestions
              </p>
            </div>
          </div>
        ) : aiPredictions.length === 0 ? (
          <div className="prediction-center">
            <div className="prediction-empty">
              <p>🧠 No AI predictions generated yet</p>
              <p className="empty-sub">
                Click "Generate AI Predictions" in the sidebar to analyze zones
                with Gemini AI
              </p>
            </div>
          </div>
        ) : (
          <div className="prediction-center">
            <div className="prediction-map">
              <PredictionMapView predictions={filteredPredictions} />
            </div>
            <SuggestionPanel suggestions={filteredSuggestions} />
          </div>
        )}
      </div>
    </div>
  );
}
