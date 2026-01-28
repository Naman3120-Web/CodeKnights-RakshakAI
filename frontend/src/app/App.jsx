import React from "react";
import routes from "./routes";
import "../styles/globals.css";
import "../styles/layout.css";

export default function App() {
  // Simple routing without react-router-dom for now,
  // or just render Dashboard since it's a one-screen app.
  return <div className="app-container">{routes[0].component}</div>;
}
