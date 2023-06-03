from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse

from web.users_api import *
from web.gyms_api import *
from web.trainer_api import *
from web.record_api import *

app = FastAPI()


@app.post('/web/user/register', tags=['Register'])
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


@app.post('/web/login', tags=['Register'])
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


@app.post("/auth", tags=['Register'])
def auth():
    return {"message": "Аутентификация успешна"}


@app.get('/web/users/', tags=['User'])
async def return_users():
    """
    ## Возвращает всех пользователей
    """
    return get_users()


@app.get('/web/user/{user_id}', tags=['User'])
async def return_user(user_id: str):
    """
    ## Возвращает пользователя по id.
    User_id: id пользователя <br>
    """
    return get_user(user_id)


@app.delete('/web/user/delete', tags=['User'])
async def delete_user(user_id: str):
    """
    ## Удаляет пользователя
    user_id: id пользователя <br>
    """
    return delete(user_id)


@app.put('/web/user/update', tags=['User'])
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


@app.get('/web/gyms/', tags=['Gym'])
async def get_gyms():
    """
    ## Выводит все залы
    """
    return gyms()


@app.post('/web/user_gyms/', tags=['Gym'])
async def get_user_gym(user_id):
    """
    ## Выводит привязанные залы пользователя по ID.<br>
    id: ID пользователя
    """
    return user_gym(user_id)


@app.post('/web/trainers_in_gym/', tags=['Trainer'])
async def get_trainers_in_gyms(id_gym):
    """
    ## Выводит тренеров конкретного зала по ID.<br>
    id - ID зала
    """
    return trainers_in_gym(id_gym)


@app.post('/web/user_trainers/', tags=['Trainer'])
async def get_bind_trainers(user_id, gym_id):
    """
    ## Выводит тренеров привязанных тренеров конкретного зала пользователя.<br>
    user_id - id пользователя <br>
    gym_id - id привязанного зала у пользователя
    """
    return bind_trainers(user_id, gym_id)


@app.post('/web/add_gym/', tags=['Gym'])
async def add_gym(id_user, id_gym):
    """
    ## Добавление зала пользователю.<br>
    id_user - ID пользователя <br>
    id_gym - ID зала
    """
    return add_gym_for_user(id_user, id_gym)


@app.delete('/web/delete_gym', tags=['Gym'])
async def delete_gym(id_user, id_gym):
    """
    ## Удаляет привязанный зал у пользователя.<br>
    id_user - ID пользователя <br>
    id_gym - ID зала
    """
    return gym_delete(id_user, id_gym)


@app.post('/web/add_trainer', tags=['Trainer'])
async def add_trainer(id_user, id_gym, id_trainer):
    """
    ## Добавляет тренера к пользователю.<br>
    id_user - ID пользователя <br>
    id_gym - ID зала <br>
    id_trainer - ID тренера
    """
    return add_trainer_for_user(id_user, id_gym, id_trainer)


@app.delete('/web/delete_trainer', tags=['Trainer'])
async def delete_trainer(id_user, id_gym, id_trainer):
    """
    ## Удаляет тренера у пользователю.<br>
    id_user - ID пользователя <br>
    id_gym - ID зала <br>
    id_trainer - ID тренера
    """
    return trainer_delete(id_user, id_gym, id_trainer)


@app.post('/web/choice_date', tags=['Record'])
async def choice_date(id_trainer):
    """
    ## Выводит рабочие дни тренера.<br>
    id_trainer - ID тренера
    """
    return date_record(id_trainer)


@app.post('/web/choice_time', tags=['Record'])
async def choice_time(id_trainer, date):
    """
    ## Выводит время для записи к тренеру(если время занято его не будет).<br>
    id_trainer - ID тренера<br>
    date - Дата в формате (10.06 , 11.07 и т.п.)
    """
    return time_record(id_trainer, date)


@app.post('/web/record_finish', tags=['Record'])
async def record_finish(id_user, id_trainer, date, time):
    """
    ## Записывает к тренеру.<br>
    id_user - ID пользователя <br>
    id_trainer - ID тренера <br>
    date - выбранный день записи <br>
    time - выбранное время записи в формате(10:00-11:00)
    """
    return finish_record(id_user, id_trainer, date, time)
