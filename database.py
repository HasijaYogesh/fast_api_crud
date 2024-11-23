from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:12345678@localhost/person2")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)