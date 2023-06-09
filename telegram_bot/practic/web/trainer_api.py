from web.bd import *
from web.checks import verify_token


def trainers_in_gym(id_gym, credentials):
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    trainers_in_gym_in_db = send_trainers_in_gym(id_gym)
    return {'trainers_name': trainers_in_gym_in_db}


def bind_trainers(user_id, gym_id, credentials):
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    trainers_bind = send_bind_trainers(user_id, gym_id)
    return {'trainer_name': trainers_bind}


def add_trainer_for_user(id_user, id_gym, id_trainer,credentials):
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    add = add_trainer_in_db(id_user, id_gym, id_trainer)
    return {'add_trainer': add}


def trainer_delete(id_user, id_gym, id_trainer,credentials):
    if not verify_token(credentials):
        return {'message:': 'Invalid token'}
    delete = delete_trainer_in_db(id_user, id_gym, id_trainer)
    return {'delete': delete}
