import datetime

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


def user_in_db(telegram_id):
    """
        Функция проверяет есть ли пользователь в базе данных
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    users = collection.find_one(query)
    if users:
        return True
    else:
        return False


def create_user_in_db(telegram_id, username, first_name):
    """
        Функция для добавления в бд нового пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    data = {
        'type': [],
        "username": username,
        "first_name": first_name,
        "id_telegram": str(telegram_id),
        "gyms": [],
        'records': [],
        'person': {
            'name': '',
            'secondname': '',
            'phone': '',
            'age': ''
        },
        'selected_gyms': [],
        'selected_type_gyms': [],
        'selected_trainers': [],
        'selected_del_record': []
    }
    collection.insert_one(data)


def user_have_gym(telegram_id):
    """
        Функция проверяет есть ли у пользователя сохраненные залы
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    if user['gyms']:
        return True
    else:
        return False


def trainers_in_user(telegram_id, gym):
    """
        Функция проверяет есть ли у пользователя сохраненные тренера
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    for user_gym in user['gyms']:
        if user_gym['gym'] == gym:
            if user_gym['id_trainers']:
                return True
    return False


def get_gyms():
    """
        Функция берет все залы
    """
    db = connect_to_mongodb()
    collection = db.get_collection('gyms')
    gyms = collection.find()
    return gyms


def get_trainers_in_gym(gym):
    """
        Функция возвращает всех тренеров конкретного зала
    """
    db = connect_to_mongodb()
    collection = db.get_collection('gyms')
    query = {'title': str(gym)}
    gym = collection.find_one(query)
    return gym['trainers']


def get_trainers(trainers_in_gym):
    """
        Функция возвращает список тренеров из конкретного зала
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    trainers = []
    for tr_in_gym in trainers_in_gym:
        query = {'_id': ObjectId(tr_in_gym['id'])}
        trainers.append(collection.find_one(query))
    return trainers


def get_user_trainers(trainers_id):
    """
        Функция возвращает список словарей с тренерами
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    trainers = []
    for trainer in trainers_id:
        trainer = ObjectId(trainer)
        trainers.append(collection.find_one({'_id': trainer}))
    return trainers


def delete_user_choice(telegram_id, choice):
    """
        Функция для удаления залов пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    collection.update_one(filter=query, update={
        '$pull': {
            'gyms': {'gym': choice}
        }
    }, upsert=True)


def save_user_choice(telegram_id, choice):
    """
        Функция для сохранения залов пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    collection.update_one(filter=query, update={
        '$addToSet': {
            'gyms': {'gym': choice,
                     'status_gym': 'дополнительный',
                     'id_trainers': []}
        }
    }, upsert=True)


def selected_trainers(telegram_id):
    """
        Функция возвращает список id выбранных тренеров
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    ids = []
    for tr_id in user['selected_trainers']:
        ids.append(tr_id['id'])
    return ids


def selected_gyms(telegram_id):
    """
        Функция возвращает список id выбранных залов
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    ids = []
    for gym_id in user['selected_gyms']:
        ids.append(gym_id['id'])
    return ids


def overwrite_main_status(telegram_id, gym):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    for g in user['gyms']:
        if g['gym'] == gym:
            g['status_gym'] = 'основной'
            collection.update_one(query, {'$set': {'gyms': user['gyms']}})

def overwrite_extra_status(telegram_id, gym):
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    for g in user['gyms']:
        if g['gym'] == gym:
            g['status_gym'] = 'дополнительный'
            collection.update_one(query, {'$set': {'gyms': user['gyms']}})


def delete_selected_gyms(gym_id, telegram_id):
    """
        Функция удаляет id выбранного зала
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    update = {'$pull': {'selected_gyms': {'id': gym_id}}}
    collection.update_one(query, update)


def add_selected_gyms(gym_id, telegram_id):
    """
        Функция добавляет id выбранного зала
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    add = {'$addToSet': {'selected_gyms': {'id': gym_id}}}
    collection.update_one(query, add)


def delete_selected_trs(telegram_id, gym_id):
    """
        Функция удаляет тренеров из selected_trainers, если пользователь удалит зал
    """
    db = connect_to_mongodb()
    collection = db.get_collection('gyms')
    query = {'_id': ObjectId(gym_id)}
    gym = collection.find_one(query)
    tr_in_gyms = []
    for g in gym['trainers']:
        tr_in_gyms.append(g['id'])

    collection = db.get_collection('users')
    q = {'id_telegram': str(telegram_id)}
    user = collection.find_one(q)
    selected_trs = user['selected_trainers']
    new_selected_trs = []
    for tr in selected_trs:
        if tr['id'] in tr_in_gyms:
            continue
        new_selected_trs.append(tr)
    update = {'$set': {'selected_trainers': new_selected_trs}}
    collection.update_one(q, update)


def delete_selected_trainers(telegram_id, trainer_id):
    """
        Функция удаляет id выбранного тренера
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    update = {'$pull': {'selected_trainers': {'id': trainer_id}}}
    collection.update_one(query, update)


def add_selected_trainers(telegram_id, trainer_id):
    """
        Функция добавляет id выбранного тренера
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    add = {'$addToSet': {'selected_trainers': {'id': trainer_id}}}
    collection.update_one(query, add)


