# 🎨 Visual Architecture Guide

## System Overview

```
┌───────────────────────────────────────────────────────────────┐
│                         USER BROWSER                           │
│                     http://localhost:5173                      │
└───────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Requests
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                     REACT FRONTEND (Vite)                      │
├───────────────────────────────────────────────────────────────┤
│  Components:                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Dashboard  │  │   Sidebar   │  │   MapView   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│         │                 │                 │                  │
│         └─────────────────┴─────────────────┘                 │
│                           │                                    │
│  Custom Hook:             ▼                                    │
│  ┌───────────────────────────────────────┐                    │
│  │      useCrimeData(filters)            │                    │
│  │  - Fetches data from backend          │                    │
│  │  - Transforms data format             │                    │
│  │  - Manages loading/error states       │                    │
│  └───────────────────────────────────────┘                    │
│                           │                                    │
│  API Service:             ▼                                    │
│  ┌───────────────────────────────────────┐                    │
│  │         api.js (Axios Client)         │                    │
│  │  - fetchCrimes()                      │                    │
│  │  - fetchZones()                       │                    │
│  │  - fetchPredictions()                 │                    │
│  │  - transformCrimeData()               │                    │
│  └───────────────────────────────────────┘                    │
└───────────────────────────────────────────────────────────────┘
                              │
                              │ /api/* requests
                              │ (proxied by Vite)
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND (Uvicorn)                    │
│                     http://localhost:8000                      │
├───────────────────────────────────────────────────────────────┤
│  Main App:                                                     │
│  ┌───────────────────────────────────────┐                    │
│  │           main.py                     │                    │
│  │  - CORS middleware                    │                    │
│  │  - Router registration                │                    │
│  │  - Health endpoints                   │                    │
│  └───────────────────────────────────────┘                    │
│                           │                                    │
│  API Routes:              ▼                                    │
│  ┌─────────────┬─────────────┬─────────────┐                 │
│  │ crimes.py   │  zones.py   │predictions.py│                │
│  │             │             │              │                 │
│  │ GET/POST/   │ GET/POST/   │ GET/POST/    │                │
│  │ PUT/DELETE  │ PUT/DELETE  │ PUT/DELETE   │                │
│  └─────────────┴─────────────┴─────────────┘                 │
│                           │                                    │
│  Services:                ▼                                    │
│  ┌───────────────────────────────────────┐                    │
│  │      CrimeService (Business Logic)    │                    │
│  │  - get_all() / get_by_id()            │                    │
│  │  - create() / update() / delete()     │                    │
│  │  - get_by_zone() / get_by_type()      │                    │
│  └───────────────────────────────────────┘                    │
│                           │                                    │
│  Models (SQLAlchemy):     ▼                                    │
│  ┌─────────────┬─────────────┬─────────────┐                 │
│  │  Crime      │    Zone     │ Prediction  │                 │
│  │  CrimeStat  │ PatrolSugg. │             │                 │
│  └─────────────┴─────────────┴─────────────┘                 │
│                           │                                    │
│  Schemas (Pydantic):      │                                    │
│  ┌───────────────────────────────────────┐                    │
│  │  Input Validation & Serialization     │                    │
│  │  - CrimeCreate / CrimeResponse        │                    │
│  │  - ZoneCreate / ZoneResponse          │                    │
│  └───────────────────────────────────────┘                    │
└───────────────────────────────────────────────────────────────┘
                              │
                              │ SQL Queries
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                    SQLite DATABASE                             │
│                     rakshak_ai.db                              │
├───────────────────────────────────────────────────────────────┤
│  Tables:                                                       │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐   │
│  │   crimes    │    zones    │ predictions │ crime_stats │   │
│  │             │             │             │             │   │
│  │ - id        │ - id        │ - id        │ - id        │   │
│  │ - type      │ - name      │ - zone_id   │ - zone_id   │   │
│  │ - lat/lng   │ - center    │ - risk      │ - type      │   │
│  │ - date      │ - radius    │ - score     │ - count     │   │
│  │ - zone_id   │ - type      │ - month     │ - dates     │   │
│  └─────────────┴─────────────┴─────────────┴─────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

---

## Data Flow Example: Fetching Crimes

```
1. USER clicks "Show All Crimes" in UI
        ↓
