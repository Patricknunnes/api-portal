client_with_secret = {
    'id': '34930736-8424-4254-84f5-92dd68e771ef',
    'client_id': 'client1',
    'client_secret': (
        'gAAAAABjmwIQgchFg_BswmIDoSZW4YSf6_d'
        'JRHpgPVEI7ZPeHIjD9IovpoU6WmydfIxg2t'
        'WANIqoUK8kM-an67HQwntmCH9LPw=='
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
    'state': 'any_jwt',
    'client_secret': 'client1_secret'
}
