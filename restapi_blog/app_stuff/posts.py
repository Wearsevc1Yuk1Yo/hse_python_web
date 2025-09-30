from fastapi import HTTPException
from main_structures.main import Post, posts_db, users_db
from storage.files import save
from datetime import datetime

# создать, получить-прочитать все посты, получить один конкретный по ID, обновить, удалить

async def create_post(authorId: int, title: str, content: str):
    if authorId not in users_db:
        raise HTTPException(status_code=404, detail="Автор не найден")
    if not title.strip():
        raise HTTPException(status_code=400, detail="Заголовок не может быть пустым")
    if not content.strip():
        raise HTTPException(status_code=400, detail="Содержание не может быть пустым")
    
    # создаем
    new_post = Post(authorId, title.strip(), content.strip())
    posts_db[new_post.id] = new_post
    save()

    return {
        "id": new_post.id,
        "authorId": new_post.authorId,
        "title": new_post.title,
        "content": new_post.content,
        "createdAt": new_post.createdAt,
        "updatedAt": new_post.updatedAt
    }
