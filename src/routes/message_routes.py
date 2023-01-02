from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.settings.config import get_db
from src.shared.auth.auth_utils import current_user
from src.controllers.message_controller import MessageController
from src.schemas.message_schema import MessageResponsePaginate
from src.schemas.user_schema import UserResponse

message_router = APIRouter(prefix='/message', tags=['Messages'])


@message_router.get('', response_model=MessageResponsePaginate)
def handle_get_messages(
    page: int = None,
    limit: int = None,
    db: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Return messages from database
    """
    return MessageController().handle_list(db=db, page=page, limit=limit)
