from datetime import datetime
from database.db_setup import SessionLocal
from Borrow.borrowed_model import BorrowedBook
from Book.book_model import Book
from User.user_model import User

class BorrowViewModel:
    def __init__(self):
        self.db = SessionLocal()

    def borrow_book(self, user_id: int, book_id: int):
        # بررسی وجود کاربر
        user = self.db.query(User).get(user_id)
        if not user:
            return False, "کاربر پیدا نشد"

        # بررسی وجود کتاب
        book = self.db.query(Book).get(book_id)
        if not book:
            return False, "کتاب پیدا نشد"

        # بررسی موجودی
        if book.total_copies <= 0:
            return False, "موجودی کتاب تمام شده"

        # ثبت قرض
        borrow = BorrowedBook(
            user_id=user_id,
            book_id=book_id
        )

        book.stock -= 1

        self.db.add(borrow)
        self.db.commit()
        return True, "کتاب با موفقیت قرض داده شد"

    def return_book(self, borrow_id: int, admin_id: int):
        borrow = self.db.query(BorrowedBook).get(borrow_id)
        if not borrow or borrow.status == "returned":
            return False, "رکورد معتبر نیست"

        book = self.db.query(Book).get(borrow.book_id)

        borrow.status = "returned"
        borrow.returned_at = datetime.utcnow()
        borrow.is_active = False
        borrow.returned_by = admin_id

        book.stock += 1

        self.db.commit()
        return True, "کتاب با موفقیت پس گرفته شد"
    

    def get_active_borrows(self):
        return (
            self.db.query(BorrowedBook)
            .filter(BorrowedBook.is_active == True)
            .all()
        )
    
    def get_user_borrow_history(self, user_id: int):
        return (
            self.db.query(BorrowedBook)
            .filter(BorrowedBook.user_id == user_id)
            .order_by(BorrowedBook.borrowed_at.desc())
            .all()
        )
    
    def get_borrows_between(self, start_date, end_date):
        return (
            self.db.query(BorrowedBook)
            .filter(
                BorrowedBook.borrowed_at >= start_date,
                BorrowedBook.borrowed_at <= end_date
            )
            .all()
        )