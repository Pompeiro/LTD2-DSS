from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user}:{settings.database_password}@\
{settings.database_host}:{settings.database_port}/{settings.database_name}"


engine = create_engine(settings.url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)