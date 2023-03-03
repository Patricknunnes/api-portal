from sqlalchemy import or_
from sqlalchemy.orm import Session, Query
from typing import Any, List

from src.db.cruds.base import BaseCRUD


class PaginationOrientedCRUD(BaseCRUD):
    def __init__(self, model: Any):
        super(PaginationOrientedCRUD, self).__init__(model)

    def _filter_query(self, db: Session, filters: str = None, filter_attrs: List[str] = []):
        '''
        Return filtered query considering just its own columns
        '''
        if filters:
            filters_tuple = (
                getattr(self.model, attr).ilike(f'%{filters}%') for attr in filter_attrs)
            return db.query(self.model).filter(or_(filters_tuple))
        return db.query(self.model)

    def _sort_query(self, query: Query, sort_params: tuple = None):
        '''
        Return sorted query considering just its own columns
        '''
        if sort_params is not None:
            for column, order in sort_params:
                column_obj = getattr(self.model, column, None)

                if column_obj is not None:
                    if order == 'asc':
                        query = query.order_by(column_obj.asc())
                    elif order == 'desc':
                        query = query.order_by(column_obj.desc())
        return query

    def _paginate_query(
        self,
        query: Query,
        limit: int = None,
        page: int = None
    ):
        page = page if page else 1
        limit = limit if limit else 20
        return query.limit(limit).offset((page - 1) * limit)

    def handle_list(
        self,
        db: Session,
        limit: int = None,
        page: int = None,
        filters: str = None,
        filter_attrs: List[str] = [],
        sort: tuple = None
    ):
        query = self._filter_query(db=db, filters=filters, filter_attrs=filter_attrs)
        query = self._sort_query(query=query, sort_params=sort)
        query_pagination = self._paginate_query(query=query, page=page, limit=limit)
        return {
            'total': query.count(),
            'page': page if page else 1,
            'results': query_pagination.all()
        }
