from sqlalchemy.orm import Session
from uuid import UUID

from src.db.cruds.base import BaseCRUD
from src.db.models.models import RoleModel


class RoleCRUD(BaseCRUD):
    def __init__(self):
        super(RoleCRUD, self).__init__(RoleModel)

    def list_allowed_accesses(self, db: Session, role_id: UUID):
        role = self.get(db=db, id=role_id)
        if role is not None:
            return role.accesses

