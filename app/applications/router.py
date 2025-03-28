from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.responses import RedirectResponse
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.applications.dao import ApplicationDAO
from app.applications.schemas import SApplicationAdd, SRemidialUserUpdate, SComplaintTextUpdate, SAppearanceDateUpdate
from app.applications.schemas import SDeleteApplication, SClosedText
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

@router.post("/add/")
async def add_application(application: SApplicationAdd) -> dict:
    logger.info(f"Данные заявок: {application}")
    check = await ApplicationDAO.add_application(**application.dict())
    if check:
        # return RedirectResponse(url=f"/pages/searchnumber/{application.subscriber_number}")
        return {"message": "Новая заявка успешно добавлена!", "application": application, "ok": True}
    else:
        return {"message": "Ошибка при добавлении заявки!"}

@router.post("/remedialuserupdate/")
async def update_remidial_user_to_application(application: SRemidialUserUpdate) -> dict:
    logger.info(f"ID заявки и исполнителя для обновления: {application}")

    updated_count = await ApplicationDAO.add_remedial_users(
        application_id=application.application_id,
        user_ids=application.remedial_user_ids
    )

    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    
    updated_rows = await ApplicationDAO.update_application_status(
        application_id=application.application_id,
        application_status=1
    )

    return {'ok': True, "application_id": application.application_id}

@router.post("/complainttextupdate/")
async def update_complaint_text_to_application(application: SComplaintTextUpdate) -> dict:
    logger.info(f"Информация для обновления текста жалобы: {application}")

    updated_rows = await ApplicationDAO.update_complaint_text(
        application_id=application.application_id, 
        complaint_text=application.complaint_text
    )

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    return {'ok': True, "application_id": application.application_id}

@router.post("/changeappearancedate/")
async def change_appearance_date_application(application: SAppearanceDateUpdate) -> dict:
    logger.info(f"Информация для зменения даты явки: {application}")

    updated_rows = await ApplicationDAO.update_appearance_date(
        application_id=application.application_id, 
        appearance_date=application.appearance_date
    )

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    return {'ok': True, "application_id": application.application_id}

@router.post("/deleteapplication/")
async def delete_application(application: SDeleteApplication) -> dict:
    logger.info(f"Информация по удаляемой заявке: {application}")

    deleted_rows = await ApplicationDAO.delete_application(application.application_id)

    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    return {'ok': True, "application_id": application.application_id}

@router.post("/closeapplication/")
async def close_application(application: SClosedText) -> dict:
    logger.info(f"Информация по закрытию заявки: {application}")

    updated_rows = await ApplicationDAO.close_application(
        application_id=application.application_id, 
        closed_text=application.closed_text,
        application_status=2
    )

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    return {'ok': True, "application_id": application.application_id}