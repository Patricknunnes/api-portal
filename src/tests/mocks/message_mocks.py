from datetime import datetime

message = {
    'title': 'message title',
    'text': 'message text',
    'expiration_date': datetime.today(),
    'role_permission': None,
    'user_permission': None
}

message_with_invalid_string_as_date = {
    'title': 'message title',
    'text': 'message text',
    'expiration_date': 'date'
}

message_with_invalid_format_date = {
    'title': 'message title',
    'text': 'message text',
    'expiration_date': '2030/11/25'
}

message_with_expiration_date_past = {
    'title': 'message title',
    'text': 'message text',
    'expiration_date': '2022-12-31'
}

message_with_role_id = {
    'title': 'message title',
    'text': 'message text',
    'role_permission': '5545ccbe-9e27-4d3f-b26d-5aa5466906c6'
}

message_with_user_id = {
    'title': 'message title',
    'text': 'message text',
    'user_permission': '5545ccbe-9e27-4d3f-b26d-aaa5466906c9'
}
