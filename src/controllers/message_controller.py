from sqlalchemy.orm import Session
from datetime import datetime

from src.exceptions.exceptions import BadRequestException
from src.controllers.pagination_oriented_controller import PaginationOrientedController
from src.controllers.role_controller import RoleController
from src.controllers.user_controller import UserController
from src.schemas.message_schema import MessageCreate
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

    def __validate_create_fields(self, db: Session, data: MessageCreate):
        self.__validate_expiration_date(data.expiration_date)

        if data.role_permission:
            RoleController().handle_get(
                db=db,
                object_id=data.role_permission,
                exception_message='Cargo não encontrado.'
            )
        
        if data.user_permission:
            UserController().handle_get(
                db=db,
                object_id=data.user_permission,
                exception_message='Usuário não encontrado.'
            )


    def handle_create(self, db: Session, data: MessageCreate):
        self.__validate_create_fields(db=db, data=data)

        return super().handle_create(db, data)
