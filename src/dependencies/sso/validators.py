from sqlalchemy.orm import Session

from src.dependencies.sso.sso_utils import AuthRequestParameters
from src.db.cruds.client_crud import ClientCRUD


class ParamsValidator:
    def check_client_id(self, db: Session, client_id: str):
        client = ClientCRUD().get(db=db, client_id=client_id)
        if client:
            return True
        return False

    def check_client_secret(self, db: Session, client_id: str, client_secret: str = None):
        client = ClientCRUD().get(db=db, client_id=client_id)
        if client.client_secret == None:
            return True
        pass

    def check_scope(self, request_scope: str):
        return 'openid' in request_scope

    def check_response_type(self, type: str):
        return 'code' == type

    def check_redirection_uri(self, db: Session, client_id: str, uri: str):
        client = ClientCRUD().get(db=db, client_id=client_id)

        return client.redirect_uri == uri

    def validate_authorize_params(self, params: AuthRequestParameters, db: Session):
        return (
            self.check_client_id(db, params.client_id) and
            self.check_client_secret(db, params.client_id, params.client_secret) and
            self.check_redirection_uri(db, params.client_id, params.redirect_uri) and
            self.check_response_type(params.response_type) and
            self.check_scope(params.scope)
        )
