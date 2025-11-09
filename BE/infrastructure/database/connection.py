"""Database connection management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from contextlib import contextmanager

from core.config import settings

# Create synchronous engine - no greenlet issues
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)

# Create session factory
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

Base = declarative_base()


async def init_database():
    """Initialize database - create all tables."""
    from .models import Base
    Base.metadata.create_all(bind=engine)


async def close_database():
    """Close database connection."""
    engine.dispose()


@contextmanager
def get_database_session() -> Session:
    """Get database session."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_sync_session():
    """Get synchronous session."""
    return SessionLocal()
