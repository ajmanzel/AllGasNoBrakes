from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from dependencies import get_db
import schemas, service

templates = Jinja2Templates(directory="templates")

# prefix="/example",
# dependencies=[Depends(get_db)]

router = APIRouter()

@router.get("/example")
def get_examples(db: Session = Depends(get_db)):
    """API endpoint for getting all examples"""
    return service.get_examples(db)

@router.get("/")
async def home(request: Request):
	return templates.TemplateResponse("general_pages/homepage.html",{"request":request})