from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AlertType(str, Enum):
    """Alert type enumeration"""
    queue_overflow = "queue_overflow"
    capacity_warning = "capacity_warning"
    system_error = "system_error"
    security_concern = "security_concern"


class AlertSeverity(str, Enum):
    """Alert severity enumeration"""
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class AlertCreate(BaseModel):
    """Alert creation model"""
    booth_id: str
    alert_type: AlertType
    severity: AlertSeverity
    message: str


class AlertResponse(BaseModel):
    """Alert response model"""
    id: Optional[str] = None
    booth_id: str
    alert_type: AlertType
    severity: AlertSeverity
    message: str
    is_read: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
