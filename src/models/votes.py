from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    vote = Column(String)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    voted_user_id = Column(Integer, ForeignKey("users.id"))

    comment = relationship("Comment", back_populates="votes")
    voter = relationship("User", back_populates="voter")
