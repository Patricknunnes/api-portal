from uuid import UUID

from sqlalchemy.orm import Session

from src.db.cruds.user_crud import UserCRUD
from src.schemas.utils_schema import (
    Image
)


class ImageController:

    def handle_patch(self, db: Session, data: Image, user_id: UUID):
        UserCRUD().patch(db=db, object_id=user_id, data=data)
