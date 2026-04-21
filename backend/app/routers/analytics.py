from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import datetime, timedelta
from app.models.analytics import SystemMetrics
from app.services import alert_service
from app.database import get_collection
from app.routers.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/system", response_model=SystemMetrics)
async def get_system_metrics(current_user = Depends(get_current_user)):
    """Get system-wide metrics"""
    booths_collection = get_collection("booths")
    alerts_collection = get_collection("alerts")
    
    # Get booth metrics
    total_booths = await booths_collection.count_documents({})
    active_booths = await booths_collection.count_documents({"status": {"$ne": "critical"}})
    
    # Get voter metrics
    booths = await booths_collection.find().to_list(length=None)
    total_voters = sum(booth.get("current_voters", 0) for booth in booths)
    avg_wait = sum(booth.get("wait_time_minutes", 0) for booth in booths) / max(1, len(booths))
    
    # Get alert metrics
    total_alerts = await alerts_collection.count_documents({})
    critical_alerts = await alerts_collection.count_documents({"severity": "critical"})
    
    return SystemMetrics(
        active_booths=active_booths,
        total_voters=total_voters,
        total_alerts=total_alerts,
        critical_alerts=critical_alerts,
        avg_wait_time=round(avg_wait, 2)
    )


@router.get("/booths/history")
async def get_booth_history(
    booth_id: Optional[str] = None,
    hours: int = 24,
    current_user = Depends(get_current_user)
):
    """Get historical booth data"""
    snapshots_collection = get_collection("analytics_snapshots")
    
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    query = {"timestamp": {"$gte": cutoff_time}}
    
    if booth_id:
        query["booth_id"] = booth_id
    
    cursor = snapshots_collection.find(query).sort("timestamp", -1)
    snapshots = await cursor.to_list(length=1000)
    
    return {
        "booth_id": booth_id or "all",
        "time_range_hours": hours,
        "data_points": len(snapshots),
        "snapshots": snapshots
    }


@router.get("/alerts/summary")
async def get_alerts_summary(
    hours: int = 24,
    current_user = Depends(get_current_user)
):
    """Get alert summary statistics"""
    alerts_collection = get_collection("alerts")
    
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    total_alerts = await alerts_collection.count_documents({"timestamp": {"$gte": cutoff_time}})
    unread_alerts = await alerts_collection.count_documents({
        "timestamp": {"$gte": cutoff_time},
        "is_read": False
    })
    
    # Get severity breakdown
    pipeline = [
        {"$match": {"timestamp": {"$gte": cutoff_time}}},
        {"$group": {"_id": "$severity", "count": {"$sum": 1}}}
    ]
    severity_data = await alerts_collection.aggregate(pipeline).to_list(length=None)
    
    # Get type breakdown
    pipeline_type = [
        {"$match": {"timestamp": {"$gte": cutoff_time}}},
        {"$group": {"_id": "$alert_type", "count": {"$sum": 1}}}
    ]
    type_data = await alerts_collection.aggregate(pipeline_type).to_list(length=None)
    
    return {
        "time_range_hours": hours,
        "total_alerts": total_alerts,
        "unread_alerts": unread_alerts,
        "alerts_by_severity": {item["_id"]: item["count"] for item in severity_data},
        "alerts_by_type": {item["_id"]: item["count"] for item in type_data}
    }


@router.get("/audit-logs")
async def get_audit_logs(
    username: Optional[str] = None,
    hours: int = 24,
    limit: int = 100,
    current_user = Depends(require_admin)
):
    """Get audit logs (admin/manager only)"""
    audit_collection = get_collection("audit_logs")
    
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    query = {"timestamp": {"$gte": cutoff_time}}
    
    if username:
        query["username"] = username
    
    cursor = audit_collection.find(query).sort("timestamp", -1).limit(limit)
    logs = await cursor.to_list(length=None)
    
    return {
        "count": len(logs),
        "logs": logs
    }
