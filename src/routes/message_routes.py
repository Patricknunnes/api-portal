from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from uuid import UUID

from src.db.settings.config import get_db
from src.shared.auth.auth_utils import current_user
from src.controllers.message_controller import MessageController
from src.schemas.message_schema import (
    MessageResponsePaginate,
    MessageResponse,
    MessageCreate,
    MessageUpdate
)
from src.schemas.user_schema import UserResponse

message_router = APIRouter(prefix='/message', tags=['Messages'])


@message_router.get('', response_model=MessageResponsePaginate)
def handle_list_messages(
    page: int = None,
    limit: int = None,
    db: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Return messages from database
    """
    return MessageController().handle_list(db=db, page=page, limit=limit)


@message_router.get('/me', response_model=MessageResponsePaginate)
def handle_list_per_permissions(
    page: int = None,
    limit: int = None,
    db: Session = Depends(get_db),
    profile: UserResponse = Depends(current_user)
):
    """
    Return messages according to role id and user id according to token
    """
    return MessageController().handle_list_per_permissions(
        db=db,
        user=profile,
        page=page,
        limit=limit
    )


@message_router.post(
    '',
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED
)
def handle_create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Create message
    """
    return MessageController().handle_create(db=db, data=message_data)


@message_router.delete(
    '/{message_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
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


@message_router.patch(
    '/{message_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
def handle_patch_message(
    message_id: UUID,
    message_data: MessageUpdate,
    db: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Update message
    """
    MessageController().handle_patch(
        db=db,
        object_id=message_id,
        data=message_data
    )
