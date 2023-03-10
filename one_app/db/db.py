import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()


SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    os.environ.get("DB_DRIVER"),
    os.environ.get("DB_USERNAME"),
    os.environ.get("DB_PASSWORD"),
    os.environ.get("DB_HOST"),
    os.environ.get("DB_PORT"),
    os.environ.get("DB_NAME"),
)

SQLALCHEMY_DATABASE_URL_ALEMBIC = "{}://{}:{}@{}:{}/{}".format(
    os.environ.get("ALEMBIC_DB_DRIVER"),
    os.environ.get("ALEMBIC_DB_USERNAME"),
    os.environ.get("ALEMBIC_DB_PASSWORD"),
    os.environ.get("ALEMBIC_DB_HOST"),
    os.environ.get("ALEMBIC_DB_PORT"),
    os.environ.get("ALEMBIC_DB_NAME"),
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
