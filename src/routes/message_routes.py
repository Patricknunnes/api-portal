from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.db.settings.config import get_db
from src.shared.auth.auth_utils import current_user
from src.controllers.message_controller import MessageController
from src.schemas.message_schema import MessageResponsePaginate, MessageResponse, MessageCreate
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


@message_router.post('', response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def handle_create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Create message
    """
    return MessageController().handle_create(db=db, data=message_data)


@message_router.delete('/{message_id}', status_code=status.HTTP_204_NO_CONTENT)
def handle_delete_message(
    message_id: UUID,
    db: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Delete message
    """
    MessageController().handle_delete(
        db=db,
        object_id=message_id, 
        exception_message='Mensagem não encontrada'
    )
