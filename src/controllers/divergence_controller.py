from src.controllers.pagination_oriented_controller import PaginationOrientedController
from src.db.cruds.divergence_crud import DivergenceCRUD


class DivergenceController(PaginationOrientedController):
    def __init__(self):
        super(DivergenceController, self).__init__(DivergenceCRUD)
