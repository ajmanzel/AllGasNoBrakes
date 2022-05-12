from fastapi import APIRouter, Depends, UploadFile, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import service
from dependencies import get_db
from utils.file import IMAGE_DIR

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/api/profile",
    dependencies=[Depends(get_db)]
)


@router.post("/")
async def create_profile_picture(request: Request, file: UploadFile, db: Session = Depends(get_db)):
    """API endpoint for saving a profile picture to the server"""
    auth_token = request.cookies.get('auth_token')
    user = service.User.get_user_by_auth_token(db, auth_token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    contents = await file.read()
    image = service.profile.save_profile_picture(db, file.filename, contents)
    updated_user = service.User.change_profile_picture(db, user, image.filename)

    return RedirectResponse('/user/me', 302, headers={'Cache-Control': 'no-cache'})


@router.get("/{username}")
async def get_profile_picture(username, db: Session = Depends(get_db)):
    """API endpoint for returning a profile picture from the server"""
    user = service.User.get_user_by_username(db, username)
    return FileResponse(IMAGE_DIR + user.profile_pic)
