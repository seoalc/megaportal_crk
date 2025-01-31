from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.users.router import router as router_users
from app.pages.router import router as router_pages
from app.users.dependencies import has_valid_token

app = FastAPI()
templates = Jinja2Templates(directory='app/templates')

@app.get("/")
def home_page(request: Request):
    # return {"message": "Это мегапортал ЦРК"}
    if has_valid_token(request):
        return RedirectResponse(url="/pages/unassigned_applications")
    return templates.TemplateResponse(name='login_form.html', context={'request': request})

app.include_router(router_users)
app.include_router(router_pages)

app.mount('/static', StaticFiles(directory='app/static'), 'static')