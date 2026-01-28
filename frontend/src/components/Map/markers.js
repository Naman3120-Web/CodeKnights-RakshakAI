import L from "leaflet";

/**
 * SVG Icons for different crime types
 * Based on Lucide React icons
 */

const theftSVG = `
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
   viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
   stroke-linecap="round" stroke-linejoin="round">
   <path d="M6 11v-1a4 4 0 1 1 8 0v1"/>
   <path d="M5 11h10v6H5z"/>
  </svg>
`;

const assaultSVG = `
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
   viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
   stroke-linecap="round" stroke-linejoin="round">
   <path d="M12 9v2m0 4h.01"/>
   <path d="M10.29 3.86 1.82 18h16.36L10.29 3.86z"/>
  </svg>
`;

const accidentSVG = `
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
   viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
   stroke-linecap="round" stroke-linejoin="round">
   <path d="M3 13l2-5h14l2 5M5 13v4h2v-4M17 13v4h2v-4"/>
  </svg>
`;

const defaultSVG = `
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
   viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
   stroke-linecap="round" stroke-linejoin="round">
   <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
  </svg>
`;

/**
 * Get SVG icon based on crime type
 */
const getSVG = (type) => {
  switch (type?.toLowerCase()) {
    case "theft":
      return theftSVG;
    case "assault":
      return assaultSVG;
    case "accident":
      return accidentSVG;
    default:
      return defaultSVG;
  }
};

/**
 * Get color based on crime type
 */
const getColorClass = (type) => {
  switch (type?.toLowerCase()) {
    case "theft":
      return "theft"; // blue
    case "assault":
      return "assault"; // red
    case "accident":
      return "accident"; // orange
    default:
      return "default"; // purple
  }
};

/**
 * Create custom Leaflet marker with crime-specific icon
 * @param {string} crimeType - Type of crime (theft, assault, accident)
 * @returns {L.DivIcon} - Leaflet DivIcon for the marker
 */
export const createCrimeMarker = (crimeType) => {
  const colorClass = getColorClass(crimeType);
  const iconHTML = `
    <div class="crime-marker ${colorClass}">
      <div class="marker-icon">
        ${getSVG(crimeType)}
      </div>
    </div>
  `;

  return L.divIcon({
    html: iconHTML,
    className: "crime-marker-container", // Empty to avoid default Leaflet styling
    iconSize: [40, 40],
    iconAnchor: [20, 40], // Point of the marker corresponds to bottom center
    popupAnchor: [0, -40], // Popup appears above the marker
  });
};

/**
 * Create marker for hotspot zones (larger, semi-transparent)
 */
export const createHotspotMarker = (intensity = 0.5) => {
  const opacity = Math.min(intensity, 1);
  const size = 48;

  const iconHTML = `
    <div class="hotspot-marker" style="opacity: ${opacity}">
      <div class="hotspot-pulse"></div>
    </div>
  `;

  return L.divIcon({
    html: iconHTML,
    className: "hotspot-marker-container",
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
};

export default createCrimeMarker;
