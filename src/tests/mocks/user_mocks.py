user_create_data = {
    'name': 'new_user',
    'role_id': '34930736-8424-4254-84f5-92dd68e771ef',
    'email': 'new_user@email.com',
    'document': '54709936803',
    'phone': 11111111111,
    'password': 'user_password'
}

user_create_data_no_phone = {
    'name': 'new_user',
    'role_id': '34930736-8424-4254-84f5-92dd68e771ef',
    'email': 'new_user@email.com',
    'document': '54709936803',
    'password': 'user_password'
}

user_update_data = {
    'name': 'updated_user',
    'role_id': '34930736-8424-4254-84f5-92dd68e77148',
    'email': 'updated_user@email.com',
    'document': '54709936803',
    'phone': 22222222222,
}

invalid_user_create_data = {
    'name': '',
    'role_id': '34930736-8424-4254-84f5-92dd68e771ef',
    'email': 'new_user@email.com',
    'document': '54709936803',
    'password': ''
}

totvs_user_db_response = {
    'id': '071aac88-f263-4c07-b215-7170d180da6b',
    'name': 'new_user',
    'email': 'totvs@email.com',
    'document': '38956656576',
    'phone': 11111111111,
    'is_totvs': True,
    'password': 'user_password',
    'role': {
        'id': '34930736-8424-4254-84f5-92dd68e771ef',
        'name': 'role_1'
    }
}

user_db_response = {
    'id': '071aac88-f263-4c07-b215-7170d180da6a',
    'name': 'new_user',
    'email': 'new_user@email.com',
    'document': '54709936803',
    'phone': 11111111111,
    'is_totvs': False,
    'password': 'user_password',
    'role': {
        'id': '34930736-8424-4254-84f5-92dd68e771ef',
        'name': 'role_1'
    }
}

user_db_response_no_phone = {
    'id': '071aac88-f263-4c07-b215-7170d180da6a',
    'name': 'new_user',
    'email': 'new_user@email.com',
    'document': '54709936803',
    'password': 'user_password',
    'role': {
        'id': '34930736-8424-4254-84f5-92dd68e771ef',
        'name': 'role_1'
    }
}

invalid_document = '11111111111'

invalid_phone = 123

valid_user_id = '071aac88-f263-4c07-b215-7170d180da6a'

invalid_user_id = '52a558a6-8fbe-4c54-bfba-6667005f7a1a'
