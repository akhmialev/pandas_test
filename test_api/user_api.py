from fastapi import HTTPException

from db import *
from tools import hash_password, create_access_token, create_refresh_token, verify_token


def add_user(username, password, first_name, last_name, age):
    """
    Функция добавляет пользователя в бд
    """
    password = hash_password(password)
    return add_user_in_db(username, password, first_name, last_name, age)


def user_login(username, password):
    """
    Функция для авторизации пользователя и выдачи токенов
    """
    password = hash_password(password)
    if find_user(username, password):
        user_id = get_user_id(username, password)
        token = create_access_token(username, user_id)
        refresh_token = create_refresh_token(username, user_id)
        return {"access_token": token,
                'refresh_token': refresh_token}
    else:
        return {'message': "Учетные данные неверны. Пользователь не найден."}


def refresh(credentials):
    """
    Функция для обновления токена
    """
    decoded_token = verify_token(credentials)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    data = decoded_token.get('user')
    username = data['username']
    user_id = data['user_id']
    access_token = create_access_token(username, user_id)
    return {"access_token": access_token, 'data': data}
