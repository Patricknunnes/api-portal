from src.db.cruds.base import BaseCRUD
from src.db.models.models import RouteModel


class RouteCRUD(BaseCRUD):
    def __init__(self):
        super(RouteCRUD, self).__init__(RouteModel)
