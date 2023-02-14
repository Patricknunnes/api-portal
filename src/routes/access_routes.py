from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.controllers.access_controller import AccessController
from src.controllers.favorite_access_controller import FavoriteAccessController
from src.controllers.role_controller import RoleController
from src.db.settings.config import get_db
from src.schemas.access_schema import AccessResponse, AccessMeResponse
from src.schemas.favorite_access_schema import (
    FavoriteAccessResponse,
    FavoriteAccessPrimaryKeys
)
from src.schemas.user_schema import UserResponse
from src.shared.auth.auth_utils import current_user

access_router = APIRouter(prefix='/access', tags=['Accesses'])


@access_router.get('', response_model=List[AccessResponse])
def handle_list_access(
    session: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Return all access from database
    """
    return AccessController().handle_list(db=session)


@access_router.get('/me', response_model=List[AccessMeResponse])
def handle_list_allowed_accesses(
    session: Session = Depends(get_db),
    profile: UserResponse = Depends(current_user)
):
    """
    Return allowed accesses according to user role
    """
    return RoleController().handle_list_allowed_accesses(
        db=session,
        role_id=profile.role.id)


@access_router.post(
    '/me/favorite/{access_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=FavoriteAccessResponse
)
def handle_favorite_access(
    access_id: UUID,
    db: Session = Depends(get_db),
    profile: UserResponse = Depends(current_user)
):
    '''Set access as favorite by the user'''
    return FavoriteAccessController().handle_create(
        db=db,
        data=FavoriteAccessPrimaryKeys(access_id=access_id, user_id=profile.id)
    )


@access_router.delete(
    '/me/favorite/{access_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
def delete_favorite_access(
    access_id: UUID,
    db: Session = Depends(get_db),
    profile: UserResponse = Depends(current_user)
):
    '''Unset access as favorite by the user'''
    FavoriteAccessController().handle_delete(
        db=db,
        data=FavoriteAccessPrimaryKeys(access_id=access_id, user_id=profile.id)
    )
