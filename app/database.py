"""
Database module for the application.

This module sets up the SQLAlchemy database connection, session maker, and base declarative class.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings

# Construct the database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{Settings.database_username}:"
    f"{Settings.database_password}@{Settings.database_hostname}:"
    f"{Settings.database_port}/{Settings.database_name}"
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
