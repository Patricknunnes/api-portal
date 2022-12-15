from sqlalchemy.orm import Session

from src.db.cruds.base import BaseCRUD
from src.db.models.models import DivergenceModel


class DivergenceCRUD(BaseCRUD):
    def __init__(self):
        super(DivergenceCRUD, self).__init__(DivergenceModel)

    def handle_list(
        self,
        db: Session,
        page: int = None,
        limit: int = None
    ):
        page = page if page else 1
        limit = limit if limit else 20

        result = db.query(self.model).limit(limit).offset((page - 1) * limit).all()
        count = self.count_registers(db=db)
        return {'total': count, 'page': page, 'divergences': result}

    def count_registers(self, db: Session):
        return db.query(self.model).count()
