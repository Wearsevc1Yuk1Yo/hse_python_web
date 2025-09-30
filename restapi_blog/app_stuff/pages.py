from main_structures.main import users_db, posts_db
from datetime import datetime

def make_html_page(title: str, content: str):
    ...
    # тут каркас фронта

def author_name(author_id: int):
    if author_id in users_db:
        return users_db[author_id].login
    return "Неизвестный автор"

def mainpage():
    ...
    # глав страница
    # сюда пойдут for post om posts и с автором датой вот это все

def viewed_post(post_id: int):
    ...
    # страница после просмотра

def create_post():
    ...
    # как создать пост 
    # создать пользователя -> инфо -> пост

def edit_post():
    ...
    # форма редакта поста

def create_user():
    ...
    # форма создания акка

