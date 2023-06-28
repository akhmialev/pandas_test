from web.bd import *
from web.checks import *
from fastapi import HTTPException


def get_users(credentials):
    """
        Функция для вывода всех пользователей
    """
    users = send_users()
    data = []
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    for user in users:
        data.append({
            '_id': str(user['_id']),
            'username': user['username'],
            'first_name': user['first_name'],
            'id_telegram': user['id_telegram'],
            'gyms': user['gyms'],
            'records': user['records'],
            'person': user['person']
        })
    return data


def get_user(user_id, credentials):
    """
        Функция для вывода пользователя по ID
    """
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
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
    if not check_email(email):
        if not check_phone(phone):
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
        tg_reg_in_db(email, password, phone, name, secondname, age)
        return {'created_user': 'success'}
    return {'message': "It's email is already used"}


def delete(user_id, credentials):
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    user = delete_user(user_id)
    if user:
        return {'delete': 'success'}
    else:
        return {'delete': 'id not in db'}


def user_update(user_id, name, secondname, phone, age, credentials):
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    return update(user_id, name, secondname, phone, age)


def user_login(email, password):
    if find_user(email, password):
        username, user_id, user_type = user_data(email)
        token = create_access_token(username, user_id, user_type)
        refresh_token = create_refresh_token(username, user_id, user_type)
        return {"access_token": token,
                'refresh_token': refresh_token}
    else:
        return {'message': 'access invalid'}


def refresh(credentials):
    decoded_token = verify_token(credentials)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    data = decoded_token.get('user')
    username = data['username']
    user_id = data['user_id']
    user_type = data['user_type']
    access_token = create_access_token(username, user_id, user_type)
    return {"access_token": access_token, 'data': data}
