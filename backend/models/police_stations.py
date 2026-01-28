from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum


class StationType(str, enum.Enum):
    MAIN_STATION = "Main Station"
    TRAFFIC_DIVISION = "Traffic Division"
    CHOWKI = "Chowki (Outpost)"


class PoliceStation(Base):
    __tablename__ = "police_stations"
    
    id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String, unique=True, nullable=False, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    contact_number = Column(String, nullable=False)
    station_type = Column(Enum(StationType), nullable=False)
    personnel_count = Column(Integer, nullable=False)
    has_lockup = Column(Boolean, nullable=False, default=False)
    
    # Relationship
    zone = relationship("Zone", backref="police_stations")