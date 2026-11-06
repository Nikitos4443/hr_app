from config import settings
from hr_core.sql.session import create_session_factory

# Created once per cold start and reused by warm invocations.
# One connection per lambda instance: concurrency is handled by more instances, not a bigger pool.
SessionLocal = create_session_factory(
    settings.database_url,
    pool_size=1,
    max_overflow=0,
    pool_pre_ping=True,
)
