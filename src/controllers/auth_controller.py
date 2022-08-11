from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from src.db.settings.config import get_db
from src.exceptions.exceptions import BadRequestException, UnAuthorizedException
from src.settings.providers.hash_provider import verify_password
from src.db.cruds.user_crud import UserCRUD
from src.schemas.auth_schema import LoginBase, TokenResponse
from src.settings.providers.token_provider import create_access_token, decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthController:

    def handle_login(self, db: Session, data_login: LoginBase) -> TokenResponse:
        user = UserCRUD().get_user_document_or_email(db=db, email=data_login.email)

        if not user or not verify_password(data_login.password, user.password):
            raise BadRequestException(detail='Email ou senha invalidos.')

        return TokenResponse(user=user,
                             access_token=create_access_token(data={'sub': str(user.id)}))

    def handle_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
