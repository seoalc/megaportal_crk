from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.material_users.router import router as router_material_users
from app.users.router import router as router_users
from app.pages.router import router as router_pages
from app.applications.router import router as router_applications
from app.materials_types.router import router as router_materials_types
from app.materials_titles.router import router as router_materials_titles
from app.material_stocks.router import router as router_materials_stocks
from app.users.dependencies import has_valid_token
from app.material_users.models import Material_user
from app.materials_titles.models import Material_title
from app.materials_types.models import Material_type
from app.material_stocks.models import Material_stock

app = FastAPI()
templates = Jinja2Templates(directory='app/templates')

@app.get("/")
def home_page(request: Request):
    # return {"message": "Это мегапортал ЦРК"}
    if has_valid_token(request):
        return RedirectResponse(url="/pages/unassigned_applications")
    return templates.TemplateResponse(name='login_form.html', context={'request': request})

app.include_router(router_materials_types)
app.include_router(router_materials_titles)
app.include_router(router_material_users)
app.include_router(router_users)
app.include_router(router_applications)
app.include_router(router_materials_stocks)
app.include_router(router_pages)

app.mount('/static', StaticFiles(directory='app/static'), 'static')