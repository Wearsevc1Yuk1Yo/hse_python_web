from datetime import datetime
from typing import Dict


users_db: Dict[int, 'User'] = {}
posts_db: Dict[int, 'Post'] = {}

next_user_id = 1
next_post_id = 1

# юзер
class User:
    def __init__(self, email: str, login: str, password: str):
        global next_user_id
        
        self.id = next_user_id
        self.email = email
        self.login = login
        self.password = password
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()

        next_user_id += 1

# пост
class Post:
    def __init__(self, authorId: int, title: str, content: str):
        global next_post_id
        
        self.id = next_post_id
        self.authorId = authorId
        self.title = title
        self.content = content
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()

        next_post_id += 1

