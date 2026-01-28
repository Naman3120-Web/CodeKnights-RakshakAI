from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class StationType(str, Enum):
    MAIN_STATION = "Main Station"
    TRAFFIC_DIVISION = "Traffic Division"
    CHOWKI = "Chowki (Outpost)"


class PoliceStationBase(BaseModel):
    station_name: str
    zone_id: int
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    contact_number: str
    station_type: StationType
    personnel_count: int = Field(..., ge=0)
    has_lockup: bool


class PoliceStationCreate(PoliceStationBase):
    pass


class PoliceStationUpdate(BaseModel):
    station_name: Optional[str] = None
    zone_id: Optional[int] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    contact_number: Optional[str] = None
    station_type: Optional[StationType] = None
    personnel_count: Optional[int] = Field(None, ge=0)
    has_lockup: Optional[bool] = None


class PoliceStationResponse(PoliceStationBase):
    id: int
    
    class Config:
        from_attributes = True