from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    steamId = Column(String)
    comment = Column(String)
    commenter_id = Column(Integer, ForeignKey("users.id"))

    commenter = relationship("User", back_populates="comments")
    votes = relationship("Vote", back_populates="comment")
