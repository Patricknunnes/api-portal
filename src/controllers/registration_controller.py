from datetime import datetime
from sqlalchemy.orm import Session

from src.controllers.pagination_oriented_controller import PaginationOrientedController
from src.db.cruds.registration_crud import RegistrationCRUD
from src.exceptions.exceptions import BadRequestException, NotFoundException
from src.schemas.registration_schema import RegistrationCreateModel


class RegistrationController(PaginationOrientedController):
    def __init__(self):
        super(RegistrationController, self).__init__(RegistrationCRUD)

    def __validate_date(self, date: str):
        try:
            return datetime.strptime(date, '%Y-%m-%d')

        except ValueError:
            raise BadRequestException(
                detail='Data de expiração inválida. Siga o formato YYYY-MM-DD.'
            )

    def handle_create(self, db: Session, data: RegistrationCreateModel):
        data.birthdate = self.__validate_date(data.birthdate)
        service_registration = self.crud_class().get(
            db=db,
            document=data.document,
            service=data.service
        )
        if service_registration is not None:
            raise BadRequestException('O usuário já tem cadastro no serviço.')

        return super().handle_create(db, data)

    def handle_get_by_data(self, db: Session, data: dict, exception_message: str):
        result = self.crud_class().get(db=db, **data)
        if result is None:
            raise NotFoundException(detail=exception_message)

        return result

    def __format_sort(self, sort: str):
        sort_tuple = tuple()
        for option in sort.split(','):
            sort_data = option.split(':')
            if len(sort_data) == 1:
                sort_data.append('asc')
            sort_tuple = tuple([*sort_tuple, tuple(sort_data)])
        print(sort_tuple)
        return sort_tuple

    def handle_list(
        self,
        db: Session,
        filters: str = None,
        page: int = None,
        limit: int = None,
        sort: str = None
    ):
        return self.crud_class().handle_list(
            db=db,
            page=page,
            limit=limit,
            filters=filters,
            sort=self.__format_sort(sort) if sort else None,
            attrs=['email', 'status', 'service']
        )
