from pydantic import BaseModel
from typing import Optional
from schemas.prediction import RiskLevel

class PatrolSuggestionBase(BaseModel):
    zone_id: int
    risk_level: RiskLevel
    suggestion_text: str
    prediction_id: int

class PatrolSuggestionCreate(PatrolSuggestionBase):
    pass

class PatrolSuggestionUpdate(BaseModel):
    zone_id: Optional[int] = None
    risk_level: Optional[RiskLevel] = None
    suggestion_text: Optional[str] = None
    prediction_id: Optional[int] = None

class PatrolSuggestionResponse(PatrolSuggestionBase):
    id: int
    
    class Config:
        from_attributes = True