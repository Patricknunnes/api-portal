from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from uuid import UUID
from src.db.settings.config import get_db
from src.shared.auth.auth_utils import current_user
from src.schemas.user_schema import (
    UserBase,
    UserResponse,
    UserResponsePaginate,
    UserUpdate,
    DivergenceResponsePaginate
)
from src.controllers.user_controller import UserController
from src.controllers.divergence_controller import DivergenceController

user_router = APIRouter(prefix='/user', tags=['Users'])


@user_router.get('', response_model=UserResponsePaginate)
def handle_get_all_users(
    filters: str = None,
    page: int = None,
    limit: int = None,
    db: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Return all users from database
    """
    return UserController().handle_list(db=db, filters=filters, page=page, limit=limit)


@user_router.get('/divergences', response_model=DivergenceResponsePaginate)
def handle_get_all_divergences(
    db: Session = Depends(get_db),
    page: int = None,
    limit: int = None,
    _: UserResponse = Depends(current_user)
):
    """
    Return all registration divergences from database
    """
    return DivergenceController().handle_list(db=db, page=page, limit=limit)


@user_router.get('/{user_id}',
                 response_model=UserResponse,
                 status_code=status.HTTP_200_OK)
def handle_get_user(user_id: UUID,
                    db: Session = Depends(get_db),
                    _: UserResponse = Depends(current_user)):
    """
    This route return the user data by UUID.
    """
    return UserController().handle_get(db=db,
                                       object_id=user_id,
                                       exception_message='Usuário não encontrado')


@user_router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def handle_create_user(user_data: UserBase,
                       db: Session = Depends(get_db),
                       _: UserResponse = Depends(current_user)):
    """
    This route is used do create a new user.
    """
    return UserController().handle_create(db=db, data=user_data)


@user_router.patch('/{user_id}',
                   status_code=status.HTTP_204_NO_CONTENT,
                   response_class=Response)
def handle_patch_user(user_data: UserUpdate,
                      user_id: UUID,
                      db: Session = Depends(get_db),
                      profile: UserResponse = Depends(current_user)):
    """
    Update values from a user
    """
    UserController().handle_patch(db=db,
                                  object_id=user_id,
                                  data=user_data,
                                  profile=profile)
