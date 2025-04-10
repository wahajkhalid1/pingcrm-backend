from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the database URL from the environment
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables")

# Create engine with SSL configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "sslmode": "require"
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
