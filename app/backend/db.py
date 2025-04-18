from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///reservtable.db")


SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

