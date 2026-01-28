import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import CrimeMarker from "./CrimeMarker";
import PoliceStationMarker from "./PoliceStationMarker";
import HotspotLayer from "./HotspotLayer";
import HeatmapLayer from "./HeatmapLayer";
import { MAP_CENTER } from "../utils/constants";
import "leaflet/dist/leaflet.css";
import "../styles/map.css";
import "./Map/mapStyles.css"; // Custom marker styles

export default function MapView({ 
  crimes, 
  policeStations = [], 
  showHeatmap, 
  showHotspots,
  showPoliceStations = true 
}) {
  return (
    <div className="map-wrapper">
      <MapContainer
        center={MAP_CENTER}
        zoom={13}
        scrollWheelZoom={true}
        className="leaflet-container"
      >
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        />

        {/* Crime Markers */}
        {!showHeatmap &&
          crimes.map((crime) => <CrimeMarker key={crime.id} crime={crime} />)}

        {/* Police Station Markers */}
        {showPoliceStations &&
          policeStations.map((station) => (
            <PoliceStationMarker key={station.id} station={station} />
          ))}

        {showHotspots && <HotspotLayer crimes={crimes} />}

        {showHeatmap && <HeatmapLayer crimes={crimes} />}
      </MapContainer>
    </div>
  );
}
