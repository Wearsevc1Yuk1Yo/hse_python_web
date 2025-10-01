from fastapi import HTTPException
from datetime import datetime
from main_structures.main import users_db, User
from storage.files import save

async def create_user(email: str, login: str, password: str):
    if not email or not login or not password:
        raise HTTPException(status_code=400, detail="Все поля обязательны: email, login, password")
    
    for user in users_db.values():
        if user.email == email:
             raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    new_user = User(email, login, password)
    users_db[new_user.id] = new_user
    save()

    return {
        "id": new_user.id,
        "email": new_user.email,
        "login": new_user.login,
        "createdAt": new_user.createdAt,
        "updatedAt": new_user.updatedAt
    }

async def get_all_users():
    users_list = []
    for user in users_db.values():
        users_list.append({
            "id": user.id,
            "email": user.email,
            "login": user.login,
            "createdAt": user.createdAt,
            "updatedAt": user.updatedAt
        })
    return users_list

async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user = users_db[user_id]
    return {
        "id": user.id,
        "email": user.email,
        "login": user.login,
        "createdAt": user.createdAt,
        "updatedAt": user.updatedAt
    }

async def update_user(user_id: int, email: str = None, login: str = None, password: str = None):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user = users_db[user_id]
    
    if email is not None:
        # Проверка уникальности email
        for uid, existing_user in users_db.items():
            if existing_user.email == email and uid != user_id:
                raise HTTPException(status_code=400, detail="Email уже используется")
        user.email = email
    
    if login is not None:
        user.login = login
    
    if password is not None:
        user.password = password
    
    user.updatedAt = datetime.now()
    save()
    
    return {
        "id": user.id,
        "email": user.email,
        "login": user.login,
        "createdAt": user.createdAt,
        "updatedAt": user.updatedAt
    }

async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    del users_db[user_id]
    save()
    
    return {"message": f"Пользователь с ID {user_id} удален"}