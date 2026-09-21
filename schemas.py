from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(
        ...,
        description="Уникальное имя пользователя",
        example="invalid"
    )
    email: EmailStr = Field(
        ...,
        description="Действительный адрес электронной почты",
        example="invalid@example.com"
    )
    password: str = Field(
        ...,
        min_length=6,
        description="Пароль пользователя (минимум 6 символов)",
        example="secret_password123"
    )

class UserResponse(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор пользователя", example=1)
    username: str = Field(..., description="Имя пользователя", example="invalid")
    email: str = Field(..., description="Email пользователя", example="invalid@example.com")
    is_active: bool = Field(..., description="Статус активности аккаунта", example=True)

    class Config:
        from_attributes = True

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