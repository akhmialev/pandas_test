from fastapi import FastAPI, HTTPException, status
import uvicorn
from fastapi.responses import RedirectResponse
from users_api import *

app = FastAPI()


@app.post('/api/user/register', tags=['User'])
def register(email: str, password: str, name=None, secondname=None, phone=None, age=None):
    return add_user(email, password, name, secondname, phone, age)


@app.post('/api/login', tags=['Other'])
def login(email: str, password: str):
    if user_login(email, password):
        return RedirectResponse(url='/auth')
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильные имя пользователя или пароль",
        )


@app.post("/auth")
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


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
