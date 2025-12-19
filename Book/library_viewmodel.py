from database.db_setup import SessionLocal
from .book_model import Book
from .book_schema import BookSchema
from .utils import normalize_pydantic_error_schema
from pydantic import ValidationError

class LibraryViewModel:
    def __init__(self):
        self.db = SessionLocal()
        self.dataValidationError = lambda errors: None  


    def get_all_books(self):
        return self.db.query(Book).all()


    def validate(self, title, author, isbn):
        try:
            validated = BookSchema(title=title, author=author, isbn=isbn)
            self.dataValidationError({})  
            return validated
        except ValidationError as e:
            errors = normalize_pydantic_error_schema(e.errors())
            self.dataValidationError(errors)
            return None

    def add_book(self, title, author, isbn):
        validated = self.validate(title, author, isbn)
        if not validated:
            return False

        exists = self.db.query(Book).filter(Book.isbn == isbn).first()
        if exists:
            self.dataValidationError({'isbn': ['کتابی با این ISBN قبلاً ثبت شده است']})
            return False

      
        new_book = Book(title=title.strip(), author=author.strip(), isbn=isbn.strip())
        self.db.add(new_book)
        self.db.commit()
        self.dataValidationError({}) 
        return True


    def delete_book(self, book_id):
        book = self.db.query(Book).get(book_id)
        if not book:
            self.dataValidationError({'general': ['کتاب پیدا نشد']})
            return False

        self.db.delete(book)
        self.db.commit()
        self.dataValidationError({}) 
        return True
