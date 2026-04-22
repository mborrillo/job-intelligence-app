from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    skills: str
    keywords: str
    modality: str = "remote"


class JobOut(BaseModel):
    title: str
    company: str
    score: int
