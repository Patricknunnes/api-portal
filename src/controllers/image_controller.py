import re
from uuid import UUID
from typing import Union

from sqlalchemy.orm import Session

from src.controllers.base import BaseController
from src.controllers.role_controller import RoleController
from src.exceptions.exceptions import BadRequestException
from src.schemas.utils_schema import ValidateDocs
from src.shared.utils import UtilService
from src.shared.auth.hash_provider import get_password_hash
from src.db.cruds.user_crud import UserCRUD
from src.schemas.utils_schema import (
    Image
)


class ImageController:

    def handle_create(self, db: Session, data: Image, user_id: UUID):
        UserCRUD().patch(db=db, object_id=user_id, data=data)
