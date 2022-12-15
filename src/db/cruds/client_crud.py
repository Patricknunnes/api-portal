from src.db.cruds.base import BaseCRUD
from src.db.models.models import ClientModel


class ClientCRUD(BaseCRUD):
    def __init__(self):
        super(ClientCRUD, self).__init__(ClientModel)
