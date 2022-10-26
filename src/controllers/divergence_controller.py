from src.controllers.base import BaseController
from src.db.cruds.divergence_crud import DivergenceCRUD


class DivergenceController(BaseController):

    def __init__(self):
        super(DivergenceController, self).__init__(DivergenceCRUD)
