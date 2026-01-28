import React, { useEffect, useRef } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet.heat";

export default function HeatmapLayer({ crimes }) {
  const map = useMap();
  const heatLayerRef = useRef(null);

  useEffect(() => {
    if (!crimes || crimes.length === 0) {
      console.log("No crimes data for heatmap");
      return;
    }

    // Remove existing heatmap layer if any
    if (heatLayerRef.current) {
      map.removeLayer(heatLayerRef.current);
      heatLayerRef.current = null;
    }

    // Calculate density for each crime point
    const gridSize = 0.01; // Grid cell size (~1km)
    const densityMap = new Map();

    crimes.forEach((crime) => {
      const gridX = Math.round(crime.lat / gridSize);
      const gridY = Math.round(crime.lng / gridSize);
      const key = `${gridX},${gridY}`;
      densityMap.set(key, (densityMap.get(key) || 0) + 1);
    });

    // Find max density for normalization
    const maxDensity = Math.max(...densityMap.values(), 1);

    // Transform crimes into heat layer format: [lat, lng, intensity]
    const heatPoints = crimes.map((crime) => {
      const gridX = Math.round(crime.lat / gridSize);
      const gridY = Math.round(crime.lng / gridSize);
      const key = `${gridX},${gridY}`;
      const density = densityMap.get(key) || 1;
      const intensity = Math.min(density / maxDensity, 1);

      // Return [lat, lng, intensity] format required by leaflet.heat
      return [crime.lat, crime.lng, intensity];
    });

    // Create heat layer with custom gradient (green -> yellow -> red)
    const heatLayer = L.heatLayer(heatPoints, {
      radius: 25, // Radius of each point in pixels
      blur: 20, // Blur amount
      maxZoom: 17, // Max zoom to show heat
      max: 1.0, // Maximum intensity value
      minOpacity: 0.3,
      gradient: {
        0.0: "green",
        0.3: "lime",
        0.5: "yellow",
        0.8: "orange",
        1.0: "red",
      },
    });

    heatLayer.addTo(map);
    heatLayerRef.current = heatLayer;

    console.log(
      `✓ Heatmap layer added: ${crimes.length} points, max density: ${maxDensity}`,
    );

    // Cleanup function
    return () => {
      if (heatLayerRef.current && map.hasLayer(heatLayerRef.current)) {
        map.removeLayer(heatLayerRef.current);
        heatLayerRef.current = null;
      }
    };
  }, [crimes, map]);

  return null;
}
