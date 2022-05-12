from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class User(UserCreate):
    id: int
    password_hash: str
    token_hash: str
    salt: str
    profile_pic: str

    class Config:
        orm_mode = True
