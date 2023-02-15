from sqlalchemy.orm import Session

from src.controllers.base import BaseController
from src.controllers.user_controller import UserController
from src.controllers.access_controller import AccessController
from src.db.cruds.favorite_access_crud import FavoriteAccessCRUD
from src.exceptions.exceptions import BadRequestException
from src.schemas.favorite_access_schema import FavoriteAccessPrimaryKeys


class FavoriteAccessController(BaseController):
    def __init__(self):
        super(FavoriteAccessController, self).__init__(FavoriteAccessCRUD)

    def __validate_required_fields(self, db: Session, data: FavoriteAccessPrimaryKeys):
        AccessController().handle_get(
            db=db,
            object_id=data.access_id,
            exception_message='Acesso não encontrado.'
        )

        UserController().handle_get(
            db=db,
            object_id=data.user_id,
            exception_message='Usuário não encontrado.'
        )

        if self.handle_get(db=db, data=data.dict()) is not None:
            raise BadRequestException(
                detail='O acesso já foi definido como favorito pelo usuário.')

    def handle_create(self, db: Session, data: FavoriteAccessPrimaryKeys):
        self.__validate_required_fields(db=db, data=data)
        return super().handle_create(db=db, data=data)

    def handle_get(self, db: Session, data: dict):
        return self.crud_class().get(db, **data)

    def handle_delete(self, db: Session, data: FavoriteAccessPrimaryKeys):
        object = self.handle_get(db=db, data=data.dict())

        return super().handle_delete(
            db=db,
            object_id=object.id if object else None,
            exception_message='Acesso não favoritado.')
