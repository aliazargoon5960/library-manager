from PyQt5.QtWidgets import QDialog, QMessageBox, QAbstractItemView, QPushButton, QLineEdit, QTableView
from main_window_ui import Ui_Dialog
from .library_viewmodel import LibraryViewModel
from .table_model import BookTableModel
from PyQt5.QtCore import Qt

class LibraryMainView(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.vm = LibraryViewModel()

        self.btn_add = self.findChild(QPushButton, "btn_add")
        self.btn_delete = self.findChild(QPushButton, "btn_delete")
        self.txt_title = self.findChild(QLineEdit, "txt_title")
        self.txt_author = self.findChild(QLineEdit, "txt_author")
        self.txt_isbn = self.findChild(QLineEdit, "txt_isbn")
        self.table_books = self.findChild(QTableView, "table_books")

      
        if self.table_books:
            self.table_books.setLayoutDirection(Qt.RightToLeft)
            self.table_books.setSelectionBehavior(QAbstractItemView.SelectRows) 
            self.table_books.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table_books.horizontalHeader().setStretchLastSection(True)

       
        if self.btn_add:
            self.btn_add.clicked.connect(self.handle_add_book)
        if self.btn_delete:
            self.btn_delete.clicked.connect(self.handle_delete_book)
        
        self.refresh_table()

    def refresh_table(self):
        books = self.vm.get_all_books()
        self.table_model = BookTableModel(books)
        if self.table_books:
            self.table_books.setModel(self.table_model)

    def handle_add_book(self):
        title = self.txt_title.text()
        author = self.txt_author.text()
        isbn = self.txt_isbn.text()
        
        if self.vm.add_book(title, author, isbn):
            self.refresh_table()
            self.txt_title.clear()
            self.txt_author.clear()
            self.txt_isbn.clear()
        else:
            QMessageBox.warning(self, "خطا", "لطفاً تمام فیلدها را پر کنید.")

    def handle_delete_book(self):
        if not self.table_books:
            return

        selected_indexes = self.table_books.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "خطا", "لطفاً یک ردیف را انتخاب کنید.")
            return
            
        row = selected_indexes[0].row()
        book_id = int(self.table_model.books[row].id)
        
        if self.vm.delete_book(book_id):
            self.refresh_table()