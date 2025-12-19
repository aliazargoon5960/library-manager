from sqlalchemy import Column, Integer, String
from database.db_setup import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)

    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
