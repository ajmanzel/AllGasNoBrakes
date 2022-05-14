from sqlalchemy.orm import Session
import json

import models


class Comments:

    @classmethod
    def initialize_profile(cls, db: Session, steamId: str) -> models.Comments:

        comments = json.dumps({"comments":[]})

        db_comments = models.Comments(steamId=steamId, comments=comments)
        db.add(db_comments)
        db.commit()
        db.refresh(db_comments)

        return db_comments

    @classmethod
    def get_comments_by_steamId(cls, db: Session, steamId: str) -> models.Comments:
        return db.query(models.Comments).filter(models.Comments.steamId == steamId).first()

    @classmethod
    def add_comment(cls, db:Session, profile_page: models.Comments, comment: str, user:models.User) -> models.Comments:
        comments = profile_page.comments
        comments = json.loads(comments)
        username = user.username
        profile_pic = user.profile_pic
        comments["comments"].append({"id":len(comments['comments']), "user": username, "profile_pic": profile_pic, "text":comment, "upvotes":"0", "downvotes":"0"})
        print(comments)
        profile_page.comments = json.dumps(comments)

        db.add(profile_page)
        db.commit()
        db.refresh(profile_page)

        return profile_page