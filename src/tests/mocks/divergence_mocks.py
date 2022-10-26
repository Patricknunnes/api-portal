email_null = {
    'id': '04e77e15-b296-4b02-a06b-6dd40a2334c8',
    'name': 'nome 1',
    'email': None,
    'document': '11111111111',
    'username': 'usuário1',
    'error': 'email inválido'
}

email_invalid = {
    'id': 'b673c463-ecb1-4b94-886d-53567106869d',
		'name': 'nome 2',
		'email': 'user@mail',
		'document': '22222222222',
		'username': 'usuário2',
		'error': 'email inválido'
}

email_in_use = {
    'id': '7238f396-c8ea-4bec-8446-e715d12fedf0',
		'name': 'nome 3',
		'email': 'user@mail.com',
		'document': '33333333333',
		'username': 'usuário3',
		'error': 'email já cadastrado'
}

divergences = [
    email_null,
    email_invalid,
    email_in_use
]