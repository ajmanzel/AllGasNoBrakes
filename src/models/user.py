from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password_hash = Column(String)
    salt = Column(String)
    token_hash = Column(String)
    profile_pic = Column(String)
