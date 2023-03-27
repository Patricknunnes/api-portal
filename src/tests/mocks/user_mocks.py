from src.db.models.models import UserModel, RoleModel

from src.tests.mocks.institution_mocks import institution_mock

user_create_data = {
    'name': 'new_user',
    'role_id': '34930736-8424-4254-84f5-92dd68e771ef',
    'email': 'new_user@email.com',
    'document': '54709936803',
    'phone': 11111111111,
    'password': 'user_password',
    'username': '54709936803'
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
    'email': 'totvs@email.com',
    'phone': 22222222222
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
    'canvas_id': 1,
    'password': 'user_password',
    'role': {
        'id': '34930736-8424-4254-84f5-92dd68e771ef',
        'name': 'role_1'
    },
    'institution': institution_mock,
    'username': 'totvs_user',
    'session_code': 'session_code'
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
    },
    'institution': institution_mock,
    'image': None
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

invalid_username = 'invalid_username'

invalid_phone = 123

valid_user_id = '071aac88-f263-4c07-b215-7170d180da6a'

invalid_user_id = '52a558a6-8fbe-4c54-bfba-6667005f7a1a'

user_with_role_as_model = {
    'id': '071aac88-f263-4c07-b215-7170d180da6a',
    'name': 'new_user',
    'email': 'new_user@email.com',
    'document': '54709936803',
    'phone': 11111111111,
    'is_totvs': False,
    'password': 'user_password',
    'role': RoleModel(
        id='34930736-8424-4254-84f5-92dd68e771ef',
        name='role_1'
    ),
    'image': None
}

user_model = UserModel(**user_with_role_as_model)
