from typing import List, Optional, Dict
from datetime import datetime
from app.database import get_collection
from app.models.booth import BoothCreate, BoothUpdate, BoothResponse, BoothStatus
from app.models.alert import AlertType, AlertSeverity


def calculate_booth_status(capacity: int, current_voters: int) -> BoothStatus:
    """Calculate booth status based on capacity usage"""
    if capacity == 0:
        return BoothStatus.smooth
    
    usage_percentage = (current_voters / capacity) * 100
    
    if usage_percentage >= 90:
        return BoothStatus.critical
    elif usage_percentage >= 70:
        return BoothStatus.busy
    else:
        return BoothStatus.smooth


def estimate_wait_time(capacity: int, current_voters: int) -> int:
    """Estimate wait time in minutes based on voter queue"""
    if current_voters <= 0:
        return 0
    
    # Simple estimation: 2 minutes per voter, scaled by capacity
    base_time = current_voters * 2
    capacity_factor = max(0.5, 1 - (capacity / 1000))
    
    return max(0, int(base_time * capacity_factor))


async def create_booth(booth_data: BoothCreate) -> BoothResponse:
    """Create a new polling booth"""
    booths_collection = get_collection("booths")
    
    # Check if booth_id already exists
    existing = await booths_collection.find_one({"booth_id": booth_data.booth_id})
    if existing:
        raise ValueError(f"Booth with ID '{booth_data.booth_id}' already exists")
    
    # Calculate initial status and metrics
    status = calculate_booth_status(booth_data.capacity, booth_data.current_voters)
    wait_time = estimate_wait_time(booth_data.capacity, booth_data.current_voters)
    queue_length = max(0, booth_data.current_voters - int(booth_data.capacity * 0.3))
    
    booth_dict = {
        "booth_id": booth_data.booth_id,
        "name": booth_data.name,
        "constituency": booth_data.constituency,
        "ward": booth_data.ward,
        "capacity": booth_data.capacity,
        "coordinates": booth_data.coordinates.dict() if booth_data.coordinates else None,
        "current_voters": booth_data.current_voters,
        "queue_length": queue_length,
        "wait_time_minutes": wait_time,
        "status": status.value,
        "last_updated": datetime.utcnow()
    }
    
    await booths_collection.insert_one(booth_dict)
    
    return BoothResponse(**booth_dict)


async def get_booth(booth_id: str) -> Optional[BoothResponse]:
    """Get a booth by ID"""
    booths_collection = get_collection("booths")
    booth_dict = await booths_collection.find_one({"booth_id": booth_id})
    
    if booth_dict:
        return BoothResponse(**booth_dict)
    return None


async def get_all_booths(
    constituency: Optional[str] = None,
    status: Optional[BoothStatus] = None
) -> List[BoothResponse]:
    """Get all booths with optional filters"""
    booths_collection = get_collection("booths")
    
    query = {}
    if constituency:
        query["constituency"] = constituency
    if status:
        query["status"] = status.value
    
    cursor = booths_collection.find(query)
    booths = await cursor.to_list(length=None)
    
    return [BoothResponse(**booth) for booth in booths]


async def update_booth(booth_id: str, update_data: BoothUpdate) -> Optional[BoothResponse]:
    """Update a booth"""
    booths_collection = get_collection("booths")
    
    # Get existing booth
    existing = await booths_collection.find_one({"booth_id": booth_id})
    if not existing:
        return None
    
    # Build update dict
    update_dict = {}
    if update_data.name is not None:
        update_dict["name"] = update_data.name
    if update_data.constituency is not None:
        update_dict["constituency"] = update_data.constituency
    if update_data.ward is not None:
        update_dict["ward"] = update_data.ward
    if update_data.capacity is not None:
        update_dict["capacity"] = update_data.capacity
    if update_data.coordinates is not None:
        update_dict["coordinates"] = update_data.coordinates.dict()
    
    # If current_voters is updated, recalculate metrics
    if update_data.current_voters is not None:
        update_dict["current_voters"] = update_data.current_voters
        capacity = update_data.capacity if update_data.capacity else existing["capacity"]
        update_dict["queue_length"] = max(0, update_data.current_voters - int(capacity * 0.3))
        update_dict["wait_time_minutes"] = estimate_wait_time(capacity, update_data.current_voters)
        update_dict["status"] = calculate_booth_status(capacity, update_data.current_voters).value
    
    update_dict["last_updated"] = datetime.utcnow()
    
    if update_dict:
        await booths_collection.update_one(
            {"booth_id": booth_id},
            {"$set": update_dict}
        )
    
    # Return updated booth
    return await get_booth(booth_id)


async def delete_booth(booth_id: str) -> bool:
    """Delete a booth"""
    booths_collection = get_collection("booths")
    result = await booths_collection.delete_one({"booth_id": booth_id})
    return result.deleted_count > 0


async def get_booth_recommendations(limit: int = 5) -> List[BoothResponse]:
    """Get best booths with lowest wait times"""
    booths_collection = get_collection("booths")
    
    cursor = booths_collection.find({"status": BoothStatus.smooth.value}).sort("wait_time_minutes", 1).limit(limit)
    booths = await cursor.to_list(length=None)
    
    return [BoothResponse(**booth) for booth in booths]
