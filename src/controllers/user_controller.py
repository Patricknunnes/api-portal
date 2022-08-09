import re
from uuid import UUID
from typing import Union

from sqlalchemy.orm import Session

from src.controllers.base import BaseController
from src.controllers.role_controller import RoleController
from src.exceptions.excepetions import BadRequestException, NotFoundException
from src.schemas.utils_schema import ValidateDocs
from src.shared.utils import UtilService
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
            role = RoleController().handle_get(db=session, object_id=data.role_id)
            if not role:
                raise NotFoundException('Role não encontrada.')

        if data.document:
            document = ValidateDocs(type_doc='cpf', number=data.document)

            if not UtilService.validate_doc(document).get('valid'):
                raise BadRequestException('Documento invalido.')

            new_form['document'] = re.sub(r'\W+', '', data.document)

        return new_form

    def handle_create(self, db: Session, data: UserBase, commit=True) -> UserResponse:
        new_data = self.__clean_form(data=data, session=db)

        user = self.crud_class().get_user_document_or_email(db=db, document=new_data['document'],
                                                            email=new_data['email'])
        print(new_data)

        return self.crud_class().create(db=db, data=new_data, commit=commit)
