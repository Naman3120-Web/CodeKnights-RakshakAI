from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from services.crime_service import CrimeService
from schemas import CrimeCreate, CrimeUpdate, CrimeResponse
from models.crime import CrimeType

router = APIRouter(prefix="/api/crimes", tags=["Crimes"])

@router.get("/", response_model=List[CrimeResponse])
async def get_all_crimes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """Get all crimes with pagination"""
    return CrimeService.get_all(db, skip, limit)

@router.get("/{crime_id}", response_model=CrimeResponse)
async def get_crime(crime_id: int, db: Session = Depends(get_db)):
    """Get crime by ID"""
    return CrimeService.get_by_id(db, crime_id)

@router.post("/", response_model=CrimeResponse, status_code=201)
async def create_crime(crime_data: CrimeCreate, db: Session = Depends(get_db)):
    """Create new crime record"""
    return CrimeService.create(db, crime_data)

@router.put("/{crime_id}", response_model=CrimeResponse)
async def update_crime(
    crime_id: int,
    crime_data: CrimeUpdate,
    db: Session = Depends(get_db)
):
    """Update crime record"""
    return CrimeService.update(db, crime_id, crime_data)

@router.delete("/{crime_id}")
async def delete_crime(crime_id: int, db: Session = Depends(get_db)):
    """Delete crime record"""
    CrimeService.delete(db, crime_id)
    return {"message": "Crime record deleted successfully"}

# ========== Custom Endpoints ==========

@router.get("/zone/{zone_id}", response_model=List[CrimeResponse])
async def get_crimes_by_zone(zone_id: int, db: Session = Depends(get_db)):
    """Get all crimes in a zone"""
    return CrimeService.get_by_zone(db, zone_id)

@router.get("/type/{crime_type}", response_model=List[CrimeResponse])
async def get_crimes_by_type(crime_type: CrimeType, db: Session = Depends(get_db)):
    """Get crimes by type"""
    return CrimeService.get_by_type(db, crime_type)

@router.get("/stats/by-zone")
async def get_crime_stats_by_zone(db: Session = Depends(get_db)):
    """Get crime count grouped by zone"""
    return CrimeService.get_crime_count_by_zone(db)

# ========== AI/ML Endpoints ==========

@router.post("/ai/train")
async def train_ai_models(db: Session = Depends(get_db)):
    """Train AI models with current crime data"""
    return CrimeService.train_ai_models(db)

@router.get("/ai/predict-risk")
async def predict_crime_risk(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    hour: int = Query(..., ge=0, le=23),
    day: int = Query(..., ge=1, le=31),
    month: int = Query(..., ge=1, le=12),
):
    """Predict crime risk for a location and time"""
    return CrimeService.predict_crime_risk(latitude, longitude, hour, day, month)

@router.get("/ai/analyze")
async def analyze_crime_report(
    area: str = Query(...),
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    hour: int = Query(..., ge=0, le=23),
    day: int = Query(..., ge=1, le=31),
    month: int = Query(..., ge=1, le=12),
    crime_type: str = Query(...),
):
    """Full ML analysis of a crime report"""
    return CrimeService.analyze_crime_report(
        area, latitude, longitude, hour, day, month, crime_type
    )

@router.get("/ai/patrol-suggestions")
async def get_patrol_suggestions(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    area: str = Query(...),
    crime_type: str = Query(...),
):
    """Get AI-powered patrol suggestions"""
    return CrimeService.get_ai_patrol_suggestions(latitude, longitude, area, crime_type)