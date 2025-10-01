from main_structures.main import users_db, posts_db
from datetime import datetime

def make_html_page(title: str, content: str):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            .post {{ border: 1px solid #ccc; padding: 15px; margin: 10px 0; }}
            .nav {{ margin: 20px 0; }}
            form {{ max-width: 600px; }}
            input, textarea, select {{ width: 100%; padding: 8px; margin: 5px 0; }}
            button {{ background: #4CAF50; color: white; padding: 10px; border: none; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {content}
    </body>
    </html>
    """

def author_name(author_id: int):
    if author_id in users_db:
        return users_db[author_id].login
    return "Неизвестный автор"

def mainpage():
    # глав страница
    if not posts_db:
        posts_html = "<p>Пока нет постов. <a href='/create-post'>Создайте первый!</a></p>"
    else:
        posts_html = ""
        postss = list(posts_db.values())
        postss.sort(key=lambda x: x.id, reverse=True)

        for post in postss:
            author_name = author_name(post.authorId)
            posts_html += f"""
            <div class="post">
                <h3><a href="/post/{post.id}">{post.title}</a></h3>
                <p><strong>Автор:</strong> {author_name}</p>
                <p><strong>Дата:</strong> {post.createdAt}</p>
                <p>{post.content[:100]}...</p>
                <a href="/post/{post.id}">Читать полностью</a> | 
                <a href="/edit-post/{post.id}">Редактировать</a>
            </div>
            """


def viewed_post(post_id: int):
    if post_id not in posts_db:
        return "пост не найден"
    post = posts_db[post_id]
    author_name = author_name(post.authorId)
    content = f"""
    <div class="post">
        <h2>{post.title}</h2>
        <p><strong>Автор:</strong> {author_name}</p>
        <p><strong>Создан:</strong> {post.createdAt}</p>
        <p><strong>Обновлен:</strong> {post.updatedAt}</p>
        <div style="white-space: pre-line; margin: 20px 0;">{post.content}</div>
    </div>
    <div class="nav">
        <a href="/">← На главную</a> | 
        <a href="/edit-post/{post_id}">✏️ Редактировать</a> |
        <a href="/delete-post/{post_id}" onclick="return confirm('Удалить этот пост?')">🗑️ Удалить</a>
    </div>
    """
    return make_html_page(post.title, content)

def create_post():

    if not users_db:
        user_options = "<option value=''>Сначала создайте пользователя</option>"
    else:
        user_options = ""
        for user_id, user in users_db.items():
            user_options += f"<option value='{user_id}'>{user.login} ({user.email})</option>"
    
    form_html = f"""
    <form method="post" action="/create-post">
        <div>
            <label>Автор:</label>
            <select name="authorId" required>
                <option value="">Выберите автора</option>
                {user_options}
            </select>
        </div>
        <div>
            <label>Заголовок:</label>
            <input type="text" name="title" required>
        </div>
        <div>
            <label>Содержание:</label>
            <textarea name="content" rows="10" required></textarea>
        </div>
        <button type="submit">Создать пост</button>
    </form>
    <div class="nav">
        <a href="/">← На главную</a>
    </div>
    """
    
    return make_html_page("Создание поста", form_html)


def edit_post(post_id: int):
    if post_id not in posts_db:
        return "Пост не найден"
    
    post = posts_db[post_id]

    form_html = f"""
    <form method="post" action="/edit-post/{post_id}">
        <div>
            <label>Заголовок:</label>
            <input type="text" name="title" value="{post.title}" required>
        </div>
        <div>
            <label>Содержание:</label>
            <textarea name="content" rows="10" required>{post.content}</textarea>
        </div>
        <button type="submit">Сохранить изменения</button>
    </form>
    <div class="nav">
        <a href="/post/{post_id}">← Назад к посту</a> | 
        <a href="/">На главную</a>
    </div>
    """
    
    return make_html_page("Редактирование поста", form_html)

def create_user():

    form_html = """
    <form method="post" action="/create-user">
        <div>
            <label>Email:</label>
            <input type="email" name="email" required>
        </div>
        <div>
            <label>Логин:</label>
            <input type="text" name="login" required>
        </div>
        <div>
            <label>Пароль:</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Создать пользователя</button>
    </form>
    <div class="nav">
        <a href="/">← На главную</a>
    </div>
    """
    return make_html_page("Создание пользователя", form_html)
