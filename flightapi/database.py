from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query

from .db_config import DATABASE_HOST, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_USERNAME
from .models import Base


# Custom Query will allow for less if/else statements in the crud.py - with multiple parameters, there would
# essentially be an infinite amount of if/else statements
class CustomQuery(Query):
    def filter_if(self: Query, condition: bool, *criterion):
        if condition:
            return self.filter(*criterion)
        else:
            return self


SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/{DATABASE_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, query_cls=CustomQuery)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
