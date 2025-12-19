from database.db_setup import engine, Base
from Book.book_model import Book
from User.user_model import User
from Borrow.borrowed_model import BorrowedBook

Base.metadata.create_all(bind=engine)
