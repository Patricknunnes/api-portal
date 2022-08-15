from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from src.db.cruds.user_crud import UserCRUD
from src.db.settings.config import get_db
from src.exceptions.exceptions import UnAuthorizedException
from src.schemas.user_schema import UserResponse
from src.shared.auth.token_provider import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def current_user(token: str = Depends(oauth2_scheme),
                       db: Session = Depends(get_db)) -> UserResponse:
    exception = UnAuthorizedException(detail="Token invalido.")

    try:
        user_id: str = decode_token(token=token)

        if not user_id:
            raise exception

    except JWTError:
        raise exception

    user = UserCRUD().get(db=db, id=user_id)

    if not user:
        raise exception

    return user
