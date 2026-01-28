from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import PatrolSuggestion
from schemas import PatrolSuggestionCreate, PatrolSuggestionUpdate, PatrolSuggestionResponse

router = APIRouter(prefix="/api/patrol-suggestions", tags=["Patrol Suggestions"])

@router.get("/", response_model=List[PatrolSuggestionResponse])
async def get_all_patrol_suggestions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """Get all patrol suggestions"""
    return db.query(PatrolSuggestion).offset(skip).limit(limit).all()

@router.get("/{suggestion_id}", response_model=PatrolSuggestionResponse)
async def get_patrol_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    """Get patrol suggestion by ID"""
    suggestion = db.query(PatrolSuggestion).filter(PatrolSuggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Patrol suggestion not found")
    return suggestion

@router.post("/", response_model=PatrolSuggestionResponse, status_code=201)
async def create_patrol_suggestion(
    suggestion_data: PatrolSuggestionCreate,
    db: Session = Depends(get_db)
):
    """Create a new patrol suggestion"""
    suggestion = PatrolSuggestion(**suggestion_data.model_dump())
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)
    return suggestion

@router.put("/{suggestion_id}", response_model=PatrolSuggestionResponse)
async def update_patrol_suggestion(
    suggestion_id: int,
    suggestion_data: PatrolSuggestionUpdate,
    db: Session = Depends(get_db)
):
    """Update a patrol suggestion"""
    suggestion = db.query(PatrolSuggestion).filter(PatrolSuggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Patrol suggestion not found")
    
    update_data = suggestion_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(suggestion, field, value)
    
    db.commit()
    db.refresh(suggestion)
    return suggestion

@router.delete("/{suggestion_id}")
async def delete_patrol_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    """Delete a patrol suggestion"""
    suggestion = db.query(PatrolSuggestion).filter(PatrolSuggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Patrol suggestion not found")
    
    db.delete(suggestion)
    db.commit()
    return {"message": "Patrol suggestion deleted successfully"}

@router.get("/zone/{zone_id}", response_model=List[PatrolSuggestionResponse])
async def get_patrol_suggestions_by_zone(zone_id: int, db: Session = Depends(get_db)):
    """Get all patrol suggestions for a specific zone"""
    return db.query(PatrolSuggestion).filter(PatrolSuggestion.zone_id == zone_id).all()

@router.get("/prediction/{prediction_id}", response_model=List[PatrolSuggestionResponse])
async def get_patrol_suggestions_by_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    """Get all patrol suggestions for a specific prediction"""
    return db.query(PatrolSuggestion).filter(
        PatrolSuggestion.prediction_id == prediction_id
    ).all()
