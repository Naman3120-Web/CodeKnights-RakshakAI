# 🚀 Quick Start Guide - SafeCity

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- Git (optional)

---

## 🛠️ Setup Instructions

### Step 1: Backend Setup

```bash
# Navigate to backend folder
cd backend

# Install Python dependencies
pip install fastapi uvicorn sqlalchemy pydantic python-multipart

# Run the backend server
python main.py
```

**Backend will start on:** `http://localhost:8000`

**Verify it's running:**

- Open browser: `http://localhost:8000/docs` (Swagger UI)
- Or: `http://localhost:8000/health`

---

### Step 2: Import Sample Data (First Time Only)

```bash
# While in backend folder
python import_csv.py
```

This will populate your database with:

- ✅ Zones (Mumbai areas)
- ✅ Crimes (Historical data)
- ✅ Crime Statistics
- ✅ Predictions
- ✅ Patrol Suggestions

---

### Step 3: Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Frontend will start on:** `http://localhost:5173`

---

## ✅ Verify Integration

### Test 1: Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected: `{"status": "healthy", "database": "connected"}`

### Test 2: Fetch Crimes

```bash
curl http://localhost:8000/api/crimes
```

Expected: JSON array of crimes

### Test 3: Open Frontend

1. Open browser: `http://localhost:5173`
2. You should see the SafeCity dashboard
3. Crime markers should appear on the map
4. Check browser console for API calls

---

## 📁 Project Structure

```
CodeKnights-RakshakAI/
├── backend/              # FastAPI Backend
│   ├── main.py          # Entry point
│   ├── database.py      # Database connection
│   ├── models/          # SQLAlchemy models
│   ├── routes/          # API endpoints
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── csv_files/       # Sample data
│
├── frontend/            # React Frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API client
│   │   ├── hooks/       # React hooks
│   │   └── styles/      # CSS files
│   └── package.json
│
└── safecity_data/       # CSV datasets
```

---

## 🔌 API Endpoints

### Crimes

- `GET /api/crimes` - Get all crimes
- `POST /api/crimes` - Create crime
- `GET /api/crimes/{id}` - Get specific crime
- `GET /api/crimes/zone/{zone_id}` - Crimes by zone
- `GET /api/crimes/type/{type}` - Crimes by type

### Zones

- `GET /api/zones` - Get all zones
- `POST /api/zones` - Create zone
- `GET /api/zones/{id}` - Get specific zone

### Predictions

- `GET /api/predictions` - Get all predictions
- `GET /api/predictions/zone/{zone_id}` - Predictions by zone
- `GET /api/predictions/zone/{zone_id}/latest` - Latest prediction

### Patrol Suggestions

- `GET /api/patrol-suggestions` - Get all suggestions
- `GET /api/patrol-suggestions/zone/{zone_id}` - By zone
- `GET /api/patrol-suggestions/prediction/{pred_id}` - By prediction

### Crime Stats

- `GET /api/crime-stats` - Get all statistics
- `GET /api/crime-stats/zone/{zone_id}` - Stats by zone

---

## 🎯 Common Commands

### Backend

```bash
# Start server
python main.py

# Import data
python import_csv.py

# Check database
python -c "from database import engine; print(engine.table_names())"
```

### Frontend

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🐛 Troubleshooting

### Backend won't start

- ✅ Check if Python 3.8+ is installed: `python --version`
- ✅ Install missing packages: `pip install -r requirements.txt`
- ✅ Check if port 8000 is available

### Frontend won't start

- ✅ Check if Node.js is installed: `node --version`
- ✅ Delete `node_modules` and run `npm install` again
- ✅ Check if port 5173 is available

### No data showing

- ✅ Run `python import_csv.py` in backend folder
- ✅ Check backend logs for errors
- ✅ Check browser console for API errors

### CORS errors

- ✅ Verify backend is running on port 8000
- ✅ Verify frontend is running on port 5173
- ✅ Check backend CORS configuration in `main.py`

---

## 📚 Additional Resources

- **API Documentation:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Integration Guide:** See `API_INTEGRATION.md`

---

## 🎉 You're All Set!

Your SafeCity application should now be running with:

- ✅ Backend API on port 8000
- ✅ Frontend UI on port 5173
- ✅ Full integration between frontend and backend
- ✅ Sample data loaded

**Next Steps:**

1. Explore the dashboard
2. Try filtering crimes by type
3. Toggle heatmap and hotspot layers
4. Check the Insights Panel for analytics

---

**Need Help?** Check the browser console and backend terminal for detailed error messages.
