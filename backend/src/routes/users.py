"""User API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.database.init import get_session
from src.database.schemas import User, UserCreate, UserUpdate, UserPublic

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserPublic, status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    Create a new user.
    
    - **user_id**: Unique user identifier
    - **first_name**: User's first name (max 100 characters)
    - **second_name**: User's last name (max 100 characters)
    - **phone_number**: Optional phone number (must be unique)
    - **active_flag**: Whether user is active (default: true)
    - **role_id**: Role ID for the user
    """
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=list[UserPublic])
def read_users(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    """
    Get all users with pagination.
    
    - **skip**: Number of users to skip (default: 0)
    - **limit**: Maximum number of users to return (default: 10)
    """
    users = session.exec(
        select(User).offset(skip).limit(limit)
    ).all()
    return users


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    """
    Get a specific user by ID.
    
    - **user_id**: The user identifier
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a user.
    
    - **user_id**: The user identifier
    - **first_name**: New first name (optional)
    - **second_name**: New last name (optional)
    - **phone_number**: New phone number (optional)
    - **active_flag**: Update active status (optional)
    - **role_id**: Update user's role (optional)
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """
    Delete a user.
    
    - **user_id**: The user identifier
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()

