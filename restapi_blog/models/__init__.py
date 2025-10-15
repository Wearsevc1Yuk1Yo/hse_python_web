from .user import User, users_db, next_user_id
from .post import Post, posts_db, next_post_id

__all__ = [
    'User', 'users_db', 'next_user_id',
    'Post', 'posts_db', 'next_post_id'
]