from sqlalchemy import Column, Integer, String, Float, Enum
from database import Base
import enum

class AreaType(str, enum.Enum):
    RESIDENTIAL = "residential"
    MARKET = "market"
    HIGHWAY = "highway"
    COMMERCIAL = "commercial"   # Add this
    INDUSTRIAL = "industrial"

class Zone(Base):
    __tablename__ = "zones"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String, unique=True, nullable=False, index=True)
    center_lat = Column(Float, nullable=False)
    center_lng = Column(Float, nullable=False)
    radius = Column(Integer, nullable=False)  # in meters
    area_type = Column(Enum(AreaType), nullable=False)