from fastapi import APIRouter, Depends, Form, status, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.db.settings.config import get_db
from src.schemas.user_schema import UserResponse

from src.dependencies.sso.controller import SSOController
from src.dependencies.sso.exceptions import BadRequestException
from src.dependencies.sso.sso_utils import (
    current_user,
    AuthRequestParameters,
    TokenRequestBody
)
from src.dependencies.sso.token_provider import create_access_token
from src.dependencies.sso.validators import ParamsValidator

sso_router = APIRouter(prefix='/sso', tags=['sso'])


@sso_router.post('/auth')
async def handle_auth(
    access_key: str = Form(),
    db: Session = Depends(get_db),
    params: AuthRequestParameters = Depends(AuthRequestParameters)
):
    user = await current_user(token=access_key, db=db)
    if not ParamsValidator().validate_authorize_params(params=params, db=db):
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
    if ParamsValidator().validate_token_params(params=body, db=db):
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


@sso_router.get(
    '/user_info',
    status_code=status.HTTP_200_OK
)
async def handle_user_info(user: UserResponse = Depends(current_user)):
    return {
        'sub': user.username,
        'name': user.name,
        'email': user.email
    }
