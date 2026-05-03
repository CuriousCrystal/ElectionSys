from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from app.config import settings
from app.models.user import UserCreate, UserResponse, UserLogin
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class TokenRefreshRequest(BaseModel):
    refresh_token: str


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        token_type: str = payload.get("token_type")
        if username is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await auth_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


async def require_admin(current_user = Depends(get_current_user)):
    """Require admin role"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


@router.post("/login")
async def login(login_data: UserLogin):
    """Authenticate user and return access and refresh tokens"""
    user = await auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    refresh_token = auth_service.create_refresh_token(
        data={"sub": user.username, "role": user.role}
    )
    await auth_service.store_refresh_token(user.username, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
async def refresh_token(token_data: TokenRefreshRequest):
    """Rotate an existing refresh token and issue a new access token"""
    user = await auth_service.authenticate_refresh_token(token_data.refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    new_refresh_token = auth_service.create_refresh_token(
        data={"sub": user.username, "role": user.role}
    )

    await auth_service.revoke_refresh_token(user.username, token_data.refresh_token)
    await auth_service.store_refresh_token(user.username, new_refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(token_data: TokenRefreshRequest):
    """Invalidate a refresh token and log out"""
    user = await auth_service.authenticate_refresh_token(token_data.refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    await auth_service.revoke_refresh_token(user.username, token_data.refresh_token)
    return {"detail": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    current_user = Depends(require_admin)
):
    """Register a new user (admin only)"""
    try:
        return await auth_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
