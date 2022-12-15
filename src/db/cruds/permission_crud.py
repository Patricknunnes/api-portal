from sqlalchemy.orm import Session
from src.db.cruds.base import BaseCRUD
from src.db.models.permission_model import PermissionModel
from src.db.models.models import RouteModel
from src.schemas.auth_schema import PermissionParams


class PermissionCRUD(BaseCRUD):
    def __init__(self):
        super(PermissionCRUD, self).__init__(PermissionModel)

    def get_permission(self, db=Session, datas=PermissionParams):
        permission = db.query(self.model.id) \
            .where(self.model.role_id == datas.user_role.id,
                   RouteModel.path == datas.path,
                   RouteModel.method == datas.method) \
            .join(RouteModel).first()

        return permission
