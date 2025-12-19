from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout

class BookTableModel(QAbstractTableModel):
    borrow_clicked = pyqtSignal(int)  # book_id

    def __init__(self, books, show_borrow_button=False):
        super().__init__()
        self.books = books
        self.show_borrow_button = show_borrow_button
        self.headers = ["عنوان", "نویسنده", "ISBN", "موجودی"]
        if self.show_borrow_button:
            self.headers.append("عملیات")

    def rowCount(self, parent=None):
        return len(self.books)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        book = self.books[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:
                return book.title
            elif col == 1:
                return book.author
            elif col == 2:
                return book.isbn
            elif col == 3:
                return str(book.available_copies)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return super().headerData(section, orientation, role)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setIndexWidget(self, table_view):
        """
        این تابع را بعد از ساخت مدل صدا بزنیم تا دکمه‌ها اضافه شوند
        """
        if not self.show_borrow_button:
            return

        for row, book in enumerate(self.books):
            btn = QPushButton("قرض گرفتن")
            btn.setEnabled(book.available_copies > 0)
            btn.clicked.connect(lambda _, bid=book.id: self.borrow_clicked.emit(bid))

            # گذاشتن دکمه در جدول
            table_view.setIndexWidget(table_view.model().index(row, 4), btn)
