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
