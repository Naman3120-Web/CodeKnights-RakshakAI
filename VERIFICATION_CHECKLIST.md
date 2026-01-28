# ✅ Integration Verification Checklist

Use this checklist to verify that your SafeCity application is fully integrated and working correctly.

---

## 🔍 Pre-Flight Checks

### 1. Prerequisites Installed

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Git installed (optional)

---

## 🎯 Backend Verification

### 2. Backend Setup

- [ ] Navigate to `backend` folder
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] No errors during installation

### 3. Database Setup

- [ ] Run: `python import_csv.py`
- [ ] See success messages for data import
- [ ] File `rakshak_ai.db` created in backend folder

### 4. Backend Server

- [ ] Run: `python main.py`
- [ ] See message: `Uvicorn running on http://localhost:8000`
- [ ] No error messages in terminal

### 5. Backend API Tests

#### Health Check

- [ ] Open browser: `http://localhost:8000`
- [ ] See: `{"status": "ok", "message": "Rakshak AI Backend"}`

#### Health Endpoint

- [ ] Open browser: `http://localhost:8000/health`
- [ ] See: `{"status": "healthy", "database": "connected"}`

#### API Documentation

- [ ] Open browser: `http://localhost:8000/docs`
- [ ] See interactive Swagger UI
- [ ] All endpoints listed (crimes, zones, predictions, etc.)

#### Test Endpoints Manually

```bash
# In a new terminal
curl http://localhost:8000/api/crimes
curl http://localhost:8000/api/zones
curl http://localhost:8000/api/predictions
```

- [ ] All return JSON data (not empty arrays)
- [ ] No error messages

#### Run Automated Tests

```bash
cd backend
python test_api.py
```

- [ ] All tests pass (✅ symbols)
- [ ] Test summary shows X/X tests passed

---

## 🎨 Frontend Verification

### 6. Frontend Setup

- [ ] Navigate to `frontend` folder
- [ ] Run: `npm install`
- [ ] No errors during installation
- [ ] `node_modules` folder created

### 7. Configuration Check

- [ ] Open `frontend/src/services/api.js`
- [ ] Verify: `USE_REAL_API = true`
- [ ] Verify: `API_BASE = "http://localhost:8000/api"`

### 8. Frontend Server

- [ ] Run: `npm run dev`
- [ ] See message: `Local: http://localhost:5173/`
- [ ] No error messages in terminal

### 9. Application Load

- [ ] Open browser: `http://localhost:5173`
- [ ] Page loads successfully
- [ ] No blank screen
- [ ] See SafeCity interface

---

## 🔌 Integration Tests

### 10. Browser Console Check

- [ ] Open browser DevTools (F12)
- [ ] Go to Console tab
- [ ] No red error messages
- [ ] See success messages for API calls

### 11. Network Activity

- [ ] Open DevTools → Network tab
- [ ] Refresh page
- [ ] See requests to `/api/crimes`
- [ ] Status: 200 OK
- [ ] Response type: json
- [ ] Response has data (not empty)

### 12. Visual Verification

#### Map Component

- [ ] Map is visible and centered
- [ ] Crime markers appear on map
- [ ] Can click on markers
- [ ] Popup shows crime details

#### Sidebar Component

- [ ] Crime type dropdown works
- [ ] Time range filter works
- [ ] Toggle switches respond to clicks
- [ ] Reset button works

#### Insights Panel

- [ ] Shows total crimes count
- [ ] Shows most common crime type
- [ ] Statistics update when filters change

---

## 🎯 Functional Tests

### 13. Filtering

- [ ] Change crime type to "Theft"
- [ ] Map updates to show only theft crimes
- [ ] Insights panel updates
- [ ] Change to "All" - all crimes show again

### 14. Time Range

- [ ] Change time range to "7 days"
- [ ] Crime count changes
- [ ] Map updates accordingly

### 15. Toggles

- [ ] Click "Show Heatmap"
- [ ] Heatmap layer appears
- [ ] Click again - heatmap disappears
- [ ] Same for hotspots toggle

### 16. Loading States

- [ ] Hard refresh page (Ctrl+Shift+R)
- [ ] See "Loading crime data..." message
- [ ] Loading disappears when data loads
- [ ] Map renders with data

---

## 🐛 Error Handling Tests

### 17. Backend Down Test

