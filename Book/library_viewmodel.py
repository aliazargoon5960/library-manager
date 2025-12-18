from PyQt5.QtCore import QObject, pyqtSignal 
from database.db_setup import SessionLocal
from book_model import Book
from schemas import BookSchema 
from pydantic import ValidationError


class LibraryViewModel(QObject):
    dataValidationError = pyqtSignal(dict)

    def __init__(self):
        super().__init__() 
        self.db = SessionLocal()

    def get_all_books(self):
        return self.db.query(Book).all()

    def add_book(self, title, author, isbn):
        try:
            validated_data = BookSchema(title=title, author=author, isbn=isbn)
            
            new_book = Book(
                title=validated_data.title, 
                author=validated_data.author, 
                isbn=validated_data.isbn
            )
            self.db.add(new_book)
            self.db.commit()
            
            self.dataValidationError.emit({})
            return True

        except ValidationError as e:
            errors = {}
            for error in e.errors():
                field = str(error['loc'][0])
                msg = error['msg']
                errors[field] = [msg]
            
            self.dataValidationError.emit(errors)
            return False

    def delete_book(self, book_id):
        book = self.db.query(Book).get(book_id)
        if book:
            self.db.delete(book)
            self.db.commit()
            return True
        return False