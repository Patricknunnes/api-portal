from datetime import datetime
from src.db.models.models import MessageModel

uuid_test = '5545ccbe-9e27-4d3f-b26d-5aa5466906c6'

message = {
    'title': 'message title',
    'text': 'message text',
    'updated_by': uuid_test,
    'created_by': uuid_test
}

message_with_max_length_title = {
    'title': ''.join([str(i) for i in range(30)]),
    'text': 'message text',
    'is_important': False
}

message_with_too_long_title = {
    'title': ''.join([str(i) for i in range(31)]),
    'text': 'message text'
}

valid_expiration_date = '2023-12-31'

invalid_message_id = '52a558a6-8fbe-4c54-bfba-6667005f7a1a'

message_with_expiration_date = dict(
    **message,
    expiration_date=valid_expiration_date
)

message_with_role_permission = dict(**message, role_permission=uuid_test)

message_with_user_permission = dict(**message, user_permission=uuid_test)

message_with_all_fields = dict(
    **message_with_expiration_date,
    role_permission=uuid_test,
    user_permission=uuid_test,
    is_important=True
)

message_with_invalid_string_as_date = dict(**message, expiration_date='date')

message_with_invalid_format_date = dict(
    **message,
    expiration_date='2030/11/25'
)

message_created_with_all_fields = MessageModel(
    **message_with_role_permission,
    expiration_date=datetime.strptime(valid_expiration_date, '%Y-%m-%d'),
    id=uuid_test,
    user_permission=uuid_test,
    created_at=datetime(2000, 1, 1, 0, 0),
    updated_at=None,
    is_important=True
)
