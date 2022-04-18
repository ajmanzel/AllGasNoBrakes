from sqlalchemy.orm import Session

import models, schemas
from utils.file import IMAGE_DIR, save_file_to_server, get_server_filename


def save_profile_picture(db: Session, filename, contents):
    """
    Service to save the profile picture to the db and return the model object
    """
    filename = get_server_filename(filename)
    save_file_to_server(filename, contents)
    image = models.image.Image(filename=filename)

    db.add(image)
    db.commit()
    db.refresh(image)

    return image
