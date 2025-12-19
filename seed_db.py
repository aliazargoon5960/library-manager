from database.db_setup import SessionLocal, Base, engine
from Book.book_model import Book
from User.user_model import User
from Borrow.borrowed_model import BorrowedBook
from datetime import datetime

# ساخت جداول
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 1. اضافه کردن کاربران
admin_user = User(username="admin", password="admin123", is_admin=True)
normal_user = User(username="Ali", password="123456", is_admin=False)

db.add(admin_user)
db.add(normal_user)
db.commit()

# 2. اضافه کردن کتاب‌ها
book1 = Book(title="کتاب آموزش پایتون", author="نویسنده ۱", isbn="111", total_copies=3)
book2 = Book(title="کتاب ریاضی گسسته", author="نویسنده ۲", isbn="222", total_copies=2)
book3 = Book(title="کتاب دیتابیس", author="نویسنده ۳", isbn="333", total_copies=1)

db.add_all([book1, book2, book3])
db.commit()

# 3. اضافه کردن یک رکورد قرض داده شده
borrow1 = BorrowedBook(
    user_id=normal_user.id,
    book_id=book1.id,
    borrowed_at=datetime.utcnow(),
    status="borrowed",
    is_active=True
)

# کم کردن موجودی کتاب
book1.total_copies -= 1

db.add(borrow1)
db.commit()
db.close()

print("دیتابیس با داده تستی پر شد!")
