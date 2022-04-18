from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session


from dependencies import get_db
from models.image import Image
from service.profile import save_profile_picture
from utils.file import IMAGE_DIR

router = APIRouter(
    prefix="/api/profile",
    dependencies=[Depends(get_db)]
)


@router.post("/")
async def create_profile_picture(file: UploadFile, db: Session = Depends(get_db)):
    """API endpoint for saving a profile picture to the server"""
    contents = await file.read()
    image = save_profile_picture(db, file.filename, contents)

    # associate image with current user after authentication

    return image


@router.get("/{filename}")
async def get_profile_picture(filename):
    """API endpoint for returning a profile picture from the server"""
    return FileResponse(IMAGE_DIR + filename)
