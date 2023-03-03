from sqlalchemy import or_
from sqlalchemy.orm import Session, Query
from typing import List

from src.db.cruds.pagination_oriented_crud import PaginationOrientedCRUD
from src.db.models.models import RegistrationModel, UserModel, RoleModel


class RegistrationCRUD(PaginationOrientedCRUD):
    def __init__(self):
        super(RegistrationCRUD, self).__init__(RegistrationModel)

    def _filter_query(self, db: Session, filters: str = None, attrs: list = []):
        query = db.query(self.model).join(UserModel).join(RoleModel)
        if filters:
            filters_tuple = (
                getattr(self.model, attr).ilike(f'%{filters}%') for attr in attrs)
            return query.filter(or_(
                UserModel.name.ilike(f'%{filters}%'),
                RoleModel.name.ilike(f'%{filters}%'),
                *filters_tuple
            ))
        return query

    def _sort_query(self, query: Query, sort_params: tuple = None):
        if sort_params is not None:
            for column, order in sort_params:
                column_parts = column.split('.')
                column_obj = None
                if len(column_parts) == 1:
                    column_obj = getattr(self.model, column_parts[0], None)
                else:
                    if column_parts[0] == 'user':
                        column_obj = getattr(UserModel, column_parts[1], None)
                    elif column_parts[0] == 'role':
                        column_obj = getattr(RoleModel, column_parts[1], None)
                if column_obj is not None:
                    if order == 'asc':
                        query = query.order_by(column_obj.asc())
                    elif order == 'desc':
                        query = query.order_by(column_obj.desc())
        return query

    def handle_list(
        self,
        db: Session,
        filter_attrs: List[str],
        filters: str = None,
        limit: int = None,
        page: int = None,
        sort: tuple = None
    ):
        query = self._sort_query(
            self._filter_query(db=db, filters=filters, attrs=filter_attrs),
            sort_params=sort if sort else (('user.name', 'asc'),)
        )
        query_pagination = self._paginate_query(
            query=query,
            page=page,
            limit=limit
        )
        return {
            'total': query.count(),
            'page': page if page else 1,
            'results': query_pagination.all()
        }
