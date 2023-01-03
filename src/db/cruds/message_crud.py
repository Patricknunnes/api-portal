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
        limit: int = None
    ):
        page = page if page else 1
        limit = limit if limit else 20

        result = db.query(self.model) \
            .filter(
                ((self.model.expiration_date > func.now()) | \
                    (self.model.expiration_date == None)) & \
                ((self.model.role_permission == role_permission) | \
                    (self.model.user_permission == user_permission) | \
                    ((self.model.role_permission == None) & \
                        (self.model.user_permission == None)))
            ).limit(limit).offset((page - 1) * limit).all()
        count = self.count_records_per_permissions(
            db=db,
            role_permission=role_permission,
            user_permission=user_permission
        )
        return {'total': count, 'page': page, 'results': result}

    def count_records_per_permissions(
        self,
        db: Session,
        role_permission: UUID,
        user_permission: UUID
    ):
        return db.query(self.model).filter(
                ((self.model.expiration_date > func.now()) | \
                    (self.model.expiration_date == None)) & \
                ((self.model.role_permission == role_permission) | \
                    (self.model.user_permission == user_permission) | \
                    ((self.model.role_permission == None) & \
                        (self.model.user_permission == None)))
            ).count()
