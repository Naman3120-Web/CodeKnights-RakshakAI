import React from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

// Create a custom police station icon
const policeIcon = new L.DivIcon({
  className: "police-station-marker",
  html: `
    <div style="
      background: #1e40af;
      border: 3px solid #fff;
      border-radius: 50%;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    ">
      <span style="font-size: 16px;">🚔</span>
    </div>
  `,
  iconSize: [32, 32],
  iconAnchor: [16, 16],
  popupAnchor: [0, -16],
});

export default function PoliceStationMarker({ station }) {
  return (
    <Marker position={[station.lat, station.lng]} icon={policeIcon}>
      <Popup className="police-popup">
        <div style={{ minWidth: "220px" }}>
          <h4
            style={{
              margin: "0 0 8px 0",
              color: "#fff",
              fontSize: "14px",
              fontWeight: "bold",
            }}
          >
            🚔 {station.name}
          </h4>
          <p style={{ margin: "4px 0", fontSize: "12px", color: "#d1d5db" }}>
            📞 {station.contact}
          </p>
          <p style={{ margin: "4px 0", fontSize: "12px", color: "#d1d5db" }}>
            🏢 {station.type}
          </p>
          <p style={{ margin: "4px 0", fontSize: "12px", color: "#d1d5db" }}>
            👮 Personnel: {station.personnelCount}
          </p>
          <p style={{ margin: "4px 0", fontSize: "12px", color: "#d1d5db" }}>
            🔒 Lockup: {station.hasLockup ? "Yes" : "No"}
          </p>
          <p style={{ margin: "4px 0", fontSize: "11px", color: "#9ca3af" }}>
            Zone ID: {station.zoneId}
          </p>
        </div>
      </Popup>
    </Marker>
  );
}