from PyQt5.QtWidgets import QDialog, QMessageBox, QAbstractItemView, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from ui.main_window_ui import Ui_Dialog
from .library_viewmodel import LibraryViewModel
from .table_model import BookTableModel
from Borrow.borrow_viewmodel import BorrowViewModel
from Borrow.borrowed_view import BorrowedBooksView  # صفحه کتاب‌های قرضی


class LibraryMainView(QDialog, Ui_Dialog):
    def __init__(self, current_user):
        super().__init__()
        self.setupUi(self)

        self.current_user = current_user

        # ViewModel کتابخانه
        self.vm = LibraryViewModel()
        self.vm.dataValidationError.connect(self.show_errors)

        # پیدا کردن اجزای UI
        self.btn_add = self.findChild(QPushButton, "btn_add")
        self.btn_delete = self.findChild(QPushButton, "btn_delete")
        self.btn_borrowed_books = self.findChild(QPushButton, "btnBorrowedBooks")
        self.btn_borrow = self.findChild(QPushButton, "btnBorrow")
        self.txt_title = self.findChild(QLineEdit, "txt_title")
        self.txt_author = self.findChild(QLineEdit, "txt_author")
        self.txt_isbn = self.findChild(QLineEdit, "txt_isbn")
        self.table_books = self.findChild(QAbstractItemView, "table_books")

        self.lbl_title_error = self.findChild(QLabel, "lbl_title_error")
        self.lbl_author_error = self.findChild(QLabel, "lbl_author_error")
        self.lbl_isbn_error = self.findChild(QLabel, "lbl_isbn_error")

        self.error_labels_map = {
            'title': self.lbl_title_error,
            'author': self.lbl_author_error,
            'isbn': self.lbl_isbn_error,
        }

        # تنظیمات جدول
        self.table_books.setLayoutDirection(Qt.RightToLeft)
        self.table_books.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_books.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_books.horizontalHeader().setStretchLastSection(True)

        # اتصال سیگنال‌ها
        self.btn_add.clicked.connect(self.handle_add_book)
        self.btn_delete.clicked.connect(self.handle_delete_book)
        self.btn_borrowed_books.clicked.connect(self.show_borrowed_books)
        self.btn_borrow.clicked.connect(self.handle_borrow_book)  # مهم: قرض گرفتن

        # بارگذاری اولیه جدول
        self.refresh_table()

    # -----------------------
    # بروزرسانی جدول کتاب‌ها
    # -----------------------
    def refresh_table(self):
        books = self.vm.get_all_books()
        self.table_model = BookTableModel(books)
        self.table_books.setModel(self.table_model)

    # -----------------------
    # پاک کردن برچسب خطا
    # -----------------------
    def clear_labels(self):
        for label in self.error_labels_map.values():
            label.setStyleSheet("color: red")
            label.setText("")
            label.hide()

    # -----------------------
    # نمایش خطاها
    # -----------------------
    def show_errors(self, errors: dict):
        self.clear_labels()
        for field, errors_list in errors.items():
            label = self.error_labels_map.get(field)
            if label:
                label.setText('\n'.join(errors_list))
                label.show()

    # -----------------------
    # اضافه کردن کتاب
    # -----------------------
    def handle_add_book(self):
        title = self.txt_title.text()
        author = self.txt_author.text()
        isbn = self.txt_isbn.text()

        success = self.vm.add_book(title, author, isbn)

        if success:
            self.refresh_table()
            self.txt_title.clear()
            self.txt_author.clear()
            self.txt_isbn.clear()
            self.clear_labels()

    # -----------------------
    # حذف کتاب
    # -----------------------
    def handle_delete_book(self):
        selected_indexes = self.table_books.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "خطا", "لطفاً یک کتاب انتخاب کنید.")
            return

        row = selected_indexes[0].row()
        book_id = int(self.table_model.books[row].id)

        if self.vm.delete_book(book_id):
            self.refresh_table()

    # -----------------------
    # قرض گرفتن کتاب
    # -----------------------
    def handle_borrow_book(self):
        selected_indexes = self.table_books.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "خطا", "لطفاً یک کتاب انتخاب کنید.")
            return

        row = selected_indexes[0].row()
        book_id = int(self.table_model.books[row].id)

        vm_borrow = BorrowViewModel()
        success, message = vm_borrow.borrow_book(
            user_id=self.current_user.id,
            book_id=book_id
        )
        vm_borrow.close()

        if success:
            QMessageBox.information(self, "موفق", message)
        else:
            QMessageBox.warning(self, "خطا", message)

        self.refresh_table()

    # -----------------------
    # نمایش کتاب‌های قرضی
    # -----------------------
    def show_borrowed_books(self):
        borrowed_view = BorrowedBooksView(current_user=self.current_user)
        borrowed_view.exec_()

