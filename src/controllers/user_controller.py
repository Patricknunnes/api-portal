import re
from uuid import UUID
from typing import Union

from sqlalchemy.orm import Session

from src.controllers.base import BaseController
from src.controllers.role_controller import RoleController
from src.exceptions.excepetions import BadRequestException
from src.schemas.utils_schema import ValidateDocs
from src.shared.utils import UtilService
from src.settings.providers.hash_provider import get_password_hash
from src.db.cruds.user_crud import UserCRUD
from src.schemas.user_schema import (
    UserBase,
    UserResponse,
    UserUpdate
)


class UserController(BaseController):

    def __init__(self):
        super(UserController, self).__init__(UserCRUD)

    def __clean_form(self, data: Union[UserBase, UserUpdate], session: Session = None):
        new_form = UtilService.remove_none_in_form(data)

        if data.role_id:
            RoleController().handle_get(db=session, object_id=data.role_id, exception_message='Role não encontrada.')

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

        UtilService.validate_schema(schema_base=UserBase, form=new_data)
        new_data['password'] = get_password_hash(new_data['password'])

        return self.crud_class().create(db=db, data=new_data, commit=commit)

    def handle_patch(self, db: Session, object_id: UUID, data: UserUpdate, commit=True) -> None:
        new_data = self.__clean_form(data=data, session=db)

        self.handle_get(db=db, object_id=object_id, exception_message='Usuário não encontrado.')

        return self.crud_class().patch(db=db, object_id=object_id, data=new_data, commit=True)
