from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    skills = Column(Text)
    keywords = Column(Text)
    modality = Column(String)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    company = Column(String)
    description = Column(Text)
    source = Column(String)
    url = Column(String)
    score = Column(Integer)
