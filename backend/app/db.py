import os
import re
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase

# PUBLIC_INTERFACE
class Base(DeclarativeBase):
    """This is the Declarative Base for SQLAlchemy models."""

_engine = None
_SessionFactory: Optional[sessionmaker] = None
SessionLocal: Optional[scoped_session] = None


def _parse_conn_from_text(file_path: str) -> Optional[str]:
    """
    Internal helper to parse a 'psql postgresql://...' line and extract the DSN.
    """
    try:
        with open(file_path, "r") as f:
            line = f.read().strip()
        # Expect "psql postgresql://user:pass@host:port/db"
        match = re.search(r"(postgresql:\/\/[^\s]+)", line)
        if match:
            return match.group(1)
    except FileNotFoundError:
        return None
    return None


# PUBLIC_INTERFACE
def get_database_url() -> str:
    """Get database URL, preferring env vars; fallback to database/db_connection.txt.
    Env precedence:
      - DATABASE_URL
      - POSTGRES_URL
    Fallback: parse 'database/db_connection.txt'
    """
    env_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
    if env_url:
        return env_url

    # Fallback to db_connection.txt in sibling 'database' workspace
    default_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "..", "database", "db_connection.txt"
    )
    # Normalize path
    default_path = os.path.abspath(default_path)
    parsed = _parse_conn_from_text(default_path)
    if parsed:
        return parsed

    # As a last resort, build from discrete env vars (host, port, etc.)
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5001")  # per project standard
    user = os.getenv("POSTGRES_USER", "appuser")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    db = os.getenv("POSTGRES_DB", "myapp")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


# PUBLIC_INTERFACE
def init_db(app) -> None:
    """Initialize SQLAlchemy engine and scoped session; bind Base.metadata."""
    global _engine, _SessionFactory, SessionLocal
    database_url = get_database_url()

    _engine = create_engine(database_url, pool_pre_ping=True, future=True)
    _SessionFactory = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)
    SessionLocal = scoped_session(_SessionFactory)

    # Stash for app-level access if needed
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    # Import models so metadata knows about them
    # Import models so metadata knows about them
    from .models import experiment  # noqa: F401
    from .models import step  # noqa: F401

    # Create tables if they don't exist (idempotent for demos)
    Base.metadata.create_all(bind=_engine)


# PUBLIC_INTERFACE
def get_session():
    """Yield a SQLAlchemy session from the scoped session registry."""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db(app) first.")
    return SessionLocal()
