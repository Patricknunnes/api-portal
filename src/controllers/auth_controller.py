import re
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.dependencies.totvs.soap_api import TotvsWebServer
from src.exceptions.exceptions import BadRequestException
from src.schemas.user_schema import UserResponse
from src.shared.auth.hash_provider import (
    verify_password,
    decode_password,
    get_password_hash
)
from src.db.cruds.user_crud import UserCRUD
from src.schemas.auth_schema import LoginBase, TokenResponse, ResponseSsoTotvs
from src.shared.auth.token_provider import create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthController:

    def handle_login(self, db: Session, data_login: LoginBase) -> TokenResponse:
        user = UserCRUD().get_user_by_username_or_email(db=db, username=data_login.username)

        if not user:
            raise BadRequestException(detail='Usuário ou senha inválidos.')

        if user.is_totvs:
            TotvsWebServer().get_auth_totvs(username=user.username,
                                            password=data_login.password)

            password = get_password_hash(data_login.password)

            UserCRUD().patch(db=db, data={'password': password}, object_id=user.id)

        elif not verify_password(data_login.password, user.password):
            raise BadRequestException(detail='Usuário ou senha inválidos.')

        response = TokenResponse(access_token=create_access_token(
            data={'sub': str(user.id)}),
            user=user)
        return response

    def handle_sso_totvs(self, db: Session, profile: UserResponse) -> ResponseSsoTotvs:
        user = UserCRUD().get(db=db, id=profile.id).__dict__

        datas_sso = ResponseSsoTotvs()

        if user.get("username"):
            key_totvs = decode_password(hashed_password=user.get("password"))
            datas_sso.user_name = user.get("username")
            datas_sso.key_totvs = key_totvs

        return datas_sso
