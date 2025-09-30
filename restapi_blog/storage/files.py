from datetime import datetime
import json
import os
from main_structures import users_db, posts_db, next_user_id, next_post_id, User, Post


DATA = "blog_data.json"

def save():
    # сохраняем данные в json
    try:
        data_save = {
            "users": {},
            "posts": {},
            "next_user_id": next_user_id,
            "next_post_id": next_post_id
        }

        # для юзеров
        for user_id, user in users_db.items():
            data_save["users"][user_id] = {
                "id": user.id,
                "email": user.email,
                "login": user.login,
                "password": user.password,
                "createdAt": user.createdAt.isoformat(),
                "updatedAt": user.updatedAt.isoformat()
            }
        # для постов 
        for post_id, post in posts_db.items():
            data_save["posts"][post_id] = {
                "id": post.id,
                "authorId": post.authorId,
                "title": post.title,
                "content": post.content,
                "createdAt": post.createdAt.isoformat(),
                "updatedAt": post.updatedAt.isoformat()
            }
        
        with open(DATA, 'w', encoding='utf-8') as f:
            json.dump(data_save, f, indent=2, ensure_ascii=False)
        print("Данные сохранены")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")


# теперь достаем данные из файла, if needed
def load():
    global users_db, posts_db, next_user_id, next_post_id

    # если еще не сохраняли ничего
    if not os.path.exists(DATA):
        print("Файл не найден")
        return
    
    try:
        with open(DATA, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # очищаем текущие данные
        users_db.clear()
        posts_db.clear()

        # зазрузка юзеров
        for user_id_str, user_data in data.get("users", {}).items():
            user_id = int(user_id_str)
            user = User(user_data["email"], user_data["login"], user_data["password"])
            user.id = user_id

            user.createdAt = datetime.fromisoformat(user_data["createdAt"])
            user.updatedAt = datetime.fromisoformat(user_data["updatedAt"])
            users_db[user_id] = user
        
        # загрузка постов
        for post_id_str, post_data in data.get("posts", {}).items():
            post_id = int(post_id_str)
            post = Post(post_data["authorId"], post_data["title"], post_data["content"])
            post.id = post_id

            post.createdAt = datetime.fromisoformat(post_data["createdAt"])
            post.updatedAt = datetime.fromisoformat(post_data["updatedAt"])
            posts_db[post_id] = post

        next_user_id = data.get("next_user_id", 1)
        next_post_id = data.get("next_post_id", 1)
        print("Все данные загружены")
        
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
