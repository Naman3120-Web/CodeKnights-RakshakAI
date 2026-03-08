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
        <img src="/logo.png" alt="RakshakAI logo" width="50" height="50" />
        <h1>RakshakAI</h1>
      </div>

      <div className="topbar-items">
        <div className="topbar-item">📍 Mumbai City</div>
      </div>
    </header>
  );
}
