from typing import Any
from sqlalchemy.orm import Session

from src.controllers.base import BaseController


class PaginationOrientedController(BaseController):
    def __init__(self, crud_class: Any):
        super(PaginationOrientedController, self).__init__(crud_class)

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
