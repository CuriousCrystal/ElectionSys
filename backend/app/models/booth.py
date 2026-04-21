from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class BoothStatus(str, Enum):
    """Booth status enumeration"""
    smooth = "smooth"
    busy = "busy"
    critical = "critical"


class Coordinates(BaseModel):
    """Geographic coordinates"""
    latitude: float
    longitude: float


class BoothBase(BaseModel):
    """Base booth model"""
    booth_id: str
    name: str
    constituency: str
    ward: Optional[str] = None
    capacity: int = Field(..., gt=0)
    coordinates: Optional[Coordinates] = None


class BoothCreate(BoothBase):
    """Booth creation model"""
    current_voters: int = 0


class BoothUpdate(BaseModel):
    """Booth update model (all fields optional)"""
    name: Optional[str] = None
    constituency: Optional[str] = None
    ward: Optional[str] = None
    capacity: Optional[int] = None
    current_voters: Optional[int] = None
    coordinates: Optional[Coordinates] = None


class BoothResponse(BoothBase):
    """Booth response model with computed fields"""
    current_voters: int = 0
    queue_length: int = 0
    wait_time_minutes: int = 0
    status: BoothStatus = BoothStatus.smooth
    last_updated: datetime = Field(default_factory=datetime.utcnow)
