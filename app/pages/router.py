from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import shutil

from app.users.router import get_me
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.dependencies import has_valid_token


router = APIRouter(prefix='/pages', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')

@router.get('/register')
async def get_register_form(request: Request):
    return templates.TemplateResponse(name='register_form.html', context={'request': request})

@router.get('/login')
async def get_login_form(request: Request):
    if has_valid_token(request):
        return RedirectResponse(url="/pages/profile")
    return templates.TemplateResponse(name='login_form.html', context={'request': request})

@router.get('/profile')
async def get_my_profile(request: Request, profile=Depends(get_me)):
    return templates.TemplateResponse(name='profile.html', context={'request': request, 'profile': profile})