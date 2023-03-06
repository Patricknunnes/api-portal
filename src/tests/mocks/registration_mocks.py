from datetime import datetime


registrations = [
    {
        'document': '12345678903',
        'email': 'test1@email.com',
        'birthdate': datetime.strptime('2000-01-01', '%Y-%m-%d'),
        'status': 'ANALYSIS',
        'service': 'service 1'
    },
    {
        'document': '12345678902',
        'email': 'test2@email.com',
        'birthdate': datetime.strptime('2000-01-01', '%Y-%m-%d'),
        'status': 'APPROVED',
        'service': 'service 2'
    },
    {
        'document': '12345678901',
        'email': 'test3@email.com',
        'birthdate': datetime.strptime('2000-01-01', '%Y-%m-%d'),
        'status': 'REJECTED',
        'service': 'service 3'
    }
]

invalid_date_registration = {
    'document': '12345678903',
    'email': 'test1@email.com',
    'birthdate': '01/01/2000',
    'status': 'ANALYSIS',
    'service': 'service 1'
}

valid_date_registration = {
    'document': '12345678903',
    'email': 'test1@email.com',
    'birthdate': '2000-01-01',
    'status': 'ANALYSIS',
    'service': 'service 1'
}
