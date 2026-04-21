from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.models.alert import AlertResponse, AlertSeverity
from app.services import alert_service
from app.routers.auth import get_current_user
from app.services.alert_service import ALERT_THRESHOLDS

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("/", response_model=list[AlertResponse])
async def get_alerts(
    unread_only: bool = False,
    severity: Optional[AlertSeverity] = None,
    limit: int = 50,
    current_user = Depends(get_current_user)
):
    """Get alerts with optional filters"""
    return await alert_service.get_alerts(
        unread_only=unread_only,
        severity=severity,
        limit=limit
    )


@router.get("/recent", response_model=list[AlertResponse])
async def get_recent_alerts(
    limit: int = 10,
    current_user = Depends(get_current_user)
):
    """Get recent alerts"""
    return await alert_service.get_recent_alerts(limit=limit)


@router.get("/unread-count")
async def get_unread_count(current_user = Depends(get_current_user)):
    """Get count of unread alerts"""
    count = await alert_service.get_unread_count()
    return {"unread_count": count}


@router.post("/{alert_id}/read")
async def mark_alert_read(
    alert_id: str,
    current_user = Depends(get_current_user)
):
    """Mark an alert as read"""
    success = await alert_service.mark_alert_as_read(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert marked as read"}


@router.get("/thresholds")
async def get_thresholds(current_user = Depends(get_current_user)):
    """Get alert threshold configuration"""
    return ALERT_THRESHOLDS
