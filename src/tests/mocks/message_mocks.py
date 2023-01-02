message = {
    'title': 'message title',
    'text': 'message text'
}

valid_expiration_date = '2023-12-31'

uuid_test = '5545ccbe-9e27-4d3f-b26d-5aa5466906c6'

message_with_expiration_date = dict(
    **message,
    expiration_date=valid_expiration_date
)

message_with_role_permission = dict(**message, role_permission=uuid_test)

message_with_user_permission = dict(**message, user_permission=uuid_test)

message_with_all_fields = dict(
    **message_with_expiration_date,
    role_permission=uuid_test,
    user_permission=uuid_test
)

message_with_invalid_string_as_date = dict(
    **message,
    expiration_date='date'
)

message_with_invalid_format_date = dict(
    **message,
    expiration_date='2030/11/25'
)
