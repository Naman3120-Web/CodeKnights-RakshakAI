from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class AreaType(str, Enum):
    RESIDENTIAL = "residential"
    MARKET = "market"
    HIGHWAY = "highway"
    COMMERCIAL = "commercial"   # Add this
    INDUSTRIAL = "industrial"

class ZoneBase(BaseModel):
    zone_name: str
    center_lat: float = Field(..., ge=-90, le=90)
    center_lng: float = Field(..., ge=-180, le=180)
    radius: int = Field(..., gt=0, description="Radius in meters")
    area_type: AreaType

class ZoneCreate(ZoneBase):
    pass

class ZoneUpdate(BaseModel):
    zone_name: Optional[str] = None
    center_lat: Optional[float] = None
    center_lng: Optional[float] = None
    radius: Optional[int] = None
    area_type: Optional[AreaType] = None

class ZoneResponse(ZoneBase):
    id: int
    
    class Config:
        from_attributes = True