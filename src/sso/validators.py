from src.sso.sso_utils import AuthRequestParameters


def check_client_id(client_id: str):
    valid_client_ids = ['canvas_idor']
    return client_id in valid_client_ids


def check_scope(request_scope: str):
    scopes = request_scope.split()

    valid_scopes = ['openid', 'canvas']
    for scope in scopes:
        if scope not in valid_scopes:
            return False
    return True


def check_response_type(type: str):
    valid_types = ['code']
    return type in valid_types


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
