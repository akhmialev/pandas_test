from tools import verify_token, get_user_id_in_token
from db import add_like_in_db, add_dislike_in_db


def like(post_id, credentials):
    """
    Функция проверяет токен и записывает лайк в бд
    """
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    user_id = get_user_id_in_token(credentials)
    return add_like_in_db(post_id, user_id)


def dislike(post_id, credentials):
    """
    Функция проверяет токен и записывает дизлайк в бд
    """
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    user_id = get_user_id_in_token(credentials)
    return add_dislike_in_db(post_id, user_id)
