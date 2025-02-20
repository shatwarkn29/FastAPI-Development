"""
Database module for the application.

This module sets up the SQLAlchemy database connection, session maker, and base declarative class.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings  # Adjust the import path if needed

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@{settings.database_hostname}:"
    f"{settings.database_port}/{settings.database_name}"
)
# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency function to provide a SQLAlchemy session.
    
    Yields:
        sqlalchemy.orm.Session: A SQLAlchemy session.
    """
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
