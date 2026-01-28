from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.police_stations import PoliceStation, StationType
from schemas.police_stations import (
    PoliceStationCreate, 
    PoliceStationUpdate, 
    PoliceStationResponse
)

router = APIRouter(prefix="/api/police-stations", tags=["Police Stations"])


@router.get("/", response_model=List[PoliceStationResponse])
async def get_all_stations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """Get all police stations with pagination"""
    return db.query(PoliceStation).offset(skip).limit(limit).all()


@router.get("/{station_id}", response_model=PoliceStationResponse)
async def get_station(station_id: int, db: Session = Depends(get_db)):
    """Get police station by ID"""
    station = db.query(PoliceStation).filter(PoliceStation.id == station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail="Police station not found")
    return station


@router.post("/", response_model=PoliceStationResponse, status_code=201)
async def create_station(
    station_data: PoliceStationCreate, 
    db: Session = Depends(get_db)
):
    """Create new police station"""
    station = PoliceStation(**station_data.model_dump())
    db.add(station)
    db.commit()
    db.refresh(station)
    return station


@router.put("/{station_id}", response_model=PoliceStationResponse)
async def update_station(
    station_id: int,
    station_data: PoliceStationUpdate,
    db: Session = Depends(get_db)
):
    """Update police station"""
    station = db.query(PoliceStation).filter(PoliceStation.id == station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail="Police station not found")
    
    update_data = station_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(station, field, value)
    
    db.commit()
    db.refresh(station)
    return station


@router.delete("/{station_id}")
async def delete_station(station_id: int, db: Session = Depends(get_db)):
    """Delete police station"""
    station = db.query(PoliceStation).filter(PoliceStation.id == station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail="Police station not found")
    
    db.delete(station)
    db.commit()
    return {"message": "Police station deleted successfully"}


# ========== Custom Endpoints ==========

@router.get("/zone/{zone_id}", response_model=List[PoliceStationResponse])
async def get_stations_by_zone(zone_id: int, db: Session = Depends(get_db)):
    """Get all police stations in a zone"""
    return db.query(PoliceStation).filter(PoliceStation.zone_id == zone_id).all()


@router.get("/type/{station_type}", response_model=List[PoliceStationResponse])
async def get_stations_by_type(station_type: StationType, db: Session = Depends(get_db)):
    """Get police stations by type"""
    return db.query(PoliceStation).filter(PoliceStation.station_type == station_type).all()


@router.get("/nearby/", response_model=List[PoliceStationResponse])
async def get_nearby_stations(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(5.0, gt=0),
    db: Session = Depends(get_db)
):
    """Get police stations within a radius"""
    lat_range = radius_km / 111.0
    lng_range = radius_km / 85.0  # Approximate for Mumbai's latitude
    
    return db.query(PoliceStation).filter(
        PoliceStation.latitude.between(latitude - lat_range, latitude + lat_range),
        PoliceStation.longitude.between(longitude - lng_range, longitude + lng_range)
    ).all()