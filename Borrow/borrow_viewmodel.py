from datetime import datetime

from sqlalchemy.orm import Session

from database.db_setup import SessionLocal
from Borrow.borrowed_model import BorrowedBook
from Book.book_model import Book
from User.user_model import User


class BorrowViewModel:
    def __init__(self, session: Session | None = None):
        # امکان تزریق session (برای تست یا پروژه بزرگ‌تر)
        self.db: Session = session or SessionLocal()

    # --------------------------------------------------
    # قرض گرفتن کتاب
    # --------------------------------------------------
    def borrow_book(self, user_id: int, book_id: int):
        # بررسی کاربر
        user = self.db.get(User, user_id)
        if not user:
            return False, "کاربر پیدا نشد"

        # بررسی کتاب
        book = self.db.get(Book, book_id)
        if not book:
            return False, "کتاب پیدا نشد"

        # بررسی موجودی
        if book.total_copies  <= 0:
            return False, "موجودی کتاب تمام شده"

        # جلوگیری از قرض گرفتن تکراری
        already_borrowed = (
            self.db.query(BorrowedBook)
            .filter(
                BorrowedBook.user_id == user_id,
                BorrowedBook.book_id == book_id,
                BorrowedBook.is_active.is_(True)
            )
            .first()
        )

        if already_borrowed:
            return False, "این کتاب قبلاً توسط شما قرض گرفته شده"

        # ثبت قرض
        borrow = BorrowedBook(
            user_id=user_id,
            book_id=book_id,
            borrowed_at=datetime.utcnow(),
            status="borrowed",
            is_active=True
        )

        # کاهش موجودی
        book.total_copies  -= 1

        self.db.add(borrow)
        self.db.commit()

        return True, "کتاب با موفقیت قرض داده شد"

    # --------------------------------------------------
    # پس گرفتن کتاب
    # --------------------------------------------------
    def return_book(self, borrow_id: int, admin_id: int):
        borrow = self.db.get(BorrowedBook, borrow_id)
        if not borrow:
            return False, "رکورد پیدا نشد"

        if borrow.status == "returned":
            return False, "این کتاب قبلاً پس داده شده"

        book = self.db.get(Book, borrow.book_id)
        if not book:
            return False, "کتاب مربوطه پیدا نشد"

        borrow.status = "returned"
        borrow.returned_at = datetime.utcnow()
        borrow.is_active = False
        borrow.returned_by = admin_id

        # افزایش موجودی
        book.total_copies  += 1

        self.db.commit()
        return True, "کتاب با موفقیت پس گرفته شد"

    # --------------------------------------------------
    # لیست کتاب‌های قرضی فعال
    # --------------------------------------------------
    def get_active_borrows(self):
        return (
            self.db.query(BorrowedBook)
            .filter(BorrowedBook.is_active.is_(True))
            .order_by(BorrowedBook.borrowed_at.desc())
            .all()
        )

    # --------------------------------------------------
    # تاریخچه قرض‌های یک کاربر
    # --------------------------------------------------
    def get_user_borrow_history(self, user_id: int):
        return (
            self.db.query(BorrowedBook)
            .filter(BorrowedBook.user_id == user_id)
            .order_by(BorrowedBook.borrowed_at.desc())
            .all()
        )

    # --------------------------------------------------
    # گزارش‌گیری بین دو تاریخ
    # --------------------------------------------------
    def get_borrows_between(self, start_date, end_date):
        return (
            self.db.query(BorrowedBook)
            .filter(
                BorrowedBook.borrowed_at >= start_date,
                BorrowedBook.borrowed_at <= end_date
            )
            .order_by(BorrowedBook.borrowed_at.desc())
            .all()
        )

    # --------------------------------------------------
    # بستن session
    # --------------------------------------------------
    def close(self):
        self.db.close()
