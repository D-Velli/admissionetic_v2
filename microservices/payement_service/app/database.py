import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# dossier racine du service = programme_service/
BASE_DIR = Path(__file__).resolve().parent.parent

# charge programme_service/.env_programme
load_dotenv(BASE_DIR / ".env_payement")

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Check your .env_payement file.")

connect_args = {}
# check_same_thread uniquement pour sqlite
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    from sqlalchemy.orm import Session
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
