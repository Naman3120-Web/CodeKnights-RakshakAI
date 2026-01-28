import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import PredictionMarker from "./PredictionMarker";
import { MAP_CENTER } from "../utils/constants";
import "leaflet/dist/leaflet.css";
import "../styles/map.css";
import "./Map/mapStyles.css";

export default function PredictionMapView({ predictions }) {
  return (
    <div className="map-wrapper">
      <MapContainer
        center={MAP_CENTER}
        zoom={12}
        scrollWheelZoom={true}
        className="leaflet-container"
      >
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        />

        {predictions.map((prediction) => (
          <PredictionMarker key={prediction.id} prediction={prediction} />
        ))}
      </MapContainer>
    </div>
  );
}
