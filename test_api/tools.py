import hashlib
import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta

from config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, REFRESH_TOKEN_EXPIRE_DAYS


def hash_password(password):
    """
    Функция для хеширования пароля
    """
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def create_access_token(username, user_id):
    """
    Функция для создания токена
    """
    user = {
        'username': username,
        'user_id': user_id,
    }
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'user': user, 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(username, user_id):
    """
    Функция для создания ре-фреш токена
    """
    user = {
        'username': username,
        'user_id': user_id,
    }
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {'user': user, 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials):
    """
    Функция для декодирования токена
    """
    token = credentials.credentials
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.PyJWTError:
        return False


def get_user_id_in_token(credentials):
    """
    Функция для возврата id user из токена
    """
    token = credentials.credentials
    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decode_token['user']['user_id']
        return user_id
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
