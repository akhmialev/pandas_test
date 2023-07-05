from tools import get_user_id_in_token, verify_token
from db import add_post_to_db, delete_post_in_db, update_post_in_db, get_user_posts_in_db, get_post_in_db


def post(username, post_data, credentials):
    """
    Функция добавляет пост в бд
    """
    user_id = get_user_id_in_token(credentials)
    title = post_data.get('title')
    content = post_data.get('content')
    if user_id:
        return add_post_to_db(username, title, content, user_id)
    else:
        return {'message': 'user_id not found'}


def delete_post(post_id, credentials):
    """
    Функция удаляет пост из бд
    """
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    user_id = get_user_id_in_token(credentials)
    return delete_post_in_db(post_id, user_id)


def update(post_id, post_data, credentials):
    """
    Функция обновляет пост в бд
    """
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    user_id = get_user_id_in_token(credentials)
    title = post_data.get('title')
    content = post_data.get('content')
    return update_post_in_db(post_id, title, content, user_id)


def send_posts(credentials):
    """
    Функция показывает все посты конкретного юзера
    """
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    user_id = get_user_id_in_token(credentials)
    return get_user_posts_in_db(user_id)


def send_post(post_id, credentials):
    """
    Функция показывает конкретный пост
    """
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    return get_post_in_db(post_id)
