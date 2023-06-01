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


def send_user_gym(user_id):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'_id': ObjectId(user_id)}
    user = collection.find_one(query)
    return user['gyms']


def send_trainers_in_gym(id_gym):
    db = connect_to_mongodb()
    collection = db.get_collection('gyms')
    query = {'_id': ObjectId(id_gym)}
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

    tr_ids = []
    collection = db.get_collection('users')
    query = {'_id': ObjectId(user_id)}
    user = collection.find_one(query)
    for gym in user['gyms']:
        if gym_title == gym['gym']:
            for tr_tile in gym['id_trainers']:
                tr_ids.append(tr_tile['id'])

    tr_name = []
    collection = db.get_collection('trainers')
    for tr_id in tr_ids:
        query = {'_id': ObjectId(tr_id)}
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
    updating = {'$addToSet': {'gyms': {'gym': gym_title,
                                       'status_gym': 'дополнительный',
                                       'id_trainers': []}}}
    collection.update_one(query, updating)
    updating = {'$addToSet': {'selected_gyms': {'id': id_gym}}}
    collection.update_one(query, updating)
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


def add_trainer_in_db(id_user, id_gym, id_trainer):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('gyms')
        gym = collection.find_one({'_id': ObjectId(id_gym)})
        gym_title = gym['title']

        collection = db.get_collection('users')
        query = {'_id': ObjectId(id_user)}

        add = {'$addToSet': {'selected_trainers': {'id': id_trainer}}}
        collection.update_one(query, add)

        updating = {'$addToSet': {'gyms.$.id_trainers': {'id': id_trainer}}}
        query = {'gyms.gym': gym_title}
        collection.update_one(query, updating)
        return 'success'

    except Exception as e:
        return f'{e}'


def delete_trainer_in_db(id_user, id_gym, id_trainer):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('gyms')
        gym = collection.find_one({'_id': ObjectId(id_gym)})
        gym_title = gym['title']

        collection = db.get_collection('users')
        query = {'_id': ObjectId(id_user)}
        delete = {'$pull': {'selected_trainers': {'id': id_trainer}}}
        collection.update_one(query, delete)

        query = {'gyms.gym': gym_title}
        delete = {'$pull': {'gyms.$.id_trainers': {'id': id_trainer}}}
        collection.update_one(query, delete)
        return 'success'

    except Exception as e:
        return f'{e}'


def send_data(id_trainer):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('trainers')
        query = {'_id': ObjectId(id_trainer)}

        trainer = collection.find_one(query)

        date = []
        for d in trainer['working_schedule']['work_days']:
            date.append(d['date'])
        return date

    except Exception as e:
        return f'{e}'


def send_time(id_trainer, date):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('trainers')
        query = {'_id': ObjectId(id_trainer)}

        trainer = collection.find_one(query)
        time = []
        for tr_date in trainer['working_schedule']['work_days']:
            if date == tr_date['date']:
                time.append(tr_date['time'])
        return time

    except Exception as e:
        return f'{e}'


def check_record_time(id_trainer, date):
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    query = {'_id': ObjectId(id_trainer)}

    time = []
    trainer = collection.find_one(query)
    for i in trainer['records']:
        if date == i['date']:
            time.append(i['time'][:2])

    return time

def record_in_db(id_trainer, date, time):
    ...



