from fastapi import APIRouter, Depends, UploadFile, Request, Form, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from utils import str_tools
import service
from dependencies import get_db
import hashlib
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


@router.post("/comment")
async def post_comment(comment: str = Form(...), userid: str = Form(...), steamid: str = Form(...), db: Session = Depends(get_db)):
    escaped_comment = str_tools.escaped_html(comment)

    user = service.User.get_user_by_auth_token(db, userid)

    profile_page = service.Comments.get_comments_by_steamId(db, steamid)

    if profile_page == None:
        raise HTTPException(status_code=403, detail="steamID Incorrect")

    if user == None:
        raise HTTPException(status_code=403, detail="UserID Incorrect")

    service.Comments.add_comment(db, profile_page, escaped_comment, user)

    return RedirectResponse(f'/profile/?steamID={steamid}', 302, headers={'Cache-Control': 'no-cache'})
