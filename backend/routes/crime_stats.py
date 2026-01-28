from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import CrimeStat
from schemas import CrimeStatCreate, CrimeStatUpdate, CrimeStatResponse

router = APIRouter(prefix="/api/crime-stats", tags=["Crime Stats"])

@router.get("/", response_model=List[CrimeStatResponse])
async def get_all_crime_stats(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """Get all crime statistics"""
    return db.query(CrimeStat).offset(skip).limit(limit).all()

@router.get("/{stat_id}", response_model=CrimeStatResponse)
async def get_crime_stat(stat_id: int, db: Session = Depends(get_db)):
    """Get crime stat by ID"""
    stat = db.query(CrimeStat).filter(CrimeStat.id == stat_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail="Crime stat not found")
    return stat

@router.post("/", response_model=CrimeStatResponse, status_code=201)
async def create_crime_stat(stat_data: CrimeStatCreate, db: Session = Depends(get_db)):
    """Create a new crime stat"""
    stat = CrimeStat(**stat_data.model_dump())
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat

@router.put("/{stat_id}", response_model=CrimeStatResponse)
async def update_crime_stat(
    stat_id: int,
    stat_data: CrimeStatUpdate,
    db: Session = Depends(get_db)
):
    """Update a crime stat"""
    stat = db.query(CrimeStat).filter(CrimeStat.id == stat_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail="Crime stat not found")
    
    update_data = stat_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stat, field, value)
    
    db.commit()
    db.refresh(stat)
    return stat

@router.delete("/{stat_id}")
async def delete_crime_stat(stat_id: int, db: Session = Depends(get_db)):
    """Delete a crime stat"""
    stat = db.query(CrimeStat).filter(CrimeStat.id == stat_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail="Crime stat not found")
    
    db.delete(stat)
    db.commit()
    return {"message": "Crime stat deleted successfully"}

@router.get("/zone/{zone_id}", response_model=List[CrimeStatResponse])
async def get_crime_stats_by_zone(zone_id: int, db: Session = Depends(get_db)):
    """Get all crime stats for a specific zone"""
    return db.query(CrimeStat).filter(CrimeStat.zone_id == zone_id).all()
