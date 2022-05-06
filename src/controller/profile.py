import json
import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from dependencies import get_db
from service.profile import save_profile_picture
from utils.file import IMAGE_DIR

load_dotenv()

TRACKER_API_KEY = os.getenv('TRACKER_API_KEY')

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


@router.get("/csgo/{steam_id}")
async def get_csgo_data(steam_id):
    """GET request to Tracker.gg for CSGO Data"""

    url = "https://public-api.tracker.gg/v2/csgo/standard/profile/steam/" + steam_id
    header = {"TRN-Api-Key": TRACKER_API_KEY}

    res = requests.get(url, header)
    json_res = json.loads(res.text)

    # Data Parsing
    try:
        username = json_res["data"]["platformInfo"]["platformUserHandle"]
        avatar_url = json_res["data"]["platformInfo"]["avatarUrl"]
        lifetime_stats = json_res["data"]["segments"][0]["stats"]

        data = {"username": username, "avatar_url": avatar_url, "stats": lifetime_stats}

        return json.dumps(data)
    except:
        #This will return the list of errors that occured.
        return json.dumps(json_res)
