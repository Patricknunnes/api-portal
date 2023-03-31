from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.dependencies.totvs.soap_api import TotvsWebServer
from src.exceptions.exceptions import (
    BadRequestException,
    UnAuthorizedException,
    NotFoundException
)
from src.schemas.user_schema import UserResponse
from src.shared.auth.hash_provider import (
    verify_password,
    decode_password,
    get_password_hash
)
from src.db.cruds.user_crud import UserCRUD
from src.db.cruds.token_crud import TokenCRUD
from src.schemas.auth_schema import LoginBase, TokenResponse, ResponseSsoTotvs, UserMe
from src.shared.auth.token_provider import create_access_token, create_refresh_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthController:
    def handle_login(self, db: Session, data_login: LoginBase) -> TokenResponse:
        user = UserCRUD().get_user_by_username_or_email(
            db=db,
            username=data_login.username
        )

        if not user:
            raise BadRequestException(detail='Usuário ou senha inválidos.')

        if user.is_totvs:
            TotvsWebServer().get_auth_totvs(username=user.username,
                                            password=data_login.password)

            password = get_password_hash(data_login.password)

            UserCRUD().patch(db=db, data={'password': password}, object_id=user.id)

        elif not verify_password(data_login.password, user.password):
            raise BadRequestException(detail='Usuário ou senha inválidos.')

        refresh_token, refresh_token_exp_date = create_refresh_token()
        session = TokenCRUD().create(db=db, data={
            'expiration_date': refresh_token_exp_date,
            'token_hash': get_password_hash(refresh_token),
            'user_id': user.id
        })

        response = TokenResponse(
            access_token=create_access_token(data={'sub': str(user.id)}),
            user=user,
            refresh_token=refresh_token,
            session_id=str(session.id)
        )
        response.user = self.handle_user_data(response.user)
        return response

    def handle_sso_totvs(self, db: Session, profile: UserResponse) -> ResponseSsoTotvs:
        user = UserCRUD().get(db=db, id=profile.id).__dict__

        datas_sso = ResponseSsoTotvs()

        if user.get("username"):
            key_totvs = decode_password(hashed_password=user.get("password"))
            datas_sso.user_name = user.get("username")
            datas_sso.key_totvs = key_totvs

        return datas_sso

    def handle_refresh_token(self, db: Session, session_id: str, refresh_token: str):
        token = TokenCRUD().get(db=db, id=session_id)

        if token is None:
            raise NotFoundException(detail='Sessão não encontrada.')

        if (refresh_token != decode_password(token.token_hash)
                or token.expiration_date < datetime.utcnow()):
            TokenCRUD().delete(db=db, object_id=session_id)
            raise UnAuthorizedException(detail='Token de atualização inválido.')

        refresh_token, _ = create_refresh_token()

        TokenCRUD().patch(
            db=db,
            object_id=session_id,
            data=dict(token_hash=get_password_hash(refresh_token)))
        return {
            'access_token': create_access_token(data={'sub': str(token.user_id)}),
            'refresh_token': refresh_token
        }

    def handle_user_data(self, profile: UserMe):
        profile.document = f'{profile.document[0:3]}******{profile.document[-2:]}'
        return profile
