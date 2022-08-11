# from fastapi import Depends, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from jose import JWTError
#
# from src.db.settings.config import get_db
# from src.exceptions.exceptions import UnAuthorizedException
# from src.settings.providers.token_provider import decode_token
# from src.schemas.auth_schema import ProfileResponse
# from src.db.cruds.user_crud import UserCRUD
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
#
#
# def profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> ProfileResponse:
#     exception = UnAuthorizedException(detail="Token invalido.")
#
#     try:
#         user_id: str = decode_token(token=token)
#
#         if not user_id:
#             raise exception
#
#     except JWTError:
#         raise exception
#
#     user = UserCRUD().get(db=db, id=user_id)
#
#     if not user:
#         raise exception
#
#     print(user)
#
#     return  # ProfileDTO(email=data['email'], is_accessible=accessible)
#
#
# def is_accessible(user_id: str, url: str, method: str) -> bool:
#     user = get_user_by_email(user_email)
#     user_permissions = user.user_permission.select()
#     for permission in user_permissions:
#         if permission.role.is_admin:
#             return True
#
#     try:
#         end_point = EndPoint.get(method=method, url=url)
#     except EndPoint.DoesNotExist:
#         raise UrlException("Impossível verificar acesso para essa url - Url não encontrada na database")
#
#     for permission in user_permissions:
#         if Access.select(Access).where((Access.end_point == end_point) & (Access.role == permission.role)).exists():
#             return True
#     return False
#
# #
# # class VerifyProfile():
# #
# #     def __init__(self, profile: ProfileResponse) -> None:
# #         self._profile = profile
# #
# #     def verify(self) -> bool:
# #         return self._profile.is_accessible
# #
# #     def verifyOrFail(self) -> None:
# #         if not self.verify():
# #             raise HTTPException(
# #                 status_code=status.HTTP_401_UNAUTHORIZED,
# #                 detail='Não possui nível de permissão necessário para continuar.'
# #             )
# #
# #     def getOrFail(self) -> ProfileDTO:
# #         self.verifyOrFail()
# #         return self._profile
# #
# #
# # def verify_profile_factory(profile: ProfileDTO = Depends(profile)) -> VerifyProfile:
# #     return VerifyProfile(profile)
