from sqlalchemy import String, Integer, Column, Boolean
from database import Base, engine

def create_tables():
    Base.metadata.create_all(engine)

class Person(Base):
    __tablename__ = "person"
    id= Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    isMale = Column(Boolean)
    status = Column(String(50), nullable=True)