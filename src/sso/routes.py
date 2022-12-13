from fastapi import APIRouter, Depends, Form, status, Request
from fastapi.responses import RedirectResponse
from random import choices

from src.schemas.user_schema import UserResponse
from src.shared.auth.token_provider import create_access_token
from src.sso.sso_utils import current_user, AuthRequestParameters
from src.sso.validators import validate_params


sso_router = APIRouter(prefix='/sso', tags=['sso'])


@sso_router.post('/auth')
def handle_auth(
    params: AuthRequestParameters = Depends(AuthRequestParameters),
    _: UserResponse = Depends(current_user)
):
    if not validate_params(params):
        return RedirectResponse(
            url=f'{params.redirect_uri}?error=invalid_request&state={params.state}'
        )

    code = ''.join(choices(params.state, k=25))

    return RedirectResponse(url=f'{params.redirect_uri}?state={params.state}&code={code}')


@sso_router.post(
    '/token',
    status_code=status.HTTP_200_OK
)
async def handle_token(code: str = Form()):
    token = create_access_token(data={'sub': 2244})

    return {"id_token": token}


@sso_router.get(
    '/user_info',
    status_code=status.HTTP_200_OK
)
def handle_user_info(request: Request):
    return {'sub': 2244}
