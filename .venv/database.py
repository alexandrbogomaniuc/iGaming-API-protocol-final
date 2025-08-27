import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import logging

# We will check the env variables here to see if they're being loaded.
logger = logging.getLogger(__name__)
mysql_host = os.getenv('MYSQL_HOST')
logger.info(f"Database connection attempt. Reading MYSQL_HOST as: {mysql_host}")

# Database URL setup
DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{mysql_host}/{os.getenv('MYSQL_DB')}"

try:
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
    Base = declarative_base(metadata=metadata)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("SQLAlchemy engine and session maker initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize SQLAlchemy engine: {e}")
    # You might want to re-raise the exception or handle it gracefully
    raise e

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
