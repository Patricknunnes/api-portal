from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from uuid import UUID

from src.controllers.registration_controller import RegistrationController
from src.db.settings.config import get_db
from src.schemas.user_schema import UserResponse
from src.schemas.registration_schema import (
    Registration,
    RegistrationCreateBody,
    RegistrationCreateModel,
    RegistrationResponse,
    RegistrationResponsePaginate,
    RegistrationUpdateBody
)
from src.shared.auth.auth_utils import current_user

registration_router = APIRouter(prefix='/registration', tags=['Registrations'])


@registration_router.get(
    '',
    response_model=RegistrationResponsePaginate,
    status_code=status.HTTP_200_OK
)
def handle_list_registrations(
    filters: str = None,
    page: int = None,
    limit: int = None,
    sort: str = None,
    session: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Return registration list
    """
    return RegistrationController().handle_list(
        db=session,
        filters=filters,
        limit=limit,
        page=page,
        sort=sort
    )


@registration_router.get(
    '/office365/me',
    response_model=Registration,
    status_code=status.HTTP_200_OK
)
def handle_get_office_registration(
    session: Session = Depends(get_db),
    profile: UserResponse = Depends(current_user)
):
    """
    Return office registration data
    """
    return RegistrationController().handle_get_by_data(
        db=session,
        exception_message='Cadastro não encontrado.',
        data=dict(document=profile.document, service='office 365')
    )


@registration_router.post(
    '/office365',
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
def handle_create_office_registration(
    user_data: RegistrationCreateBody,
    session: Session = Depends(get_db),
    profile: UserResponse = Depends(current_user)
):
    """
    Create office 365 registration
    """
    return RegistrationController().handle_create(
        db=session,
        data=RegistrationCreateModel(
            **user_data.dict(),
            document=profile.document,
            service='office 365'
        )
    )


@registration_router.patch(
    '/{registration_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
def handle_approve_registration(
    data: RegistrationUpdateBody,
    registration_id: UUID,
    session: Session = Depends(get_db),
    _: UserResponse = Depends(current_user)
):
    """
    Update registration
    """
    return RegistrationController().handle_patch(
        db=session,
        object_id=registration_id,
        data=data.dict(),
        exception_message='Cadastro não encontrado.'
    )
