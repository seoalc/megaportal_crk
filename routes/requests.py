from fastapi import APIRouter, Body, HTTPException, status, Depends, Request
from db.db import get_database_connection
from models.requests import Request
from typing import List
from auth.authenticate import authenticate

request_router = APIRouter(
    tags=["Requests"]
)

events = []

@request_router.get("/", response_model=List[Request])
async def retrieve_all_requests(db=Depends(get_database_connection), user: str = Depends(authenticate)) -> List[Request]:
    try:
        # Выборка всех заявок
        with db.cursor() as cursor:
            sql = "SELECT * FROM requests"
            cursor.execute(sql)
            result = cursor.fetchall()

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )