import hashlib
import secrets

import bcrypt
from sqlalchemy.orm import Session

import models
import schemas


class User:
    @classmethod
    def create_user(cls, db: Session, user: schemas.UserCreate) -> models.User:
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(user.password.encode(), salt)

        db_user = models.User(username=user.username, password_hash=hashed_pw.decode(), salt=salt.decode(),
                              token_hash=None, profile_pic="default.jpg")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @classmethod
    def get_user_by_username(cls, db: Session, username: str) -> models.User:
        return db.query(models.User).filter(models.User.username == username).first()

    @classmethod
    def get_user_by_auth_token(cls, db: Session, auth_token: str) -> models.User:
        if auth_token is None:
            return None

        m = hashlib.sha256()
        m.update(auth_token.encode())
        hashed_token = m.hexdigest()

        return db.query(models.User).filter(models.User.token_hash == hashed_token).first()

    @classmethod
    def gen_auth_token(cls) -> str:
        return secrets.token_hex(16)

    @classmethod
    def save_auth_token(cls, db: Session, user: models.User, auth_token: str):
        m = hashlib.sha256()
        m.update(auth_token.encode())
        hashed_token = m.hexdigest()

        user.token_hash = hashed_token

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @classmethod
    def is_correct_user(cls, db: Session, username: str, password: str):
        user = cls.get_user_by_username(db, username)
        if user:
            test_password = bcrypt.hashpw(password.encode(), user.salt.encode())
        else:
            return None

        if test_password == user.password_hash.encode():
            return user
        else:
            return None

    @classmethod
    def change_profile_picture(cls, db: Session, user: models.User, profile_pic_location: str):
        user.profile_pic = profile_pic_location

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
