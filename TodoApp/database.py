from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://todoapp_db_a32a_user:a3Ayp85MmL7kRz1XioHy8JayhXyEwsYP@dpg-d4i5gaf5r7bs73c8fmp0-a/todoapp_db_a32a'

engine = create_engine (SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker (autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()