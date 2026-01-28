import React from "react";
import { Circle } from "react-leaflet";
import { SEVERITY_COLORS } from "../utils/constants";

export default function HotspotLayer({ crimes }) {
  // Logic: Identify high-density areas or high-severity crimes
  // For this mock, we draw circles around High Severity crimes

  const highRiskCrimes = crimes.filter((c) => c.severity === "High");

  return (
    <>
      {highRiskCrimes.map((crime) => (
        <Circle
          key={`hotspot-${crime.id}`}
          center={[crime.lat, crime.lng]}
          pathOptions={{
            fillColor: SEVERITY_COLORS.High,
            color: SEVERITY_COLORS.High,
            opacity: 0.2,
            fillOpacity: 0.3,
            weight: 1,
          }}
          radius={400} // Meters
        />
      ))}
    </>
  );
}
