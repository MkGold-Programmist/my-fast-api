from pydantic import BaseModel, EmailStr, Field

# Схема для регистрации пользователя
class UserCreate(BaseModel):
    username: str = Field(
        ...,
        description="Уникальное имя пользователя",
        example="Narzullo"
    )
    email: EmailStr = Field(
        ...,
        description="Действительный адрес электронной почты",
        example="user@example.com"
    )
    password: str = Field(
        ...,
        min_length=6,
        description="Пароль пользователя (минимум 6 символов)",
        example="secret_password123"
    )

# Схема ответа с данными пользователя
class UserResponse(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор пользователя", example=1)
    username: str = Field(..., description="Имя пользователя", example="Narzullo")
    email: str = Field(..., description="Email пользователя", example="user@example.com")
    is_active: bool = Field(..., description="Статус активности аккаунта", example=True)

    class Config:
        from_attributes = True

# Схема ответа при успешной авторизации
class Token(BaseModel):
    access_token: str = Field(
        ...,
        description="JWT токен доступа для авторизованных запросов",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    token_type: str = Field(
        ...,
        description="Тип используемого токена",
        example="bearer"
    )