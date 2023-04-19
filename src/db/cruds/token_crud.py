from src.db.cruds.base import BaseCRUD
from src.db.models.models import TokenModel


class TokenCRUD(BaseCRUD):
    def __init__(self):
        super(TokenCRUD, self).__init__(TokenModel)
