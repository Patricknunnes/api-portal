from src.sso.sso_utils import AuthRequestParameters


def check_client_id(client_id: str):
    valid_client_ids = ['portal_idor']
    return client_id in valid_client_ids


def check_scope(request_scope: str):
    return 'openid' in request_scope


def check_response_type(type: str):
    return 'code' in type


def check_redirection_uri(uri: str):
    valid_uris = ['https://sso.test.canvaslms.com/login/oauth2/callback']
    return uri in valid_uris


def validate_params(params: AuthRequestParameters):
    return (
        check_client_id(params.client_id) and
        check_redirection_uri(params.redirect_uri) and
        check_response_type(params.response_type) and
        check_scope(params.scope)
    )
