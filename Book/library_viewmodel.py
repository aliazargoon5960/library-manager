from PyQt5.QtCore import QObject, pyqtSignal
from database.db_setup import SessionLocal
from .book_model import Book
from .book_schema import BookSchema
from .utils import normalize_pydantic_error_schema
from pydantic import ValidationError

class LibraryViewModel(QObject):
    dataValidationError = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.db = SessionLocal()


    def get_all_books(self):
        return self.db.query(Book).all()


    def validate(self, title, author, isbn):
        try:
            validated = BookSchema(title=title, author=author, isbn=isbn)
            self.dataValidationError.emit({})  
            return validated
        except ValidationError as e:
            errors = normalize_pydantic_error_schema(e.errors())
            self.dataValidationError.emit(errors)
            return None


    def add_book(self, title, author, isbn):
        validated = self.validate(title, author, isbn)
        if not validated:
            return False

        exists = self.db.query(Book).filter(Book.isbn == isbn).first()
        if exists:
            self.dataValidationError.emit({'isbn': ['کتابی با این ISBN قبلاً ثبت شده است']})
            return False

        new_book = Book(title=title.strip(), author=author.strip(), isbn=isbn.strip())
        self.db.add(new_book)
        self.db.commit()
        self.dataValidationError.emit({})  
        return True

    def delete_book(self, book_id):
        book = self.db.query(Book).get(book_id)
        if not book:
            self.dataValidationError.emit({'general': ['کتاب پیدا نشد']})
            return False

        self.db.delete(book)
        self.db.commit()
        self.dataValidationError.emit({})
        return True
