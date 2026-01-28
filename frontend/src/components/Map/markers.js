import L from "leaflet";

/**
 * SVG Icons for different crime types
 * Based on Lucide React icons - optimized for small sizes
 */

const theftSVG = `
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
   viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"
   stroke-linecap="round" stroke-linejoin="round">
   <path d="M6 11v-1a4 4 0 1 1 8 0v1"/>
   <path d="M5 11h10v6H5z"/>
  </svg>
`;

const assaultSVG = `
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
   viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"
   stroke-linecap="round" stroke-linejoin="round">
   <circle cx="12" cy="13" r="3"/>
   <path d="M12 8v1m0 10v1M8 12h1m10 0h1"/>
   <path d="M10.29 3.86 1.82 18h16.36L10.29 3.86z"/>
  </svg>
`;

const accidentSVG = `
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
   viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"
   stroke-linecap="round" stroke-linejoin="round">
   <circle cx="7" cy="18" r="2"/>
   <circle cx="17" cy="18" r="2"/>
   <path d="M2 6h20v8H2z"/>
   <path d="M6 9v3m12-3v3"/>
  </svg>
`;

const defaultSVG = `
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
   viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"
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
 * Create custom Leaflet marker with crime-specific icon (SMALLER VERSION)
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
    className: "crime-marker-container",
    iconSize: [30, 30], // Reduced from 40 to 30
    iconAnchor: [15, 30],
    popupAnchor: [0, -30],
  });
};

/**
 * Create marker for hotspot zones
 */
export const createHotspotMarker = (intensity = 0.5) => {
  const opacity = Math.min(intensity, 1);
  const size = 40;

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
