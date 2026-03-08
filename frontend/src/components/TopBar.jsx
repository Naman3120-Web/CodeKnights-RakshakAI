import React from "react";
import { ArrowLeft } from "lucide-react";

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
        <img src="/RakshakIcon.png" alt="RakshakAI logo" className="brand-logo" />
        <h1>RakshakAI</h1>
      </div>

      <div className="topbar-items">
        <div className="topbar-item">
          <img
            src="/location.png"
            alt="Location"
            className="topbar-location-icon"
          />
          Mumbai City
        </div>
      </div>
    </header>
  );
}
