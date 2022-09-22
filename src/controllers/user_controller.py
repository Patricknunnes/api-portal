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

        if data.role_id:
            RoleController().handle_get(db=session,
                                        object_id=data.role_id,
                                        exception_message='Role não encontrada.')
        if data.phone:
            UtilService.validate_phone(phone=data.phone)

        if data.document:
            UtilService.validate_doc(ValidateDocs(type_doc='cpf', number=data.document))

            new_form['document'] = re.sub(r'\W+', '', data.document)

        return new_form

    def handle_create(self, db: Session, data: UserBase, commit=True) -> UserResponse:
        new_data = self.__clean_form(data=data, session=db)

        user = self.crud_class() \
            .get_user_document_or_email(db=db,
                                        document=new_data['document'],
                                        email=new_data['email'])

        if user:
            raise BadRequestException(detail='Documento ou Email já cadastrado.')

        UtilService.validate_schema(schema_base=UserSchemaValidate, form=new_data)
        new_data['password'] = get_password_hash(new_data['password'])

        return self.crud_class().create(db=db, data=new_data, commit=commit)

    def handle_list(self, db: Session,
                    filters: str = None,
                    page: int = None,
                    limit: int = None):

        search_result = self.crud_class().handle_list(db=db, filters=filters,
                                                      page=page,
                                                      limit=limit)

        return search_result

    def handle_patch(self,
                     db: Session,
                     object_id: UUID,
                     data: UserUpdate,
                     commit=True) -> None:
        new_data = self.__clean_form(data=data, session=db)

        user = self.handle_get(db=db,
                               object_id=object_id,
                               exception_message='Usuário não encontrado.')

        if user.is_totvs:
            raise BadRequestException(detail='Usuário só pode ser editado na TOTVS.')
        
        if 'document' in new_data:
            user_with_document = self.crud_class() \
            .get_user_document_or_email(db=db,
                                        document=new_data['document'])
            
            if user_with_document and user_with_document.email != user.email:
                raise BadRequestException(detail='Documento já cadastrado.')

        if 'email' in new_data:
            user_with_email = self.crud_class() \
            .get_user_document_or_email(db=db,
                                        email=new_data['email'])
            
            if user_with_email and user_with_email.document != user.document:
                raise BadRequestException(detail='E-mail já cadastrado.')

        return self.crud_class().patch(db=db,
                                       object_id=object_id,
                                       data=new_data,
                                       commit=True)
