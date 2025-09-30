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
