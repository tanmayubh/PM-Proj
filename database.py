from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# DB selection priority:
# 1) DATABASE_URL override (explicit full URL)
# 2) DATABASE_MODE=aws + AWS_DATABASE_URL
# 3) local SQLite default
DATABASE_MODE = os.getenv("DATABASE_MODE", "sqlite").strip().lower()
DATABASE_URL = os.getenv("DATABASE_URL")
AWS_DATABASE_URL = os.getenv("AWS_DATABASE_URL")
LOCAL_SQLITE_URL = os.getenv("LOCAL_SQLITE_URL", "sqlite:///./app.db")

if not DATABASE_URL:
    if DATABASE_MODE == "aws" and AWS_DATABASE_URL:
        DATABASE_URL = AWS_DATABASE_URL
    else:
        DATABASE_URL = LOCAL_SQLITE_URL

engine_args = {"pool_pre_ping": True}
if DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db() -> None:
    # Import models so SQLAlchemy sees table definitions before create_all.
    import model  # noqa: F401
    Base.metadata.create_all(bind=engine)


# Auto-create tables for local SQLite to make Swagger usage work immediately.
if DATABASE_URL.startswith("sqlite"):
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
