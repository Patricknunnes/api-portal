client_with_secret = {
    'id': '34930736-8424-4254-84f5-92dd68e771ef',
    'client_id': 'client1',
    'client_secret': (
        'gAAAAABjm297gUUedBE6Zx4nYNG7CiDilafKewZdqn5D7bF7cbp0I0uso2'
        'YYf9ztPIPPoPqm9fFAtv_DEm0c2XvfY-cwaLh1HA=='
    ),
    # plain_client_secret: client1_secret
    'redirect_uri': 'http://redirect_uri/client1.com'
}

client_without_secret = {
    'id': '34930736-8424-4254-84f5-92dd68e771ef',
    'client_id': 'client2',
    'client_secret': None,
    'redirect_uri': 'http://redirect_uri/client2.com'
}

valid_auth_request_params = {
    'client_id': 'client1',
    'redirect_uri': 'http://redirect_uri/client1.com',
    'response_type': 'code',
    'scope': 'openid',
    'state': 'any_jwt'
}

valid_token_request_body = {
    'client_id': 'client1',
    'redirect_uri': 'http://redirect_uri/client1.com',
    'grant_type': 'authorization_code',
    'client_secret': 'openid',
    'code': 'valid_code'
}
