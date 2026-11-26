from config import DATABASE_PROVIDER, MONGO_DB_NAME, MONGO_URI, settings

SessionLocal = None
mongo_db = None


def init_db():
    global SessionLocal, mongo_db

    if DATABASE_PROVIDER == "sql":
        from hr_core.sql.session import create_all_tables, create_session_factory

        SessionLocal = create_session_factory(settings.database_url, pool_pre_ping=True)
        # Postgres (Neon) schema is managed by Alembic (shared/migrations), never at startup.
        # Local SQLite is a throwaway dev DB, so just create the tables there.
        if settings.database_url.startswith("sqlite"):
            create_all_tables(SessionLocal)

    elif DATABASE_PROVIDER == "mongo":
        from pymongo import MongoClient

        client = MongoClient(MONGO_URI)
        mongo_db = client[MONGO_DB_NAME]


def get_sql_db():
    if DATABASE_PROVIDER == "sql":
        if SessionLocal is None:
            raise RuntimeError("SQL Database is not initialized")
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None


def get_mongo_db():
    if DATABASE_PROVIDER == "mongo":
        if mongo_db is None:
            raise RuntimeError("Mongo Database is not initialized")
        return mongo_db
    return None
