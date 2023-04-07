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
        "id_telegram": user_id,
        "trainers": [{
            "id_trainers": "",
            "status": "",
        }],
        "gym": [{
            "id_gym": "",
            "status_gym": "",
        }]
    }
    users = collection.find()
    for user in users:
        if user['id_telegram'] != user_id:
            collection.insert_one(data)


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


def update_record(data_to_save, tr_id):
    my_query = {"_id": ObjectId(tr_id)}
    my_data = {"$push": {"clients": data_to_save}}
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


def check_user_click(telegram_id):
    """
        Функция проверяет записан ли клиент
    :param telegram_id: телеграм ID
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users_check_click')
    all_record = collection.find()
    for record in all_record:
        if record['telegram_id'] == telegram_id and record['date'] == str(datetime.datetime.now().date()):
            return True
    return False


def save_user_click(date_to_save):
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
            'record_time': record_time
        }
    })


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
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    id_tr = ObjectId(tr_id)
    trainer = collection.find_one({'_id': id_tr})
    return len(trainer['working_schedule']['work_days'])

# def add_el():
#     db = connect_to_mongodb()
#     collection = db.get_collection('trainers')
#     data = {
#         "name": "Иван",
#         "last_name": "Иванович",
#         "id_telegram": "",
#         "records": [{
#             "id_user": "",
#             "date": "",
#             "time": "",
#             "status": ""
#         }],
#         "working_schedule": {
#             "weekend_days": [],
#             "work_days": [
#                 {
#                     "date": "06.04",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "07.04",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "08.04",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "09.04",
#                     "time": "11-15"
#                 },
#                 {
#                     "date": "10.04",
#                     "time": "12-15"
#                 },
#                 {
#                     "date": "11.04",
#                     "time": "13-15"
#                 },
#                 {
#                     "date": "12.04",
#                     "time": "5-15"
#                 },
#                 {
#                     "date": "13.04",
#                     "time": "6-15"
#                 },
#                 {
#                     "date": "14.04",
#                     "time": "7-15"
#                 },
#                 {
#                     "date": "15.04",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "16.04",
#                     "time": "9-15"
#                 },
#                 {
#                     "date": "17.04",
#                     "time": "10-14"
#                 },
#                 {
#                     "date": "18.04",
#                     "time": "10-16"
#                 },
#                 {
#                     "date": "19.04",
#                     "time": "10-17"
#                 },
#                 {
#                     "date": "20.04",
#                     "time": "10-18"
#                 },
#                 {
#                     "date": "21.04",
#                     "time": "10-19"
#                 },
#                 {
#                     "date": "22.04",
#                     "time": "7-20"
#                 },
#                 {
#                     "date": "23.04",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "24.04",
#                     "time": "8-21"
#                 },
#                 {
#                     "date": "25.04",
#                     "time": "9-22"
#                 },
#                 {
#                     "date": "26.04",
#                     "time": "10-23"
#                 },
#                 {
#                     "date": "28.04",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "29.04",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "30.04",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "01.05",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "02.05",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "03.05",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "04.05",
#                     "time": "10-15"
#                 },
#                 {
#                     "date": "05.05",
#                     "time": "10-15"
#                 },
#             ]
#         },
#         "rating": {
#             "id_user": "",
#             "rating": ""
#         },
#         "grade": {
#             "title": "",
#             "description": "",
#             "date": "",
#         },
#         "photo_url": ""
#     }
#     collection.insert_one(data)
# add_el()