2. React Dashboard Component
   - Calls useCrimeData({ crimeType: "All" })
        ↓
3. useCrimeData Hook
   - useEffect triggers on mount
   - Calls fetchCrimes(filters)
        ↓
4. api.js Service
   - axios.get('http://localhost:8000/api/crimes')
   - Adds pagination params: { skip: 0, limit: 100 }
        ↓
5. Vite Dev Server (Proxy)
   - Forwards /api/* to backend
        ↓
6. FastAPI Backend (main.py)
   - CORS middleware validates origin
   - Routes request to crimes router
        ↓
7. routes/crimes.py
   - @router.get("/")
   - Calls CrimeService.get_all(db, skip, limit)
        ↓
8. services/crime_service.py
   - db.query(Crime).offset(skip).limit(limit).all()
        ↓
9. SQLAlchemy ORM
   - Generates SQL: SELECT * FROM crimes LIMIT 100
   - Executes against SQLite database
        ↓
10. Database Returns Rows
        ↓
11. SQLAlchemy Maps to Crime Objects
        ↓
12. Pydantic Schema (CrimeResponse)
    - Validates and serializes to JSON
        ↓
13. FastAPI Returns JSON Response
    - [{ id: 1, crime_type: "theft", ... }, ...]
        ↓
14. api.js Receives Response
    - Maps crimes with transformCrimeData()
    - Converts: crime_type → type, latitude → lat
        ↓
15. useCrimeData Hook
    - setData(transformedData)
    - setLoading(false)
        ↓
16. React Re-renders
    - Dashboard passes crimes to MapView
    - MapView renders crime markers
    - InsightsPanel shows statistics
        ↓
17. USER sees updated map with crime markers ✅
```

---

## Component Hierarchy

```
App
└── Dashboard
    ├── TopBar
    ├── Sidebar
    │   ├── Crime Type Filter
    │   ├── Time Range Filter
    │   ├── Heatmap Toggle
    │   ├── Hotspot Toggle
    │   └── Reset Button
    ├── MapView
    │   ├── Leaflet Map
    │   ├── CrimeMarker (multiple)
    │   ├── HeatmapLayer (optional)
    │   └── HotSpotLayer (optional)
    └── InsightsPanel
        ├── Total Crimes Count
        ├── Most Common Crime Type
        └── Peak Crime Time
```

---

## API Request/Response Flow

### Example 1: GET Crimes

**Request:**

```http
GET http://localhost:8000/api/crimes?skip=0&limit=100
Headers:
  Content-Type: application/json
  Origin: http://localhost:5173
```

**Backend Processing:**

```python
1. CORS Middleware: Validates origin ✓
2. Route Handler: crimes.router.get("/")
3. Dependency: Depends(get_db) → Creates DB session
4. Service Call: CrimeService.get_all(db, 0, 100)
5. Database Query: SELECT * FROM crimes LIMIT 100
6. Schema Validation: List[CrimeResponse]
7. JSON Serialization
```

**Response:**

```json
[
  {
    "id": 1,
    "crime_type": "theft",
    "latitude": 19.076,
    "longitude": 72.8777,
    "date_time": "2024-01-25T14:30:00",
    "area_name": "Bandra West",
    "zone_id": 1
  },
  ...
]
```

**Frontend Processing:**

```javascript
1. axios receives response
2. transformCrimeData() converts fields
3. useCrimeData sets state
4. React re-renders with new data
```

---

## Database Schema Relationships

```
┌─────────────┐         ┌─────────────┐
│    zones    │◄────────│   crimes    │
│             │ 1     * │             │
│ id          │         │ id          │
│ zone_name   │         │ crime_type  │
│ center_lat  │         │ latitude    │
│ center_lng  │         │ longitude   │
│ radius      │         │ zone_id (FK)│
│ area_type   │         │ date_time   │
└─────────────┘         └─────────────┘
      │
      │ 1
      │
      │ *
┌─────────────┐
│ predictions │
│             │
│ id          │
│ zone_id (FK)│
│ risk_level  │
│ risk_score  │
└─────────────┘
      │
      │ 1
      │
      │ *
┌─────────────────────┐
│ patrol_suggestions  │
│                     │
│ id                  │
│ zone_id (FK)        │
│ prediction_id (FK)  │
│ suggestion_text     │
└─────────────────────┘
```

---

## Frontend State Management

```
┌─────────────────────────────────────────┐
│         Dashboard Component             │
│                                         │
│  State:                                 │
│  ┌─────────────────────────────────┐   │
│  │ filters: {                      │   │
│  │   crimeType: "All",             │   │
│  │   timeRange: "24h"              │   │
│  │ }                               │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ toggles: {                      │   │
│  │   showHeatmap: false,           │   │
│  │   showHotspots: true            │   │
│  │ }                               │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Custom Hook:                           │
│  ┌─────────────────────────────────┐   │
│  │ useCrimeData(filters) {         │   │
│  │   crimes: [...],                │   │
│  │   loading: false,               │   │
│  │   error: null                   │   │
│  │ }                               │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
         │           │           │
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌──────────┐
    │Sidebar │  │MapView │  │ Insights │
    └────────┘  └────────┘  └──────────┘
```

---

## Error Handling Flow

```
Frontend Error Handling:
┌─────────────────────────────────────────┐
│  API Call (api.js)                      │
│  try {                                  │
│    response = await axios.get(...)     │
│  } catch (error) {                      │
│    console.error(...)                   │
│    return MOCK_DATA // Fallback        │
│  }                                      │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Hook (useCrimeData.js)                 │
│  try {                                  │
│    data = await fetchCrimes()          │
│  } catch (err) {                        │
│    setError("Failed to load...")       │
│    setData([])                          │
│  }                                      │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Component (Dashboard.jsx)              │
│  {loading && <LoadingSpinner />}        │
│  {error && <ErrorMessage />}            │
│  {!loading && !error && <MapView />}    │
└─────────────────────────────────────────┘
```

---

## Development Workflow

```
┌─────────────┐
│  Terminal 1 │
│             │
│  Backend    │
│             │
│  $ cd backend
│  $ python main.py
│             │
│  Running on │
│  :8000      │
└─────────────┘

┌─────────────┐
│  Terminal 2 │
│             │
│  Frontend   │
│             │
│  $ cd frontend
│  $ npm run dev
│             │
│  Running on │
│  :5173      │
└─────────────┘

┌─────────────┐
│  Browser    │
│             │
│  localhost: │
│  5173       │
│             │
│  DevTools:  │
│  - Network  │
│  - Console  │
└─────────────┘

┌─────────────┐
│  API Docs   │
│             │
│  localhost: │
│  8000/docs  │
│             │
│  Swagger UI │
│  Interactive│
└─────────────┘
```

---

## File Organization

```
backend/
├── main.py              ← Entry point, CORS, routing
├── database.py          ← DB connection, session
├── requirements.txt     ← Python dependencies
│
├── models/              ← SQLAlchemy ORM
│   ├── crime.py        ← Crime table definition
│   ├── zone.py         ← Zone table definition
│   └── ...
│
├── routes/              ← API endpoints
│   ├── crimes.py       ← /api/crimes/*
│   ├── zones.py        ← /api/zones/*
│   └── ...
│
├── schemas/             ← Pydantic validation
│   ├── crime.py        ← CrimeCreate, CrimeResponse
│   └── ...
│
└── services/            ← Business logic
    └── crime_service.py ← CRUD operations

frontend/
├── src/
│   ├── main.jsx         ← React entry point
│   ├── App.jsx          ← Root component
│   │
│   ├── components/      ← Reusable UI
│   │   ├── MapView.jsx
│   │   ├── Sidebar.jsx
│   │   └── ...
│   │
│   ├── pages/           ← Page components
│   │   └── Dashboard.jsx
│   │
│   ├── services/        ← API client
│   │   └── api.js      ← Axios HTTP calls
│   │
│   ├── hooks/           ← Custom hooks
│   │   └── UseCrimeData.js
│   │
│   └── styles/          ← CSS files
│
└── vite.config.js       ← Vite config, proxy
```

---

This visual guide should help you understand how all the pieces fit together! 🎨
