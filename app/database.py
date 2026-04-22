from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("postgresql://neondb_owner:npg_z2p3fUHDAMLE@ep-super-frost-abq1wnsj-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
