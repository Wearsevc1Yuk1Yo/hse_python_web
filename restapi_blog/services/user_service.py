from fastapi import HTTPException
from datetime import datetime
from models.user import User, users_db
from schemas.user import UserCreate, UserUpdate
from utils.storage import save_data

class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate):
        # Проверка уникальности email
        for user in users_db.values():
            if user.email == user_data.email:
                raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
        
        new_user = User(user_data.email, user_data.login, user_data.password)
        users_db[new_user.id] = new_user
        save_data()
        
        return {
            "id": new_user.id,
            "email": new_user.email,
            "login": new_user.login,
            "created_at": new_user.created_at.isoformat(),
            "updated_at": new_user.updated_at.isoformat()
        }

    @staticmethod
    async def get_all_users():
        return [
            {
                "id": user.id,
                "email": user.email,
                "login": user.login,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            }
            for user in users_db.values()
        ]

    @staticmethod
    async def get_user(user_id: int):
        if user_id not in users_db:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        user = users_db[user_id]
        return {
            "id": user.id,
            "email": user.email,
            "login": user.login,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate):
        if user_id not in users_db:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        user = users_db[user_id]
        
        if user_data.email is not None:
            # Проверка уникальности email
            for uid, existing_user in users_db.items():
                if existing_user.email == user_data.email and uid != user_id:
                    raise HTTPException(status_code=400, detail="Email уже используется")
            user.email = user_data.email
        
        if user_data.login is not None:
            user.login = user_data.login
        
        if user_data.password is not None:
            user.password = user_data.password
        
        user.updated_at = datetime.now()
        save_data()
        
        return {
            "id": user.id,
            "email": user.email,
            "login": user.login,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }

    @staticmethod
    async def delete_user(user_id: int):
        if user_id not in users_db:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        del users_db[user_id]
        save_data()
        
        return {"message": f"Пользователь с ID {user_id} удален"}