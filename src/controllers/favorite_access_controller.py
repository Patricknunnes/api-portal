from sqlalchemy.orm import Session

from src.controllers.access_controller import AccessController
from src.controllers.base import BaseController
from src.controllers.role_controller import RoleController
from src.controllers.user_controller import UserController
from src.db.cruds.favorite_access_crud import FavoriteAccessCRUD
from src.exceptions.exceptions import BadRequestException
from src.schemas.favorite_access_schema import FavoriteAccessPrimaryKeys
from src.schemas.user_schema import UserResponse


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

    def handle_allowed_access_with_favorite_info(
        self,
        db: Session,
        user: UserResponse
    ):
        accesses = RoleController().handle_list_allowed_accesses(
            db=db,
            exception_message='Cargo não encontrado.',
            role_id=user.role.id
        )

        return [dict(
            is_favorite=self.handle_get(
                db=db,
                data=dict(user_id=user.id, access_id=access.id)
            ) is not None,
            **access.__dict__
        ) for access in accesses]
