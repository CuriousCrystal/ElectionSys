from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Optional
from database import get_db, ZoneSnapshot, Alert, AuditLog
from pydantic import BaseModel
from auth import get_current_active_user, UserInDB

router = APIRouter(prefix="/api/analytics", tags=["Analytics & Reporting"])

# Pydantic models
class ZoneReport(BaseModel):
    zone_name: str
    avg_density: float
    max_density: float
    min_density: float
    avg_wait_time: float
    max_wait_time: float
    total_snapshots: int

class AlertSummary(BaseModel):
    total_alerts: int
    unread_alerts: int
    alerts_by_severity: dict
    alerts_by_type: dict

class AuditLogEntry(BaseModel):
    username: str
    action: str
    details: str
    timestamp: datetime

@router.get("/zones/history")
async def get_zone_history(
    zone_name: Optional[str] = None,
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get historical zone data for the last N hours"""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(ZoneSnapshot).filter(ZoneSnapshot.timestamp >= cutoff_time)
    
    if zone_name:
        query = query.filter(ZoneSnapshot.zone_name == zone_name)
    
    snapshots = query.order_by(ZoneSnapshot.timestamp.desc()).all()
    
    return {
        "zone_name": zone_name or "all",
        "time_range_hours": hours,
        "data_points": len(snapshots),
        "snapshots": [
            {
                "zone_name": s.zone_name,
                "density": s.density,
                "wait_time": s.wait_time,
                "status": s.status,
                "timestamp": s.timestamp.isoformat()
            }
            for s in snapshots
        ]
    }

@router.get("/zones/report")
async def get_zone_report(
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Generate aggregated report for all zones"""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    zones = db.query(ZoneSnapshot.zone_name).distinct().all()
    reports = []
    
    for (zone_name,) in zones:
        stats = db.query(
            func.avg(ZoneSnapshot.density).label('avg_density'),
            func.max(ZoneSnapshot.density).label('max_density'),
            func.min(ZoneSnapshot.density).label('min_density'),
            func.avg(ZoneSnapshot.wait_time).label('avg_wait_time'),
            func.max(ZoneSnapshot.wait_time).label('max_wait_time'),
            func.count(ZoneSnapshot.id).label('total_snapshots')
        ).filter(
            ZoneSnapshot.zone_name == zone_name,
            ZoneSnapshot.timestamp >= cutoff_time
        ).first()
        
        if stats.avg_density is not None:
            reports.append({
                "zone_name": zone_name,
                "avg_density": round(stats.avg_density, 2),
                "max_density": stats.max_density,
                "min_density": stats.min_density,
                "avg_wait_time": round(stats.avg_wait_time, 2),
                "max_wait_time": stats.max_wait_time,
                "total_snapshots": stats.total_snapshots
            })
    
    return {
        "report_period_hours": hours,
        "generated_at": datetime.utcnow().isoformat(),
        "zones": reports
    }

@router.get("/alerts/summary")
async def get_alerts_summary(
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get alert summary and statistics"""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    total_alerts = db.query(Alert).filter(Alert.timestamp >= cutoff_time).count()
    unread_alerts = db.query(Alert).filter(
        Alert.timestamp >= cutoff_time,
        Alert.is_read == 0
    ).count()
    
    # Alerts by severity
    severity_counts = db.query(
        Alert.severity,
        func.count(Alert.id)
    ).filter(
        Alert.timestamp >= cutoff_time
    ).group_by(Alert.severity).all()
    
    # Alerts by type
    type_counts = db.query(
        Alert.alert_type,
        func.count(Alert.id)
    ).filter(
        Alert.timestamp >= cutoff_time
    ).group_by(Alert.alert_type).all()
    
    return {
        "time_range_hours": hours,
        "total_alerts": total_alerts,
        "unread_alerts": unread_alerts,
        "alerts_by_severity": {sev: count for sev, count in severity_counts},
        "alerts_by_type": {typ: count for typ, count in type_counts}
    }

@router.get("/alerts")
async def get_alerts(
    unread_only: bool = False,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get list of alerts"""
    query = db.query(Alert)
    
    if unread_only:
        query = query.filter(Alert.is_read == 0)
    
    alerts = query.order_by(desc(Alert.timestamp)).limit(limit).all()
    
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

@router.post("/alerts/{alert_id}/read")
async def mark_alert_read(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Mark an alert as read"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_read = 1
    db.commit()
    
    return {"message": "Alert marked as read"}

@router.get("/audit-logs")
async def get_audit_logs(
    username: Optional[str] = None,
    hours: int = 24,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get audit logs (admin only)"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(AuditLog).filter(AuditLog.timestamp >= cutoff_time)
    
    if username:
        query = query.filter(AuditLog.username == username)
    
    logs = query.order_by(desc(AuditLog.timestamp)).limit(limit).all()
    
    return {
        "count": len(logs),
        "logs": [
            {
                "id": log.id,
                "username": log.username,
                "action": log.action,
                "details": log.details,
                "timestamp": log.timestamp.isoformat()
            }
            for log in logs
        ]
    }
