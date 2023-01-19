from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.db.settings.config import get_db
from src.shared.auth.auth_utils import current_user
from src.schemas.role_schema import RoleResponse
from src.controllers.role_controller import RoleController
from src.schemas.user_schema import UserResponse

role_router = APIRouter(prefix='/role', tags=['Roles'])


@role_router.get('', response_model=List[RoleResponse])
def handle_get_all_roles(session: Session = Depends(get_db),
                         profile: UserResponse = Depends(current_user)):
    """
    Return all roles from database
    """
    return RoleController().handle_list(db=session)


@role_router.get('/{role_id}', response_model=RoleResponse)
def handle_get_role(role_id: UUID,
                    session: Session = Depends(get_db),
                    profile: UserResponse = Depends(current_user)):
    """
    This route return the role data by UUID.
    """
    return RoleController().handle_get(db=session,
                                       object_id=role_id,
                                       exception_message='Role não encontrada.')
