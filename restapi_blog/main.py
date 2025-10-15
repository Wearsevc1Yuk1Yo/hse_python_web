from fastapi import FastAPI, Request, Form, Response, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import Optional

from core.exceptions import not_found_handler, bad_request_handler, internal_error_handler
from routers import users_router, posts_router
from utils.storage import load_data
from services.user_service import UserService
from services.post_service import PostService
from schemas.user import UserCreate
from schemas.post import PostCreate, PostUpdate
from models.user import users_db
from models.post import posts_db

app = FastAPI(title="Simple Blog API")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(users_router)
app.include_router(posts_router)

# Add exception handlers
app.add_exception_handler(404, not_found_handler)
app.add_exception_handler(400, bad_request_handler)
app.add_exception_handler(500, internal_error_handler)

# Load data on startup
load_data()

# Helper function to get current user
def get_current_user(request: Request) -> Optional[dict]:
    user_id = request.session.get('user_id')
    if user_id and user_id in users_db:
        user = users_db[user_id]
        return {
            "id": user.id,
            "email": user.email,
            "login": user.login
        }
    return None

# HTML Routes
@app.get("/")
async def home_page(request: Request):
    current_user = get_current_user(request)
    posts_list = []
    
    for post in posts_db.values():
        author_name = "Неизвестный автор"
        if post.author_id in users_db:
            author_name = users_db[post.author_id].login
        posts_list.append({
            "id": post.id,
            "title": post.title,
            "author_name": author_name,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
            "content_preview": post.content[:100] + "..." if len(post.content) > 100 else post.content
        })
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "posts": posts_list,
        "has_users": len(users_db) > 0,
        "current_user": current_user,
        "all_users": list(users_db.values())
    })

@app.get("/post/{post_id}")
async def view_post_page(request: Request, post_id: int):
    current_user = get_current_user(request)
    
    if post_id not in posts_db:
        return not_found_handler(request, None)
    
    post = posts_db[post_id]
    author_name = "Неизвестный автор"
    if post.author_id in users_db:
        author_name = users_db[post.author_id].login
    
    post_data = {
        "id": post.id,
        "title": post.title,
        "author_name": author_name,
        "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
        "updated_at": post.updated_at.strftime("%Y-%m-%d %H:%M"),
        "content": post.content
    }
    
    return templates.TemplateResponse("view_post.html", {
        "request": request, 
        "post": post_data,
        "current_user": current_user
    })

@app.get("/create-post")
async def create_post_page(request: Request):
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse("create_post.html", {
        "request": request,
        "current_user": current_user
    })

@app.post("/create-post")
async def handle_create_post(request: Request, title: str = Form(), content: str = Form()):
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    post_data = PostCreate(author_id=current_user["id"], title=title, content=content)
    await PostService.create_post(post_data)
    return RedirectResponse(url="/", status_code=303)

@app.get("/edit-post/{post_id}")
async def edit_post_page(request: Request, post_id: int):
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    if post_id not in posts_db:
        return not_found_handler(request, None)
    
    post = posts_db[post_id]
    
    # Проверяем, что пользователь является автором поста
    if post.author_id != current_user["id"]:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "title": "Ошибка доступа",
            "message": "Вы можете редактировать только свои посты"
        }, status_code=403)
    
    post_data = {
        "id": post.id,
        "title": post.title,
        "content": post.content
    }
    
    return templates.TemplateResponse("edit_post.html", {
        "request": request, 
        "post": post_data,
        "current_user": current_user
    })

@app.post("/edit-post/{post_id}")
async def handle_edit_post(request: Request, post_id: int, title: str = Form(), content: str = Form()):
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    # Проверяем, что пользователь является автором поста
    if post_id in posts_db and posts_db[post_id].author_id != current_user["id"]:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "title": "Ошибка доступа",
            "message": "Вы можете редактировать только свои посты"
        }, status_code=403)
    
    post_data = PostUpdate(title=title, content=content)
    await PostService.update_post(post_id, post_data)
    return RedirectResponse(url=f"/post/{post_id}", status_code=303)

@app.get("/register")
async def register_page(request: Request):
    current_user = get_current_user(request)
    return templates.TemplateResponse("register.html", {
        "request": request,
        "current_user": current_user
    })

@app.post("/register")
async def handle_register(request: Request, email: str = Form(), login: str = Form(), password: str = Form()):
    user_data = UserCreate(email=email, login=login, password=password)
    new_user = await UserService.create_user(user_data)
    
    # Автоматически входим после регистрации
    request.session['user_id'] = new_user["id"]
    return RedirectResponse(url="/", status_code=303)

@app.get("/login")
async def login_page(request: Request):
    current_user = get_current_user(request)
    
    if current_user:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "current_user": current_user
    })

@app.post("/login")
async def handle_login(request: Request, email: str = Form(), password: str = Form()):
    # Ищем пользователя по email и паролю
    user = None
    for u in users_db.values():
        if u.email == email and u.password == password:
            user = u
            break
    
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неверный email или пароль"
        })
    
    # Сохраняем пользователя в сессии
    request.session['user_id'] = user.id
    return RedirectResponse(url="/", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('user_id', None)
    return RedirectResponse(url="/", status_code=303)

@app.get("/switch-user/{user_id}")
async def switch_user(request: Request, user_id: int):
    if user_id in users_db:
        request.session['user_id'] = user_id
    return RedirectResponse(url="/", status_code=303)

@app.get("/delete-post/{post_id}")
async def delete_post_page(request: Request, post_id: int):
    current_user = get_current_user(request)
    
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    # Проверяем, что пользователь является автором поста
    if post_id in posts_db and posts_db[post_id].author_id != current_user["id"]:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "title": "Ошибка доступа",
            "message": "Вы можете удалять только свои посты"
        }, status_code=403)
    
    await PostService.delete_post(post_id)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    # Добавляем middleware для сессий
    from starlette.middleware.sessions import SessionMiddleware
    app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)