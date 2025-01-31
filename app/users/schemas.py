from pydantic import BaseModel, EmailStr, Field, validator
import re


class SUserRegister(BaseModel):
    user_name: str = Field(..., min_length=5, max_length=50, description="Имя пользователя")
    fio: str = Field(..., description="Фамилия имя пользователя")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    user_status: int = Field(0, description="Статус прав пользователя")

class SUserAuth(BaseModel):
    user_name: str = Field(..., min_length=5, max_length=50, description="Имя пользователя")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")