import React from "react";
import { Marker, Popup } from "react-leaflet";
import { createCrimeMarker } from "./Map/markers";
import { formatDate, formatTime } from "../utils/formatters";
import "./Map/mapStyles.css";

export default function CrimeMarker({ crime }) {
  // Use the new custom marker system
  const icon = createCrimeMarker(crime.type);

  return (
    <Marker position={[crime.lat, crime.lng]} icon={icon}>
      <Popup className="crime-popup">
        <div style={{ minWidth: "200px" }}>
          <h4
            style={{
              margin: "0 0 8px 0",
              color: "#fff",
              textTransform: "capitalize",
              fontSize: "14px",
            }}
          >
            {crime.type}
          </h4>
          <p style={{ margin: "4px 0", fontSize: "12px", color: "#d1d5db" }}>
            📍 {crime.location}
          </p>
          <p style={{ margin: "4px 0", fontSize: "12px", color: "#d1d5db" }}>
            📅 {formatDate(crime.date)}
          </p>
          <p style={{ margin: "4px 0", fontSize: "12px", color: "#d1d5db" }}>
            🕐 {formatTime(crime.date)}
          </p>
          {crime.zoneId && (
            <p style={{ margin: "4px 0", fontSize: "11px", color: "#9ca3af" }}>
              Zone ID: {crime.zoneId}
            </p>
          )}
        </div>
      </Popup>
    </Marker>
  );
}
