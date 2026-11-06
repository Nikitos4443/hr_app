from config import DATABASE_PROVIDER, SQLALCHEMY_DATABASE_URL, MONGO_URI, MONGO_DB_NAME

SessionLocal = None
mongo_db = None

def init_db():
    global SessionLocal, mongo_db

    if DATABASE_PROVIDER == 'sql':
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from database.sql.connection import Base
        import database.sql.tables  # noqa: F401  registers all tables in Base.metadata

        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)

    elif DATABASE_PROVIDER == 'mongo':
        from pymongo import MongoClient

        client = MongoClient(MONGO_URI)
        mongo_db = client[MONGO_DB_NAME]

def get_sql_db():
    if DATABASE_PROVIDER == 'sql':
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
    if DATABASE_PROVIDER == 'mongo':
        if mongo_db is None:
            raise RuntimeError("Mongo Database is not initialized")
        return mongo_db
    return None