def save_trainer_in_user(data_trainer, telegram_id):
    """
        Функция сохраняет запись в тренере
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    trainer_id = data_trainer.split('_')[-1]
    trainer_gym = data_trainer.split('_')[1]

    query = {'id_telegram': str(telegram_id), 'gyms.gym': trainer_gym}
    update = {'$addToSet': {'gyms.$.id_trainers': {
        'id': trainer_id,
    }}}
    collection.update_one(query, update)


def delete_trainer_in_user(data_trainer, telegram_id):
    """
        Функция удаляет запись в тренере
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    trainer_id = data_trainer.split('_')[-1]
    trainer_gym = data_trainer.split('_')[1]

    query = {'id_telegram': str(telegram_id), 'gyms.gym': trainer_gym}
    delete_trainer = {'$pull': {'gyms.$.id_trainers': {
        'id': trainer_id,
    }}}
    collection.update_one(query, delete_trainer)


def get_trainers_id(telegram_id, gym):
    """
        Функция возвращает список id тренеров которые сохранены у пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    trainers_id = []
    for tr in user['gyms']:
        if tr['gym'] == gym:
            for trainer in tr['id_trainers']:
                trainers_id.append(trainer['id'])
    return trainers_id


def get_user_gyms(telegram_id):
    """
        Функция возвращает все залы пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    return user['gyms']


def save_user_data(telegram_id, selected_type_gym):
    """
        Функция для сохранения основных залов
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id), 'gyms.gym': selected_type_gym}
    update = {'$set': {'gyms.$.status_gym': 'основной'}}
    collection.update_one(filter=query, update=update, upsert=True)


def delete_user_data(telegram_id, selected_type_gym):
    """
        Функция для удаления основных залов пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id), 'gyms.gym': selected_type_gym}
    update = {'$set': {'gyms.$.status_gym': ''}}
    collection.update_one(filter=query, update=update, upsert=True)


def get_work_days(trainer_id):
    """
        Функция возвращает список рабочих дней(дат) тренера
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    query = {'_id': ObjectId(str(trainer_id))}
    trainer = collection.find_one(query)
    date_lst = []
    for date in trainer['working_schedule']['work_days']:
        date_lst.append(date['date'])
    return date_lst


def get_trainer_work_time(trainer_id, day):
    # тут косяк мы строим меню со временем, но не проверяем records!
    """
        Функция возвращает рабочие время тренера в данный день
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    query = {'_id': ObjectId(str(trainer_id))}
    trainer = collection.find_one(query)
    trainer_name = trainer['name']
    trainer_last_name = trainer['last_name']
    for tr in trainer['working_schedule']['work_days']:
        if tr['date'] == day:
            return str(tr['time']), trainer_name, trainer_last_name


def check_time(trainer_id, day):
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    query = {'_id': ObjectId(str(trainer_id))}
    trainer = collection.find_one(query)
    for record in trainer['records']:
        if str(day) == record['date']:
            time = record['time'][:5]
            return time


def check_user_click(telegram_id, trainer_id):
    """
        Функция проверяет запись в бд (пользователь может записаться к тренерам 1 раз в день)
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users_check_click')
    query = {'telegram_id': str(telegram_id)}
    user = collection.find_one(query)
    if user:
        if str(trainer_id) in user['trainer_id'] and user['date'] == str(datetime.datetime.now().date()):
            return True
    return False


def save_record_to_trainer(telegram_id, trainer_id, time, day, first_name, username):
    """
         Функция сохраняет запись к тренеру
     """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    query = {'_id': ObjectId(str(trainer_id))}
    update = {'$addToSet': {'records': {
        'id_user': str(telegram_id),
        'first_name': first_name,
        'username': username,
        'date': day,
        'time': time,
        'status': ''
    }}}
    trainer = collection.update_one(query, update=update)
    return trainer


def save_user_click(telegram_id, trainer_id):
    """
        Функция записывает клик пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users_check_click')
    update_query = {'$addToSet': {'trainer_id': trainer_id}}
    query = {'telegram_id': str(telegram_id)}
    user = collection.find_one(query)
    if user:
        collection.update_one(filter=query, update=update_query, upsert=True)
    else:
        collection.insert_one({'telegram_id': str(telegram_id),
                               'trainer_id': [trainer_id],
                               'date': str(datetime.datetime.now().date())})


def save_record_to_user(telegram_id, trainer_id, time, day, trainer_name, trainer_last_name):
    """
        Функция сохраняет запись к пользователю
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    update = {'$addToSet': {'records': {
        'trainer_id': trainer_id,
        'trainer_name': trainer_name,
        'trainer_last_name': trainer_last_name,
        'time': time,
        'date': day
    }}}
    collection.update_one(query, update=update)


def get_user_name(trainer_id):
    """
        Функция возвращает имя и фамилию тренера
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    query = {'_id': ObjectId(str(trainer_id))}
    trainer = collection.find_one(query)
    return trainer['name'], trainer['last_name']


def send_user_record(telegram_id):
    """
        Функция возвращает записи пользователя
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    return user['records']


def selected_del_record(telegram_id):
    """
        Функция возвращает список с id тренеров
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    user = collection.find_one(query)
    trainers_id = []
    for trainer in user['selected_del_record']:
        if trainer['id']:
            trainers_id.append(trainer['id'])
    return trainers_id


def delete_selected_records(telegram_id, trainer_id):
    """
        Функция удаляет id выбранной записи для удаления
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id-telegram': str(telegram_id)}
    update = {'$pull': {'selected_del_record': {'id': trainer_id}}}
    collection.update_one(query, update=update)


def add_selected_records(telegram_id, trainer_id):
    """
        Функция добавляет id выбранной записи для удаления
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'id_telegram': str(telegram_id)}
    add = {'$addToSet': {'selected_del_record': {'id': trainer_id}}}
    collection.update_one(query, add)
