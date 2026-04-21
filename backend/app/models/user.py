from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user model"""
    username: str
    email: str
    full_name: str
    role: str = "viewer"  # admin, manager, viewer


class UserCreate(UserBase):
    """User creation model"""
    password: str


class UserResponse(UserBase):
    """User response model (excludes password)"""
    is_active: bool = True
    created_at: Optional[datetime] = None


class UserInDB(UserBase):
    """User model for database operations"""
    hashed_password: str
    is_active: bool = True
    created_at: Optional[datetime] = None


class UserLogin(BaseModel):
    """Login request model"""
    username: str
    password: str
