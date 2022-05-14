import json

from sqlalchemy.orm import Session

import models


class Comments:

    @classmethod
    def get_comments_by_steamId(cls, db: Session, steamId: str) -> models.Comment:
        return db.query(models.Comment).filter(models.Comment.steamId == steamId).all()

    @classmethod
    def add_comment(cls, db: Session, profile_page: models.Comment, comment: str, user: models.User) -> models.Comment:
        comments = profile_page.comments
        comments = json.loads(comments)
        username = user.username
        profile_pic = user.profile_pic
        comments["comments"].append(
            {"id": len(comments['comments']), "user": username, "profile_pic": profile_pic, "text": comment,
             "upvotes": "0", "downvotes": "0"})
        print(comments)
        profile_page.comments = json.dumps(comments)

        db.add(profile_page)
        db.commit()
        db.refresh(profile_page)

        return profile_page

    @classmethod
    def create_comment(cls, db: Session, steamid: str, escaped_comment: str, user: models.Comment):
        comment: models.Comment = models.Comment(steamId=steamid, comment=escaped_comment, commenter=user)

        db.add(comment)
        db.commit()
        db.refresh(comment)

        return comment
