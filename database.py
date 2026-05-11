import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

try:
    engine = create_engine(DATABASE_URL)
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    
    try:
        logger.info("Database session opened")
        yield db
    finally:
        db.close()
        logger.info("Database session closed")