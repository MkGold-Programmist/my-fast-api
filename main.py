from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

import models, schemas, auth
from database import engine, get_db


origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

# Оформление заголовка и описания API в Swagger UI
app = FastAPI(
    title="User Authentication API",
    description="Полноценный сервис авторизации и регистрации пользователей с использованием JWT-токенов и SQLite.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS для подключения React/Vite фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    path="/get_users",
    response_model=List[schemas.UserResponse],
    summary="Получить список всех пользователей",
    description="Возвращает массив всех зарегистрированных пользователей из базы данных.",
    tags=["Пользователи"]
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
    description="Принимает username, email и password. Проверяет их на уникальность и создаёт новый аккаунт с захэшированным паролем.",
    response_description="Данные созданного пользователя без пароля",
    tags=["Аутентификация"]
)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        (models.User.username == user_data.username) | (models.User.email == user_data.email)
    ).first()

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким именем или Email уже существует"
        )

    hashed_pwd = auth.hash_password(user_data.password)
    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post(
    "/login",
    response_model=schemas.Token,
    summary="Авторизация пользователя (Получение JWT токена)",
    description="Принимает username и password в формате OAuth2 Form Data. Возвращает JWT токен доступа.",
    response_description="Access token и тип токена (bearer)",
    tags=["Аутентификация"]
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}