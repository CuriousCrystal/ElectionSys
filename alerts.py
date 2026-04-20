from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db, ZoneSnapshot, Alert
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/alerts", tags=["Alert System"])

# Alert thresholds
ALERT_THRESHOLDS = {
    "density": {
        "medium": 60,
        "high": 80,
        "critical": 95
    },
    "wait_time": {
        "medium": 10,
        "high": 20,
        "critical": 30
    }
}

def check_and_create_alerts(db: Session, zone_name: str, density: float, wait_time: int, status: str):
    """Check zone metrics and create alerts if thresholds are exceeded"""
    alerts_created = []
    
    # Check density thresholds
    if density >= ALERT_THRESHOLDS["density"]["critical"]:
        alert = Alert(
            zone_name=zone_name,
            alert_type="density",
            severity="critical",
            message=f"CRITICAL: {zone_name} density at {density}% - Immediate action required!"
        )
        db.add(alert)
        alerts_created.append(alert)
    elif density >= ALERT_THRESHOLDS["density"]["high"]:
        alert = Alert(
            zone_name=zone_name,
            alert_type="density",
            severity="high",
            message=f"HIGH: {zone_name} density at {density}% - Consider crowd control measures"
        )
        db.add(alert)
        alerts_created.append(alert)
    elif density >= ALERT_THRESHOLDS["density"]["medium"]:
        alert = Alert(
            zone_name=zone_name,
            alert_type="density",
            severity="medium",
            message=f"MEDIUM: {zone_name} density at {density}% - Monitor closely"
        )
        db.add(alert)
        alerts_created.append(alert)
    
    # Check wait time thresholds
    if wait_time >= ALERT_THRESHOLDS["wait_time"]["critical"]:
        alert = Alert(
            zone_name=zone_name,
            alert_type="wait_time",
            severity="critical",
            message=f"CRITICAL: {zone_name} wait time is {wait_time} minutes!"
        )
        db.add(alert)
        alerts_created.append(alert)
    elif wait_time >= ALERT_THRESHOLDS["wait_time"]["high"]:
        alert = Alert(
            zone_name=zone_name,
            alert_type="wait_time",
            severity="high",
            message=f"HIGH: {zone_name} wait time is {wait_time} minutes"
        )
        db.add(alert)
        alerts_created.append(alert)
    
    # Check for bottleneck status
    if status in ["Bottleneck", "Full"]:
        alert = Alert(
            zone_name=zone_name,
            alert_type="bottleneck",
            severity="high" if status == "Bottleneck" else "critical",
            message=f"{status.upper()}: {zone_name} is experiencing {status.lower()} conditions"
        )
        db.add(alert)
        alerts_created.append(alert)
    
    if alerts_created:
        db.commit()
        for alert in alerts_created:
            db.refresh(alert)
    
    return alerts_created

@router.get("/thresholds")
async def get_alert_thresholds():
    """Get current alert threshold configuration"""
    return ALERT_THRESHOLDS

@router.get("/unread-count")
async def get_unread_alert_count(
    db: Session = Depends(get_db)
):
    """Get count of unread alerts"""
    count = db.query(Alert).filter(Alert.is_read == 0).count()
    return {"unread_count": count}

@router.get("/recent")
async def get_recent_alerts(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent alerts without authentication (for dashboard display)"""
    from sqlalchemy import desc
    
    alerts = db.query(Alert).order_by(desc(Alert.timestamp)).limit(limit).all()
    
    return {
        "count": len(alerts),
        "alerts": [
            {
                "id": a.id,
                "zone_name": a.zone_name,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "message": a.message,
                "is_read": bool(a.is_read),
                "timestamp": a.timestamp.isoformat()
            }
            for a in alerts
        ]
    }
