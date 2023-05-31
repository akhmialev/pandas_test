from fastapi import FastAPI, HTTPException, status
from aiogram import executor
import uvicorn
from fastapi.responses import RedirectResponse

from bot_v2.bot import dp, on_startup
from users_api import *
from gyms_api import *

app = FastAPI()


@app.post('/api/user/register', tags=['User'])
def register(email: str, password: str, name=None, secondname=None, phone=None, age=None):
    """
        ## Регистрация пользователей
        При регистрации дается ID для привязки аккаунта к телеграмму.<br>
        Обязательные поля:<br>
        -email - почта<br>
        -password - пароль<br><br>
        Необязательные поля:<br>
        -name - Имя пользователя<br>
        -secondname - Фамилия<br>
        -phone - телефон<br>
        -age - возраст<br>
    """
    return add_user(email, password, name, secondname, phone, age)


@app.post('/api/login', tags=['Other'])
def login(email: str, password: str):
    """
     ## Логин
     email - почта<br>
     password - почта
    """
    if user_login(email, password):
        return RedirectResponse(url='/auth')
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильные имя пользователя или пароль",
        )


@app.post("/auth", tags=['Other'])
def auth():
    return {"message": "Аутентификация успешна"}


@app.get('/api/users/', tags=['User'])
async def return_users():
    """
    ## Возвращает всех пользователей
    """
    return get_users()


@app.get('/api/user/{user_id}', tags=['User'])
async def return_user(user_id: str):
    """
    ## Возвращает пользователя по id.
    User_id: id пользователя <br>
    """
    return get_user(user_id)


# @app.post('/api/user/add', tags=['User'])
# async def user_add(name: str, secondname: str, phone: int, age: int):
#     """
#     ## Добавляет пользователя
#     -name: Имя <br>
#     -secondname: Фамилия <br>
#     -phone: телефон <br>
#     -type: тип <br>
#     -age: возраст
#     """
#     return add_user(name, secondname, phone, age)


@app.post('/api/user/delete', tags=['User'])
async def delete_user(user_id: str):
    """
    ## Удаляет пользователя
    user_id: id пользователя <br>
    """
    return delete(user_id)


@app.post('/api/user/update', tags=['User'])
async def update_user(user_id: str, name: str, secondname: str, phone: int, age: int):
    """
    ## Обновляет пользователя
    user_id: id пользователя <br>
    name: имя <br>
    secondname: фамилия <br>
    phone: телефон <br>
    age: возраст <br>
    """
    return user_update(user_id, name, secondname, phone, age)


@app.get('/api/gyms/', tags=['gyms'])
async def get_gyms():
    """
    ## Выводит все залы
    """
    return gyms()


@app.post('/api/user_gyms/')
async def get_user_gym(id):
    """
    ## Выводит привязанные залы пользователя по ID.<br>
    id: ID пользователя
    """
    return user_gym(id)


@app.post('/api/trainers_in_gym/')
async def get_trainers_in_gyms(id):
    """
    ## Выводит тренеров конкретного зала по ID.<br>
    id - ID зала
    """
    return trainers_in_gym(id)


@app.post('/api/user_trainers/')
async def get_bind_trainers(user_id, gym_id):
    """
    ## Выводит тренеров привязанных тренеров конкретного зала пользователя.<br>
    user_id - id пользователя <br>
    gym_id - id привязанного зала у пользователя
    """
    return bind_trainers(user_id, gym_id)


@app.post('/api/add_gym/')
async def add_gym(id_user, id_gym):
    """
    ## Добавление зала пользователю.<br>
    id_user - ID пользователя <br>
    id_gym - ID зала
    """
    return add_gym_for_user(id_user, id_gym)


@app.post('/api/delete_gym')
async def delete_gym(id_user, id_gym):
    """
    ## Удаляет привязанный зал у пользователя.<br>
    id_user - ID пользователя <br>
    id_gym - ID зала
    """
    return gym_delete(id_user, id_gym)


if __name__ == '__main__':
    uvicorn.run(app, port=8080)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
