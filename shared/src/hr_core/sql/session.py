from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker


def normalize_database_url(database_url: str) -> str:
    """Neon/Heroku-style `postgres(ql)://` URLs -> SQLAlchemy psycopg3 driver."""
    for prefix in ("postgres://", "postgresql://"):
        if database_url.startswith(prefix):
            return "postgresql+psycopg://" + database_url.removeprefix(prefix)
    return database_url


def create_session_factory(database_url: str, **engine_kwargs: Any) -> sessionmaker[Session]:
    """Create engine + session factory once per process (server startup / lambda cold start)."""
    database_url = normalize_database_url(database_url)
    if make_url(database_url).get_backend_name() == "postgresql":
        # PgBouncer (Neon "-pooler" host) in transaction mode breaks psycopg's auto-prepared
        # statements ("prepared statement ... does not exist"), so disable them.
        connect_args = engine_kwargs.setdefault("connect_args", {})
        connect_args.setdefault("prepare_threshold", None)
    engine = create_engine(database_url, **engine_kwargs)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_all_tables(session_factory: sessionmaker[Session]) -> None:
    """Only for tests / throwaway SQLite. Real databases are managed by Alembic migrations."""
    import hr_core.sql.tables  # noqa: F401  registers all tables in Base.metadata
    from hr_core.sql.base import Base

    Base.metadata.create_all(bind=session_factory.kw["bind"])
