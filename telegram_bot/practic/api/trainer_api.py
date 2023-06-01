from bd import *


def trainers_in_gym(id_gym):
    trainers_in_gym_in_db = send_trainers_in_gym(id_gym)
    return {'trainers_name': trainers_in_gym_in_db}


def bind_trainers(user_id, gym_id):
    trainers_bind = send_bind_trainers(user_id, gym_id)
    return {'trainer_name': trainers_bind}


def add_trainer_for_user(id_user, id_gym, id_trainer):
    add = add_trainer_in_db(id_user, id_gym, id_trainer)
    return {'add_trainer': add}


def trainer_delete(id_user, id_gym, id_trainer):
    delete = delete_trainer_in_db(id_user, id_gym, id_trainer)
    return {'delete': delete}
