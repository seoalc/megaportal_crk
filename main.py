from fastapi import FastAPI
from routes.users import user_router
from routes.requests import request_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Depends, HTTPException
from auth.authenticate import authenticate

import uvicorn

app = FastAPI()

# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(request_router, prefix="/request")

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    return FileResponse("static/templates/index.html")
    # if user:
    #     # Если пользователь аутентифицирован, перенаправляем на requests.html
    #     return FileResponse("static/templates/requests.html")
    # else:
    #     # Если не аутентифицирован, возвращаем страницу входа
    #     return FileResponse("static/templates/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)