from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.controllers.image_controller import ImageController
from src.db.settings.config import get_db
from src.shared.auth.auth_utils import current_user
from src.schemas.utils_schema import Image

from src.schemas.user_schema import UserResponse

util_router = APIRouter(prefix='/utils', tags=['Utils'])


@util_router.post('/image', response_model=Image, status_code=status.HTTP_201_CREATED)
def handle_insert_image(image_data: Image,
                        db: Session = Depends(get_db),
                        profile: UserResponse = Depends(current_user)):
    """
    This route is used do insert a new image.
    """
    return ImageController().handle_create(db=db, data=image_data, user_id=profile.id)
