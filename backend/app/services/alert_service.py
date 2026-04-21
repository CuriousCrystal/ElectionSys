from typing import List, Optional
from datetime import datetime
from app.database import get_collection
from app.models.alert import AlertCreate, AlertResponse, AlertSeverity


ALERT_THRESHOLDS = {
    "queue_length": {
        "low": 20,
        "medium": 50,
        "high": 100,
        "critical": 150
    },
    "wait_time_minutes": {
        "low": 10,
        "medium": 20,
        "high": 30,
        "critical": 45
    },
    "capacity_percentage": {
        "low": 60,
        "medium": 80,
        "high": 90,
        "critical": 95
    }
}


async def create_alert(alert_data: AlertCreate) -> AlertResponse:
    """Create a new alert"""
    alerts_collection = get_collection("alerts")
    
    alert_dict = {
        "booth_id": alert_data.booth_id,
        "alert_type": alert_data.alert_type.value,
        "severity": alert_data.severity.value,
        "message": alert_data.message,
        "is_read": False,
        "timestamp": datetime.utcnow()
    }
    
    result = await alerts_collection.insert_one(alert_dict)
    alert_dict["id"] = str(result.inserted_id)
    
    return AlertResponse(**alert_dict)


async def get_recent_alerts(limit: int = 10) -> List[AlertResponse]:
    """Get recent alerts"""
    alerts_collection = get_collection("alerts")
    
    cursor = alerts_collection.find().sort("timestamp", -1).limit(limit)
    alerts = await cursor.to_list(length=None)
    
    return [AlertResponse(**alert) for alert in alerts]


async def get_unread_count() -> int:
    """Get count of unread alerts"""
    alerts_collection = get_collection("alerts")
    count = await alerts_collection.count_documents({"is_read": False})
    return count


async def mark_alert_as_read(alert_id: str) -> bool:
    """Mark an alert as read"""
    alerts_collection = get_collection("alerts")
    
    from bson import ObjectId
    try:
        result = await alerts_collection.update_one(
            {"_id": ObjectId(alert_id)},
            {"$set": {"is_read": True}}
        )
        return result.modified_count > 0
    except:
        return False


async def get_alerts(
    unread_only: bool = False,
    severity: Optional[AlertSeverity] = None,
    limit: int = 50
) -> List[AlertResponse]:
    """Get alerts with filters"""
    alerts_collection = get_collection("alerts")
    
    query = {}
    if unread_only:
        query["is_read"] = False
    if severity:
        query["severity"] = severity.value
    
    cursor = alerts_collection.find(query).sort("timestamp", -1).limit(limit)
    alerts = await cursor.to_list(length=None)
    
    return [AlertResponse(**alert) for alert in alerts]


def check_thresholds_and_create_alerts(
    booth_id: str,
    queue_length: int,
    wait_time: int,
    capacity_percentage: float
) -> List[AlertCreate]:
    """Check thresholds and return alerts to create"""
    from app.models.alert import AlertType
    
    alerts = []
    
    # Check queue length
    if queue_length >= ALERT_THRESHOLDS["queue_length"]["critical"]:
        alerts.append(AlertCreate(
            booth_id=booth_id,
            alert_type=AlertType.queue_overflow,
            severity=AlertSeverity.critical,
            message=f"CRITICAL: Queue length at {queue_length} voters"
        ))
    elif queue_length >= ALERT_THRESHOLDS["queue_length"]["high"]:
        alerts.append(AlertCreate(
            booth_id=booth_id,
            alert_type=AlertType.queue_overflow,
            severity=AlertSeverity.high,
            message=f"HIGH: Queue length at {queue_length} voters"
        ))
    
    # Check wait time
    if wait_time >= ALERT_THRESHOLDS["wait_time_minutes"]["critical"]:
        alerts.append(AlertCreate(
            booth_id=booth_id,
            alert_type=AlertType.queue_overflow,
            severity=AlertSeverity.critical,
            message=f"CRITICAL: Wait time is {wait_time} minutes"
        ))
    elif wait_time >= ALERT_THRESHOLDS["wait_time_minutes"]["high"]:
        alerts.append(AlertCreate(
            booth_id=booth_id,
            alert_type=AlertType.queue_overflow,
            severity=AlertSeverity.high,
            message=f"HIGH: Wait time is {wait_time} minutes"
        ))
    
    # Check capacity
    if capacity_percentage >= ALERT_THRESHOLDS["capacity_percentage"]["critical"]:
        alerts.append(AlertCreate(
            booth_id=booth_id,
            alert_type=AlertType.capacity_warning,
            severity=AlertSeverity.critical,
            message=f"CRITICAL: Capacity at {capacity_percentage:.1f}%"
        ))
    elif capacity_percentage >= ALERT_THRESHOLDS["capacity_percentage"]["high"]:
        alerts.append(AlertCreate(
            booth_id=booth_id,
            alert_type=AlertType.capacity_warning,
            severity=AlertSeverity.high,
            message=f"HIGH: Capacity at {capacity_percentage:.1f}%"
        ))
    
    return alerts
