from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.db.cruds.base import BaseCRUD
from src.db.models.user_model import UserModel


class UserCRUD(BaseCRUD):
    def __init__(self):
        super(UserCRUD, self).__init__(UserModel)

    def get_user_document_or_email(self, db: Session, document: int = None, email: str = None):
        sql = db.query(self.model).filter(or_(self.model.document == document, self.model.email == email))

        return sql
