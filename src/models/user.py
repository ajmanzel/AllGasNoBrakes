from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password_hash = Column(String)
    salt = Column(String)
    token_hash = Column(String)
    profile_pic = Column(String)

    comments = relationship("Comment", back_populates="commenter")
    voter = relationship("Vote", back_populates="voter")
