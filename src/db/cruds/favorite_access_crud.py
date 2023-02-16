from src.db.cruds.base import BaseCRUD
from src.db.models.models import FavoriteAccessModel


class FavoriteAccessCRUD(BaseCRUD):
    def __init__(self):
        super(FavoriteAccessCRUD, self).__init__(FavoriteAccessModel)
