# 🔌 API Integration Guide - SafeCity Frontend ↔️ Backend

## ✅ Integration Status: **COMPLETE**

Your frontend is now fully integrated with the FastAPI backend!

---

## 📡 Backend API Endpoints

### **Crime Endpoints** (`/api/crimes`)

| Method | Endpoint                        | Description                | Response            |
| ------ | ------------------------------- | -------------------------- | ------------------- |
| GET    | `/api/crimes`                   | Get all crimes (paginated) | `CrimeResponse[]`   |
| GET    | `/api/crimes/{id}`              | Get specific crime         | `CrimeResponse`     |
| POST   | `/api/crimes`                   | Create new crime           | `CrimeResponse`     |
| PUT    | `/api/crimes/{id}`              | Update crime               | `CrimeResponse`     |
| DELETE | `/api/crimes/{id}`              | Delete crime               | `{message: string}` |
| GET    | `/api/crimes/zone/{zone_id}`    | Crimes by zone             | `CrimeResponse[]`   |
| GET    | `/api/crimes/type/{crime_type}` | Crimes by type             | `CrimeResponse[]`   |
| GET    | `/api/crimes/stats/by-zone`     | Crime statistics           | `{zone_id: count}`  |

### **Zone Endpoints** (`/api/zones`)

| Method | Endpoint          | Description       | Response            |
| ------ | ----------------- | ----------------- | ------------------- |
| GET    | `/api/zones`      | Get all zones     | `ZoneResponse[]`    |
| GET    | `/api/zones/{id}` | Get specific zone | `ZoneResponse`      |
| POST   | `/api/zones`      | Create new zone   | `ZoneResponse`      |
| PUT    | `/api/zones/{id}` | Update zone       | `ZoneResponse`      |
| DELETE | `/api/zones/{id}` | Delete zone       | `{message: string}` |

---

## 📦 Data Models

### Backend → Frontend Transformation

**Backend Crime Model:**

```json
{
  "id": 1,
  "crime_type": "theft",
  "latitude": 19.076,
  "longitude": 72.8777,
  "date_time": "2023-10-25T14:30:00",
  "area_name": "Bandra West",
  "zone_id": 1
}
```

**Frontend Crime Model (after transformation):**

```json
{
  "id": 1,
  "type": "Theft",
  "lat": 19.076,
  "lng": 72.8777,
  "date": "2023-10-25T14:30:00",
  "location": "Bandra West",
  "zoneId": 1
}
```

---

## 🔧 Changes Made

### 1. **api.js** - Complete API Integration

- ✅ Set `USE_REAL_API = true`
- ✅ Added axios instance with proper config
- ✅ Implemented all CRUD operations for crimes
- ✅ Implemented all CRUD operations for zones
- ✅ Added data transformation helpers
- ✅ Error handling with fallback to mock data

### 2. **UseCrimeData.js** - Enhanced Hook

- ✅ Fetches real data from backend
- ✅ Transforms backend format to frontend format
- ✅ Client-side filtering for type and time range
- ✅ Error handling and loading states
- ✅ Re-fetches when filters change

### 3. **Dashboard.jsx** - Updated Controller

- ✅ Uses `useCrimeData` hook instead of mock data
- ✅ Displays loading state
- ✅ Displays error state with fallback
- ✅ Passes real data to MapView and InsightsPanel

### 4. **vite.config.js** - Proxy Configuration

- ✅ Added proxy to avoid CORS issues
- ✅ Routes `/api/*` requests to backend

---

## 🚀 How to Run

### **Step 1: Start Backend**

```bash
cd backend
python main.py
```

Backend will run on: `http://localhost:8000`

### **Step 2: Start Frontend**

```bash
cd frontend
npm run dev
```

Frontend will run on: `http://localhost:5173`

### **Step 3: Import Sample Data (if database is empty)**

```bash
cd backend
python import_csv.py
```

---

## 🧪 Testing the Integration

### Test 1: Health Check

```bash
# Browser or curl
curl http://localhost:8000/health
```

Expected: `{"status": "healthy", "database": "connected"}`

### Test 2: Fetch Crimes

```bash
curl http://localhost:8000/api/crimes
```

Expected: Array of crime objects

### Test 3: Frontend Loading

1. Open `http://localhost:5173`
2. Check browser console for API calls
3. Verify crime markers appear on map

---

## 📝 Usage Examples

### Fetching Crimes with Filters

```javascript
import { fetchCrimes } from "./services/api";

const crimes = await fetchCrimes({
  skip: 0,
  limit: 50,
});
```

### Creating a New Crime

```javascript
import { createCrime, transformCrimeToBackend } from "./services/api";

const newCrime = {
  type: "Theft",
  lat: 19.076,
  lng: 72.8777,
  date: new Date().toISOString(),
  location: "Bandra West",
  zoneId: 1,
};

const result = await createCrime(transformCrimeToBackend(newCrime));
```

### Fetching Zones

```javascript
import { fetchZones } from "./services/api";

const zones = await fetchZones();
```

---

## 🐛 Troubleshooting

### Issue: CORS Error

**Solution:** Make sure backend allows `http://localhost:5173` in CORS origins (already configured)

### Issue: Connection Refused

**Solution:**

1. Check if backend is running on port 8000
2. Check if frontend proxy is configured (already done)

### Issue: Empty Data

**Solution:** Run `python import_csv.py` in backend folder to populate database

### Issue: "Failed to load crime data"

**Solution:**

1. Check backend is running
2. Check browser console for detailed error
3. Frontend will fallback to mock data automatically

---

## 🎯 Next Steps

### Immediate Enhancements

- [ ] Add real-time updates using WebSockets
- [ ] Implement predictions API endpoint
- [ ] Add patrol suggestions API
- [ ] Create crime statistics dashboard

### Advanced Features

- [ ] Add authentication (JWT)
- [ ] Implement role-based access control
- [ ] Add crime heatmap data aggregation
- [ ] Create export functionality (CSV/PDF)

---

## 📚 API Documentation

### Interactive API Docs

Once backend is running, visit:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 🔐 Security Notes

**Current Setup (Development):**

- No authentication required
- CORS enabled for localhost
- SQLite database

**Production Recommendations:**

- Add JWT authentication
- Use PostgreSQL/MySQL
- Enable HTTPS
- Restrict CORS origins
- Add rate limiting
- Implement API keys

---

## 📊 Data Flow

```
User Action (Filter/Search)
    ↓
Dashboard Component
    ↓
useCrimeData Hook
    ↓
api.js (fetchCrimes)
    ↓
Axios Request → Backend (/api/crimes)
    ↓
FastAPI Route (crimes.py)
    ↓
CrimeService (crime_service.py)
    ↓
Database Query (SQLAlchemy)
    ↓
Response (JSON)
    ↓
Transform Data (transformCrimeData)
    ↓
Update React State
    ↓
Re-render Map & Insights
```

---

## ✨ Key Features Implemented

✅ **Full CRUD Operations** - Create, Read, Update, Delete for crimes and zones  
✅ **Data Transformation** - Automatic conversion between backend and frontend formats  
✅ **Error Handling** - Graceful fallbacks and error messages  
✅ **Loading States** - User feedback during API calls  
✅ **Filtering** - Client and server-side filtering  
✅ **Pagination** - Support for large datasets  
✅ **Type Safety** - Consistent data models

---

## 📞 Support

For issues or questions:

1. Check browser console for errors
2. Check backend terminal for API logs
3. Verify database has data (`python import_csv.py`)
4. Review this documentation

---

**Status:** ✅ Ready for Development & Testing  
**Last Updated:** January 28, 2026
