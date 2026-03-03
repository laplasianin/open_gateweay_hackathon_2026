"""Authentication module for MVP."""
from typing import Optional
from pydantic import BaseModel

# Hardcoded credentials for MVP
CREDENTIALS = {
    "admin": {
        "password": "admin_password_123",
        "role_id": 1,
        "user_id": 1,
        "first_name": "Admin",
        "second_name": "User",
    },
    "staff": {
        "password": "staff_password_456",
        "role_id": 2,
        "user_id": 2,
        "first_name": "Staff",
        "second_name": "User",
    },
}


class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response model."""
    success: bool
    user_id: int
    username: str
    role_id: int
    first_name: str
    second_name: str
    message: str


class AuthUser(BaseModel):
    """Authenticated user model."""
    user_id: int
    username: str
    role_id: int
    first_name: str
    second_name: str


def authenticate_user(username: str, password: str) -> Optional[AuthUser]:
    """
    Authenticate user with username and password.
    
    Args:
        username: Username (admin or staff)
        password: Password
        
    Returns:
        AuthUser if credentials are valid, None otherwise
    """
    if username not in CREDENTIALS:
        return None
    
    creds = CREDENTIALS[username]
    if creds["password"] != password:
        return None
    
    return AuthUser(
        user_id=creds["user_id"],
        username=username,
        role_id=creds["role_id"],
        first_name=creds["first_name"],
        second_name=creds["second_name"],
    )