- [ ] Stop backend server (Ctrl+C)
- [ ] Refresh frontend
- [ ] See error message OR fallback to mock data
- [ ] No application crash

### 18. Recovery Test

- [ ] Start backend server again
- [ ] Refresh frontend
- [ ] Data loads successfully
- [ ] Everything works normally

---

## 📊 Data Verification

### 19. Database Content

```bash
# In backend folder
python -c "from database import SessionLocal; from models import Crime, Zone; db = SessionLocal(); print(f'Crimes: {db.query(Crime).count()}'); print(f'Zones: {db.query(Zone).count()}')"
```

- [ ] Shows crime count > 0
- [ ] Shows zone count > 0

### 20. API Data Consistency

- [ ] Count crimes in browser UI
- [ ] Check same count in database
- [ ] Numbers match (or close if filtering applied)

---

## 🔐 Security Checks

### 21. CORS Configuration

- [ ] Backend `main.py` includes `http://localhost:5173` in origins
- [ ] Frontend requests work without CORS errors
- [ ] Check browser console for CORS messages (should be none)

### 22. Input Validation

```bash
# Try to create invalid crime
curl -X POST http://localhost:8000/api/crimes \
  -H "Content-Type: application/json" \
  -d '{"crime_type": "invalid_type"}'
```

- [ ] Returns 422 Validation Error
- [ ] Error message explains the issue

---

## 📚 Documentation Check

### 23. Files Present

- [ ] `README.md` exists at root
- [ ] `QUICKSTART.md` exists
- [ ] `API_INTEGRATION.md` exists
- [ ] `INTEGRATION_SUMMARY.md` exists
- [ ] `ARCHITECTURE.md` exists
- [ ] `backend/requirements.txt` exists
- [ ] `backend/test_api.py` exists

### 24. Documentation Accuracy

- [ ] README instructions work
- [ ] API endpoints match documentation
- [ ] File structure matches documentation

---

## 🚀 Performance Check

### 25. Load Time

- [ ] Page loads in < 3 seconds
- [ ] Initial data fetch in < 2 seconds
- [ ] Map renders smoothly

### 26. Responsiveness

- [ ] Filter changes update immediately
- [ ] No lag when clicking toggles
- [ ] Smooth map interactions (pan, zoom)

---

## 🎉 Final Verification

### 27. Complete User Flow

1. [ ] Open application
2. [ ] See crimes on map
3. [ ] Change filter to "Assault"
4. [ ] Only assault crimes show
5. [ ] Check insights panel - reflects filter
6. [ ] Toggle heatmap on
7. [ ] See heatmap overlay
8. [ ] Reset filters
9. [ ] All crimes show again
10. [ ] Everything works smoothly

### 28. Multi-Tab Test

- [ ] Open app in two browser tabs
- [ ] Both work independently
- [ ] Both fetch data successfully

---

## 📋 Troubleshooting Reference

### If Backend Won't Start:

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### If Frontend Won't Start:

```bash
rm -rf node_modules
rm package-lock.json
npm cache clean --force
npm install
```

### If No Data Shows:

```bash
cd backend
python import_csv.py
```

### If CORS Errors Appear:

- Verify backend is on port 8000
- Verify frontend is on port 5173
- Check `backend/main.py` CORS origins

---

## ✅ Success Criteria

**You have successfully integrated frontend and backend if:**

✅ Backend server runs on port 8000 without errors  
✅ Frontend server runs on port 5173 without errors  
✅ Browser shows map with crime markers  
✅ Filters update the map and insights  
✅ No CORS errors in browser console  
✅ API test suite passes all tests  
✅ Data flows from database → backend → frontend → UI

---

## 🎊 Completion Checklist

Mark these when fully verified:

- [ ] All backend tests passing
- [ ] All frontend components rendering
- [ ] Data fetching working
- [ ] Filters working
- [ ] Toggles working
- [ ] No console errors
- [ ] Documentation complete
- [ ] Test suite runs successfully

---

**When all items are checked, your integration is COMPLETE! 🎉**

---

## 📞 If Something Fails

1. Check which section failed
2. Review the specific step
3. Check terminal/console for error messages
4. Consult relevant documentation file
5. Ensure both servers are running
6. Verify database has data

---

**Last Updated**: January 28, 2026  
**Status**: Ready for verification
