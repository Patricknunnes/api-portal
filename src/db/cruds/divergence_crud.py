from src.db.cruds.base import BaseCRUD
from src.db.models.divergence_model import DivergenceModel


class DivergenceCRUD(BaseCRUD):
    def __init__(self):
        super(DivergenceCRUD, self).__init__(DivergenceModel)
