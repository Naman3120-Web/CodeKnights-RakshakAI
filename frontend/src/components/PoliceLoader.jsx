import React from "react";

export default function PoliceLoader({ label = "Scanning city grid" }) {
  return (
    <div
      className="police-loader-wrap"
      role="status"
      aria-live="polite"
      aria-label={label}
    >
      <div className="police-loader" aria-hidden="true">
        <div className="police-loader-ring"></div>
        <div className="police-loader-beacon">
          <span className="police-light police-light-red"></span>
          <span className="police-light police-light-blue"></span>
        </div>
      </div>
      <p className="police-loader-label">{label}</p>
    </div>
  );
}
