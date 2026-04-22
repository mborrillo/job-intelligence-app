from fastapi import FastAPI
from app.routes import users, jobs

app = FastAPI()

app.include_router(users.router)
app.include_router(jobs.router)

@app.get("/")
def root():
    return {"message": "Job Intelligence API running"}
