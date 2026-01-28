import axios from "axios";

// Toggle this to true when you have a real backend
const USE_REAL_API = true;
const API_BASE = "http://localhost:8000/api";

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Mock data as fallback
const MOCK_DATA = [
  {
    id: 1,
    crime_type: "theft",
    latitude: 19.076,
    longitude: 72.8777,
    date_time: "2023-10-25T14:30:00",
    area_name: "Bandra West",
    zone_id: 1,
  },
  {
    id: 2,
    crime_type: "assault",
    latitude: 19.08,
    longitude: 72.88,
    date_time: "2023-10-24T09:15:00",
    area_name: "Andheri East",
    zone_id: 2,
  },
  {
    id: 3,
    crime_type: "accident",
    latitude: 19.07,
    longitude: 72.86,
    date_time: "2023-10-26T18:45:00",
    area_name: "Dadar",
    zone_id: 3,
  },
  {
    id: 4,
    crime_type: "theft",
    latitude: 19.085,
    longitude: 72.89,
    date_time: "2023-10-25T20:00:00",
    area_name: "Kurla",
    zone_id: 4,
  },
];

// ========== CRIME APIs ==========

export const fetchCrimes = async (filters = {}) => {
  if (!USE_REAL_API) {
    return new Promise((resolve) => {
      setTimeout(() => resolve(MOCK_DATA), 500);
    });
  }

  try {
    const params = {
      skip: filters.skip || 0,
      limit: filters.limit || 100,
    };
    console.log(
      "Fetching crimes from:",
      `${API_BASE}/crimes`,
      "with params:",
      params,
    );
    const response = await apiClient.get("/crimes", { params });
    console.log(
      "API Response:",
      response.status,
      response.data.length,
      "items",
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching crimes:", error);
    // Fallback to mock data on error
    return MOCK_DATA;
  }
};

export const fetchCrimeById = async (crimeId) => {
  try {
    const response = await apiClient.get(`/crimes/${crimeId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching crime ${crimeId}:`, error);
    throw error;
  }
};

export const createCrime = async (crimeData) => {
  try {
    const response = await apiClient.post("/crimes", crimeData);
    return response.data;
  } catch (error) {
    console.error("Error creating crime:", error);
    throw error;
  }
};

export const updateCrime = async (crimeId, crimeData) => {
  try {
    const response = await apiClient.put(`/crimes/${crimeId}`, crimeData);
    return response.data;
  } catch (error) {
    console.error(`Error updating crime ${crimeId}:`, error);
    throw error;
  }
};

export const deleteCrime = async (crimeId) => {
  try {
    const response = await apiClient.delete(`/crimes/${crimeId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting crime ${crimeId}:`, error);
    throw error;
  }
};

export const fetchCrimesByZone = async (zoneId) => {
  try {
    const response = await apiClient.get(`/crimes/zone/${zoneId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching crimes for zone ${zoneId}:`, error);
    throw error;
  }
};

export const fetchCrimesByType = async (crimeType) => {
  try {
    const response = await apiClient.get(`/crimes/type/${crimeType}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching crimes by type ${crimeType}:`, error);
    throw error;
  }
};

export const fetchCrimeStatsGroupedByZone = async () => {
  try {
    const response = await apiClient.get("/crimes/stats/by-zone");
    return response.data;
  } catch (error) {
    console.error("Error fetching crime stats grouped by zone:", error);
    throw error;
  }
};

// ========== ZONE APIs ==========

export const fetchZones = async (filters = {}) => {
  try {
    const params = {
      skip: filters.skip || 0,
      limit: filters.limit || 100,
    };
    const response = await apiClient.get("/zones", { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching zones:", error);
    throw error;
  }
};

export const fetchZoneById = async (zoneId) => {
  try {
    const response = await apiClient.get(`/zones/${zoneId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching zone ${zoneId}:`, error);
    throw error;
  }
};

export const createZone = async (zoneData) => {
  try {
    const response = await apiClient.post("/zones", zoneData);
    return response.data;
  } catch (error) {
    console.error("Error creating zone:", error);
    throw error;
  }
};

export const updateZone = async (zoneId, zoneData) => {
  try {
    const response = await apiClient.put(`/zones/${zoneId}`, zoneData);
    return response.data;
  } catch (error) {
    console.error(`Error updating zone ${zoneId}:`, error);
    throw error;
  }
};

export const deleteZone = async (zoneId) => {
  try {
    const response = await apiClient.delete(`/zones/${zoneId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting zone ${zoneId}:`, error);
    throw error;
  }
};

// ========== HELPER FUNCTIONS ==========

// Convert backend format to frontend format
export const transformCrimeData = (crime) => ({
  id: crime.id,
  type: crime.crime_type.charAt(0).toUpperCase() + crime.crime_type.slice(1),
  lat: crime.latitude,
  lng: crime.longitude,
  date: crime.date_time,
  location: crime.area_name,
  zoneId: crime.zone_id,
});

// Convert frontend format to backend format
export const transformCrimeToBackend = (crime) => ({
  crime_type: crime.type.toLowerCase(),
  latitude: parseFloat(crime.lat),
  longitude: parseFloat(crime.lng),
  date_time: crime.date,
  area_name: crime.location,
  zone_id: parseInt(crime.zoneId),
});

// ========== PREDICTION APIs ==========

export const fetchPredictions = async (filters = {}) => {
  try {
    const params = {
      skip: filters.skip || 0,
      limit: filters.limit || 100,
    };
    const response = await apiClient.get("/predictions", { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching predictions:", error);
    throw error;
  }
};

export const fetchPredictionById = async (predictionId) => {
  try {
    const response = await apiClient.get(`/predictions/${predictionId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching prediction ${predictionId}:`, error);
    throw error;
  }
};

export const fetchPredictionsByZone = async (zoneId) => {
  try {
    const response = await apiClient.get(`/predictions/zone/${zoneId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching predictions for zone ${zoneId}:`, error);
    throw error;
  }
};

export const fetchLatestPredictionForZone = async (zoneId) => {
  try {
    const response = await apiClient.get(`/predictions/zone/${zoneId}/latest`);
    return response.data;
  } catch (error) {
    console.error(
      `Error fetching latest prediction for zone ${zoneId}:`,
      error,
    );
    throw error;
  }
};

export const createPrediction = async (predictionData) => {
  try {
    const response = await apiClient.post("/predictions", predictionData);
    return response.data;
  } catch (error) {
    console.error("Error creating prediction:", error);
    throw error;
  }
};

// ========== PATROL SUGGESTION APIs ==========

export const fetchPatrolSuggestions = async (filters = {}) => {
  try {
    const params = {
      skip: filters.skip || 0,
      limit: filters.limit || 100,
    };
    const response = await apiClient.get("/patrol-suggestions", { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching patrol suggestions:", error);
    throw error;
  }
};

export const fetchPatrolSuggestionsByZone = async (zoneId) => {
  try {
    const response = await apiClient.get(`/patrol-suggestions/zone/${zoneId}`);
    return response.data;
  } catch (error) {
    console.error(
      `Error fetching patrol suggestions for zone ${zoneId}:`,
      error,
    );
    throw error;
  }
};

export const fetchPatrolSuggestionsByPrediction = async (predictionId) => {
  try {
    const response = await apiClient.get(
      `/patrol-suggestions/prediction/${predictionId}`,
    );
    return response.data;
  } catch (error) {
    console.error(
      `Error fetching patrol suggestions for prediction ${predictionId}:`,
      error,
    );
    throw error;
  }
};

export const createPatrolSuggestion = async (suggestionData) => {
  try {
    const response = await apiClient.post(
      "/patrol-suggestions",
      suggestionData,
    );
    return response.data;
  } catch (error) {
    console.error("Error creating patrol suggestion:", error);
    throw error;
  }
};

// ========== CRIME STATS APIs ==========

export const fetchCrimeStats = async (filters = {}) => {
  try {
    const params = {
      skip: filters.skip || 0,
      limit: filters.limit || 100,
    };
    const response = await apiClient.get("/crime-stats", { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching crime stats:", error);
    throw error;
  }
};

export const fetchCrimeStatsByZone = async (zoneId) => {
  try {
    const response = await apiClient.get(`/crime-stats/zone/${zoneId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching crime stats for zone ${zoneId}:`, error);
    throw error;
  }
};
