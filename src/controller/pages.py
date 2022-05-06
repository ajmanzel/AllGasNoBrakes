from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import service
from dependencies import get_db

templates = Jinja2Templates(directory="templates")
router = APIRouter(dependencies=[Depends(get_db)])


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    auth_token = request.cookies.get('auth_token')
    user = service.User.get_user_by_auth_token(db, auth_token)
    return templates.TemplateResponse("general_pages/homepage.html", {"request": request, 'user': user})


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("general_pages/register.html", {"request": request})


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("general_pages/login.html", {"request": request})
