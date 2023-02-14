from sqlalchemy.orm import Session

from src.controllers.base import BaseController
from src.controllers.message_controller import MessageController
from src.controllers.user_controller import UserController
from src.db.cruds.message_user_crud import MessageUserCRUD
from src.exceptions.exceptions import BadRequestException
from src.schemas.message_user_schema import MessageUserPrimaryKeys


class MessageUserController(BaseController):
    def __init__(self):
        super(MessageUserController, self).__init__(MessageUserCRUD)

    def __validate_required_fields(self, db: Session, data: MessageUserPrimaryKeys):
        MessageController().handle_get(
            db=db,
            object_id=data.message_id,
            exception_message='Mensagem não encontrada.'
        )

        UserController().handle_get(
            db=db,
            object_id=data.user_id,
            exception_message='Usuário não encontrado.'
        )

        if self.handle_get(db=db, data=data.dict()) is not None:
            raise BadRequestException(detail='A mensagem já foi marcada como lida.')

    def handle_create(self, db: Session, data: MessageUserPrimaryKeys):
        self.__validate_required_fields(db=db, data=data)
        return super().handle_create(db=db, data=data)

    def handle_get(self, db: Session, data: dict):
        object_instance = self.crud_class().get(db, **data)
        return object_instance
