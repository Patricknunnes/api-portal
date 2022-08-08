from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.db.settings.config import get_db
from src.schemas.role_schema import ResponseRole
from src.controllers.role_controller import RoleController

role_router = APIRouter(prefix='/role', tags=['Roles'])


@role_router.get('', response_model=List[ResponseRole])
def handle_get_all_roles(session: Session = Depends(get_db)):
    """
    Return all roles from database
    """
    return RoleController().handle_list(db=session)


@role_router.get('/{role_id}', response_model=ResponseRole)
def handle_get_role(role_id: UUID, session: Session = Depends(get_db)):
    """
    This route return the role data by UUID.
    """
    return RoleController().handle_get(db=session, object_id=role_id)
