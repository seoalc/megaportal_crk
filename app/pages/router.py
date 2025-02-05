from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import shutil
from enum import Enum

from app.users.router import get_me
from app.users.dependencies import get_current_user, get_current_admin_user, get_current_dispatcher_user
from app.users.models import User
from app.users.dependencies import has_valid_token
from app.applications.dao import ApplicationDAO
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

@router.get('/unassigned_applications/dispatcher')
async def see_unassigned_applications_dispatcher(
        request: Request,
        profile=Depends(get_current_dispatcher_user),
        applications=Depends(ApplicationDAO.get_unassigned_applications
    )):
    logger.info(f"Неназначенные заявки: {applications}")
    return templates.TemplateResponse(
        name='unassigned_applications_dispatcher.html',
        context={'request': request, 'profile': profile, 'applications': applications}
    )

@router.get('/unassigned_applications/admin')
async def see_unassigned_applications_admin(request: Request, profile=Depends(get_current_admin_user)):
    return templates.TemplateResponse(
        name='unassigned_applications_admin.html',
        context={'request': request, 'profile': profile}
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
    if profile.user_status == UserStatus.USER:
        return RedirectResponse(url="/pages/searchnumber/user")
    elif profile.user_status == UserStatus.DISPATCHER:
        return templates.TemplateResponse(
            name='searchnumber_dispatcher.html',
            context={'request': request, 'profile': profile, 'applications': applications, 'subscriber_number': subscriber_number}
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