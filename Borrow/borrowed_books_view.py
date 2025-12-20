from PyQt5.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QPushButton,
    QMessageBox
)
from PyQt5.QtCore import Qt
from functools import partial

from Borrow.borrow_viewmodel import BorrowViewModel
from ui.borrowed_books_ui import Ui_Dialog


class BorrowedBooksView(QDialog, Ui_Dialog):
    def __init__(self, current_user):
        super().__init__()
        self.setupUi(self)

        # کاربر فعلی
        self.current_user = current_user

        # ViewModel
        self.vm = BorrowViewModel()

        self._setup_table()
        self.load_data()

    # --------------------------------------------------
    # تنظیمات اولیه جدول
    # --------------------------------------------------
    def _setup_table(self):
        self.tableWidget.setLayoutDirection(Qt.RightToLeft)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(self.tableWidget.SelectRows)
        self.tableWidget.setSelectionMode(self.tableWidget.SingleSelection)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

    # --------------------------------------------------
    # بارگذاری داده‌ها
    # --------------------------------------------------
    def load_data(self):
        borrows = self.vm.get_active_borrows()

        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(borrows))

        for row, borrow in enumerate(borrows):
            # ستون 0: عنوان کتاب
            self.tableWidget.setItem(
                row, 0, QTableWidgetItem(borrow.book.title)
            )

            # ستون 1: نام کاربری
            self.tableWidget.setItem(
                row, 1, QTableWidgetItem(borrow.user.username)
            )

            # ستون 2: تاریخ قرض
            self.tableWidget.setItem(
                row, 2,
                QTableWidgetItem(
                    borrow.borrowed_at.strftime("%Y-%m-%d %H:%M")
                )
            )

            # ستون 3: وضعیت
            self.tableWidget.setItem(
                row, 3, QTableWidgetItem(borrow.status)
            )

            # ستون 4: عملیات
            btn_return = QPushButton("پس گرفتن")
            btn_return.setEnabled(self.current_user.is_admin)
            btn_return.clicked.connect(
                partial(self.handle_return, borrow.id)
            )

            self.tableWidget.setCellWidget(row, 4, btn_return)

    # --------------------------------------------------
    # پس گرفتن کتاب
    # --------------------------------------------------
    def handle_return(self, borrow_id: int):
        reply = QMessageBox.question(
            self,
            "تأیید عملیات",
            "آیا مطمئن هستید که می‌خواهید این کتاب را پس بگیرید؟",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        success, message = self.vm.return_book(
            borrow_id=borrow_id,
            admin_id=self.current_user.id
        )

        if success:
            QMessageBox.information(self, "موفق", message)
            self.load_data()
        else:
            QMessageBox.warning(self, "خطا", message)

    # --------------------------------------------------
    # بستن پنجره و session
    # --------------------------------------------------
    def closeEvent(self, event):
        self.vm.close()
        event.accept()
