from sqlalchemy import Column, Integer, String

from database import Base


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    steamId = Column(String)
    #                                   comment id number     username          their comment 
    #JSON String in the form of {"comments":[{"id":0, "user":"User504", "text": "blahblahblah", "upvotes": 0, "downvotes": 0}]}
    comments = Column(String)