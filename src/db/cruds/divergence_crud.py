from src.db.cruds.pagination_oriented_crud import PaginationOrientedCRUD
from src.db.models.models import DivergenceModel


class DivergenceCRUD(PaginationOrientedCRUD):
    def __init__(self):
        super(DivergenceCRUD, self).__init__(DivergenceModel)
