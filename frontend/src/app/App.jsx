import React, { useState } from "react";
import Dashboard from "../pages/Dashboard";
import PredictionsDashboard from "../pages/PredictionsDashboard";
import "../styles/globals.css";
import "../styles/layout.css";

export default function App() {
  const [activePage, setActivePage] = useState("dashboard");

  return (
    <div className="app-container">
      {activePage === "dashboard" ? (
        <Dashboard onNavigate={setActivePage} activePage={activePage} />
      ) : (
        <PredictionsDashboard
          onNavigate={setActivePage}
          activePage={activePage}
        />
      )}
    </div>
  );
}
