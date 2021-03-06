from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import schemas
import service
from dependencies import get_db
from utils import str_tools

router = APIRouter(
    prefix="/api/auth",
    dependencies=[Depends(get_db)]
)


@router.post("/register")
async def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """ API endpoint for registering a user """
    user = service.User.get_user_by_username(db, username)
    escaped_username = str_tools.escaped_html(username)

    if user:
        raise HTTPException(status_code=422, detail="Username already in use")

    created_user = schemas.UserCreate(username=escaped_username, password=password)
    service.User.create_user(db, created_user)

    return RedirectResponse("/login", 302)


@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """ API endpoint for logging in a user """
    user = service.User.get_user_by_username(db, username)

    if not service.User.is_correct_user(db, username, password):
        raise HTTPException(status_code=422, detail="Username or password is incorrect")

    auth_token = service.User.gen_auth_token()
    updated_user = service.User.save_auth_token(db, user, auth_token)

    response = RedirectResponse("/", 302)
    response.set_cookie(key="auth_token", value=auth_token, max_age=3600, httponly=True)
    return response


@router.get("/logout")
async def logout():
    """ API endpoint for logging out a user """
    response = RedirectResponse("/", 302)
    response.delete_cookie(key="auth_token")
    return response
