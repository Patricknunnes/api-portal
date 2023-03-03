from typing import Any, List
from sqlalchemy.orm import Session

from src.controllers.base import BaseController


class PaginationOrientedController(BaseController):
    def __init__(self, crud_class: Any):
        super(PaginationOrientedController, self).__init__(crud_class)

    def _format_sort(self, sort: str):
        sort_tuple = tuple()
        for option in sort.split(','):
            sort_data = option.split(':')
            if len(sort_data) == 1:
                sort_data.append('asc')
            sort_tuple = tuple([*sort_tuple, tuple(sort_data)])

        return sort_tuple

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
            sort=self._format_sort(sort) if sort else None,
            filter_attrs=filter_attrs
        )
