from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app import crud, schemas, matcher, models, scraper

from dotenv import load_dotenv

load_dotenv()

# Crea tablas si no existen (en Neon)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Intelligence App")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Job Intelligence App running"}


@app.post("/users", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return db_user


@app.get("/users", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@app.post("/run-scraper")
def run_scraper_endpoint(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    if not users:
        raise HTTPException(
            status_code=400,
            detail="No hay usuarios configurados. Crea al menos uno antes de ejecutar el scraper.",
        )

    run = crud.create_run(db, source="jooble")

    try:
        jobs = scraper.scrape_jooble()
        if not jobs:
            crud.finish_run(db, run, status="no_jobs")
            return {"status": "ok", "saved_jobs": 0, "message": "Scraper sin resultados"}

        saved_jobs = 0
        for user in users:
            for job in jobs:
                if crud.job_exists(db, job["title"], job["url"], user.id, run.id):
                    continue
                score = matcher.calculate_score(job, user)
                crud.save_job(db, job, user.id, score, run.id)
                saved_jobs += 1

        crud.finish_run(db, run, status="success")
        return {"status": "ok", "saved_jobs": saved_jobs, "run_id": run.id}

    except Exception:
        crud.finish_run(db, run, status="failed")
        raise


@app.get("/jobs", response_model=list[schemas.JobRead])
def list_jobs(user_id: int | None = None, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, user_id=user_id)
    return jobs
