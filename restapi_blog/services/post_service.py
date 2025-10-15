from fastapi import HTTPException
from datetime import datetime
from models.post import Post, posts_db
from models.user import users_db
from schemas.post import PostCreate, PostUpdate
from utils.storage import save_data

class PostService:
    @staticmethod
    async def create_post(post_data: PostCreate):
        if post_data.author_id not in users_db:
            raise HTTPException(status_code=404, detail="Автор не найден")
        
        if not post_data.title.strip():
            raise HTTPException(status_code=400, detail="Заголовок не может быть пустым")
        
        if not post_data.content.strip():
            raise HTTPException(status_code=400, detail="Содержание не может быть пустым")
        
        new_post = Post(post_data.author_id, post_data.title.strip(), post_data.content.strip())
        posts_db[new_post.id] = new_post
        save_data()

        return {
            "id": new_post.id,
            "author_id": new_post.author_id,
            "title": new_post.title,
            "content": new_post.content,
            "created_at": new_post.created_at.isoformat(),
            "updated_at": new_post.updated_at.isoformat()
        }

    @staticmethod
    async def get_all_posts():
        posts_list = []
        for post in posts_db.values():
            posts_list.append({
                "id": post.id,
                "author_id": post.author_id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at.isoformat(),
                "updated_at": post.updated_at.isoformat()
            })
        return posts_list

    @staticmethod
    async def get_post(post_id: int):
        if post_id not in posts_db:
            raise HTTPException(status_code=404, detail="Пост не найден")
        
        post = posts_db[post_id]
        return {
            "id": post.id,
            "author_id": post.author_id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat()
        }

    @staticmethod
    async def update_post(post_id: int, post_data: PostUpdate):
        if post_id not in posts_db:
            raise HTTPException(status_code=404, detail="Пост не найден")
        
        post = posts_db[post_id]
        
        if post_data.title is not None:
            if not post_data.title.strip():
                raise HTTPException(status_code=400, detail="Заголовок не может быть пустым")
            post.title = post_data.title.strip()

        if post_data.content is not None:
            if not post_data.content.strip():
                raise HTTPException(status_code=400, detail="Содержание не может быть пустым")
            post.content = post_data.content.strip()
        
        post.updated_at = datetime.now()
        save_data()

        return {
            "id": post.id,
            "author_id": post.author_id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat()
        }

    @staticmethod
    async def delete_post(post_id: int):
        if post_id not in posts_db:
            raise HTTPException(status_code=404, detail="Пост не найден")
        
        del posts_db[post_id]
        save_data()
        
        return {"message": f"Пост с ID {post_id} удален"}