from typing import Any
from sqlalchemy.orm import Session

from src.db.cruds.base import BaseCRUD


class PaginationOrientedCRUD(BaseCRUD):
    def __init__(self, model: Any):
        super(PaginationOrientedCRUD, self).__init__(model)

    def handle_list(
        self,
        db: Session,
        page: int = None,
        limit: int = None
    ):
        page = page if page else 1
        limit = limit if limit else 20

        result = db.query(self.model).limit(limit).offset((page - 1) * limit).all()
        count = self.count_records(db=db)
        return {'total': count, 'page': page, 'results': result}

    def count_records(self, db: Session):
        return db.query(self.model).count()
