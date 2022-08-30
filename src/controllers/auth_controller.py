import re
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.exceptions.exceptions import BadRequestException
from src.shared.auth.hash_provider import verify_password
from src.db.cruds.user_crud import UserCRUD
from src.schemas.auth_schema import LoginBase, TokenResponse
from src.shared.auth.token_provider import create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthController:

    def handle_login(self, db: Session, data_login: LoginBase) -> TokenResponse:
        document = re.sub(r'\W+', '', data_login.document)
        user = UserCRUD().get_user_document_or_email(db=db, document=document)

        if not user or not verify_password(data_login.password, user.password):
            raise BadRequestException(detail='Documento ou senha invalidos.')

        return TokenResponse(access_token=create_access_token(data={'sub': str(user.id)}))
