from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID

from src.shared.utils import UtilService
from src.exceptions.exceptions import BadRequestException
from src.controllers.pagination_oriented_controller import PaginationOrientedController
from src.controllers.role_controller import RoleController
from src.controllers.user_controller import UserController
from src.schemas.message_schema import MessageCreate, MessageUpdate
from src.db.cruds.message_crud import MessageCRUD


class MessageController(PaginationOrientedController):
    def __init__(self):
        super(MessageController, self).__init__(MessageCRUD)

    def __validate_expiration_date(self, date: str):
        try:
            expiration_date = datetime.strptime(date, '%Y-%m-%d')
            
            if expiration_date < datetime.now():
                raise BadRequestException(detail='A data de expiração deve ser uma data futura.')
        except ValueError:
            raise BadRequestException(detail='Data de expiração inválida. Siga o formato YYYY-MM-DD.')

    def __validate_fields(self, db: Session, data: MessageCreate):
        if 'expiration_date' in data:
            self.__validate_expiration_date(data['expiration_date'])

        if 'role_permission' in data:
            RoleController().handle_get(
                db=db,
                object_id=data['role_permission'],
                exception_message='Cargo não encontrado.'
            )

        if 'user_permission' in data:
            UserController().handle_get(
                db=db,
                object_id=data['user_permission'],
                exception_message='Usuário não encontrado.'
            )


    def handle_create(self, db: Session, data: MessageCreate):
        cleaned_data = UtilService().remove_none_in_form(data)
        self.__validate_fields(db=db, data=cleaned_data)

        return super().handle_create(db, cleaned_data)

    def handle_patch(self, db: Session, object_id: UUID, data: MessageUpdate):
        cleaned_data = UtilService().remove_none_in_form(data)
        self.__validate_fields(db=db, data=cleaned_data)

        return super().handle_patch(
            db=db,
            object_id=object_id,
            data=cleaned_data,
            exception_message='Mensagem não encontrada'
        )
