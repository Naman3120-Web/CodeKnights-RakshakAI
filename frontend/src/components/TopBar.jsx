import React from "react";
import { Shield, User, MapPin } from "lucide-react";

export default function TopBar() {
  return (
    <header className="top-bar">
      <div className="brand">
        <Shield size={24} />
        <h1>RakshakAI</h1>
      </div>
      <div className="city-selector">
        <MapPin size={16} /> Mumbai, MH
      </div>
      <div className="user-profile">
        <User size={20} />
      </div>
    </header>
  );
}
