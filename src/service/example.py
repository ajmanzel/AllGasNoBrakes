

from sqlalchemy.orm import Session

import models, schemas

def get_advertisements(db: Session):
    """
    Gets all examples
    """
    examples = db.query(models.Example).all()

    return examples