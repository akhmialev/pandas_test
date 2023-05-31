import pymongo
from config import URL_FOR_CONNECT_TO_DB
from bson import ObjectId


def connect_to_mongodb():
    """
        Функция подключения к базе данных
    """
    client = pymongo.MongoClient(URL_FOR_CONNECT_TO_DB)
    db = client['record_bot']
    return db


def send_users():
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    users = collection.find()
    return users


def send_user(user_id):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'_id': ObjectId(str(user_id))}
    user = collection.find_one(query)
    return user


def create_user(user):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    user = collection.insert_one(user)
    user_id = str(user.inserted_id)
    return user_id


def delete_user(user_id):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'_id': ObjectId(str(user_id))}
    user = collection.find_one(query)
    if user:
        collection.delete_one(query)
        return True
    else:
        return False


def update(user_id, name, secondname, phone, age):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        query = {'_id': ObjectId(str(user_id))}
        update_fields = {'name': name,
                         'secondname': secondname,
                         'phone': phone,
                         'age': age}
        collection.update_one(filter=query, update={'$set': {'person': update_fields}})
        return {"message": "Items updated successfully"}
    except Exception as e:
        return {'error': str(e)}


def find_user(email, password):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    users = collection.find()
    for user in users:
        if user['person']['email'] == email and user['person']['password'] == password:
            return True
    return False


def send_gyms():
    db = connect_to_mongodb()
    collections = db.get_collection('gyms')
    gyms = collections.find()
    g = []
    for gym in gyms:
        g.append(gym)
    return g


def send_user_gym(id):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'_id': ObjectId(id)}
    user = collection.find_one(query)
    return user['gyms']


def send_trainers_in_gym(id):
    db = connect_to_mongodb()
    collection = db.get_collection('gyms')
    query = {'_id': ObjectId(id)}
    gym = collection.find_one(query)
    trainers = []
    for trainer in gym['trainers']:
        trainers.append(trainer['id'])

    collection = db.get_collection('trainers')
    trainer_data = []
    for trainer in trainers:
        tr = collection.find_one({'_id': ObjectId(trainer)})
        trainer_data.append(f"{tr['name']} {tr['last_name']}")
    return trainer_data


def send_bind_trainers(user_id, gym_id):
    db = connect_to_mongodb()
    collection = db.get_collection('gyms')
    query = {'_id': ObjectId(gym_id)}
    gym = collection.find_one(query)
    gym_title = gym['title']

    tr_id = []
    collection = db.get_collection('users')
    query = {'_id': ObjectId(user_id)}
    user = collection.find_one(query)
    for gym in user['gyms']:
        if gym_title == gym['gym']:
            for tr_tile in gym['id_trainers']:
                tr_id.append(tr_tile['id'])

    tr_name = []
    collection = db.get_collection('trainers')
    for id in tr_id:
        query = {'_id': ObjectId(id)}
        trainer_name = collection.find_one(query)
        tr_name.append(f"{trainer_name['name']} {trainer_name['last_name']}")
    return tr_name


def add_gyms_db(id_user, id_gym):
    db = connect_to_mongodb()
    collection = db.get_collection('gyms')
    query = {'_id': ObjectId(id_gym)}
    gym = collection.find_one(query)
    gym_title = gym['title']

    collection = db.get_collection('users')
    query = {'_id': ObjectId(id_user)}
    update = {'$addToSet': {'gyms': {'gym': gym_title,
                                     'status_gym': 'дополнительный',
                                     'id_trainers': []}}}
    collection.update_one(query, update)
    update = {'$addToSet': {'selected_gyms': {'id': id_gym}}}
    collection.update_one(query, update)
    return gym_title


def delete_gym_in_db(id_user, id_gym):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        query_del = {'_id': ObjectId(id_user)}

        delete = {'$pull': {'selected_gyms': {'id': id_gym}}}
        collection.update_one(query_del, delete)

        query = {'_id': ObjectId(id_gym)}
        collection = db.get_collection('gyms')
        gym = collection.find_one(query)
        gym_title = gym['title']

        collection = db.get_collection('users')
        delete = {'$pull': {'gyms': {'gym': gym_title}}}
        collection.update_one(query_del, delete)
        return 'success'

    except Exception as e:
        return f'{e}'


