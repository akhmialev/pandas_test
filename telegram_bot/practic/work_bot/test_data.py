import datetime

trainers = [
    {
        'name': 'Андрей',
        'lname': 'Андреевич',
        'time': [],
        'week_day': ['02.04', '05.04', '24.04', '20.04'],
        'clients': [
            {
                'telegram_id': "",
                'first_name': '',
                'username': '',
                'record_date': '',
                'record_time': '',
                'check_click': {
                    '':''
                }
            },
        ]
    },
    {
        'name': 'Петр',
        'lname': 'Петровчи',
        'time': [],
        'week_day': ['05.04', '06.04', '4.04', '25.04'],
        'clients': [
            {
                'telegram_id': "",
                'first_name': '',
                'username': '',
                'record_date': '',
                'record_time': '',
                'check_click': {
                    "":""
                }
            },
        ]
    },
    {
        'name': 'dmitriy',
        'lname': 'D',
        'time': [],
        'week_day': ['010.04', '12.04', '21.04', '29.04'],
        'clients': [
            {
                'telegram_id': "",
                'first_name': '',
                'username': '',
                'record_date': '',
                'record_time': '',
                'check_click': ''

            },
        ]
    },
]
for t in trainers:
    print(t['clients'])