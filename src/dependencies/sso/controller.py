from sqlalchemy.orm import Session
from random import choices

from src.db.cruds.user_crud import UserCRUD


class SSOController:
    def create_session(self, user_id: str, state: str, db: Session):
        session_code = ''.join(choices(state, k=25))
        UserCRUD().patch(db=db, object_id=user_id, data={'session_code': session_code})

        return session_code

    def validate_session(self, session_code: str, db: Session):
        return UserCRUD().get(db=db, session_code=session_code)
