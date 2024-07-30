from fastapi import FastAPI, HTTPException, Depends, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import random
import string

app = FastAPI()

# 静的ファイルの提供
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# モックデータベース
fake_users_db = {
    "johndoe@example.com": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
        "preferences": {"theme": "dark", "notifications": True},
    },
    "janedoe@example.com": {
        "username": "janedoe",
        "full_name": "Jane Doe",
        "email": "janedoe@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": False,
        "preferences": {"theme": "light", "notifications": False},
    }
}

pending_users = {}

# OAuth2PasswordBearerを使ってトークンURLを指定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None
    preferences: dict = None


class UserInDB(User):
    hashed_password: str


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(db, email: str):
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    user_dict = fake_users_db.get(email)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if (hashed_password != user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return {"access_token": user.email, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/signup")
async def signup(email: str = Form(...), password: str = Form(...)):
    if email in fake_users_db or email in pending_users:
        raise HTTPException(status_code=400, detail="Email already registered")

    verification_code = ''.join(random.choices(string.digits, k=6))
    pending_users[email] = {
        "email": email,
        "hashed_password": fake_hash_password(password),
        "verification_code": verification_code
    }
    return {"message": "Please verify your email", "verification_code": verification_code}


@app.get("/verify/{email}/{code}")
async def verify(email: str, code: str):
    if email not in pending_users:
        raise HTTPException(status_code=400, detail="Invalid email or code")

    if pending_users[email]["verification_code"] != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    user_data = pending_users.pop(email)
    fake_users_db[email] = {
        "username": email.split('@')[0],
        "full_name": None,
        "email": email,
        "hashed_password": user_data["hashed_password"],
        "disabled": False,
        "preferences": {"theme": "default", "notifications": True},
    }
    return {"message": "User successfully verified and registered"}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
