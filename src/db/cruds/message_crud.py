from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID

from src.db.cruds.pagination_oriented_crud import PaginationOrientedCRUD
from src.db.models.models import MessageModel


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
        
        if is_important != None:
            filter_result = db.query(self.model) \
                .filter(
                    ((self.model.expiration_date > func.now()) |
                        (self.model.expiration_date.is_(None))) &
                        (self.model.is_important == is_important) &
                    ((self.model.role_permission == role_permission) |
                        (self.model.user_permission == user_permission) |
                        ((self.model.role_permission.is_(None)) &
                            (self.model.user_permission.is_(None)))))

        else:
            filter_result = db.query(self.model) \
                .filter(
                    ((self.model.expiration_date > func.now()) |
                        (self.model.expiration_date.is_(None))) &
                    ((self.model.role_permission == role_permission) |
                        (self.model.user_permission == user_permission) |
                        ((self.model.role_permission.is_(None)) &
                            (self.model.user_permission.is_(None)))))

        return {
            'total': filter_result.count(),
            'page': page,
            'results': filter_result.limit(limit).offset((page - 1) * limit).all()
        }
