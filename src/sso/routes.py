from fastapi import APIRouter, Depends, Form, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.db.settings.config import get_db
from src.schemas.user_schema import UserResponse
from src.sso.sso_utils import current_user, AuthRequestParameters
from src.sso.validators import validate_params
from src.sso.token_provider import create_access_token
from src.sso.controller import SSOController


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
