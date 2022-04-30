from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

#
engine = create_engine(
    "sqlite:///sqlite.db")

db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
