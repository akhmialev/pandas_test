from bd import *


def get_users():
    """
        Функция для вывода всех пользователей
    """
    users = send_users()
    data = []
    for user in users:
        data.append({
            '_id': str(user['_id']),
            'username': user['username'],
            'first_name': user['first_name'],
            'id_telegram': user['id_telegram'],
            'gyms': user['gyms'],
            'records': user['records'],
            'crm_id': user['crm_id']
        })
    return data


def get_user(user_id):
    """
        Функция для вывода пользователя по ID
    """
    try:
        user = send_user(str(user_id))
        data = {
            '_id': str(user['_id']),
            'username': user['username'],
            'first_name': user['first_name'],
            'id_telegram': user['id_telegram'],
            'gyms': user['gyms'],
            'records': user['records'],
            'person': user['person']
        }
        return data
    except Exception as error:
        return {'error': error}


def add_user(email, password, name, secondname, phone, age):
    user = {
        'type': [],
        "username": '',
        "first_name": '',
        "id_telegram": '',
        "gyms": [],
        'records': [],
        'person': {
            'email': email,
            'password': password,
            'name': name,
            'secondname': secondname,
            'phone': phone,
            'age': age
        },
        'selected_gyms': [],
        'selected_type_gyms': [],
        'selected_trainers': [],
        'selected_del_record': [],
        'crm_id': ''
    }
    user_id = create_user(user)
    if user_id:
        return {'created_user': 'success',
                'id': user_id}
    else:
        return {'created_user': 'error'}


def delete(user_id):
    user = delete_user(user_id)
    if user:
        return {'delete': 'success'}
    else:
        return {'delete': 'id not in db'}


def user_update(user_id, name, secondname, phone, age):
    return update(user_id, name, secondname, phone, age)


def user_login(email, password):
    if find_user(email, password):
        return True
    else:
        return False

