"""Authentication API endpoints."""
from fastapi import APIRouter, HTTPException, status

from src.auth import LoginRequest, LoginResponse, authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"description": "Unauthorized"}},
)


@router.post("/login", response_model=LoginResponse, status_code=200)
def login(credentials: LoginRequest):
    """
    Authenticate user and return user info.
    
    **Available credentials for MVP:**
    - Username: `admin`, Password: `admin_password_123` (role_id: 1)
    - Username: `staff`, Password: `staff_password_456` (role_id: 2)
    
    Returns user information if credentials are valid.
    """
    user = authenticate_user(credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    return LoginResponse(
        success=True,
        user_id=user.user_id,
        username=user.username,
        role_id=user.role_id,
        first_name=user.first_name,
        second_name=user.second_name,
        message=f"Welcome {user.first_name} {user.second_name}!",
    )

