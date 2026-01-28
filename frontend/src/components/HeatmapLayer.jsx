import React, { useEffect } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";
// If you install 'leaflet.heat', you would import it here.
// import 'leaflet.heat';

export default function HeatmapLayer({ crimes }) {
  const map = useMap();

  useEffect(() => {
    // Placeholder logic since leaflet.heat might not be installed
    // If you have the library, utilize L.heatLayer here.
    const message = L.control({ position: "topright" });

    message.onAdd = () => {
      const div = L.DomUtil.create("div", "info legend");
      div.style.backgroundColor = "white";
      div.style.padding = "5px 10px";
      div.style.border = "1px solid #ccc";
      div.innerHTML = '<span style="color:red">🔥 Heatmap Mode Active</span>';
      return div;
    };

    message.addTo(map);

    return () => {
      map.removeControl(message);
    };
  }, [map]);

  return null;
}
