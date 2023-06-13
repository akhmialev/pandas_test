import datetime
import pymongo
from bson import ObjectId

from web.config import URL_FOR_CONNECT_TO_DB


def connect_to_mongodb():
    """
        Функция подключения к базе данных
    """
    client = pymongo.MongoClient(URL_FOR_CONNECT_TO_DB)
    db = client['record_bot']
    return db


def send_users():
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        users = collection.find()
        return users
    except Exception as e:
        return f'{e}'


def send_user(user_id):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        query = {'_id': ObjectId(str(user_id))}
        user = collection.find_one(query)
        return user
    except Exception as e:
        return f'{e}'


def create_user(user):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        user = collection.insert_one(user)
        user_id = str(user.inserted_id)
        return user_id
    except Exception as e:
        return f'{e}'


def delete_user(user_id):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        query = {'_id': ObjectId(str(user_id))}
        user = collection.find_one(query)
        if user:
            collection.delete_one(query)
            return True
        else:
            return False
    except Exception as e:
        return f'{e}'


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


def user_data(email):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'person.email': email}
    user = collection.find_one(query)
    return user['username'], user['_id'], user['type']




def find_user(email, password):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        users = collection.find()
        for user in users:
            if user['person']['email'] == email and user['person']['password'] == password:
                return True
        return False
    except Exception as e:
        return f'{e}'


def send_gyms():
    try:
        db = connect_to_mongodb()
        collections = db.get_collection('gyms')
        gyms = collections.find()
        g = []
        for gym in gyms:
            g.append(gym)
        return g
    except Exception as e:
        return f'{e}'


def send_user_gym(user_id):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        query = {'_id': ObjectId(user_id)}
        user = collection.find_one(query)
        return user['gyms']
    except Exception as e:
        return f'{e}'


def send_trainers_in_gym(id_gym):
    try:
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
    except Exception as e:
        return f'{e}'


def send_bind_trainers(user_id, gym_id):
    try:
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
    except Exception as e:
        return f'{e}'


def add_gyms_db(id_user, id_gym):
    try:
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
    except Exception as e:
        return f'{e}'


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


def get_trainer(id_trainer):
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    query = {'_id': ObjectId(id_trainer)}
    trainer = collection.find_one(query)
    return trainer


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
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('trainers')
        query = {'_id': ObjectId(id_trainer)}

        time = []
        trainer = collection.find_one(query)
        for i in trainer['records']:
            if date == i['date']:
                time.append(i['time'][:2])

        return time
    except Exception as e:
        return f'{e}'


def check_click(id_user, id_trainer):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        query = {'_id': ObjectId(id_user)}
        user = collection.find_one(query)
        id_telegram = user['id_telegram']

        collection = db.get_collection('users_check_click')
        query = {'telegram_id': id_telegram}
        user = collection.find_one(query)
        if user:
            if str(id_trainer) in user['trainer_id'] and user['date'] == str(datetime.datetime.now().date()):
                return True
            return False
    except Exception as e:
        return f'{e}'


def save_record_to_trainer(id_user, id_trainer, date, time):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        query = {'_id': ObjectId(id_user)}
        user = collection.find_one(query)
        first_name = user['first_name']
        username = user['username']

        collection = db.get_collection('trainers')
        query = {'_id': ObjectId(id_trainer)}
        updating = {'$addToSet': {'records': {
            'id_user': str(id_user),
            'first_name': first_name,
            'username': username,
            'date': date,
            'time': time,
            'status': ''
        }}}
        collection.update_one(query, update=updating)
    except Exception as e:
        return f'{e}'


def save_record_to_user(id_user, id_trainer, date, time):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('trainers')
        query = {'_id': ObjectId(id_trainer)}
        trainer = collection.find_one(query)
        name = trainer['name']
        last_name = trainer['last_name']

        collection = db.get_collection('users')
        query = {'_id': ObjectId(id_user)}
        updating = {'$addToSet': {'records': {
            'trainer_id': id_trainer,
            'trainer_name': name,
            'trainer_last_name': last_name,
            'time': time,
            'date': date
        }}}
        collection.update_one(query, update=updating)
        return f'вы записаны к {name} {last_name} на {date} с {time}'

    except Exception as e:
        return f'{e}'


def save_user_click(id_user, id_trainer):
    try:
        db = connect_to_mongodb()
        collection = db.get_collection('users')
        query = {'_id': ObjectId(id_user)}
        user = collection.find_one(query)
        telegram_id = user['id_telegram']

        collection = db.get_collection('users_check_click')
        query = {'telegram_id': telegram_id}
        updating = {'$addToSet': {'trainer_id': id_trainer}}
        user = collection.find_one(query)
        if user:
            collection.update_one(query, update=updating)
        else:
            collection.insert_one({'telegram_id': str(telegram_id),
                                   'trainer_id': [id_trainer],
                                   'date': str(datetime.datetime.now().date())})
    except Exception as e:
        return f'{e}'
