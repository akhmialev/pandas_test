from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

from user_api import *
from posts_api import *
from like_api import *

app = FastAPI()
security = HTTPBearer()


@app.post('/register', tags=['Register'])
async def register_user(username: str, password: str, first_name=None, last_name=None, age=None):
    """
            ## Регистрация пользователей
            Обязательные поля:<br>
            -username - имя пользователя<br>
            -password - пароль<br><br>
            Необязательные поля:<br>
            -name - Имя пользователя<br>
            -last_name - Фамилия<br>
            -age - возраст<br>
        """
    return add_user(username, password, first_name, last_name, age)


@app.post('/login', tags=['Register'])
async def login(username: str, password: str):
    """
         ## Логин
         email - почта<br>
         password - пароль
    """
    return user_login(username, password)


@app.post('/refresh', tags=['Register'])
async def create_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
        ## Создает ре фреш токен доступный 30 дней<br>
        credentials: токен<br>
        ## Отдает данные пользователя:<br>
        username: имя пользователя<br>
        password: пароль
        """
    return refresh(credentials)


@app.post('/{username}/posts', tags=['Posts'])
async def add_post(username: str, post_data: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    ## Создает новый пост
    """
    return post(username, post_data, credentials)


@app.delete('/post/delete', tags=['Posts'])
async def del_post(post_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    ## Удаляет пост
    """
    return delete_post(post_id, credentials)


@app.patch('/post/update', tags=['Posts'])
async def update_post(post_id: str, post_data: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    ## Обновляет пост
    """
    return update(post_id, post_data, credentials)


@app.get('/posts', tags=['Posts'])
async def get_posts(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    ## Выводит все посты пользователя
    """
    return send_posts(credentials)


@app.get('/post', tags=['Posts'])
async def get_post(post_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    ## Выводит конкретный пост
    """
    return send_post(post_id, credentials)


@app.post('/addLike', tags=['like'])
async def add_like(post_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    ## Добавляет лайк
    """
    return like(post_id, credentials)


@app.post('/dislike', tags=['like'])
async def add_dislike(post_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    ## Добавляет дизлайк
    """
    return dislike(post_id, credentials)

if __name__ == '__main__':
    uvicorn.run(app)
