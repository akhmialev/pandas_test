from bd import *


def gyms():
    gyms_in_db = send_gyms()
    data = []
    for gym in gyms_in_db:
        data.append({
            '_id': str(gym['_id']),
            'title': gym['title'],
            'descriptions': gym['descriptions'],
            'city': gym['city'],
            'address': gym['address'],
            'trainers': gym['trainers'],
        })
    return data


def user_gym(id):
    user_gym_in_db = send_user_gym(id)
    return {'users_gyms': user_gym_in_db}


def trainers_in_gym(id):
    trainers_in_gym_in_db = send_trainers_in_gym(id)
    return {'trainers_name': trainers_in_gym_in_db}


def bind_trainers(user_id, gym_id):
    trainers_bind = send_bind_trainers(user_id, gym_id)
    return {'trainer_name': trainers_bind}


def add_gym_for_user(id_user, id_gym):
    add = add_gyms_db(id_user, id_gym)
    return {'added_gyms': f'success added {add}'}


def gym_delete(id_user, id_gym):
    delete = delete_gym_in_db(id_user, id_gym)
    return {'delete': delete}
