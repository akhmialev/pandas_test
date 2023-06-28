from datetime import datetime, timedelta
import jwt

from web.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM

from web.bd import get_trainer, send_user, connect_to_mongodb


def check_data(data):
    if '.' in data:
        data = data.split('.')
        if len(data[0]) == 2 and len(data[1]) == 2:
            mount = data[1]
            if int(mount) <= 12:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def check_time(time):
    if '-' in time:
        time = time.split('-')
        if ':' in time[0] and ':' in time[1]:
            time_start = time[0].split(':')
            time_end = time[1].split(':')
            if len(time_start[0]) == 2 and len(time_start[1]) == 2 and len(time_end[0]) == 2 and len(time_end[1]) == 2:
                if int(time_start[0]) <= 23 and int(time_start[1]) <= 59 and int(time_end[0]) <= 23 and int(
                        time_end[1]) <= 59:
                    return True
                else:
                    return True
            else:
                return False
        else:
            return False
    else:
        return False


def check_id_trainer(id_trainer):
    if len(id_trainer) == 24:
        trainer = get_trainer(id_trainer)
        if trainer:
            return True
        else:
            return False
    else:
        return False


def check_user_id(id_user):
    if len(id_user) == 24:
        user = send_user(id_user)
        if user:
            return True
        else:
            return False
    else:
        return False


def create_access_token(username, user_id, user_type):
    user = {
        'username': username,
        'user_id': str(user_id),
        'user_type': user_type
    }
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'user': user, 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(username, user_id, user_type):
    user = {
        'username': username,
        'user_id': str(user_id),
        'user_type': user_type
    }
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {'user': user, 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials):
    token = credentials.credentials
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.PyJWTError:
        return False


def check_phone(phone):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'person.phone': str(phone)}
    user = collection.find_one(query)
    if user:
        return True


def check_email(email):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'person.email': str(email)}
    user = collection.find_one(query)
    if user:
        return True
