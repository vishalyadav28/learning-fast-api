from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
# SQLAlchemy Database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL ="postgresql://vishalyadav:mobcoder%40123@localhost:5432/fast-test-DB"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker to instantiate DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()