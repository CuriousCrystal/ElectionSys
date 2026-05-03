from datetime import datetime, timedelta
from typing import Optional, List
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
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire, "token_type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "token_type": "refresh"})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def hash_token(token: str) -> str:
    """Hash a refresh token for secure storage"""
    return bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


async def store_refresh_token(username: str, refresh_token: str) -> None:
    """Store a hashed refresh token for a user"""
    users_collection = get_collection("users")
    user = await get_user_by_username(username)
    if not user:
        return

    refresh_tokens = list(user.refresh_token_hashes or [])
    refresh_tokens.append(hash_token(refresh_token))
    if len(refresh_tokens) > 10:
        refresh_tokens = refresh_tokens[-10:]

    await users_collection.update_one(
        {"username": username},
        {"$set": {"refresh_token_hashes": refresh_tokens}},
    )


async def revoke_refresh_token(username: str, refresh_token: str) -> None:
    """Revoke a specific refresh token for a user"""
    users_collection = get_collection("users")
    user = await get_user_by_username(username)
    if not user:
        return

    valid_hashes: List[str] = []
    for token_hash in user.refresh_token_hashes or []:
        if not verify_password(refresh_token, token_hash):
            valid_hashes.append(token_hash)

    await users_collection.update_one(
        {"username": username},
        {"$set": {"refresh_token_hashes": valid_hashes}},
    )


async def authenticate_refresh_token(refresh_token: str) -> Optional[UserInDB]:
    """Authenticate a refresh token and return the owning user"""
    try:
        payload = jwt.decode(refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        token_type: str = payload.get("token_type")
        if username is None or token_type != "refresh":
            return None
    except JWTError:
        return None

    user = await get_user_by_username(username)
    if not user:
        return None

    for token_hash in user.refresh_token_hashes or []:
        if verify_password(refresh_token, token_hash):
            return user

    return None


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
