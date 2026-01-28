from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Prediction
from schemas import PredictionCreate, PredictionUpdate, PredictionResponse

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])

@router.get("/", response_model=List[PredictionResponse])
async def get_all_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """Get all predictions"""
    return db.query(Prediction).offset(skip).limit(limit).all()

@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """Get prediction by ID"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

@router.post("/", response_model=PredictionResponse, status_code=201)
async def create_prediction(prediction_data: PredictionCreate, db: Session = Depends(get_db)):
    """Create a new prediction"""
    prediction = Prediction(**prediction_data.model_dump())
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction

@router.put("/{prediction_id}", response_model=PredictionResponse)
async def update_prediction(
    prediction_id: int,
    prediction_data: PredictionUpdate,
    db: Session = Depends(get_db)
):
    """Update a prediction"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    update_data = prediction_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prediction, field, value)
    
    db.commit()
    db.refresh(prediction)
    return prediction

@router.delete("/{prediction_id}")
async def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """Delete a prediction"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    db.delete(prediction)
    db.commit()
    return {"message": "Prediction deleted successfully"}

@router.get("/zone/{zone_id}", response_model=List[PredictionResponse])
async def get_predictions_by_zone(zone_id: int, db: Session = Depends(get_db)):
    """Get all predictions for a specific zone"""
    return db.query(Prediction).filter(Prediction.zone_id == zone_id).all()

@router.get("/zone/{zone_id}/latest", response_model=PredictionResponse)
async def get_latest_prediction_for_zone(zone_id: int, db: Session = Depends(get_db)):
    """Get the latest prediction for a specific zone"""
    prediction = (
        db.query(Prediction)
        .filter(Prediction.zone_id == zone_id)
        .order_by(Prediction.generated_at.desc())
        .first()
    )
    if not prediction:
        raise HTTPException(status_code=404, detail="No predictions found for this zone")
    return prediction
