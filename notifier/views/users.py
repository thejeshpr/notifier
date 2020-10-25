# import databases


import os
from fastapi import Request
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import CookieAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase


from fastapi.responses import HTMLResponse
from notifier.db import db_cursor as database
from notifier.db import Base, engine
from notifier.db.models import UserTable
from notifier import app, templates


SECRET = os.environ.get("SECRET")
DEBUG_FLAG = os.environ.get("DEBUG", False)

class User(models.BaseUser):
    pass

class UserCreate(models.BaseUserCreate):
    pass

class UserUpdate(User, models.BaseUserUpdate):
    pass

class UserDB(User, models.BaseUserDB):
    pass


users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)


def on_after_register(user: UserDB, request: Request):
    # print(f"User {user.id} has registered.")
    pass


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    # print(f"User {user.id} has forgot their password. Reset token: {token}")
    pass


if DEBUG_FLAG:
    cookie_secure=False
else:
    cookie_secure=True

cookie_authentication = CookieAuthentication(
    secret=SECRET,
    lifetime_seconds=3600,
    cookie_secure=cookie_secure,    
    cookie_httponly=False
)



fastapi_users = FastAPIUsers(
    user_db,
    [cookie_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

# include login / logout router
app.include_router(
    fastapi_users.get_auth_router(cookie_authentication), prefix="/authorize", tags=["auth"]
)


if DEBUG_FLAG:
    # include reg router 
    app.include_router(
        fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
    )

    # password reset router
    app.include_router(
        fastapi_users.get_reset_password_router(
            SECRET, after_forgot_password=on_after_forgot_password
        ),
        prefix="/auth",
        tags=["auth"],
    )

    # user router
    app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])



@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):         
    return templates.TemplateResponse("login.html", {"request": request})