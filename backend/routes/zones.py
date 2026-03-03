from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Zone
from schemas import ZoneCreate, ZoneUpdate, ZoneResponse

router = APIRouter(prefix="/api/zones", tags=["Zones"])

@router.get("", response_model=List[ZoneResponse])
async def get_all_zones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """Get all zones"""
    return db.query(Zone).offset(skip).limit(limit).all()

@router.get("/{zone_id}", response_model=ZoneResponse)
async def get_zone(zone_id: int, db: Session = Depends(get_db)):
    """Get zone by ID"""
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone

@router.post("", response_model=ZoneResponse, status_code=201)
async def create_zone(zone_data: ZoneCreate, db: Session = Depends(get_db)):
    """Create a new zone"""
    zone = Zone(**zone_data.model_dump())
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone

@router.put("/{zone_id}", response_model=ZoneResponse)
async def update_zone(
    zone_id: int, 
    zone_data: ZoneUpdate, 
    db: Session = Depends(get_db)
):
    """Update a zone"""
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    update_data = zone_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(zone, field, value)
    
    db.commit()
    db.refresh(zone)
    return zone

@router.delete("/{zone_id}")
async def delete_zone(zone_id: int, db: Session = Depends(get_db)):
    """Delete a zone"""
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    db.delete(zone)
    db.commit()
    return {"message": "Zone deleted successfully"}