from datetime import datetime
from fastapi import FastAPI, HTTPException
# на потом
from fastapi.responses import HTMLResponse

import json
import os

app = FastAPI(title="Simple Blog")

users_db = {}
posts_db = {}

user_id_counter = 1
post_id_counter = 1

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

