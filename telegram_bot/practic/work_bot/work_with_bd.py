import pymongo



def connect_to_mongodb(host, port):
    """
        функиця подключения к базе данных
    :param host: адресс подключения
    :param port: порт подключения
    :return:
    """
    client = pymongo.MongoClient(host, port)
    db = client['mydatabase']
    collection = db['mycollection']
    return collection


def create_record(data, host, port):
    """
        Функиця для записи данных в бд mongoDB использовал insert_one для олной записи, если много записей можно исп.
        insert_many
    :param data:наши данные которые нужно записать          -> dict
    :return:
    """
    if type(data) == dict(data):
        collection = connect_to_mongodb(host, port)
        collection.insert_one(data)
        print("Данные успешно записаны")
    else:
        pass


def read_record(data, host, port):
    """
        функиця для поиска в бд
    :param data: наши данные
    :return:
    """
    collection = connect_to_mongodb(host, port)
    result = collection.find_one(data)
    print(result)


def update_record(data, new_data, host, port):
    """
        функция для редактирования записи в бд
    :param data: старые данные
    :param new_data: новыне данные              -> dict
    :return:
    """
    collection = connect_to_mongodb(host, port)
    new_data = {"$set": {new_data}}
    collection.update_one(data, new_data)
    print(f'Данные {data["name"]}')


def delete_record(data, host, port):
    """
        функиця для удаления записей из бд
    :param data: наши данные                    -> dict
    :return:
    """
    collection = connect_to_mongodb(host, port)
    result = collection.delete_one(data)

    if result.deleted_count > 0:
        print('Запись успешно удалено')
    else:
        print("Запись не найдена")
