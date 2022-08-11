from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.settings.config import get_db
from src.schemas.auth_schema import LoginBase, TokenResponse
from src.schemas.user_schema import UserResponse
from src.controllers.auth_controller import AuthController

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/token', response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def handle_create_token(login_data: LoginBase, db: Session = Depends(get_db)):
    """
    This route is used to signin in platform.
    """
    return AuthController().handle_login(db=db, data_login=login_data)


@auth_router.get('/me', response_model=UserResponse, status_code=status.HTTP_200_OK)
def handle_me_data(profile: UserResponse = Depends(AuthController().handle_current_user)):
    """
    This route is used to return user data.
    """
    return profile
