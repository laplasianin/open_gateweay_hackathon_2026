"""Role API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.database.init import get_session
from src.database.schemas import Role, RoleCreate, RoleUpdate, RolePublic

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=RolePublic, status_code=201)
def create_role(role: RoleCreate, session: Session = Depends(get_session)):
    """
    Create a new role.
    
    - **role_id**: Unique role identifier
    - **role_name**: Role name (max 20 characters, must be unique)
    - **description**: Optional role description
    """
    db_role = Role.model_validate(role)
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role


@router.get("/", response_model=list[RolePublic])
def read_roles(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    """
    Get all roles with pagination.
    
    - **skip**: Number of roles to skip (default: 0)
    - **limit**: Maximum number of roles to return (default: 10)
    """
    roles = session.exec(
        select(Role).offset(skip).limit(limit)
    ).all()
    return roles


@router.get("/{role_id}", response_model=RolePublic)
def read_role(role_id: int, session: Session = Depends(get_session)):
    """
    Get a specific role by ID.
    
    - **role_id**: The role identifier
    """
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.patch("/{role_id}", response_model=RolePublic)
def update_role(
    role_id: int,
    role: RoleUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a role.
    
    - **role_id**: The role identifier
    - **role_name**: New role name (optional)
    - **description**: New description (optional)
    """
    db_role = session.get(Role, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    role_data = role.model_dump(exclude_unset=True)
    db_role.sqlmodel_update(role_data)
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role


@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: int, session: Session = Depends(get_session)):
    """
    Delete a role.
    
    - **role_id**: The role identifier
    """
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    session.delete(role)
    session.commit()

