from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID

from src.shared.utils import UtilService
from src.exceptions.exceptions import BadRequestException
from src.controllers.pagination_oriented_controller import PaginationOrientedController
from src.controllers.role_controller import RoleController
from src.controllers.user_controller import UserController
from src.schemas.message_schema import MessageCreate, MessageUpdate
from src.schemas.user_schema import UserResponse
from src.db.cruds.message_crud import MessageCRUD


class MessageController(PaginationOrientedController):
    def __init__(self):
        super(MessageController, self).__init__(MessageCRUD)

    def __validate_expiration_date(self, date: str):
        try:
            expiration_date = datetime.strptime(date, '%Y-%m-%d')

            if expiration_date < datetime.now():
                raise BadRequestException(
                    detail='A data de expiração deve ser uma data futura.'
                )
        except ValueError:
            raise BadRequestException(
                detail='Data de expiração inválida. Siga o formato YYYY-MM-DD.'
            )

    def __format_expiration_date(self, date: str):
        '''
        Turn expiration_date into utc from utc-3
        '''
        return f'{date} 03:00:00'

    def __validate_optional_fields(self, db: Session, data: dict):
        if 'expiration_date' in data:
            self.__validate_expiration_date(data['expiration_date'])

        if 'role_permission' in data:
            UtilService.validate_str_as_uuid(data['role_permission'], 'role_permission')
            RoleController().handle_get(
                db=db,
                object_id=data['role_permission'],
                exception_message='Cargo não encontrado.'
            )

        if 'user_permission' in data:
            UtilService.validate_str_as_uuid(data['user_permission'], 'user_permission')
            UserController().handle_get(
                db=db,
                object_id=data['user_permission'],
                exception_message='Usuário não encontrado.'
            )

    def __validate_title(self, data: str):
        if len(data) > 50:
            raise BadRequestException(
                detail='O título pode ter no máximo 50 caracteres.'
            )

    def __validate_required_fields(self, data: dict):
        if 'title' not in data or 'text' not in data:
            raise BadRequestException(
                detail='O título e o conteúdo da mensagem são obrigatórios.'
            )
        self.__validate_title(data=data['title'])

    def handle_create(self, db: Session, data: MessageCreate):
        cleaned_data = UtilService.remove_none_in_form(data)
        self.__validate_required_fields(data=cleaned_data)
        self.__validate_optional_fields(db=db, data=cleaned_data)

        if 'expiration_date' in cleaned_data:
            cleaned_data['expiration_date'] = self.__format_expiration_date(
                cleaned_data['expiration_date']
            )

        return super().handle_create(db, cleaned_data)

    def handle_patch(self, db: Session, object_id: UUID, data: MessageUpdate):
        cleaned_data = UtilService.remove_none_in_form(data)
        if 'title' in cleaned_data:
            self.__validate_title(data=cleaned_data['title'])
        self.__validate_optional_fields(db=db, data=cleaned_data)

        if 'expiration_date' in cleaned_data:
            cleaned_data['expiration_date'] = self.__format_expiration_date(
                cleaned_data['expiration_date']
            )

        if data.expiration_date == '':
            cleaned_data['expiration_date'] = None
        if data.role_permission == '':
            cleaned_data['role_permission'] = None
        if data.user_permission == '':
            cleaned_data['user_permission'] = None

        return super().handle_patch(
            db=db,
            object_id=object_id,
            data=cleaned_data,
            exception_message='Mensagem não encontrada'
        )

    def handle_list_per_permissions(
        self,
        db: Session,
        user: UserResponse,
        page: int = None,
        limit: int = None,
        is_important: bool = None
    ):
        return self.crud_class().list_per_permissions(
            db=db,
            role_permission=user.role.id,
            user_permission=user.id,
            page=page,
            limit=limit,
            is_important=is_important,
        )
