from typing import List, Optional, Dict

from sqlalchemy.orm import Session

from app import models, schemas


# --------- Users ---------


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    db_user = models.User(
        name=user_in.name,
        email=user_in.email,
        skills=user_in.skills,
        keywords=user_in.keywords,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).order_by(models.User.id).all()


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


# --------- Runs ---------


def create_run(db: Session, source: str = "jooble") -> models.Run:
    run = models.Run(source=source, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def finish_run(db: Session, run: models.Run, status: str = "success") -> models.Run:
    from datetime import datetime

    run.status = status
    run.finished_at = datetime.utcnow()
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


# --------- Jobs ---------


def job_exists(db: Session, title: str, url: str, user_id: int, run_id: int) -> bool:
    """
    Comprueba si ya existe la misma oferta para el mismo usuario en el mismo run.
    Si prefieres evitar duplicar ofertas en todo el histórico, elimina 'run_id' del filtro.
    """
    q = (
        db.query(models.Job)
        .filter(models.Job.user_id == user_id)
        .filter(models.Job.url == url)
        .filter(models.Job.run_id == run_id)
    )
    return db.query(q.exists()).scalar()


def save_job(
    db: Session,
    job_data: Dict,
    user_id: int,
    score: int,
    run_id: int,
) -> models.Job:
    db_job = models.Job(
        user_id=user_id,
        run_id=run_id,
        title=job_data.get("title", "Untitled job"),
        description=job_data.get("description"),
        url=job_data.get("url"),
        company=job_data.get("company"),
        location=job_data.get("location"),
        source=job_data.get("source", "jooble"),
        score=score,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_jobs(db: Session, user_id: Optional[int] = None) -> List[models.Job]:
    q = db.query(models.Job)
    if user_id is not None:
        q = q.filter(models.Job.user_id == user_id)
    return q.order_by(models.Job.found_at.desc(), models.Job.score.desc()).all()
