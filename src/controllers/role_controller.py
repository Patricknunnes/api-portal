from uuid import UUID
from sqlalchemy.orm import Session

from src.exceptions.excepetions import NotFoundException
from src.controllers.base import BaseController
from src.db.cruds.role_crud import RoleCRUD


class RoleController(BaseController):

    def __init__(self):
        super(RoleController, self).__init__(RoleCRUD)
