"""Database table schemas using SQLModel."""
from typing import Optional
from sqlmodel import SQLModel, Field


# ============================================================================
# Base Models (for shared fields)
# ============================================================================

class RoleBase(SQLModel):
    """Base model for Role with common fields."""
    role_name: str = Field(index=True, unique=True, max_length=20)
    description: Optional[str] = None


class UserBase(SQLModel):
    """Base model for User with common fields."""
    first_name: str = Field(max_length=100)
    second_name: str = Field(max_length=100)
    phone_number: Optional[str] = Field(default=None, unique=True, max_length=20)
    active_flag: bool = Field(default=True)


# ============================================================================
# Database Models (table=True)
# ============================================================================

class Role(RoleBase, table=True):
    """Role database model."""
    role_id: Optional[int] = Field(default=None, primary_key=True)


class User(UserBase, table=True):
    """User database model."""
    user_id: Optional[int] = Field(default=None, primary_key=True)
    role_id: int = Field(foreign_key="role.role_id")


# ============================================================================
# API Response Models (for public API)
# ============================================================================

class RolePublic(RoleBase):
    """Role model for API responses."""
    role_id: int


class UserPublic(UserBase):
    """User model for API responses."""
    user_id: int
    role_id: int


# ============================================================================
# Create/Update Models (for API requests)
# ============================================================================

class RoleCreate(RoleBase):
    """Model for creating a new role."""


class RoleUpdate(SQLModel):
    """Model for updating a role."""
    role_name: Optional[str] = Field(default=None, max_length=20)
    description: Optional[str] = None


class UserCreate(UserBase):
    """Model for creating a new user."""
    role_id: int

class UserUpdate(SQLModel):
    """Model for updating a user."""
    first_name: Optional[str] = Field(default=None, max_length=100)
    second_name: Optional[str] = Field(default=None, max_length=100)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    active_flag: Optional[bool] = None
    role_id: Optional[int] = None

