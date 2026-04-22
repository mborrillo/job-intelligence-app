from app import models
from sqlalchemy.orm import Session

def create_user(db: Session, user):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def save_job(db: Session, job_data):
    job = models.Job(**job_data)
    db.add(job)
    db.commit()
