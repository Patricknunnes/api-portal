from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from src.db.cruds.user_crud import UserCRUD
from src.db.settings.config import get_db
from src.shared.utils import GetPathAndMethod
from src.exceptions.exceptions import UnAuthorizedException
from src.schemas.auth_schema import PermissionParams
from src.schemas.user_schema import UserMe
from src.shared.auth.token_provider import decode_token

from src.db.cruds.permission_crud import PermissionCRUD

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
permission = GetPathAndMethod()


async def current_user(token: str = Depends(oauth2_scheme),
                       permission: str = Depends(permission),
                       db: Session = Depends(get_db)) -> UserMe:
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

    data_permission = PermissionParams(
        user_role=user.role,
        path=permission['path'],
        method=permission['method']
    )

    await is_accessible(db=db, datas=data_permission)

    return user


async def is_accessible(db: Session, datas: PermissionParams) -> bool:
    free_paths = [
        '/access/me',
        '/access/me/favorite/{id}',
        '/auth/me',
        '/auth/sso/totvs',
        '/message/me',
        '/message/me/{id}',
        '/message/me/read/{id}',
        '/registration/office365',
        '/registration/office365/me',
        '/utils/image'
    ]

    if datas.user_role.name.lower() == 'root' or datas.path in free_paths:
        return True

    user_permissions = PermissionCRUD().get_permission(db=db, datas=datas)

    if user_permissions:
        return True

    raise UnAuthorizedException(detail="Usuário não autorizado.")
