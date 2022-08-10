from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from src.db.settings.config import get_db
from src.schemas.user_schema import (
    UserBase,
    UserResponse,
    UserUpdate
)
from src.controllers.user_controller import UserController

user_router = APIRouter(prefix='/user', tags=['Users'])


@user_router.get('', response_model=List[UserResponse])
def handle_get_all_users(db: Session = Depends(get_db)):
    """
    Return all users from database
    """
    return UserController().handle_list(db=db)


@user_router.get('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def handle_get_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    This route return the user data by UUID.
    """
    return UserController().handle_get(db=db, object_id=user_id, exception_message='Usuário não encontrado')


@user_router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def handle_create_user(user_data: UserBase, db: Session = Depends(get_db)):
    """
    This route is used do create a new user.
    """
    return UserController().handle_create(db=db, data=user_data)


@user_router.patch('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def handle_patch_user(user_data: UserUpdate,
                      user_id: UUID,
                      db: Session = Depends(get_db)):
    """
    Update values from a user
    """
    return UserController().handle_patch(db=db, object_id=user_id, data=user_data)
