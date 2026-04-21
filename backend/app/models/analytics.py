from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BoothAnalytics(BaseModel):
    """Analytics for a single booth"""
    booth_id: str
    booth_name: str
    avg_wait_time: float = 0.0
    peak_hours: List[int] = []
    voter_throughput: int = 0
    total_voters: int = 0


class ConstituencyReport(BaseModel):
    """Report for a constituency"""
    constituency: str
    booth_count: int = 0
    total_voters: int = 0
    avg_turnout: float = 0.0
    alerts_count: int = 0


class SystemMetrics(BaseModel):
    """System-wide metrics"""
    active_booths: int = 0
    total_voters: int = 0
    total_alerts: int = 0
    critical_alerts: int = 0
    avg_wait_time: float = 0.0
