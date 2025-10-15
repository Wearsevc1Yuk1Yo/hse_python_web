import json
import os
from datetime import datetime
from models.user import users_db, next_user_id, User
from models.post import posts_db, next_post_id, Post

DATA_FILE = "blog_data.json"

def save_data():

    try:
        data_to_save = {
            "users": {},
            "posts": {},
            "next_user_id": next_user_id,
            "next_post_id": next_post_id
        }

        # Сохраняем пользователей
        for user_id, user in users_db.items():
            data_to_save["users"][user_id] = {
                "id": user.id,
                "email": user.email,
                "login": user.login,
                "password": user.password,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            }

        # Сохраняем посты
        for post_id, post in posts_db.items():
            data_to_save["posts"][post_id] = {
                "id": post.id,
                "author_id": post.author_id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at.isoformat(),
                "updated_at": post.updated_at.isoformat()
            }

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        print("✅ Данные сохранены")
        
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")

def load_data():

    global users_db, posts_db, next_user_id, next_post_id

    if not os.path.exists(DATA_FILE):
        print("Файл данных не найден")
        return

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Очищаем текущие данные
        users_db.clear()
        posts_db.clear()

        # Загружаем пользователей
        for user_id_str, user_data in data.get("users", {}).items():
            try:
                user_id = int(user_id_str)
                user = User(
                    email=user_data.get("email", ""),
                    login=user_data.get("login", ""),
                    password=user_data.get("password", "")
                )
                user.id = user_id
                
                # получение дат
                created_at_str = user_data.get("created_at") or user_data.get("createdAt", "")
                updated_at_str = user_data.get("updated_at") or user_data.get("updatedAt", "")
                
                if created_at_str:
                    user.created_at = datetime.fromisoformat(created_at_str)
                if updated_at_str:
                    user.updated_at = datetime.fromisoformat(updated_at_str)
                    
                users_db[user_id] = user
            except Exception as e:
                print(f"❌ Ошибка загрузки пользователя {user_id_str}: {e}")

        # Загружаем посты
        for post_id_str, post_data in data.get("posts", {}).items():
            try:
                post_id = int(post_id_str)
                post = Post(
                    author_id=post_data.get("author_id") or post_data.get("authorId", 0),
                    title=post_data.get("title", ""),
                    content=post_data.get("content", "")
                )
                post.id = post_id
                
                # получение дат
                created_at_str = post_data.get("created_at") or post_data.get("createdAt", "")
                updated_at_str = post_data.get("updated_at") or post_data.get("updatedAt", "")
                
                if created_at_str:
                    post.created_at = datetime.fromisoformat(created_at_str)
                if updated_at_str:
                    post.updated_at = datetime.fromisoformat(updated_at_str)
                    
                posts_db[post_id] = post
            except Exception as e:
                print(f"❌ Ошибка загрузки поста {post_id_str}: {e}")

        # Восстанавливаем счетчики ID
        next_user_id = data.get("next_user_id", 1)
        next_post_id = data.get("next_post_id", 1)
        
        print(f"✅ Данные загружены: {len(users_db)} пользователей, {len(posts_db)} постов")
        
    except Exception as e:
        print(f"❌ Ошибка загрузки данных: {e}")

def get_data_stats():
    """Возвращает статистику по данным"""
    return {
        "users_count": len(users_db),
        "posts_count": len(posts_db),
        "data_file": DATA_FILE,
        "file_exists": os.path.exists(DATA_FILE)
    }