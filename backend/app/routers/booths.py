from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.models.booth import BoothCreate, BoothUpdate, BoothResponse, BoothStatus
from app.services import booth_service
from app.routers.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/booths", tags=["Polling Booths"])


@router.get("/", response_model=list[BoothResponse])
async def list_booths(
    constituency: Optional[str] = None,
    status: Optional[BoothStatus] = None,
    current_user = Depends(get_current_user)
):
    """List all polling booths with optional filters"""
    return await booth_service.get_all_booths(constituency=constituency, status=status)


@router.get("/recommendations", response_model=list[BoothResponse])
async def get_recommendations(
    limit: int = 5,
    current_user = Depends(get_current_user)
):
    """Get booth recommendations (lowest wait times)"""
    return await booth_service.get_booth_recommendations(limit=limit)


@router.get("/{booth_id}", response_model=BoothResponse)
async def get_booth(
    booth_id: str,
    current_user = Depends(get_current_user)
):
    """Get a specific booth by ID"""
    booth = await booth_service.get_booth(booth_id)
    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")
    return booth


@router.post("/", response_model=BoothResponse, status_code=201)
async def create_booth(
    booth_data: BoothCreate,
    current_user = Depends(require_admin)
):
    """Create a new polling booth (admin/manager only)"""
    try:
        return await booth_service.create_booth(booth_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{booth_id}", response_model=BoothResponse)
async def update_booth(
    booth_id: str,
    update_data: BoothUpdate,
    current_user = Depends(require_admin)
):
    """Update a booth (admin/manager only)"""
    booth = await booth_service.update_booth(booth_id, update_data)
    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")
    return booth


@router.delete("/{booth_id}")
async def delete_booth(
    booth_id: str,
    current_user = Depends(require_admin)
):
    """Delete a booth (admin only)"""
    deleted = await booth_service.delete_booth(booth_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Booth not found")
    return {"message": "Booth deleted successfully"}
