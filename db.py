from sqlalchemy import create_engine
from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def create_session() -> Session:
    with SessionLocal() as session:
        yield session
