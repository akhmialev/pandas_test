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
    my_data = {"$set": {"clients": data_to_save}}
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




def delete_record(data):
    """
        Функция для удаления записей из бд
    :param data: наши данные                    -> dict
    :return:
    """
    collection = connect_to_mongodb()
    result = collection.delete_one(data)

    if result.deleted_count > 0:
        print('Запись успешно удалено')
    else:
        print('Запись не найдена')
