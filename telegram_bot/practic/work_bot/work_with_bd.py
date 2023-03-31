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


def send_all_trainers():
    """
    Функция подключения к бд и возврата коллекции со всеми тренерами.
    """
    db = connect_to_mongodb()
    collection = db.get_collection('trainers')
    trainers = collection.find()
    return trainers


def send_trainer(query):
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
    collection = db.get_collection('users')
    all_record = collection.find()
    for record in all_record:
        if record['telegram_id'] == telegram_id and record['date'] == str(datetime.datetime.now().date()):
            return True
    return False


def save_user_click(telegram_id, date):
    """
        Функция сохраняет клиента если он 1 раз записывается или перезаписывает если дату прошла
    :param telegram_id: телеграм ID
    :param date: дата
    """
    db = connect_to_mongodb()
    collection = db.get_collection('users')
    query = {'telegram_id': telegram_id}
    find = collection.find_one(query)
    if not find:
        collection.insert_one({'telegram_id': telegram_id, 'date': date})
    collection.update_one(filter=query, update={"$set": {'date': date}})
