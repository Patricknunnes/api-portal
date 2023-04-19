from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.controllers.access_controller import AccessController
from src.db.settings.config import get_db
from src.schemas.access_schema import AccessResponse
from src.schemas.user_schema import UserResponse
from src.shared.auth.auth_utils import current_user

access_router = APIRouter(prefix='/access-control', tags=['Accesses'])


@access_router.get('', response_model=List[AccessResponse])
def handle_list_accesses(
    session: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Return all access from database
    """
    return AccessController().handle_list(db=session)
