from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.db.settings.config import get_db
from src.schemas.user_schema import UserResponse

from src.sso.sso_utils import current_user, AuthRequestParameters, TokenRequestBody
from src.sso.validators import validate_params
from src.sso.token_provider import create_access_token
from src.sso.controller import SSOController
from src.sso.exceptions import BadRequestException


sso_router = APIRouter(prefix='/sso', tags=['sso'])


@sso_router.post('/auth')
def handle_auth(
    params: AuthRequestParameters = Depends(AuthRequestParameters),
    db: Session = Depends(get_db),
    user: UserResponse = Depends(current_user)
):
    if not validate_params(params):
        return RedirectResponse(
            url=f'{params.redirect_uri}?error=invalid_request&state={params.state}'
        )

    code = SSOController().create_session(user_id=user.id, state=params.state, db=db)

    return RedirectResponse(url=f'{params.redirect_uri}?state={params.state}&code={code}')


@sso_router.post(
    '/token',
    status_code=status.HTTP_200_OK,
)
def handle_token(
    response: Response,
    body: TokenRequestBody = Depends(TokenRequestBody),
    db: Session = Depends(get_db)
):
    user = SSOController().validate_session(session_code=body.code, db=db)

    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'

    if user:
        id_token = create_access_token(data={'sub': user.username})
        access_token = create_access_token(data={'sub': str(user.id)})

        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 1800,
            'id_token': id_token
        }
    
    raise BadRequestException('invalid_request')
