from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app import crud, schemas, scraper, matcher, models

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "running"}


# 👤 Crear usuario
@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


# 👥 Listar usuarios
@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


# 🔍 Scraping + matching
@app.post("/run-scraper")
def run_scraper(db: Session = Depends(get_db)):

    users = crud.get_users(db)
    jobs = scraper.scrape_jooble()

    results = []

    for user in users:
        for job in jobs:
            score = matcher.calculate_score(job, user)

            job_data = job.copy()
            job_data["score"] = score

            if not crud.job_exists(db, job["title"], user.id):
            job_data["user_id"] = user.id
            crud.save_job(db, job_data)

            results.append({
                "user": user.name,
                "title": job["title"],
                "score": score
            })

    return results


# 📊 Obtener jobs
@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).order_by(models.Job.score.desc()).all()
