from sqlalchemy.orm import Session

from src.controllers.base import BaseController
from src.db.cruds.divergence_crud import DivergenceCRUD


class DivergenceController(BaseController):

    def __init__(self):
        super(DivergenceController, self).__init__(DivergenceCRUD)

    def handle_list(
        self,
        db: Session,
        page: int = None,
        limit: int = None
    ):
        return self.crud_class().handle_list(
            db=db,
            page=page,
            limit=limit
        )
