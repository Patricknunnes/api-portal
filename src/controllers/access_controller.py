from src.controllers.base import BaseController
from src.db.cruds.access_crud import AccessCRUD


class AccessController(BaseController):
    def __init__(self):
        super(AccessController, self).__init__(AccessCRUD)
