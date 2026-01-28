import React, { useMemo } from "react";
import { Circle, Popup } from "react-leaflet";

/**
 * Calculate distance between two coordinates in km using Haversine formula
 */
const calculateDistance = (lat1, lng1, lat2, lng2) => {
  const R = 6371; // Earth's radius in km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLng = ((lng2 - lng1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLng / 2) *
      Math.sin(dLng / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
};

export default function HotspotLayer({ crimes }) {
  if (!crimes || crimes.length === 0) return null;

  // Generate clusters based on spatial density (DBSCAN-like approach)
  const clusters = useMemo(() => {
    const clusterMap = [];
    const visited = new Set();
    const RADIUS_KM = 1.5; // 1.5 km clustering radius
    const MIN_CRIMES = 3; // Minimum 3 crimes to form a hotspot

    crimes.forEach((crime, idx) => {
      if (visited.has(idx)) return;

      // Find all nearby crimes (within radius)
      const nearby = crimes
        .map((c, i) => ({
          index: i,
          crime: c,
          distance: calculateDistance(crime.lat, crime.lng, c.lat, c.lng),
        }))
        .filter((item) => item.distance <= RADIUS_KM);

      // If cluster has minimum crimes, create a hotspot
      if (nearby.length >= MIN_CRIMES) {
        // Calculate cluster center
        const centerLat =
          nearby.reduce((sum, item) => sum + item.crime.lat, 0) / nearby.length;
        const centerLng =
          nearby.reduce((sum, item) => sum + item.crime.lng, 0) / nearby.length;

        // Calculate radius (larger for denser clusters)
        const density = nearby.length / 15; // Normalize by crime count
        const radius = 300 + density * 500; // 300m to 800m

        // Calculate intensity for color
        const intensity = Math.min(nearby.length / 20, 1);

        clusterMap.push({
          id: `hotspot-${idx}`,
          center: [centerLat, centerLng],
          radius,
          intensity,
          crimeCount: nearby.length,
        });

        // Mark all crimes in this cluster as visited
        nearby.forEach((item) => visited.add(item.index));
      }
    });

    console.log(`Generated ${clusterMap.length} hotspot clusters`);
    return clusterMap;
  }, [crimes]);

  return (
    <>
      {clusters.map((hotspot) => (
        <Circle
          key={hotspot.id}
          center={hotspot.center}
          radius={hotspot.radius}
          pathOptions={{
            fillColor: `rgba(239, 68, 68, ${hotspot.intensity * 0.6})`,
            color: "#991b1b",
            weight: 4,
            opacity: 1,
            fillOpacity: hotspot.intensity * 0.5,
            dashArray: "5, 5",
            lineCap: "round",
            lineJoin: "round",
          }}
        >
          <Popup>
            <div style={{ fontSize: "13px", color: "#1f2937", fontWeight: "500" }}>
              <strong style={{ fontSize: "14px", display: "block", marginBottom: "6px" }}>
                🔥 Crime Hotspot Zone
              </strong>
              <div style={{ marginBottom: "4px" }}>
                📍 <strong>{hotspot.crimeCount} Incidents</strong>
              </div>
              <div>
                ⚠️ Risk:{" "}
                <strong>
                  {hotspot.intensity > 0.7 ? "🔴 HIGH" : "🟠 MEDIUM"}
                </strong>
              </div>
            </div>
          </Popup>
        </Circle>
      ))}
    </>
  );
}
