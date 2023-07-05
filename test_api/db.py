import psycopg2
from config import dbname, user, password, host, port


def connect_to_db():
    """
        Функция для создания подключения к нашей базе данных
    """
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к базе данных PostgresSQL:", error)


def add_user_in_db(username, password, first_name, last_name, age):
    """
    Функция добавляет нового пользователя
    """
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        check_query = 'SELECT * FROM users WHERE username = %s'
        cursor.execute(check_query, (username,))
        existing_user = cursor.fetchall()
        if existing_user:
            return f"Пользователь с таким именем уже существует"
        else:
            insert_query = f"INSERT INTO users (username, password,first_name, last_name, age)" \
                           f" VALUES (%s, %s, %s, %s, %s)"
            values = (username, password, first_name, last_name, age)
            cursor.execute(insert_query, values)
            connection.commit()
            connection.close()
            return f"Пользователь успешно добавлен в базу данных"


def find_user(username, password):
    """
    Функция для поиска пользователя
    """
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        check_query = 'SELECT * FROM users WHERE username = %s and password = %s'
        cursor.execute(check_query, (username, password))
        result = cursor.fetchall()

        if result:
            return True
        else:
            return False
    connection.close()


def get_user_id(username, password):
    """
    Функция возвращает id user
    """
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        check_query = 'SELECT * FROM users WHERE username = %s and password = %s'
        cursor.execute(check_query, (username, password))
        return cursor.fetchall()[0][0]


def add_post_to_db(username, title, content, user_id):
    """
    Функция добавляет новый пост
    """
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        existing_user = cursor.fetchall()
        if username != existing_user[0][1]:
            return {'message': 'Вы не можете создавать посты под другим username'}
        insert_query = """
            INSERT INTO posts (user_id, title, content) VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, title, content))
        connection.commit()
        connection.close()
        return {"message": "Пост успешно создан"}


def delete_post_in_db(post_id, user_id):
    """
    Функция для удаления поста из базы данных
    """
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        check_query = "SELECT * FROM posts WHERE id = %s"
        cursor.execute(check_query, (post_id,))
        existing_posts = cursor.fetchall()
        user_post_id = existing_posts[0][-1]
        if user_id != user_post_id:
            return {'message': 'Вы не можете удалять чужие посты'}
        if existing_posts:
            delete_query = 'DELETE FROM posts WHERE id = %s'
            cursor.execute(delete_query, (post_id,))
            connection.commit()
            connection.close()
            return {"message": "Пост успешно удален"}
        else:
            return {'message': 'Пост не найден'}


def update_post_in_db(post_id, title, content, user_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        check_query = "SELECT * FROM posts WHERE id = %s"
        cursor.execute(check_query, (post_id,))
        existing_posts = cursor.fetchall()
        user_post_id = existing_posts[0][-1]
        if user_id != user_post_id:
            return {'message': 'Вы не можете редактировать чужие посты'}
        if existing_posts:
            update_query = 'UPDATE posts SET title = %s, content = %s WHERE id = %s'
            cursor.execute(update_query, (title, content, post_id))
            connection.commit()
            return {'message': 'Пост успешно обновлен'}
        else:
            return {'message': 'Пост не найдет'}


def get_user_posts_in_db(user_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM posts WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        posts = cursor.fetchall()
        connection.close()
        post_list = []
        for post in posts:
            post_dict = {
                'id_post': post[0],
                'title': post[1],
                'content': post[2]
            }
            post_list.append(post_dict)
        return {'message': f'{post_list}'}


def get_post_in_db(post_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM posts WHERE id = %s"
        cursor.execute(query, (post_id,))
        data = cursor.fetchall()
        post = {
            'id_post': data[0][0],
            'title': data[0][1],
            'content': data[0][2]
        }
        return {'message': f'{post}'}



def add_like_in_db(post_id, user_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        check_query = "SELECT * FROM posts WHERE id = %s"
        cursor.execute(check_query, (post_id,))
        result = cursor.fetchall()
        if result:
            user_id_in_post = result[0][-1]
            if user_id_in_post == user_id:
                return {'message': 'Вы не можете ставить лайк на свои посты'}
            else:
                check_query = 'SELECT * FROM likes WHERE user_id = %s and post_id = %s'
                cursor.execute(check_query, (user_id, post_id))
                result = cursor.fetchall()
                if result:
                    if not result[0][-1]:
                        update_query = 'UPDATE likes SET is_like = True WHERE user_id = %s AND post_id = %s'
                        cursor.execute(update_query, (user_id, post_id))
                        connection.commit()
                        connection.close()
                        return {'message': 'Вы изменили дизлайк на лайк'}
                    else:
                        return {'message': "Вы уже поставили лайк на этот пост"}
                else:
                    insert_query = 'INSERT INTO likes (user_id, post_id, is_like) VALUES (%s, %s, true)'
                    cursor.execute(insert_query, (user_id, post_id))
                    connection.commit()
                    connection.close()
                    return {'message': 'Like added'}
        else:
            return {'message': 'Invalid post_id'}


def add_dislike_in_db(post_id, user_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        check_query = "SELECT * FROM posts WHERE id = %s"
        cursor.execute(check_query, (post_id,))
        result = cursor.fetchall()
        if result:
            user_id_in_post = result[0][-1]
            if user_id_in_post == user_id:
                return {'message': 'Вы не можете ставить дизлайк на свои посты'}
            else:
                check_query = 'SELECT * FROM likes WHERE user_id = %s and post_id = %s'
                cursor.execute(check_query, (user_id, post_id))
                result = cursor.fetchall()
                if result:
                    if result[0][-1]:
                        update_query = 'UPDATE likes SET is_like = FALSE WHERE user_id = %s AND post_id = %s'
                        cursor.execute(update_query, (user_id, post_id))
                        connection.commit()
                        connection.close()
                        return {'message': 'Вы изменили лайк на дизлайк'}
                    else:
                        return {'message': "Вы уже поставили дизлайк на этот пост"}
                else:
                    insert_query = 'INSERT INTO likes (user_id, post_id, is_like) VALUES (%s, %s, false)'
                    cursor.execute(insert_query, (user_id, post_id))
                    connection.commit()
                    connection.close()
                    return {'message': 'Dislike added'}
        else:
            return {'message': 'Invalid post_id'}
