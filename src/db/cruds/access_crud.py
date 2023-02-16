from src.db.cruds.base import BaseCRUD
from src.db.models.models import AccessModel


class AccessCRUD(BaseCRUD):
    def __init__(self):
        super(AccessCRUD, self).__init__(AccessModel)
