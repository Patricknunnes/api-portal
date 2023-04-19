from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.db.cruds.pagination_oriented_crud import PaginationOrientedCRUD
from src.db.models.models import MessageModel, MessageUserModel


class MessageCRUD(PaginationOrientedCRUD):
    def __init__(self):
        super(MessageCRUD, self).__init__(MessageModel)

    def list_per_permissions(
        self,
        db: Session,
        role_permission: UUID,
        user_permission: UUID,
        filters: str = None,
        filter_attrs: List[str] = [],
        is_important: bool = None,
        limit: int = None,
        page: int = None
    ):
        subquery = db.query(MessageUserModel) \
            .filter(
                MessageUserModel.user_id == user_permission,
                MessageUserModel.message_id == self.model.id) \
            .subquery()

        query = db.query(
            self.model,
            func.coalesce(subquery.c.message_read, False).label('message_read')) \
            .outerjoin(subquery, self.model.id == subquery.c.message_id)

        filter_result = query.filter(
            ((self.model.expiration_date > func.now()) |
                (self.model.expiration_date.is_(None))) &
            ((self.model.role_permission == role_permission) |
                (self.model.user_permission == user_permission) |
                ((self.model.role_permission.is_(None)) &
                    (self.model.user_permission.is_(None)))))

        if filters:
            filters_tuple = (
                getattr(self.model, attr).ilike(f'%{filters}%') for attr in filter_attrs)
            filter_result = filter_result.filter(or_(filters_tuple))

        if is_important is not None:
            filter_result = filter_result.filter(self.model.is_important == is_important)

        filter_result = self._paginate_query(query=filter_result, limit=limit, page=page)

        return {
            'total': filter_result.count(),
            'page': page if page else 1,
            'results': [dict(
                message_read=row['message_read'],
                **row['MessageModel'].__dict__
            ) for row in filter_result]
        }

    def get_by_id_per_permissions(
        self,
        db: Session,
        id: UUID,
        role_permission: UUID,
        user_permission: UUID,
    ):

        query = db.query(self.model).filter(
            ((self.model.expiration_date > func.now()) |
                (self.model.expiration_date.is_(None))) &
            ((self.model.role_permission == role_permission) |
                (self.model.user_permission == user_permission) |
                ((self.model.role_permission.is_(None)) &
                    (self.model.user_permission.is_(None))))
        )

        filter_result = query.filter(self.model.id == id).first()
        return filter_result
