from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    skills = Column(Text, nullable=True)      # CSV de skills
    keywords = Column(Text, nullable=True)    # CSV de keywords
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    jobs = relationship("Job", back_populates="user")


class Run(Base):
    __tablename__ = "runs"

    id = Column(BigInteger, primary_key=True, index=True)
    started_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    finished_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), nullable=False, default="running")
    source = Column(String(100), nullable=True, default="jooble")

    jobs = relationship("Job", back_populates="run")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    run_id = Column(BigInteger, ForeignKey("runs.id"), nullable=True, index=True)

    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=False)
    company = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    source = Column(Text, nullable=True, default="jooble")

    score = Column(Integer, nullable=False)
    found_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="jobs")
    run = relationship("Run", back_populates="jobs")
