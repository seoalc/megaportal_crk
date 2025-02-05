from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.responses import RedirectResponse
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.applications.dao import ApplicationDAO
# from app.users.schemas import SUserRegister, SUserAuth
# from app.users.dependencies import get_current_user, get_current_admin_user
from app.applications.models import Application
from app.utils.logging_config import logger


router = APIRouter(prefix='/application', tags=['Auth'])

# @router.get("/", summary="Получить все заявки")
# async def get_all_students(request_body: RBStudent = Depends()) -> list[SStudent]:
#     students = await StudentDAO.find_all(**request_body.to_dict())
#     return [SStudent.model_validate({
#         **student.__dict__,
#         'major': student.major.major_name  # Преобразуйте объект Major в строку
#     }) for student in students]

@router.get("/searchnumber/{subscriber_number}")
async def get_all_applications_by_number(subscriber_number: int):
    rez = await ApplicationDAO.get_applications_by_subscriber_number(subscriber_number)
    logger.info(f"Данные заявок: {rez}")
    # return RedirectResponse(url=f"/pages/searchnumber/{subscriber_number}")
    return rez