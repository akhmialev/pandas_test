from web.bd import *


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


def user_gym(user_id):
    user_gym_in_db = send_user_gym(user_id)
    return {'users_gyms': user_gym_in_db}


def add_gym_for_user(id_user, id_gym):
    add = add_gyms_db(id_user, id_gym)
    return {'added_gyms': f'success added {add}'}


def gym_delete(id_user, id_gym):
    delete = delete_gym_in_db(id_user, id_gym)
    return {'delete': delete}
