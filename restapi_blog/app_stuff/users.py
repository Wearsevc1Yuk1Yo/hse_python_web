from fastapi import HTTPException
from main_structures.main import users_db, User
from storage.files import save

async def create_us(email: str, login: str, password: str):
    # создает юзера

    if not email or not login or not password:
        raise HTTPException(status_code=400, detail="Все поля обязательны: email, login, password")
    
    for user in users_db.values():
        if user.email == email:
             raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    new_us = User(email, login, password)
    users_db[new_us.id] = new_us
    save()

    return {
        "id": user.id,
        "email": user.email,
        "login": user.login,
        "createdAt": user.createdAt,
        "updatedAt": user.updatedAt
    }


# делитим юзера (почему нет)
async def delete_user(user_id: int):
    """Удаляет пользователя"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    del users_db[user_id]
    save()
    
    return {"message": f"Пользователь с ID {user_id} удален"}