import React from "react";
import { Shield, ArrowLeft } from "lucide-react";

export default function TopBar({ onNavigate, activePage }) {
  return (
    <header className="top-bar">
      <div className="topbar-left">
        {activePage === "predictions" && (
          <button
            className="back-button"
            onClick={() => onNavigate?.("dashboard")}
            type="button"
          >
            <ArrowLeft size={20} /> Back
          </button>
        )}
      </div>

      <div className="brand">
        <Shield size={24} />
        <h1>RakshakAI</h1>
      </div>

      <div className="topbar-items">
        <div className="topbar-item">🗺️ Map</div>
        <div className="topbar-item">🧠 AI Predictions</div>
        <div className="topbar-item">📍 Mumbai City</div>
      </div>
    </header>
  );
}
