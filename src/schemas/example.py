from pydantic import BaseModel

"""
    To avoid confusion between the SQLAlchemy models and the Pydantic models, we will
    have the file models.py with the SQLAlchemy models, and the file schemas.py with
    the Pydantic models.

    These Pydantic models define more or less a "schema" (a valid data shape).

    So this will help us avoiding confusion while using both.
"""


class ExampleCreate(BaseModel):
    """
    This is the object used before it gets created in the database. Used for writing.
    """
    message: str


class Example(ExampleCreate):
    """
    This is the object used after it gets created in the database. Used for reading and returning.
    Combines "message" from the create object and the "id" to return.
    """
    id: int

    class Config:
        orm_mode = True
