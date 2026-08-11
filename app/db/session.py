from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker


DATABASE_URL = "sqlite:///./jobs.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
def get_db() -> Generator[Session, None, None]:
    """Provide a database session for a request."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()