from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from src.db.cruds.user_crud import UserCRUD
from src.db.settings.config import get_db
from src.exceptions.exceptions import UnAuthorizedException
from src.schemas.user_schema import UserResponse
from src.sso.token_provider import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class AuthRequestParameters:
    def __init__(
        self,
        client_id: str,
        redirect_uri: str,
        response_type: str,
        scope: str,
        state: str,
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.scope = scope
        self.state = state


async def current_user(
    access_key: str = Form(),
    db: Session = Depends(get_db)
) -> UserResponse:
    exception = UnAuthorizedException(detail="Token invalido.")

    try:
        user_id: str = decode_token(token=access_key)

        if not user_id:
            raise exception

    except JWTError:
        raise exception

    user = UserCRUD().get(db=db, id=user_id)

    if not user:
        raise exception

    return user
