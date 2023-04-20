import datetime

import pymongo
from bson import ObjectId
from config import URL_FOR_CONNECT_TO_DB


def connect_to_mongodb():
    """
        Функция подключения к базе данных
    """
    client = pymongo.MongoClient(URL_FOR_CONNECT_TO_DB)
    db = client['record_bot']
    return db


def create_user_in_db(user_id, username, first_name):
    """
        Функция для добавления в бд нового пользователя
    :param user_id: телеграм id
    :param username: username телеграмма
    :param first_name: fn телеграмма
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    data = {
        "username": username,
        "first_name": first_name,
        "id_telegram": str(user_id),
        "trainers": [],
        "gym": []
    }
    query = {'id_telegram': str(user_id)}
    users = collection.find_one(query)
    if users is None:
        collection.insert_one(data)


def update_user_save(telegram_id, tr_id):
    """
        Функция для обновления данных пользователя
    """
    data = {'id_trainers': tr_id,
            'status': ''}
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    my_data = {'$addToSet': {'trainers': data}}
    collection.update_one(query, my_data)


def get_work_time(tr_id, date):
    """
        Функция берет время работы тренера на определенную дату
    :param tr_id: id тренера
    :param date: рабочая дата тренера
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    query = {'_id': ObjectId(tr_id)}
    trainer = collection.find_one(query)
    for tr in trainer['working_schedule']['work_days']:
        if date == (tr['date']):
            return tr['time']


def check_time(tr_id, date):
    """
        Функция для проверки времени
    :param tr_id: id тренера
    :param date: дата которую выбрал пользователь
    """
    tr_id = ObjectId(tr_id)
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    query = {'_id': tr_id}
    records = collection.find_one(query)
    for record in records['records']:
        if record['date'] == str(date):
            time = record['time'][:5]
            return time


def send_all_trainers():
    """
        Функция подключения к бд и возврата коллекции со всеми тренерами.
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    trainers = collection.find()
    return trainers


def send_trainer_for_query(query):
    """
        Функция для поиска нужного тренера.
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    trainer = collection.find_one(query)
    return trainer


def save_record_to_trainer(telegram_id, record_date, record_time, tr_id):
    """
        Функция для сохранения записи к тренеру
    """
    data = {
        'id_user': telegram_id,
        'date': record_date,
        'time': record_time,
        'status': ''
    }
    my_query = {"_id": ObjectId(tr_id)}
    my_data = {"$push": {"records": data}}
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    collection.update_one(my_query, my_data)


def read_record(url):
    """
        Функция для поиска в бд
    """
    client = pymongo.MongoClient(url)
    db = client['record_bot']
    collections = db.get_collection('trainers')
    res = {'id': 1}
    result = collections.find_one(res)

    print(result)


def check_user_click(telegram_id, tr_id):
    """
        Функция проверяет записан ли клиент
    :param telegram_id: телеграм ID
    :param tr_id: ID тренера
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users_check_click')
    all_record = collection.find()
    for record in all_record:
        for trainer_id in record['trainers_id']:
            if str(trainer_id) == str(tr_id):
                if record['telegram_id'] == telegram_id and record['date'] == str(datetime.datetime.now().date()):
                    return True
    return False


def save_user_click(date_to_save, tr_id):
    """
        Функция сохраняет клиента если он 1 раз записывается или перезаписывает если дату прошла
    """
    telegram_id = date_to_save['telegram_id']
    date = date_to_save['date']
    first_name = date_to_save['first_name']
    username = date_to_save['username']
    record_date = date_to_save['record_date']
    record_time = date_to_save['record_time']

    db = connect_to_mongodb()
    collection = db.get_collection('users_check_click')
    query = {'telegram_id': telegram_id}
    find = collection.find_one(query)
    if not find:
        collection.insert_one({'telegram_id': telegram_id})
    collection.update_one(filter=query, update={
        "$set": {
            'date': date,
            'first_name': first_name,
            'username': username,
            'record_date': record_date,
            'record_time': record_time,
        },
        '$addToSet': {
            'trainers_id': tr_id
        }

    }, upsert=True)


def take_trainer_name(tr_id):
    """
        Функция для поиска ФИО тренера
    :param tr_id: id тренера
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    id_tr = ObjectId(tr_id)
    trainer = collection.find_one({'_id': id_tr})
    return trainer['name'], trainer['last_name']


def take_working_schedule(tr_id):
    """
        Функция берет рабочий график тренера
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    id_tr = ObjectId(tr_id)
    trainer = collection.find_one({'_id': id_tr})
    return len(trainer['working_schedule']['work_days'])


def get_gyms():
    """
        Функция берет все залы
    """
    db = connect_to_mongodb()
    collection = db.get_collection('gyms')
    gyms = collection.find()
    return gyms


def check_user_in_menu(user_id):
    # не использую
    """
        Функция проверяет есть ли пользователь
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(user_id)}
    user = collection.find_one(query)
    for u in user['gym']:
        if u['id_gym'] is None:
            return False
        return True

def check_user_in_db(user_id):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(user_id)}
    user = collection.find_one(query)
    if user is None:
        return False
    return True


def save_user_choice(telegram_id, choice):
    """
        Функция для сохранения залов пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    collection.update_one(filter=query, update={
        '$addToSet': {
            'gym': {'id_gym': choice,
                    'status_gym': ''}
        }
    }, upsert=True)


def delete_user_choice(telegram_id, choice):
    """
        Функция для удаления залов пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    collection.update_one(filter=query, update={
        '$pull': {
            'gym': {'id_gym': choice}
        }
    }, upsert=True)


def get_user_gyms(telegram_id):
    """
        Функция возвращает все залы пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    return user['gym']


def save_user_data(telegram_id, selected_type_gym):
    """
        Функция для сохранения основных залов
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id), 'gym.id_gym': selected_type_gym}
    update = {'$set': {'gym.$.status_gym': 'основной'}}
    collection.update_one(filter=query, update=update, upsert=True)


def delete_user_data(telegram_id, selected_type_gym):
    """
        Функция для удаления основных залов пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id), 'gym.id_gym': selected_type_gym}
    update = {'$set': {'gym.$.status_gym': ''}}
    collection.update_one(filter=query, update=update, upsert=True)

def check_user_trainer(id_telegram):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': id_telegram}
    trainer = collection.find_one(query)
    if trainer['trainers'] == []:
        return True
    else:
        return False

def get_id_trainers(gym):
    db = connect_to_mongodb()
    collection = db.get_collection('gyms')
    query = {'title': str(gym)}
    trainers = collection.find_one(query)
    trainer_id = []
    for trainer in trainers['trainers']:
        trainer_id.append(trainer['id'])
    return trainer_id

def get_trainers(trainers_id):
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    trainers = []
    for trainer in trainers_id:
        tr = collection.find_one({'_id': ObjectId(trainer)})
        trainers.append(f"{tr['name']} {tr['last_name']}")
    return trainers
