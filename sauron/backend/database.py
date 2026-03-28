from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker, declarative_base  # type: ignore # Updated import

# 1. Define the database location
# sqlite:///./ids.db tells SQLAlchemy to create a file in the current folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/ids.db"

# 2. Create the Engine
# 'check_same_thread': False is REQUIRED for SQLite + FastAPI.
# By default, SQLite only allows one thread to communicate with it. 
# FastAPI handles requests in multiple threads, so we must disable this check.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a Session factory
# Each instance of SessionLocal will be a unique database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class
# Our models (Event, Device, etc.) will inherit from this class.
Base = declarative_base()

# 5. Dependency to get the database session
# This is used in your FastAPI routes to ensure the connection 
# is closed automatically after the request is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()