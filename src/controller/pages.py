import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request, Query
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import service
from dependencies import get_db

load_dotenv()
templates = Jinja2Templates(directory="templates")
router = APIRouter(dependencies=[Depends(get_db)])
TRACKER_API_KEY = os.getenv('TRACKER_API_KEY')


@router.get("/user/me")
async def user(request: Request, db: Session = Depends(get_db)):
    auth_token = request.cookies.get('auth_token')
    user = service.User.get_user_by_auth_token(db, auth_token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("general_pages/userpage.html", {"request": request, 'user': user})


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    auth_token = request.cookies.get('auth_token')
    print(auth_token)
    user = service.User.get_user_by_auth_token(db, auth_token)
    print(user)
    return templates.TemplateResponse("general_pages/homepage.html", {"request": request, 'user': user})


@router.get("/profile")
async def profile(request: Request, steamID: str = Query(..., description="Steam ID"), db: Session = Depends(get_db)):
    """GET request to Tracker.gg for CSGO Data"""

    url = "https://public-api.tracker.gg/v2/csgo/standard/profile/steam/" + steamID
    header = {"TRN-Api-Key": TRACKER_API_KEY}

    json_res = requests.get(url=url, params=header).json()

    auth_token = request.cookies.get('auth_token')
    user = service.User.get_user_by_auth_token(db, auth_token)

    # Data Parsing
    username = json_res["data"]["platformInfo"]["platformUserHandle"]
    avatar_url = json_res["data"]["platformInfo"]["avatarUrl"]
    lifetime_stats = json_res["data"]["segments"][0]["stats"]
    stats = {}

    for i in lifetime_stats:
        label = lifetime_stats[i]["displayName"]
        val = lifetime_stats[i]["displayValue"]

        if lifetime_stats[i]["percentile"]:
            percentile = int(lifetime_stats[i]["percentile"])
            if percentile < 50:
                percentile = f"Bottom {percentile}%"
            elif percentile >= 50:
                percentile = f"Top {100 - percentile}%"
        else:
            percentile = "---"
        
        stats[i] = {"label":label, "value": val, "percentile": percentile}
    

    data = {"username": username, "avatar_url": avatar_url, "stats": stats}

    return templates.TemplateResponse("general_pages/profilepage.html",
                                      {"request": request, "data": data, 'user': user})


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("general_pages/register.html", {"request": request})


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("general_pages/login.html", {"request": request})
