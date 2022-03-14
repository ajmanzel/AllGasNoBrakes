from sqlalchemy import Column, Integer, String
from database import Base


class Example(Base):
    """
        SQLAlchemy uses the term "model" to refer to these classes and instances that
        interact with the database.

        But Pydantic also uses the term "model" to refer to something different, the
        data validation, conversion, and documentation classes and instances.
    """
    __tablename__ = "example"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)