from sqlalchemy import Column, Integer, String
from database.db_setup import Base, engine

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    isbn = Column(String)  # International Standard Book Number

Base.metadata.create_all(engine)