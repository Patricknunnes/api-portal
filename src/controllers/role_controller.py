from uuid import UUID
from sqlalchemy.orm import Session

from src.controllers.base import BaseController
from src.db.cruds.role_crud import RoleCRUD
from src.exceptions.exceptions import NotFoundException


class RoleController(BaseController):
    def __init__(self):
        super(RoleController, self).__init__(RoleCRUD)

    def handle_list_allowed_accesses(
        self,
        db: Session,
        exception_message: str,
        role_id: UUID
    ):
        accesses = self.crud_class().list_allowed_accesses(db=db, role_id=role_id)
        if accesses is None:
            raise NotFoundException(detail=exception_message)
        return accesses
