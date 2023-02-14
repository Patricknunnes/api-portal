from sqlalchemy import func
from sqlalchemy.orm import Session
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
        page: int = None,
        limit: int = None,
        is_important: bool = None
    ):
        page = page if page else 1
        limit = limit if limit else 20

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

        if is_important is not None:
            filter_result = filter_result.filter(self.model.is_important == is_important)

        total_count = filter_result.count()
        filter_result = filter_result.limit(limit).offset((page - 1) * limit).all()

        return {
            'total': total_count,
            'page': page,
            'results': [dict(
                message_read=row['message_read'],
                **row['MessageModel'].__dict__
            ) for row in filter_result]
        }
