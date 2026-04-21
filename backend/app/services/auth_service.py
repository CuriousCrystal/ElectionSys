from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from app.config import settings
from app.database import get_collection
from app.models.user import UserCreate, UserInDB, UserResponse


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


async def get_user_by_username(username: str) -> Optional[UserInDB]:
    """Get user from MongoDB by username"""
    users_collection = get_collection("users")
    user_dict = await users_collection.find_one({"username": username})
    
    if user_dict:
        return UserInDB(**user_dict)
    return None


async def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Get user from MongoDB by email"""
    users_collection = get_collection("users")
    user_dict = await users_collection.find_one({"email": email})
    
    if user_dict:
        return UserInDB(**user_dict)
    return None


async def create_user(user_data: UserCreate) -> UserResponse:
    """Create a new user in MongoDB"""
    users_collection = get_collection("users")
    
    # Check if username or email already exists
    existing_user = await get_user_by_username(user_data.username)
    if existing_user:
        raise ValueError("Username already exists")
    
    existing_email = await get_user_by_email(user_data.email)
    if existing_email:
        raise ValueError("Email already exists")
    
    # Create user document
    user_dict = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": hash_password(user_data.password),
        "role": user_data.role,
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    
    return UserResponse(**user_dict)


async def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate a user"""
    user = await get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
