from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import psycopg
from psycopg import rows
import time
from .config import settings
DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        conn=psycopg.connect(host="localhost", dbname="fastapi", user="postgres",
                            password="please1234", row_factory=rows.dict_row)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)