from sqlalchemy.orm import Session
from typing import List

from src.controllers.pagination_oriented_controller import PaginationOrientedController
from src.db.cruds.divergence_crud import DivergenceCRUD


class DivergenceController(PaginationOrientedController):
    def __init__(self):
        super(DivergenceController, self).__init__(DivergenceCRUD)

    def handle_list(
        self,
        db: Session,
        filter_attrs: List[str],
        filters: str = None,
        page: int = None,
        limit: int = None,
        sort: str = None
    ):
        return self.crud_class().handle_list(
            db=db,
            page=page,
            limit=limit,
            filters=filters,
            sort=self._format_sort(sort) if sort else (('name', 'asc'),),
            filter_attrs=filter_attrs
        )
