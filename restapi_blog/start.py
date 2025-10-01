from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

from storage.files import load
from app_stuff import users, posts, pages
from main_structures.main import users_db, posts_db

app = FastAPI(title="Simple Blog API")

load()

print("✅ Модули загружены")
print("✅ Данные загружены из файла")

# errorssssssssss ------------------------------------------------
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    """Обработчик для 404 ошибок"""
    error_html = pages.error_page(
        "404 - Страница не найдена", 
        "Запрошенная страница не существует. Проверьте URL или вернитесь на главную."
    )
    return HTMLResponse(content=error_html, status_code=404)

@app.exception_handler(400)
async def bad_request_exception_handler(request: Request, exc: HTTPException):
    """Обработчик для 400 ошибок"""
    error_html = pages.error_page(
        "400 - Ошибка валидации", 
        exc.detail or "Неверные данные. Пожалуйста, проверьте введенную информацию."
    )
    return HTMLResponse(content=error_html, status_code=400)

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    """Обработчик для 500 ошибок"""
    error_html = pages.error_page(
        "500 - Внутренняя ошибка сервера", 
        "Что-то пошло не так. Пожалуйста, попробуйте позже."
    )
    return HTMLResponse(content=error_html, status_code=500)


# USERS -----------------------------------------------------------
@app.post("/api/users/")
async def api_create_user(email: str, login: str, password: str):
    return await users.create_user(email, login, password)

@app.get("/api/users/")
async def api_get_users():
    return await users.get_all_users()

@app.get("/api/users/{user_id}")
async def api_get_user(user_id: int):
    return await users.get_user(user_id)

@app.put("/api/users/{user_id}")
async def api_update_user(user_id: int, email: str = None, login: str = None, password: str = None):
    return await users.update_user(user_id, email, login, password)

@app.delete("/api/users/{user_id}")
async def api_delete_user(user_id: int):
    return await users.delete_user(user_id)

# POSTS -----------------------------------------------------------

@app.post("/api/posts/")
async def api_create_post(authorId: int, title: str, content: str):
    return await posts.create_post(authorId, title, content)

@app.get("/api/posts/")
async def api_get_posts():
    return await posts.get_all_posts()

@app.get("/api/posts/{post_id}")
async def api_get_post(post_id: int):
    return await posts.get_post(post_id)

@app.put("/api/posts/{post_id}")
async def api_update_post(post_id: int, title: str = None, content: str = None):
    return await posts.update_post(post_id, title, content)

@app.delete("/api/posts/{post_id}")
async def api_delete_post(post_id: int):
    return await posts.delete_post(post_id)

# PAGES -----------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home_page():
    html_content = pages.mainpage()
    return HTMLResponse(content=html_content)

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def view_post_page(post_id: int):
    html_content = pages.viewed_post(post_id)
    return HTMLResponse(content=html_content)

@app.get("/create-post", response_class=HTMLResponse)
async def create_post_page():
    html_content = pages.create_post()
    return HTMLResponse(content=html_content)

@app.get("/edit-post/{post_id}", response_class=HTMLResponse)
async def edit_post_page(post_id: int):
    html_content = pages.edit_post(post_id)
    return HTMLResponse(content=html_content)

@app.get("/create-user", response_class=HTMLResponse)
async def create_user_page():
    html_content = pages.create_user()
    return HTMLResponse(content=html_content)

# formsss  -----------------------------------------------------------

@app.post("/create-post")
async def handle_create_post(authorId: int = Form(...), title: str = Form(...), content: str = Form(...)):
    await posts.create_post(authorId, title, content)
    return RedirectResponse(url="/", status_code=303)

@app.post("/edit-post/{post_id}")
async def handle_edit_post(post_id: int, title: str = Form(...), content: str = Form(...)):
    await posts.update_post(post_id, title, content)
    return RedirectResponse(url=f"/post/{post_id}", status_code=303)

@app.post("/create-user")
async def handle_create_user(email: str = Form(...), login: str = Form(...), password: str = Form(...)):
    await users.create_user(email, login, password)
    return RedirectResponse(url="/", status_code=303)

@app.get("/delete-post/{post_id}")
async def delete_post_page(post_id: int):
    await posts.delete_post(post_id)
    return RedirectResponse(url="/", status_code=303)



if __name__ == "__main__":
    print("Сервер запускается...")
    print("Главная страница: http://localhost:8000/")
    print("API документация: http://localhost:8000/docs")
    print("Данные сохраняются в blog_data.json")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
