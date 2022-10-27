import re
from uuid import UUID
from typing import Union

from sqlalchemy.orm import Session

from src.controllers.base import BaseController
from src.controllers.role_controller import RoleController
from src.exceptions.exceptions import BadRequestException
from src.schemas.utils_schema import ValidateDocs
from src.shared.utils import UtilService
from src.shared.auth.hash_provider import get_password_hash
from src.db.cruds.user_crud import UserCRUD
from src.schemas.user_schema import (
    UserBase,
    UserResponse,
    UserUpdate, UserSchemaValidate
)


class UserController(BaseController):

    def __init__(self):
        super(UserController, self).__init__(UserCRUD)

    def __clean_form(self, data: Union[UserBase, UserUpdate], session: Session = None):
        new_form = UtilService.remove_none_in_form(data)

        if 'role_id' in new_form:
            RoleController().handle_get(db=session,
                                        object_id=data.role_id,
                                        exception_message='Role não encontrada.')
        if data.phone:
            UtilService.validate_phone(phone=data.phone)

        if 'document' in new_form:
            UtilService.validate_doc(ValidateDocs(type_doc='cpf', number=data.document))

            new_form['document'] = re.sub(r'\W+', '', data.document)

        if 'password' in new_form:
            new_form['password'] = get_password_hash(new_form['password'])

        return new_form

    def handle_create(self, db: Session, data: UserBase, commit=True) -> UserResponse:
        new_data = self.__clean_form(data=data, session=db)

        user = self.crud_class().get_user_by_username_or_email(
            db=db,
            username=new_data['document'],
            email=new_data['email']
        )

        if user:
            raise BadRequestException(detail='Documento ou Email já cadastrado.')

        UtilService.validate_schema(schema_base=UserSchemaValidate, form=new_data)

        new_data['username'] = new_data['document']

        return self.crud_class().create(db=db, data=new_data, commit=commit)

    def handle_list(self, db: Session,
                    filters: str = None,
                    page: int = None,
                    limit: int = None):

        search_result = self.crud_class().handle_list(db=db, filters=filters,
                                                      page=page,
                                                      limit=limit)

        return search_result

    def handle_patch(self, db: Session,
                     object_id: UUID,
                     data: UserUpdate,
                     profile: UserResponse = None) -> None:
        new_data = self.__clean_form(data=data, session=db)

        user = self.handle_get(db=db,
                               object_id=object_id,
                               exception_message='Usuário não encontrado.')

        if 'password' in new_data and profile.role.name.upper() != 'ROOT':
            raise BadRequestException(
                detail='Usuário sem permissão para atualizar a senha.'
            )

        if user.is_totvs:
            raise BadRequestException(detail='Usuário só pode ser editado na TOTVS.')

        if 'email' in new_data and new_data['email'] != user.email:
            user_with_email = self.crud_class().get_user_by_username_or_email(
                db=db,
                email=new_data['email']
            )

            if user_with_email:
                raise BadRequestException(detail='E-mail já cadastrado.')

        return self.crud_class().patch(db=db,
                                       object_id=object_id,
                                       data=new_data,
                                       commit=True)
