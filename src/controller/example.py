from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
import schemas, service

router = APIRouter(
    prefix="/example",
    dependencies=[Depends(get_db)]
    )

@router.get("/example")
def get_examples(db: Session = Depends(get_db)):
    """API endpoint for getting all examples"""
    return service.get_examples(db)