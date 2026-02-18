from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:please1234@localhost/fastapi"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass


