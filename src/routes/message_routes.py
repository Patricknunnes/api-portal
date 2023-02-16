from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from uuid import UUID

from src.controllers.message_controller import MessageController
from src.controllers.message_user_controller import MessageUserController
from src.db.settings.config import get_db
from src.shared.auth.auth_utils import current_user
from src.schemas.message_schema import (
    MessageCreate,
    MessageCreateReqBody,
    MessageMeResponsePaginate,
    MessageResponse,
    MessageResponsePaginate,
    MessageUpdate,
    MessageUpdateReqBody
)
from src.schemas.message_user_schema import MessageUserPrimaryKeys, MessageUserResponse
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


@message_router.get('/me', response_model=MessageMeResponsePaginate)
def handle_list_per_permissions(
    page: int = None,
    limit: int = None,
    db: Session = Depends(get_db),
    profile: UserResponse = Depends(current_user),
    is_important: bool = None
):
    """
    Return messages according to role id and user id according to token
    """
    return MessageController().handle_list_per_permissions(
        db=db,
        user=profile,
        page=page,
        limit=limit,
        is_important=is_important
    )


@message_router.post(
    '',
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED
)
def handle_create_message(
    message_data: MessageCreateReqBody,
    db: Session = Depends(get_db),
    profile: UserResponse = Depends(current_user)
):
    """
    Create message
    """
    message_data = MessageCreate(**message_data.dict(), created_by=profile.id)
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


@message_router.get(
    '/me/{message_id}',
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK
)
def handle_get_message(
    message_id: UUID,
    db: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    This route return the message data by UUID.
    """
    return MessageController().handle_get(
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
    message_data: MessageUpdateReqBody,
    db: Session = Depends(get_db),
    profile: UserResponse = Depends(current_user)
):
    """
    Update message
    """
    message_data = MessageUpdate(**message_data.dict(), updated_by=profile.id)
    MessageController().handle_patch(
        db=db,
        object_id=message_id,
        data=message_data
    )


@message_router.post(
    '/me/read/{message_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=MessageUserResponse
)
def handle_message_read(
    message_id: UUID,
    db: Session = Depends(get_db),
    profile: UserResponse = Depends(current_user)
):
    '''Mark message as read by the user'''
    return MessageUserController().handle_create(
        db=db,
        data=MessageUserPrimaryKeys(message_id=message_id, user_id=profile.id)
    )
