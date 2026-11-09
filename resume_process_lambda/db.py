from config import settings
from hr_core.sql.session import create_session_factory

SessionLocal = create_session_factory(
    settings.database_url,
    pool_size=1,
    max_overflow=0,
    pool_pre_ping=True,
)
