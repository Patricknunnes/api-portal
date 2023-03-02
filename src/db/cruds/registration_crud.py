from src.db.cruds.pagination_oriented_crud import PaginationOrientedCRUD
from src.db.models.models import RegistrationModel


class RegistrationCRUD(PaginationOrientedCRUD):
    def __init__(self):
        super(RegistrationCRUD, self).__init__(RegistrationModel)
