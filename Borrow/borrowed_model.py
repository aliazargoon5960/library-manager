from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String,
    Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database.db_setup import Base


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    borrowed_at = Column(DateTime, default=datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)

    status = Column(String, default="borrowed")  # borrowed | returned
    is_active = Column(Boolean, default=True)

    returned_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # relations
    user = relationship("User", foreign_keys=[user_id])
    book = relationship("Book")
    admin = relationship("User", foreign_keys=[returned_by])

