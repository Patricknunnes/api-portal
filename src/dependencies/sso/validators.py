from sqlalchemy.orm import Session

from src.dependencies.sso.sso_utils import AuthRequestParameters, TokenRequestBody
from src.db.cruds.client_crud import ClientCRUD
from src.dependencies.sso.hash_provider import verify_password


class ParamsValidator:
    def check_client_id(self, db: Session, client_id: str):
        client = ClientCRUD().get(db=db, client_id=client_id)
        return True if client else False

    def check_client_secret(self, db: Session, client_id: str, client_secret: str = None):
        client = ClientCRUD().get(db=db, client_id=client_id)

        if client and client.client_secret is None:
            return True
        return verify_password(client_secret, client.client_secret)

    def check_scope(self, request_scope: str):
        return 'openid' in request_scope

    def check_response_type(self, type: str):
        return 'code' == type

    def check_redirect_uri(self, db: Session, client_id: str, uri: str):
        client = ClientCRUD().get(db=db, client_id=client_id)

        return True if client and client.redirect_uri == uri else False

    def check_grant_type(self, type: str):
        return 'authorization_code' == type

    def validate_authorize_params(self, params: AuthRequestParameters, db: Session):
        return all([
            self.check_client_id(db, params.client_id),
            self.check_redirect_uri(db, params.client_id, params.redirect_uri),
            self.check_response_type(params.response_type),
            self.check_scope(params.scope)
        ])

    def validate_token_params(self, params: TokenRequestBody, db: Session):
        return all([
            self.check_client_id(db, params.client_id),
            self.check_redirect_uri(db, params.client_id, params.redirect_uri),
            self.check_client_secret(db, params.client_id, params.client_secret),
            self.check_grant_type(params.grant_type)
        ])
