from database.db_setup import SessionLocal
from .book_model import Book

class LibraryViewModel:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_books(self):
        return self.db.query(Book).all()

    def add_book(self, title, author, isbn):
        if title and author and isbn:
            new_book = Book(title=title, author=author, isbn=isbn)
            self.db.add(new_book)
            self.db.commit()
            return True
        return False

    def delete_book(self, book_id):
        book = self.db.query(Book).get(book_id)
        if book:
            self.db.delete(book)
            self.db.commit()
            return True
        return False