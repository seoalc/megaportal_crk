from fastapi import APIRouter, Request, Depends, UploadFile, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import shutil
from enum import Enum

from app.users.router import get_me, get_all_users, get_all_users_for_admin
from app.users.dependencies import get_current_user, get_current_admin_user, get_current_dispatcher_user
from app.users.models import User
from app.users.dependencies import has_valid_token
from app.applications.dao import ApplicationDAO
from app.materials_types.dao import MaterialtypeDAO
from app.materials_titles.dao import MaterialtitleDAO
from app.material_users.dao import MaterialuserDAO
from app.utils.logging_config import logger


router = APIRouter(prefix='/pages', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')

class UserStatus(int, Enum):
    USER = 0
    DISPATCHER = 1
    ADMIN = 2

@router.get('/register')
async def get_register_form(request: Request):
    return templates.TemplateResponse(name='register_form.html', context={'request': request})

@router.get('/login')
async def get_login_form(request: Request):
    if has_valid_token(request):
        return RedirectResponse(url="/pages/unassigned_applications")
    return templates.TemplateResponse(name='login_form.html', context={'request': request})

@router.get('/profile')
async def get_my_profile(request: Request, profile=Depends(get_me)):
    return templates.TemplateResponse(name='profile.html', context={'request': request, 'profile': profile})

@router.get('/unassigned_applications')
async def see_unassigned_applications(request: Request, profile=Depends(get_me)):
    logger.info(f"Данные пользователя: {profile.user_status}")
    if profile.user_status == UserStatus.USER:
        return RedirectResponse(url="/pages/unassigned_applications/user")
    elif profile.user_status == UserStatus.DISPATCHER:
        return RedirectResponse(url="/pages/unassigned_applications/dispatcher")
    elif profile.user_status == UserStatus.ADMIN:
        return RedirectResponse(url="/pages/unassigned_applications/admin")
    else:
        raise HTTPException(status_code=400, detail="Неизвестная роль пользователя")
    return templates.TemplateResponse(name='unassigned_applications.html', context={'request': request, 'profile': profile})

@router.get('/unassigned_applications/user')
async def see_unassigned_applications_user(request: Request,
        profile=Depends(get_current_user),
        applications=Depends(ApplicationDAO.get_unassigned_applications)
    ):
    if profile.user_status != UserStatus.USER:
        if profile.user_status == UserStatus.DISPATCHER:
            return RedirectResponse(url="/pages/unassigned_applications/dispatcher")
        elif profile.user_status == UserStatus.ADMIN:
            return RedirectResponse(url="/pages/unassigned_applications/admin")
    parts = profile.fio.split()  # Разбиваем строку по пробелам
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        filtered_fio = f"{last_name} {first_name[0]}. {patronymic[0]}."
    return templates.TemplateResponse(
        name='unassigned_applications.html',
        context={'request': request, 'profile': profile, 'applications': applications, 'filtered_fio': filtered_fio}
    )

@router.get('/unassigned_applications/dispatcher')
async def see_unassigned_applications_dispatcher(
        request: Request,
        profile=Depends(get_current_dispatcher_user),
        applications=Depends(ApplicationDAO.get_unassigned_applications),
        users=Depends(get_all_users)
    ):
    logger.info(f"Неназначенные заявки: {applications}")
    parts = profile.fio.split()  # Разбиваем строку по пробелам
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        filtered_fio = f"{last_name} {first_name[0]}. {patronymic[0]}."
    return templates.TemplateResponse(
        name='unassigned_applications_dispatcher.html',
        context={'request': request, 'profile': profile, 'applications': applications, 'filtered_fio': filtered_fio, 'users': users}
    )

@router.get('/unassigned_applications/admin')
async def see_unassigned_applications_admin(
    request: Request,
        profile=Depends(get_current_admin_user),
        applications=Depends(ApplicationDAO.get_unassigned_applications),
        users=Depends(get_all_users_for_admin)
    ):
    logger.info(f"Неназначенные заявки: {applications}")
    parts = profile.fio.split()  # Разбиваем строку по пробелам
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        filtered_fio = f"{last_name} {first_name[0]}. {patronymic[0]}."
    return templates.TemplateResponse(
        name='unassigned_applications_admin.html',
        context={'request': request, 'profile': profile, 'applications': applications, 'filtered_fio': filtered_fio, 'users': users}
    )

@router.get('/searchnumber/{subscriber_number}')
async def search_applications_by_subscriber_number(
        request: Request,
        subscriber_number: int,
        profile=Depends(get_me),
        applications=Depends(ApplicationDAO.get_applications_by_subscriber_number
    )):
    logger.info(f"Данные пользователя: {profile.user_status}")
    logger.info(f"Результат поиска: {applications}")
    parts = profile.fio.split()  # Разбиваем строку по пробелам
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        filtered_fio = f"{last_name} {first_name[0]}. {patronymic[0]}."
    if profile.user_status == UserStatus.USER:
        return RedirectResponse(url="/pages/searchnumber/user")
    elif profile.user_status == UserStatus.DISPATCHER:
        return templates.TemplateResponse(
            name='searchnumber_dispatcher.html',
            context={'request': request, 'profile': profile, 'applications': applications, 'subscriber_number': subscriber_number, 'filtered_fio': filtered_fio}
        )
    elif profile.user_status == UserStatus.ADMIN:
        return RedirectResponse(url="/pages/searchnumber/admin")
    else:
        raise HTTPException(status_code=400, detail="Неизвестная роль пользователя")
    return templates.TemplateResponse(name='searchnumber.html', context={'request': request, 'profile': profile})

@router.get('/searchnumber/user')
async def see_unassigned_applications_user(request: Request, profile=Depends(get_current_user)):
    if profile.user_status != UserStatus.USER:
        if profile.user_status == UserStatus.DISPATCHER:
            return RedirectResponse(url="/pages/unassigned_applications/dispatcher")
        elif profile.user_status == UserStatus.ADMIN:
            return RedirectResponse(url="/pages/unassigned_applications/admin")
    return templates.TemplateResponse(
        name='unassigned_applications.html',
        context={'request': request, 'profile': profile}
    )

@router.get('/searchnumber/dispatcher/{subscriber_number}')
async def see_unassigned_applications_dispatcher(
        request: Request,
        profile=Depends(get_current_dispatcher_user),
        applications=Depends(ApplicationDAO.get_applications_by_subscriber_number
    )):
    logger.info(f"Результат поиска по номеру: {applications}")
    return templates.TemplateResponse(
        name='searchnumber_dispatcher.html',
        context={'request': request, 'profile': profile, 'applications': applications}
    )

@router.get('/searchnumber/admin')
async def see_unassigned_applications_admin(request: Request, profile=Depends(get_current_admin_user)):
    return templates.TemplateResponse(
        name='unassigned_applications_admin.html',
        context={'request': request, 'profile': profile}
    )

@router.get('/assigned_applications')
async def see_assigned_applications(request: Request, profile=Depends(get_me)):
    logger.info(f"Данные пользователя: {profile.user_status}")
    if profile.user_status == UserStatus.USER:
        return RedirectResponse(url="/pages/assigned_applications/user")
    elif profile.user_status == UserStatus.DISPATCHER:
        return RedirectResponse(url="/pages/assigned_applications/dispatcher")
    elif profile.user_status == UserStatus.ADMIN:
        return RedirectResponse(url="/pages/assigned_applications/admin")
    else:
        raise HTTPException(status_code=400, detail="Неизвестная роль пользователя")
    return templates.TemplateResponse(name='assigned_applications.html', context={'request': request, 'profile': profile, 'users': users})

@router.get('/assigned_applications/user')
async def see_assigned_applications_user(request: Request, profile=Depends(get_current_user)):
    if profile.user_status != UserStatus.USER:
        if profile.user_status == UserStatus.DISPATCHER:
            return RedirectResponse(url="/pages/unassigned_applications/dispatcher")
        elif profile.user_status == UserStatus.ADMIN:
            return RedirectResponse(url="/pages/unassigned_applications/admin")
    assigned_applications = await ApplicationDAO.get_assigned_applications_for_user(profile.id)
    return templates.TemplateResponse(
        name='assigned_applications.html',
        context={'request': request, 'profile': profile, 'applications': assigned_applications}
    )

@router.get('/assigned_applications/dispatcher')
async def see_assigned_applications_dispatcher(
        request: Request,
        profile=Depends(get_current_dispatcher_user),
        applications=Depends(ApplicationDAO.get_assigned_applications),
        users=Depends(get_all_users)
    ):
    logger.info(f"Заявки в работе: {applications}")
    # Формируем данные
    result = [
        {
            "id": app.id,
            "appearance_date": app.appearance_date,
            "subscriber_number": app.subscriber_number,
            "subscriber_address": app.subscriber_addres,
            "complaint_text": app.complaint_text,
            "contact_number": app.contact_number,
            "solution_description": app.solution_description,
            "user_id_created_application": app.user_id_created_application,
            "application_status": app.application_status,
            "remedial_users": [
                {"id": user.id, "fio": user.fio, "user_name": user.user_name}
                for user in app.remedial_users
            ],
        }
        for app in applications
    ]

    # Логируем полученные заявки
    logger.info(f"Назначенные заявки: {result}")
    parts = profile.fio.split()  # Разбиваем строку по пробелам
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        filtered_fio = f"{last_name} {first_name[0]}. {patronymic[0]}."
    return templates.TemplateResponse(
        name='assigned_applications_dispatcher.html',
        context={'request': request, 'profile': profile, 'applications': applications, 'filtered_fio': filtered_fio, 'users': users}
    )

@router.get('/assigned_applications/admin')
async def see_assigned_applications_admin(
    request: Request,
        profile=Depends(get_current_admin_user),
        applications=Depends(ApplicationDAO.get_assigned_applications),
        users=Depends(get_all_users_for_admin)
    ):
    logger.info(f"Заявки в работе: {applications}")
    # Формируем данные
    result = [
        {
            "id": app.id,
            "appearance_date": app.appearance_date,
            "subscriber_number": app.subscriber_number,
            "subscriber_address": app.subscriber_addres,
            "complaint_text": app.complaint_text,
            "contact_number": app.contact_number,
            "solution_description": app.solution_description,
            "user_id_created_application": app.user_id_created_application,
            "application_status": app.application_status,
            "remedial_users": [
                {"id": user.id, "fio": user.fio, "user_name": user.user_name}
                for user in app.remedial_users
            ],
        }
        for app in applications
    ]

    # Логируем полученные заявки
    logger.info(f"Назначенные заявки: {result}")
    parts = profile.fio.split()  # Разбиваем строку по пробелам
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        filtered_fio = f"{last_name} {first_name[0]}. {patronymic[0]}."
    return templates.TemplateResponse(
        name='assigned_applications_dispatcher.html',
        context={'request': request, 'profile': profile, 'applications': applications, 'filtered_fio': filtered_fio, 'users': users}
    )

@router.get('/closed_applications')
async def see_closed_applications(request: Request, profile=Depends(get_me)):
    logger.info(f"Данные пользователя: {profile.user_status}")
    if profile.user_status == UserStatus.USER:
        return RedirectResponse(url="/pages/closed_applications/user")
    elif profile.user_status == UserStatus.DISPATCHER:
        return RedirectResponse(url="/pages/closed_applications/dispatcher")
    elif profile.user_status == UserStatus.ADMIN:
        return RedirectResponse(url="/pages/closed_applications/admin")
    else:
        raise HTTPException(status_code=400, detail="Неизвестная роль пользователя")
    return templates.TemplateResponse(name='closed_applications.html', context={'request': request, 'profile': profile, 'users': users})

@router.get('/closed_applications/user')
async def see_closed_applications_user(request: Request, profile=Depends(get_current_user)):
    if profile.user_status != UserStatus.USER:
        if profile.user_status == UserStatus.DISPATCHER:
            return RedirectResponse(url="/pages/closed_applications/dispatcher")
        elif profile.user_status == UserStatus.ADMIN:
            return RedirectResponse(url="/pages/closed_applications/admin")
    closed_applications = await ApplicationDAO.get_closed_applications_for_user(profile.id)
    return templates.TemplateResponse(
        name='closed_applications.html',
        context={'request': request, 'profile': profile, 'applications': closed_applications}
    )

@router.get('/store_get')
async def get_to_store(request: Request, profile=Depends(get_me)):
    logger.info(f"Данные пользователя: {profile.user_status}")
    if profile.user_status == UserStatus.USER:
        return RedirectResponse(url="/pages/assigned_applications/user")
    elif profile.user_status == UserStatus.DISPATCHER:
        return RedirectResponse(url="/pages/assigned_applications/dispatcher")
    elif profile.user_status == UserStatus.ADMIN:
        return RedirectResponse(url="/pages/store_get/admin")
    else:
        raise HTTPException(status_code=400, detail="Неизвестная роль пользователя")
    return templates.TemplateResponse(name='assigned_applications.html', context={'request': request, 'profile': profile, 'users': users})

@router.get('/store_get/admin')
async def get_to_store_admin(
    request: Request,
        profile=Depends(get_current_admin_user),
        users=Depends(get_all_users_for_admin)
    ):

    # Получаем все типы материалов из базы
    material_types = await MaterialtypeDAO.find_all()
    
    parts = profile.fio.split()  # Разбиваем строку по пробелам
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        filtered_fio = f"{last_name} {first_name[0]}. {patronymic[0]}."
    return templates.TemplateResponse(
        name='store_get_admin.html',
        context={
            'request': request,
            'profile': profile,
            'filtered_fio': filtered_fio,
            'users': users,
            'material_types': material_types  # Передаём типы материалов в шаблон
        }
    )

@router.get('/store_get/user')
async def get_to_store_user(
    request: Request,
        profile=Depends(get_current_user)
    ):

    # Получаем все типы материалов из базы
    materials_qantities = await MaterialuserDAO.get_materials_user_qantity_by_user_id(profile.id)
    # Создаем список для хранения данных о материалах
    materials_data = []
    for m_q in materials_qantities:
        logger.info(f"Данные о количестве: {m_q.quantity}")
        material_title_info = await MaterialtitleDAO.get_material_title_by_id(m_q.material_title_id)
        material_type_info = await MaterialtypeDAO.get_material_type_by_id(material_title_info.material_type_id)

        # Добавляем данные о каждом материале в список
        materials_data.append({
            'quantity': m_q.quantity,
            'title': material_title_info.material_title,  # Предполагается, что есть поле title
            'type': material_type_info.material_type  # Предполагается, что есть поле type_name
        })
    logger.info(f"Данные о количестве: {materials_qantities}")
    
    parts = profile.fio.split()  # Разбиваем строку по пробелам
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        filtered_fio = f"{last_name} {first_name[0]}. {patronymic[0]}."
    return templates.TemplateResponse(
        name='store_get_user.html',
        context={
            'request': request,
            'profile': profile,
            'filtered_fio': filtered_fio,
            'materials_data': materials_data
        }
    )

@router.post('/store_write_of')
async def get_to_store(request: Request, data: dict = Body(...), profile=Depends(get_me)):
    application_id = data.get("application_id_write_of")
    logger.info(f"Получен POST-запрос с application_id: {application_id}")
    parts = profile.fio.split()  # Разбиваем строку по пробелам
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        filtered_fio = f"{last_name} {first_name[0]}. {patronymic[0]}."

    if profile.user_status == UserStatus.USER:
        return templates.TemplateResponse(
            name='store_write_of_user.html',
            context={
                'request': request,
                'profile': profile,
                'filtered_fio': filtered_fio
            }
        )
    elif profile.user_status == UserStatus.DISPATCHER:
        return RedirectResponse(url="/pages/store_write_of/dispatcher")
    elif profile.user_status == UserStatus.ADMIN:
        return RedirectResponse(url="/pages/store_write_of/admin")
    else:
        raise HTTPException(status_code=400, detail="Неизвестная роль пользователя")
    #return templates.TemplateResponse(name='assigned_applications.html', context={'request': request, 'profile': profile, 'users': users})

@router.post('/store_write_of/user')
async def get_to_store_user(
    request: Request,
        profile=Depends(get_current_user)
    ):

    parts = profile.fio.split()  # Разбиваем строку по пробелам
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        filtered_fio = f"{last_name} {first_name[0]}. {patronymic[0]}."

    return templates.TemplateResponse(
        name='store_write_of_user.html',
        context={
            'request': request,
            'profile': profile,
            'filtered_fio': filtered_fio
        }
    )