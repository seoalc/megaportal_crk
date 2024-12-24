from fastapi import APIRouter, HTTPException, status, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, TokenResponse
from auth.hash_password import HashPassword
from db.db import get_database_connection

user_router = APIRouter(
    tags=["User"]
)

users = {}

@user_router.post("/signup")
async def sign_new_user(data: User, db=Depends(get_database_connection), hash_password=Depends(HashPassword)) -> dict:
    # Проверяем, существует ли пользователь
    with db.cursor() as cursor:
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (data.username,))
        result = cursor.fetchone()
        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with supplied username exists"
            )

    # Хэшируем пароль
    hashed_password = hash_password.create_hash(data.password)

    # Сохраняем пользователя в базе данных
    with db.cursor() as cursor:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (data.username, hashed_password))
        db.commit()

    return {
        "message": "User successfully registered!"
    }

@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database_connection), hash_password=Depends(HashPassword)) -> dict:
    try:
        # Ищем пользователя в базе данных
        with db.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (user.username,))
            result = cursor.fetchone()

        # Если пользователь не найден
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Проверяем пароль
        if not hash_password.verify_hash(user.password, result["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        access_token = create_access_token(result["username"])

        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )