from sqlalchemy import Column, Integer, String
from database import Base


class Image(Base):
    """
    Save the filename with an id so that the id can go in the user's profile model
    for a O(1) lookup by id
    """
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
