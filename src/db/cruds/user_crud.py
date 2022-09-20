from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.db.cruds.base import BaseCRUD
from src.db.models.user_model import UserModel


class UserCRUD(BaseCRUD):
    def __init__(self):
        super(UserCRUD, self).__init__(UserModel)

    def get_user_document_or_email(self,
                                   db: Session,
                                   document: str = None,
                                   email: str = None) -> Union[UserModel, None]:
        user = db.query(self.model) \
            .where(or_(self.model.document == document, self.model.email == email)) \
            .first()
        return user

    def handle_list(self, db: Session,
                    filters: str = None,
                    page: int = None,
                    limit: int = None):
        page = page if page else 1
        limit = limit if limit else 20

        if filters:
            result = db.query(self.model) \
                .filter(or_(self.model.name.ilike(f'%{filters}%'),
                            self.model.email.ilike(f'%{filters}%'),
                            self.model.document.ilike(f'%{filters}%'),
                            self.model.phone.ilike(f'%{filters}%'))) \
                .limit(limit).offset((page - 1) * limit).all()

            count = self.count_registers(db=db, filters=filters)
        else:
            result = db.query(self.model).limit(limit).offset((page - 1) * limit).all()
            count = self.count_registers(db=db, filters=filters)

        return {'total': count, 'page': page, 'user_response': result}

    def count_registers(self, db: Session, filters: str = None):
        if filters:
            return db.query(self.model) \
                .filter(or_(self.model.name.ilike(f'%{filters}%'),
                            self.model.email.ilike(f'%{filters}%'),
                            self.model.document.ilike(f'%{filters}%'),
                            self.model.phone.ilike(f'%{filters}%'))).count()
        return db.query(self.model).count()
